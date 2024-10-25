import click

from pipc_flask_app.flaskapp import create_flask
from textPlay.colors import *

title = f"{BLUE}PIPCREATOR FLASK APP{RESET}"

@click.group()
def cli():
    print(f"\n{title}")
    pass

@click.command(help="Create Flask App")
@click.argument('directory', required=False)
def create(directory):
    while not directory:
        if not directory:
            directory = input("Enter location / project name: ")
    create_flask(directory)

cli.add_command(create)