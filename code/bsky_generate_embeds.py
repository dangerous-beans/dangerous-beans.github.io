import requests

OUT_FILE = "embeds.html"


def get_embed_html(post_url):
    endpoint = "https://embed.bsky.app/oembed"
    response = requests.get(endpoint, params={"url": post_url})
    if response.status_code == 200:
        embed_data = response.json()
        return embed_data["html"]
    else:
        raise Exception(f"Error fetching embed data: {response.status_code}")


def main():
    with open("posts.txt", "r") as f:
        post_urls = [line.strip().split()[0] for line in f.readlines()]

    for url in post_urls:
        try:
            embed_html = get_embed_html(url)
            with open(OUT_FILE, "a") as out_f:
                out_f.write(embed_html)
        except Exception as e:
            print(f"Error fetching embed for {url}: {e}")


if __name__ == "__main__":
    main()
