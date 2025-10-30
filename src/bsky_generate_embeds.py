import random

import requests

OUT_FILE = "embeds.html"
RANDOM_SEED = 43


def get_embed_html(post_url):
    endpoint = "https://embed.bsky.app/oembed"
    response = requests.get(endpoint, params={"url": post_url})
    if response.status_code == 200:
        embed_data = response.json()
        html = embed_data["html"]

        # Remove the <script> tag if present
        if "<script" in html:
            html = html.split("<script")[0]

        return html
    else:
        raise Exception(f"Error fetching embed data: {response.status_code}")


def main():
    with open("posts.txt", "r") as f:
        post_urls = [line.strip().split()[0] for line in f.readlines()]

    if RANDOM_SEED is not None:
        random.seed(RANDOM_SEED)
        random.shuffle(post_urls)

    count = 0
    with open(OUT_FILE, "w") as out_f:
        for url in post_urls:
            try:
                out_f.write(get_embed_html(url))
            except Exception as e:
                print(f"Error fetching embed for {url}: {e}")
            count += 1
            print(f"Processed {count}/{len(post_urls)}")


if __name__ == "__main__":
    main()
