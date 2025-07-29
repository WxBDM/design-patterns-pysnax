import csv
from pathlib import Path

from blog.models import Post

# =======
# This `PostRepository` class as our repository interface.
# It is outlining the methods that are needed to 

class PostRepository:
    def get_published(self):
        raise NotImplementedError

    def get_by_slug(self, slug: str):
        raise NotImplementedError
# =======

# =======
# Source 1: Leveraging Django's ORM
# Here, we're subclassing the PostRepository class and
#   implementing Django's ORM to read from a database.

class DjangoPostRepository(PostRepository):
    def get_published(self):
        return Post.objects.filter(published=True).order_by("-created_at")

    def get_by_slug(self, slug: str):
        return Post.objects.get(slug=slug)
# =======

# =======
# Source 2: a CSV file.
# Here, we'll subclass the PostRepository class but
#   now implement logic to read the data from a CSV file instead.

CSV_FILE_PATH = Path("data/posts.csv")

class CsvPostRepository(PostRepository):
    def _load_posts(self):
        with open(CSV_FILE_PATH, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            return list(reader)

    def get_published(self):
        return [
            post for post in self._load_posts()
            if post.get("published", "").lower() == "true"
        ]

    def get_by_slug(self, slug):
        for post in self._load_posts():
            if post.get("slug") == slug:
                return post
        raise ValueError(f"Post with slug '{slug}' not found.")
# =======