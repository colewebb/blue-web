#!/usr/bin/python3
import json
import time
from sys import argv, exit
from os import listdir as ls


version = "0.2"


def read_json(filepath):
    """Opens a JSON file, load it, and return the contents"""
    return json.load(open(filepath))


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



def grab(filepath, title = None):
    """grabs the contents of a file and returns it"""
    toReturn = ""
    for line in open(filepath):
        toReturn += line
    return toReturn


def render_page(filepath):
    """renders a page from a JSON file"""
    config = read_json(filepath)
    columns = int(config['page']['columns'])
    t = time.ctime()
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
    page += f"\n<!-- Rendered by render.py v{version} on {t} in {end_time - start_time:0.5f} seconds -->\n"
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
