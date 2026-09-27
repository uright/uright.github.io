#!/usr/bin/env bash
# Mint a Meta Model API key from a Muse Code subscription, for use as META_API_KEY.
#
# Login flow adapted from the Pi coding agent (https://github.com/earendil-works/pi),
# packages/ai/src/auth/oauth/meta.ts.
#
# Sign in once, straight from the web (nothing is installed):
#
#   curl -fsSL https://uright.ca/assets/scripts/meta-mint-key.sh | bash -s -- --login
#
# --login signs in with your Meta account via the OAuth device flow and stores
# the identity token in ${META_AUTH_FILE:-~/.uright-meta-auth.json} (mode 0600).
# Without --login, each run reuses the cached key while it's still valid, and
# otherwise mints a fresh ~24h key via POST https://api.meta.ai/muse-code/key
# and caches it. Prints the key to stdout (nothing else) so it composes:
#
#   export META_API_KEY="$(meta-mint-key.sh)"
#   meta-mint-key.sh --export
#   meta-mint-key.sh --exec -- my-command --flag
#
# Guide: https://uright.ca/posts/using-claude-code-with-muse-spark-subscription/
# Requires: curl plus jq or node for JSON parsing.
set -euo pipefail

CLIENT_ID="1031625952748946" # Muse Code CLI OAuth client
DEVICE_AUTH_URL="https://auth.meta.com/oidc/device/authorization/"
DEVICE_TOKEN_URL="https://auth.meta.com/oidc/device/token/"
MINT_URL="https://api.meta.ai/muse-code/key"
KEY_LIFETIME_SECS=86400  # minted keys last ~24h
SAFETY_MARGIN_SECS=300   # reuse cached key only if valid for 5+ more minutes
CURL_TIMEOUT=30

STORE_FILE="${META_AUTH_FILE:-$HOME/.uright-meta-auth.json}"
LOGIN_HINT="curl -fsSL https://uright.ca/assets/scripts/meta-mint-key.sh | bash -s -- --login"

LOGIN=0
FORCE_MINT=0
EMIT_EXPORT=0
EXEC=0

usage() {
	cat <<'EOF'
Usage: meta-mint-key.sh [--login] [--force-mint] [--export] [--exec -- <cmd>...]

  (no flags)   print a valid Meta Model API key to stdout
  --login      sign in with your Meta account (one-time; again when the session expires)
  --force-mint skip the cached key, always mint a fresh one
  --export     print export META_API_KEY='<key>' instead of the bare key
  --exec       run <cmd>... with META_API_KEY set (key never touches history)
  -h, --help   show this help
EOF
}

die() { echo "error: $*" >&2; exit 1; }

while [ $# -gt 0 ]; do
	case "$1" in
		--login) LOGIN=1; shift ;;
		--force-mint) FORCE_MINT=1; shift ;;
		--export) EMIT_EXPORT=1; shift ;;
		--exec) EXEC=1; shift; break ;; # rest (after optional --) is the command
		-h | --help) usage; exit 0 ;;
		*) echo "error: unexpected argument: $1" >&2; usage >&2; exit 2 ;;
	esac
done

if [ "$EXEC" = "1" ]; then
	if [ "${1:-}" = "--" ]; then shift; fi
	if [ $# -eq 0 ]; then echo "error: --exec needs a command" >&2; exit 2; fi
fi

command -v curl >/dev/null || die "curl is required"

# JSON helpers: jq preferred, node fallback.
#   jget <file> <dotted.path>  prints the scalar value, or nothing when absent/null
#   jerror_detail <file>       prints the most useful error message field
#   jcredential                prints the credential JSON built from $CRED_* env vars
if command -v jq >/dev/null; then
	jget() { jq -r "$2 // empty" "$1" 2>/dev/null; }
	jerror_detail() { jq -r '.error_description // .detail // .message // .error // empty' "$1" 2>/dev/null; }
	jcredential() {
		jq -n '{meta: {type: "oauth", refresh: env.CRED_REFRESH, access: env.CRED_ACCESS,
			expires: (env.CRED_EXPIRES | tonumber)}}'
	}
elif command -v node >/dev/null; then
	jget() {
		node -e '
			const fs = require("fs");
			let v = JSON.parse(fs.readFileSync(process.argv[1], "utf8"));
			for (const k of process.argv[2].replace(/^\./, "").split(".")) v = v == null ? v : v[k];
			if (v != null && typeof v !== "object") process.stdout.write(String(v));
		' "$1" "$2" 2>/dev/null
	}
	jerror_detail() {
		node -e '
			const fs = require("fs");
			const d = JSON.parse(fs.readFileSync(process.argv[1], "utf8"));
			for (const k of ["error_description", "detail", "message", "error"]) {
				if (typeof d[k] === "string" && d[k]) { process.stdout.write(d[k]); break; }
			}
		' "$1" 2>/dev/null
	}
	jcredential() {
		node -e '
			const e = process.env;
			const meta = { type: "oauth", refresh: e.CRED_REFRESH, access: e.CRED_ACCESS, expires: Number(e.CRED_EXPIRES) };
			process.stdout.write(JSON.stringify({ meta }, null, 2) + "\n");
		'
	}
else
	die "jq or node is required for JSON parsing"
fi

# ": <detail>" from an error response body, or nothing.
detail() {
	local d
	d="$(jerror_detail "$1")"
	if [ -n "$d" ]; then printf ': %s' "$d"; fi
}

# positive_int <value> <default>
positive_int() {
	if [[ "$1" =~ ^[0-9]+$ ]] && [ "$1" -gt 0 ]; then echo "$1"; else echo "$2"; fi
}

TMP="$(mktemp)"
trap 'rm -f "$TMP"' EXIT

# http_post <url> [curl args...]: body goes to $TMP, prints the HTTP status.
http_post() {
	local url="$1"; shift
	curl -sS -o "$TMP" -w '%{http_code}' -X POST "$url" \
		-H "Accept: application/json" --max-time "$CURL_TIMEOUT" "$@"
}

# save_credential <identity> <key> <expires-epoch-ms>: atomic write, mode 0600.
save_credential() {
	local tmp
	tmp="$(mktemp "$STORE_FILE.XXXXXX")" # mktemp creates files as 0600
	CRED_REFRESH="$1" CRED_ACCESS="$2" CRED_EXPIRES="$3" jcredential >"$tmp"
	mv "$tmp" "$STORE_FILE"
}

# RFC 8628 device flow. Sets IDENTITY to the Meta identity token.
login() {
	local status device_code user_code uri interval expires_in deadline
	status="$(http_post "$DEVICE_AUTH_URL" --data-urlencode "client_id=$CLIENT_ID")" ||
		die "device authorization request failed (network/curl error)"
	[ "${status:0:1}" = "2" ] || die "Meta device authorization failed with status $status$(detail "$TMP")"

	device_code="$(jget "$TMP" '.device_code')"
	user_code="$(jget "$TMP" '.user_code')"
	uri="$(jget "$TMP" '.verification_uri_complete')"
	[ -n "$uri" ] || uri="$(jget "$TMP" '.verification_uri')"
	[ -n "$device_code" ] || die "Meta did not return a device code"
	[[ "$uri" =~ ^https?:// ]] || die "Meta returned an invalid verification URL"
	interval="$(positive_int "$(jget "$TMP" '.interval')" 5)"
	expires_in="$(positive_int "$(jget "$TMP" '.expires_in')" 600)"

	echo "Open this link and sign in with the Meta account that has Muse Code:" >&2
	echo "  $uri" >&2
	echo "Enter code: $user_code" >&2
	echo "Waiting for approval..." >&2

	deadline=$(($(date +%s) + expires_in))
	while :; do
		sleep "$interval"
		[ "$(date +%s)" -lt "$deadline" ] || die "Meta login code expired. Run --login again."
		status="$(http_post "$DEVICE_TOKEN_URL" \
			--data-urlencode "grant_type=urn:ietf:params:oauth:grant-type:device_code" \
			--data-urlencode "device_code=$device_code" \
			--data-urlencode "client_id=$CLIENT_ID")" ||
			die "device token request failed (network/curl error)"
		IDENTITY="$(jget "$TMP" '.access_token')"
		if [ "${status:0:1}" = "2" ] && [ -n "$IDENTITY" ]; then return; fi
		case "$(jget "$TMP" '.error')" in
			authorization_pending) ;;
			slow_down) interval="$(positive_int "$(jget "$TMP" '.interval')" $((interval + 5)))" ;;
			access_denied) die "Meta login was denied." ;;
			expired_token) die "Meta login code expired. Run --login again." ;;
			*) die "Meta device token request failed with status $status$(detail "$TMP")" ;;
		esac
	done
}

# mint_key: exchanges $IDENTITY for a fresh Model API key in KEY.
mint_key() {
	local status
	# Auth header goes through stdin so the token doesn't show up in `ps`.
	status="$(printf 'Authorization: Bearer %s\n' "$IDENTITY" | http_post "$MINT_URL" \
		-H @- \
		-H "Content-Type: application/json" \
		-H "x-api-version: 1.0.0" \
		-d '{}')" || die "mint request failed (network/curl error)"
	if [ "$status" = "401" ] || [ "$status" = "403" ]; then
		die "Meta session expired (status $status)$(detail "$TMP"). Sign in again: $LOGIN_HINT"
	fi
	[ "${status:0:1}" = "2" ] || die "Meta API key mint failed with status $status$(detail "$TMP")"
	KEY="$(jget "$TMP" '.api_key')"
	if [ -z "$KEY" ]; then
		local action
		action="$(jget "$TMP" '.action_url')"
		die "Meta did not issue an API key${action:+. Complete setup at $action}"
	fi
}

KEY=""
if [ "$LOGIN" = "1" ]; then
	login
	FORCE_MINT=1
else
	[ -f "$STORE_FILE" ] || die "not signed in. Sign in with: $LOGIN_HINT"
	IDENTITY="$(jget "$STORE_FILE" '.meta.refresh')"
	[ -n "$IDENTITY" ] || die "no Meta identity token in $STORE_FILE. Sign in with: $LOGIN_HINT"
fi

if [ "$FORCE_MINT" = "0" ]; then
	CACHED="$(jget "$STORE_FILE" '.meta.access')"
	EXPIRES_MS="$(jget "$STORE_FILE" '.meta.expires')" # epoch milliseconds
	if [ -n "$CACHED" ] && [[ "$EXPIRES_MS" =~ ^[0-9]+$ ]] &&
		[ $((EXPIRES_MS / 1000)) -gt $(($(date +%s) + SAFETY_MARGIN_SECS)) ]; then
		KEY="$CACHED"
	fi
fi

if [ -z "$KEY" ]; then
	mint_key
	save_credential "$IDENTITY" "$KEY" $((($(date +%s) + KEY_LIFETIME_SECS) * 1000))
fi

if [ "$LOGIN" = "1" ]; then
	echo "Signed in. Credential saved to $STORE_FILE" >&2
	exit 0
fi

rm -f "$TMP"
trap - EXIT
if [ "$EXEC" = "1" ]; then
	META_API_KEY="$KEY" exec "$@"
elif [ "$EMIT_EXPORT" = "1" ]; then
	printf "export META_API_KEY='%s'\n" "${KEY//\'/\'\\\'\'}"
else
	printf '%s\n' "$KEY"
fi
