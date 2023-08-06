import os

import redditwarp.SYNC
import requests
import typer
from redditwarp.models.submission_SYNC import LinkPost

app = typer.Typer()


#  Main download function
# @app.command()
def download(subreddit, limit, dpath):
    # Check for download path
    if not os.path.isdir(f"{dpath}/{subreddit}"):
        os.makedirs(f"{dpath}/{subreddit}")

    downloaded_images = os.listdir(f"{dpath}/{subreddit}")

    accepted_formats = [".jpg", ".jpeg", ".png"]

    # Get top posts from subbreddit
    client = redditwarp.SYNC.Client()
    posts = client.p.subreddit.pull.top(subreddit, amount=limit, time="week")

    for post in posts:
        if not isinstance(post, LinkPost):
            continue
        if post.link.split("/")[-1] not in downloaded_images:
            if post.link.endswith(tuple(accepted_formats)):

                # Retrive the image
                r = requests.get(post.link)

                # Save image to file
                with open(
                    f"{dpath}/{subreddit}/{post.link.split('/')[-1]}", "wb"
                ) as f:
                    f.write(r.content)

                typer.echo(f"{post.link} saved to file")

            else:
                typer.echo("URL does not contain a valid image format...")

        else:
            typer.echo("Image already downloaded...")


# @app.callback()
def main(
    subreddit: str = typer.Argument(
        ...,
        help="The given subreddit(s) to pull images from"
    ),
    limit: int = typer.Option(
        10,
        help="The amount of posts to pull from subreddit(s)",
        prompt="How many images would you like to download? "
    ),
    dpath: str = typer.Option(
        "./downloads",
        help="The path where you would like to save images",
        prompt="Where would you like to save the images? "
    )
):
    download(subreddit, limit, dpath)


# Main function to be called from terminal
@app.callback()
def cli():
    typer.run(main)


# For when the file is called explicitly like during development
if __name__ == "__main__":
    typer.run(main)
