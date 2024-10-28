from os.path import join, exists
from os import makedirs, getcwd
import os
import sys
import shutil
from pathlib import Path
from .init import create_file
from configparser import ConfigParser
import pkg_resources
from .copyfile import copy_files
from .changeapps import create_project_apps_py


def new_app(app_name: str):
    """
    new app for project
    :param folder:
    :return:
    """
    if len(sys.argv) < 3:
        print('Please enter your plugins name')
    else:
        project_path = join(getcwd(), app_name)
        if exists(plugins_path):
            print('Plugins directory already exists')
        else:
            if sys.argv[2] in [pkg.key for pkg in pkg_resources.working_set]:
                print('Plugins directory already exists')
            else:
                apps_path = join(plugins_path, 'apps.py')
                os.remove(apps_path)
                create_plugins_apps_py(apps_path, sys.argv[2])

                print('Initialized plugins workspace %s' % sys.argv[2])
