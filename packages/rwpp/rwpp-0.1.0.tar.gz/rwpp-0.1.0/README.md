# Reddit Wallpaper Puller (rwpp)

This project is a simple python command line application to download images from Reddit built using [Typer](https://typer.tiangolo.com) and [Redditwarp](https://redditwarp.readthedocs.io).

## Setup

For general usage as a user you can simply install the program using `pip install rwpp`.

### Development Environment

For development I have been simply creating a _virtualenv_ and installing the required dependencies.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

The project now uses [Poetry](https://python-poetry.org/docs/) to build and upload the project to [PyPi](https://pypi.org/), those more familiar with it may use it instead to install dependencies in a development environment.

## Usage

After installing the program using `pip` you can call it from the command line using `rwpp`.
The CLI will prompt you for a limit and a download path, press enter to use the defaults.

```bash
rwpp earthporn

# Output
How many images would you like to download?  [10]:
Where would you like to save the images?  [./downloads]:
```

### Development

After setting up `rwpp` for development, you can call the `rwpp/main.py` file with the name of a _subreddit_.
The CLI will prompt you for a limit and a download path, press enter to use the defaults.

```bash
python rwpp/main.py earthporn

# Output
How many images would you like to download?  [10]:
Where would you like to save the images?  [./downloads]:
```

## Notes

This project is currently in beta and dev mode, no code is assumed to be safe.
Run at your own risk, there is currently no check to make sure the url pulled from top posts contains an image, just a valid extension

The script will check the given download paths for images that 'have already been downloaded'. This is a simple check against the names of the files (titles of their respective posts) to see what's been downloaded. This can become an issue when a user wants to download to multiple paths.
A sqlite db/csv file could be implemented to save details about downloads so that when checking a given path for already downloaded images, the image in question does not have to be inside of the given directory.

Had to save the images using the unique post.id rather then the post.title as sometimes it will throw an error if the title is too long.
We can get the unique url which contains part of the title for a more detailed file name.

## Todo

- [ ] Check to see if the subreddit exists before pulling images
- [ ] Add time filters, so rather then top:all we can do top:day,week,month etc.
- [ ] After adding extra time filters, add the option to pull 'hot' posts with the same filters
- [ ] Add option to pull new posts

The goal is to get this script up to the state where it can be a simple command line utility you can run using `rwpp` and then pass in args such as subreddit(s), how many posts, whether to be top or hot posts, the downloads path to use if not the default one

Currently doing a simple check against the list of the names ofs the images which have already been downloaded should be suffice, though I don't see it being an issue immediately, I do wonder how well it would scale and at what point does it really start to hinder performance. Maybe look at ways to do a more performant check.
