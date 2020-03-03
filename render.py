#!/usr/bin/python3
import json
import time
from sys import argv, exit
from os import listdir as ls


version = "0.2"


def read_json(filepath):
    """Opens a JSON file, load it, and return the contents"""
    return json.load(open(filepath))


def grab(filepath, title = None):
    """grabs the contents of a file and returns it"""
    toReturn = ""
    for line in open(filepath):
        toReturn += line
    return toReturn


def render_card(title, description, destination = None):
    """renders a single card from provided information and returns a string of it"""
    if destination == None:
        return f"""
            <div class="col-sm">
                <div class="card">
                    <p class="bold">{title}</p>
                    <p>{description}</p>
                </div>
            </div>"""
    else:
        return f"""
            <div class="col-sm">
                <a href="{destination}">
                    <div class="card">
                        <p class="bold">{title}</p>
                        <p>{description}</p>
                    </div>
                </a>
            </div>"""


def render_content(filepath, all_files = False):
    """renders content from a file, be it video, audio, or html
    
    does not support Ogg Vorbis files"""
    # check that the file exists
    try:                
        f = open(filepath)
        f.close()
    # return if it doesn't
    except:
        return
    # set filetypes to false
    video = False
    audio = False
    text = False
    # empty string for mime type
    type = ""
    # mp4 video case:
    if filepath.endswith(".mp4"):
        video = True
        type = "video/mp4"
    # webm video case:
    else if filepath.endswith(".webm"):
        video = True
        type = "video/webm"
    # mp3 audio case
    else if filepath.endswith(".mp3"):
        audio = True
        type = "audio/mpeg"
    # WAV audio case
    else if filepath.endswith(".wav"):
        audio = True
        type = "audio/wav"
    # if all_files has been overridden, then all files are considered (not just media)
    else if all_files:
        # plain text case
        if filepath.endswith(".txt"):
            text = True
            type = "text/plain"
        # html stub case
        else if filepath.endswith(".html"):
            text = True
            type = "text/html"
        # markdown case
        # TODO: consider md rendering to HTML in here
        else if filepath.endswith(".md"):
            text = True
            type = "text/markdown"
        # none of the above case
        else:
            pass
    # if we're not looking at all files, and the file isn't recognized media, return empty
    else:
        return
    # video rendering
    if video:
        return f"""
            <div class='center'>
                <video width=90% controls>
                    <source src='{filepath}' type='{type}'>
                    Your browser does not support video.
                </video>
            </div>"""
    # audio rendering
    else if audio:
        return f"""
            <div class='center'>
                <audio width=90% controls>
                    <source src='{filepath}' type='{type}'>
                    Your browser does not support audio.
                </audio>
            </div>"""
    # text rendering, if allowed
    else if all_files:
        if text:
            return grab(filepath)
        # if the file isn't a recognized text file, link to it
        else:
            return f"""
            <a href='{filepath}'>{filepath}</a>"""
    # return empty if nothing else happens
    else:
        return
        
    


def render_page(filepath):
    """renders a page from a JSON file"""
    config = read_json(filepath)
    columns = int(config['page']['columns'])
    start_time = time.time()
    page = ""
    page += grab(argv[1] + config['page']['header'], title = config['page']['title'])
    page += "\n   <body>\n        <div class='row justify-content-start'>"
    i = 0
    for card in config['cards']:
        if 'destination' in card:
            page += render_card(card['title'], card['description'], card['destination'])
        else:
            page += render_card(card['title'], card['description'])
        i += 1
        if i % columns == 0:
            page += "\n        </div>\n        <div class='row justify-content-start'>"
    page += ("\n            <div class='col-sm'></div>" * ((columns - i % columns) % columns))
    page += "\n        </div>\n   </body>\n"
    page += grab(argv[1] + config['page']['footer'])
    end_time = time.time()
    page += f"\n<!-- Rendered by render.py v{version} on {time.ctime()} in {end_time - start_time:0.5f} seconds -->\n"
    return page


def main(args):
    if len(args) < 2:
        print("Please include a directory to work from.")
        exit(1)
    contents = ls(args[1])
    for f in contents:
        if f.endswith(".json"):
            j = read_json(args[1] + "/" + f)
            print(render_page(args[1] + "/" + f), file = open(j['page']['path'], "w"))


if __name__ == "__main__":
    main(argv)
