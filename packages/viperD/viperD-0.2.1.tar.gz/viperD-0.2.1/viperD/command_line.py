import click
import os
import pkgutil
import os.path, pkgutil
import pickle
import importlib.resources
from .utils import _create_folders, _get_folder_file_structure_of_templates, _create_files

@click.group()
def cli():
    pass

@click.command()
@click.option('--app_name', prompt='Your application name', help='Name of your python application')
def new(app_name):
    """Creates folder structure along with necessary files to run your
     python application with docker"""
    path_current_dir = os.getcwd()
    path_app = os.path.join(path_current_dir, app_name)
    dirs, files = _get_folder_file_structure_of_templates()
    _create_folders(path_app, dirs)
    _create_files(app_name, path_app, files)


    # pkgpath = os.path.dirname('viperD/')
    # print([name for _, name, _ in pkgutil.iter_modules([pkgpath])])
    # # create_folders(app_name)

@click.command()
@click.option('--var', prompt='simple var',
              help='T.')
def test(var):
    """Simple program to test"""
    click.echo(var)

cli.add_command(test)
cli.add_command(new)