from blog.post_repository import CsvPostRepository as CSVReader
from blog.post_repository import DjangoPostRepository as DjangoReader

# Let's suppose we want to see if a post is a "breaking news" kind of article.
def is_breaking_news(post):
    return (
        post.get("published", False) in [True, 'true', "True"]
        and "breaking news" in post.get("title", "").lower()
    )

# Here, we'll use the DjangoReader to pull the breaking news posts.
#   But, here's the best part: you can swap this out for CSVReader and it will
#   not break! :)
post_repo = DjangoReader()

breaking_news_posts = [post for post in post_repo.get_published() if is_breaking_news(post)]
print(breaking_news_posts)