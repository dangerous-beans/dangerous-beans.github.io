import os
from operator import is_

from atproto import Client

handle = os.getenv("BLUESKY_HANDLE")
password = os.getenv("BLUESKY_PASSWORD")

if not handle or not password:
    raise Exception("BLUESKY_HANDLE and BLUESKY_PASSWORD env vars are required!")


def is_valid(post) -> bool:
    return (
        post.author.handle == handle  # Not a repost
        and not post.record.reply  # Not a reply
        and not hasattr(post.embed, "record")  # Not a quoted post
    )


def get_posts(client: Client, handle: str) -> list:
    posts = []

    cursor = None
    while True:
        profile_feed = client.get_author_feed(
            actor=handle,
            cursor=cursor,
            limit=100,
        )
        posts.extend(
            [
                feed_view.post
                for feed_view in profile_feed.feed
                if is_valid(feed_view.post)
            ]
        )
        if not (cursor := profile_feed.cursor):
            break

    return posts


def main(client: Client, handle: str):
    print(f"\nProfile Posts of {handle}:\n\n")
    posts = get_posts(client, handle)
    for post in posts:
        print(
            f"https://bsky.app/profile/{post.author.handle}/post/{post.uri.split('/')[-1]}    {post.record.text.strip().split('\n')[0][:100]}"
        )
    print(f"\nTotal posts: {len(posts)}")


if __name__ == "__main__":
    at_client = Client()
    at_client.login(handle, password)
    main(at_client, handle)
