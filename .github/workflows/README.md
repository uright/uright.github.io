# GitHub Actions Workflows

## PR Preview Build

This workflow automatically builds preview versions of the blog for each pull request and provides downloadable artifacts.

### How It Works

1. **On PR Creation/Update**:
   - Builds the Jekyll site from the PR branch
   - Runs htmlproofer tests to catch broken links
   - Uploads the built site as a downloadable artifact
   - Comments on the PR with instructions

2. **Preview Access**:
   - Download the artifact from the workflow run
   - Extract and serve locally with any static server
   - OR pull the branch and use Docker for preview

### Why This Approach?

This simplified approach:
- ✅ No conflicts with existing GitHub Pages deployment
- ✅ Works with your custom domain (uright.ca)
- ✅ No additional infrastructure needed
- ✅ Artifacts auto-expire after 7 days (no cleanup needed)
- ✅ Compatible with mobile workflow (pull branch + Docker)

### Setup Requirements

**No additional setup required!** The workflow works out of the box with:
- ✅ Standard GitHub Actions permissions
- ✅ No external services
- ✅ No additional branches

**Optional**: Require PR builds to pass before merging:
- Go to: Settings → Branches → Branch protection rules
- Add rule for `master` or `main`
- Check "Require status checks to pass before merging"
- Select "build-preview"

### Benefits

- ✅ **Review Before Merge**: Verify posts build correctly before publishing
- ✅ **Automated Testing**: htmlproofer catches broken links automatically
- ✅ **Download & Test**: Get a built copy of your changes for local testing
- ✅ **Mobile-Friendly**: Pull branch and use Docker on any machine
- ✅ **Automatic Cleanup**: Artifacts expire after 7 days (no manual cleanup)

### Workflow Details

**File**: `.github/workflows/pr-preview.yml`

**Triggers**:
- Pull request opened
- Pull request synchronized (new commits pushed)
- Pull request reopened

**Job**: `build-preview`
1. Checks out PR branch
2. Sets up Ruby and dependencies
3. Builds Jekyll site
4. Creates compressed archive
5. Uploads as artifact
6. Runs htmlproofer tests
7. Comments on PR with instructions

### Troubleshooting

#### Workflow Fails to Build

- Check the Actions tab for detailed error logs
- Common issues:
  - Missing dependencies in `Gemfile`
  - Syntax errors in posts or config
  - Invalid front matter in markdown files

#### htmlproofer Fails

- The workflow continues even if htmlproofer fails (set to `continue-on-error: true`)
- Check the logs to see which links are broken
- Fix broken internal links before merging
- External link failures can be ignored if the site is accessible

#### Can't Download Artifact

- Artifacts expire after 7 days
- You need to be logged into GitHub to download
- If expired, push a new commit to trigger a fresh build

### Preview Methods

**Method 1: Download Artifact**
```bash
# Download from GitHub Actions → Run → Artifacts
# Extract and serve
tar -xzf pr-*-preview.tar.gz
python3 -m http.server 8000
```

**Method 2: Pull and Docker** (Recommended for Mobile Workflow)
```bash
git fetch origin
git checkout <pr-branch-name>
docker compose up --build
# Visit http://localhost:4000
```

**Method 3: Pull and Jekyll**
```bash
git fetch origin
git checkout <pr-branch-name>
bundle exec jekyll serve
# Visit http://localhost:4000
```

### Testing the Workflow

To test the PR preview workflow:

1. Create a test PR from any feature branch:
   ```bash
   git checkout -b test-pr-preview
   # Make some changes
   git commit -am "Test changes"
   git push origin test-pr-preview
   ```

2. Create PR on GitHub

3. Watch the Actions tab for the workflow run

4. Check the PR for the preview comment with instructions

5. Download artifact or pull branch to preview

6. Merge/close the PR (artifact auto-expires after 7 days)

### Integration with Your Mobile Blogging Workflow

This PR preview system perfectly complements your mobile blogging workflow described in the blog post:

1. **Write from Mobile**: Use Claude Code Cloud to create posts
2. **Auto-Build**: PR preview workflow builds automatically
3. **Review Locally**: Pull the branch and preview with Docker on any device
4. **Merge**: Approve and merge the PR
5. **Auto-Deploy**: Existing deploy.yml deploys to production

### Future Enhancements

Possible improvements to this workflow:

- **Netlify/Vercel Integration**: Deploy live previews to Netlify for instant URL access
- **Visual Regression**: Add Percy or Chromatic for screenshot comparisons
- **Lighthouse Scores**: Include performance metrics in PR comments
- **Auto-Screenshots**: Generate preview images of changed pages
- **Diff View**: Show visual diffs of styling changes
