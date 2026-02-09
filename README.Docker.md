# Docker Development Setup

This Docker setup allows you to run the Jekyll blog without installing Ruby, Bundler, or other dependencies locally.

## Prerequisites

- Docker Desktop installed on your system
- Docker Compose (included with Docker Desktop)

## Quick Start

### Using Docker Compose (Recommended)

1. **Build and start the container:**
   ```bash
   docker-compose up --build
   ```

2. **Access the site:**
   - Open your browser to: http://localhost:4000
   - LiveReload is enabled on port 35729

3. **Stop the container:**
   ```bash
   docker-compose down
   ```

### Using Docker directly

1. **Build the image:**
   ```bash
   docker build -t uright-jekyll-blog .
   ```

2. **Run the container:**
   ```bash
   docker run -p 4000:4000 -p 35729:35729 \
     -v $(pwd):/srv/jekyll \
     -v bundle_cache:/usr/local/bundle \
     uright-jekyll-blog
   ```

3. **Access the site:**
   - Open your browser to: http://localhost:4000

## Development Workflow

### Making Changes

- Edit files in your local directory
- Changes are automatically detected and the site rebuilds
- Browser automatically refreshes with LiveReload

### Running Jekyll Commands

Execute Jekyll commands inside the container:

```bash
# Using docker-compose
docker-compose exec jekyll bundle exec jekyll build

# Using docker directly
docker exec -it uright-jekyll-blog bundle exec jekyll build
```

### Installing New Gems

If you modify the Gemfile:

```bash
# Rebuild the container
docker-compose up --build
```

### Accessing the Container Shell

```bash
# Using docker-compose
docker-compose exec jekyll bash

# Using docker directly
docker exec -it uright-jekyll-blog bash
```

## Troubleshooting

### Port Already in Use

If port 4000 is already in use, modify the ports in `docker-compose.yml`:

```yaml
ports:
  - "4001:4000"  # Change 4001 to any available port
  - "35730:35729"
```

### Permission Issues

If you encounter permission issues with generated files:

```bash
# Fix ownership
docker-compose run --rm jekyll chown -R $(id -u):$(id -g) /srv/jekyll
```

### Container Won't Start

1. Check Docker is running
2. Remove old containers: `docker-compose down`
3. Rebuild: `docker-compose up --build`

### Changes Not Reflecting

1. Clear Jekyll cache: `rm -rf .jekyll-cache _site`
2. Restart container: `docker-compose restart`

## Production Build

To build the site for production:

```bash
# Build the site
docker-compose run --rm jekyll bundle exec jekyll build

# Output will be in _site directory
```

## Volume Management

### Clear Bundle Cache

If you need to reinstall all gems:

```bash
docker-compose down
docker volume rm uright.github.io_bundle_cache
docker-compose up --build
```

## Performance Notes

- `--force_polling` is used for file watching on all platforms
- Volume mounting provides live reload capabilities
- Bundle cache volume speeds up subsequent builds

## Additional Resources

- [Jekyll Documentation](https://jekyllrb.com/docs/)
- [Docker Documentation](https://docs.docker.com/)
- [Chirpy Theme Documentation](https://github.com/cotes2020/jekyll-theme-chirpy)
