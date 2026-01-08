#!/usr/bin/env python3
"""
Jekyll Blog Post Generator

Creates new blog posts for the uright.github.io Jekyll blog with proper
front matter, slug generation, and automatic directory creation.
"""

import argparse
import re
import sys
import warnings
from datetime import datetime
from pathlib import Path
from typing import Optional

import pytz
from jinja2 import Environment, FileSystemLoader


class SlugGenerator:
    """Converts titles to URL-safe slugs"""

    @staticmethod
    def generate(title: str, max_length: int = 100) -> str:
        """
        Transform title into URL-safe slug.

        Rules:
        - Lowercase conversion
        - Special character removal (keep alphanumeric + spaces)
        - Space → hyphen conversion
        - Multiple hyphen collapsing
        - Strip leading/trailing hyphens
        - Max length enforcement

        Examples:
            "How I Built This!" → "how-i-built-this"
            "Python 3.11: New Features" → "python-311-new-features"
            "AI & ML in 2024" → "ai-ml-in-2024"
        """
        # Convert to lowercase
        slug = title.lower()

        # Remove special characters (keep alphanumeric, spaces, and hyphens)
        slug = re.sub(r'[^a-z0-9\s-]', '', slug)

        # Replace spaces with hyphens
        slug = re.sub(r'\s+', '-', slug)

        # Collapse multiple hyphens
        slug = re.sub(r'-+', '-', slug)

        # Strip leading/trailing hyphens
        slug = slug.strip('-')

        # Enforce max length
        if len(slug) > max_length:
            slug = slug[:max_length].rstrip('-')

        return slug


class PathBuilder:
    """Generate standardized paths for posts and images"""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.posts_dir = self.project_root / "_posts"
        self.images_dir = self.project_root / "assets" / "img"

    def get_post_path(self, date: str, slug: str) -> Path:
        """Generate: _posts/YYYY-MM-DD-slug.md"""
        date_part = date.split()[0]  # Extract YYYY-MM-DD
        filename = f"{date_part}-{slug}.md"
        return self.posts_dir / filename

    def get_image_dir(self, date: str, slug: str) -> Path:
        """Generate: assets/img/YYYY-MM-DD-slug/"""
        date_part = date.split()[0]  # Extract YYYY-MM-DD
        return self.images_dir / f"{date_part}-{slug}"

    def get_image_path(self, date: str, slug: str, filename: str) -> str:
        """Generate: /assets/img/YYYY-MM-DD-slug/filename"""
        date_part = date.split()[0]  # Extract YYYY-MM-DD
        return f"/assets/img/{date_part}-{slug}/{filename}"


class TemplateRenderer:
    """Jinja2 template rendering with validation"""

    def __init__(self, template_dir: Path):
        self.env = Environment(loader=FileSystemLoader(str(template_dir)))
        self.template = self.env.get_template('post-template.j2')

    def render(self, context: dict) -> str:
        """Render template with provided context"""
        return self.template.render(**context)


class PostValidator:
    """Validation and collision detection"""

    @staticmethod
    def validate_title(title: str) -> None:
        """Ensure title is not empty and reasonable length"""
        if not title or not title.strip():
            raise ValueError("Title cannot be empty")
        if len(title) > 200:
            raise ValueError("Title is too long (max 200 characters)")

    @staticmethod
    def validate_categories(categories: list) -> None:
        """Check categories format and count"""
        if not categories:
            raise ValueError("At least one category is required")
        if len(categories) > 3:
            warnings.warn("More than 3 categories may impact organization")

    @staticmethod
    def validate_tags(tags: list) -> None:
        """Check tags format and count"""
        if not tags:
            raise ValueError("At least one tag is required")
        if len(tags) < 3:
            warnings.warn("Consider adding more tags for discoverability (3-10 recommended)")
        if len(tags) > 10:
            warnings.warn("Too many tags may dilute relevance (3-10 recommended)")

    @staticmethod
    def check_collision(post_path: Path) -> bool:
        """Return True if post already exists"""
        return post_path.exists()


class FileCreator:
    """File and directory creation orchestration"""

    @staticmethod
    def create_directory(path: Path, dry_run: bool = False) -> None:
        """Create directory with parent creation"""
        if dry_run:
            print(f"Would create directory: {path}")
        else:
            path.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def create_post(path: Path, content: str, dry_run: bool = False) -> None:
        """Write post file with error handling"""
        if dry_run:
            print(f"Would create post: {path}")
        else:
            try:
                path.write_text(content, encoding='utf-8')
            except PermissionError:
                raise PermissionError(f"Cannot write to {path}. Check permissions")

    @staticmethod
    def create_structure(
        post_path: Path,
        image_dir: Path,
        content: str,
        dry_run: bool = False
    ) -> dict:
        """
        Orchestrate complete creation:
        1. Create image directory
        2. Write post file
        3. Return operation summary
        """
        FileCreator.create_directory(image_dir, dry_run)
        FileCreator.create_post(post_path, content, dry_run)

        return {
            'post_path': post_path,
            'image_dir': image_dir,
            'dry_run': dry_run
        }


def parse_categories(input_str: str) -> list:
    """Parse 'Tech, AI' → ['Tech', 'AI']"""
    categories = [c.strip().title() for c in input_str.split(',')]

    # Filter out empty strings
    categories = [c for c in categories if c]

    if not categories:
        raise ValueError("At least one category required")

    # Check for valid characters
    for cat in categories:
        if not re.match(r'^[A-Za-z0-9\s]+$', cat):
            raise ValueError(f"Invalid category: {cat}")

    return categories


def parse_tags(input_str: str) -> list:
    """Parse 'python, openai, gpt4o' → ['python', 'openai', 'gpt4o']"""
    tags = [t.strip().lower() for t in input_str.split(',')]

    # Filter out empty strings
    tags = [t for t in tags if t]

    if not tags:
        raise ValueError("At least one tag required")

    # Check for valid characters (allow hyphens in tags)
    for tag in tags:
        if not re.match(r'^[a-z0-9\-]+$', tag):
            raise ValueError(f"Invalid tag: {tag}")

    return tags


def generate_date(custom_date: Optional[str] = None) -> str:
    """Generate properly formatted date with timezone"""
    tz = pytz.timezone('America/Toronto')

    if custom_date:
        # Parse custom date
        try:
            if len(custom_date) == 10:  # YYYY-MM-DD
                dt = datetime.strptime(custom_date, '%Y-%m-%d')
                dt = dt.replace(hour=0, minute=0, second=0)
            else:  # YYYY-MM-DD HH:MM:SS
                dt = datetime.strptime(custom_date, '%Y-%m-%d %H:%M:%S')
            dt = tz.localize(dt)
        except ValueError as e:
            raise ValueError(f"Invalid date format: {e}")
    else:
        dt = datetime.now(tz)

    return dt.strftime('%Y-%m-%d %H:%M:%S %z')


def main():
    """Main execution flow"""
    parser = argparse.ArgumentParser(
        description='Create a new Jekyll blog post with proper front matter',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  %(prog)s --title "My Post" --description "Description" --categories "Tech, AI" --tags "python, tutorial"
  %(prog)s -t "Post Title" -d "Description" -c "Tech" --tags "tag1, tag2, tag3" --mermaid
  %(prog)s -t "Title" -d "Desc" -c "Tech" --tags "python" --image-path "img.png" --image-alt "Alt text"
        '''
    )

    # Required arguments
    parser.add_argument(
        '--title', '-t',
        required=True,
        help='Post title'
    )
    parser.add_argument(
        '--description', '-d',
        required=True,
        help='Post description (for SEO and previews)'
    )
    parser.add_argument(
        '--categories', '-c',
        required=True,
        help='Comma-separated categories (e.g., "Tech, AI")'
    )
    parser.add_argument(
        '--tags',
        required=True,
        help='Comma-separated tags (e.g., "python, tutorial, beginner")'
    )

    # Optional arguments
    parser.add_argument(
        '--image-path',
        help='Image filename (e.g., "hero-image.png")'
    )
    parser.add_argument(
        '--image-alt',
        help='Image alt text (required if --image-path is provided)'
    )
    parser.add_argument(
        '--mermaid',
        action='store_true',
        help='Enable Mermaid diagram support'
    )
    parser.add_argument(
        '--date',
        help='Custom date (YYYY-MM-DD or YYYY-MM-DD HH:MM:SS). Default: current time'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Preview what would be created without actually creating files'
    )

    args = parser.parse_args()

    # Validate image arguments
    if args.image_path and not args.image_alt:
        parser.error("--image-alt is required when --image-path is provided")
    if args.image_alt and not args.image_path:
        parser.error("--image-path is required when --image-alt is provided")

    try:
        # Get project root (script is in tools/, project root is parent)
        script_dir = Path(__file__).parent
        project_root = script_dir.parent

        # Validate inputs
        PostValidator.validate_title(args.title)
        categories = parse_categories(args.categories)
        PostValidator.validate_categories(categories)
        tags = parse_tags(args.tags)
        PostValidator.validate_tags(tags)

        # Generate slug and date
        slug = SlugGenerator.generate(args.title)
        date = generate_date(args.date)

        # Build paths
        path_builder = PathBuilder(project_root)
        post_path = path_builder.get_post_path(date, slug)
        image_dir = path_builder.get_image_dir(date, slug)

        # Check for collision
        if PostValidator.check_collision(post_path) and not args.dry_run:
            print(f"Error: Post already exists at {post_path}", file=sys.stderr)
            sys.exit(1)

        # Prepare template context
        context = {
            'title': args.title,
            'description': args.description,
            'date': date,
            'categories': ', '.join(categories),
            'tags': ', '.join(tags),
            'mermaid': args.mermaid,
        }

        # Add image if provided
        if args.image_path:
            context['image_path'] = path_builder.get_image_path(date, slug, args.image_path)
            context['image_alt'] = args.image_alt

        # Render template
        template_dir = script_dir / 'templates'
        if not template_dir.exists():
            print(f"Error: Template directory not found at {template_dir}", file=sys.stderr)
            sys.exit(1)

        renderer = TemplateRenderer(template_dir)
        content = renderer.render(context)

        # Display dry-run output
        if args.dry_run:
            print("DRY RUN MODE - No files will be created")
            print("=" * 50)
            print(f"\nWould create post:")
            print(f"  Path: {post_path}")
            print(f"\nFront Matter Preview:")
            print(content[:500] + "..." if len(content) > 500 else content)
            print(f"\nWould create directory:")
            print(f"  Path: {image_dir}")
            print(f"\nTo execute, run without --dry-run flag")
            sys.exit(0)

        # Create files and directories
        result = FileCreator.create_structure(post_path, image_dir, content, args.dry_run)

        # Display success message
        print("✓ Post created successfully!")
        print()
        print(f"  File: {result['post_path']}")
        print(f"  Images: {result['image_dir']}/")
        print()
        print("  Next steps:")
        print("  1. Add your content to the post file")
        print("  2. Add images to the images directory")
        print("  3. Preview with: bundle exec jekyll serve")

    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except PermissionError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
