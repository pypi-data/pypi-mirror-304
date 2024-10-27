from os.path import join, exists
from os import makedirs, getcwd, rename
import shutil
from pathlib import Path
from .init import create_file
from configparser import ConfigParser
import sys
import os


def deploy(folder: str):
    """
    deploy project
    :param folder:
    :return:
    """

    if len(sys.argv) < 3:
        print('Please enter your deploy project name')
    else:
        current_path = Path(__file__).resolve()
        file_path = join(current_path.parent, 'file')
        create_file('')
        exists(join(getcwd(), 'deploy')) or makedirs(join(getcwd(), 'deploy'))
        deploy_path = join(getcwd(), 'deploy')
        uwsgi_path = join(deploy_path, 'uwsgi')
        exists(uwsgi_path) or os.makedirs(uwsgi_path)
        supervisor_path = join(deploy_path, 'supervisor')
        exists(supervisor_path) or os.makedirs(supervisor_path)
        if exists(join(uwsgi_path, str(sys.argv[2]) + '.ini')) is False:
            shutil.copy2(join(file_path, 'uwsgi.ini'), uwsgi_path)
            rename(join(uwsgi_path, 'uwsgi.ini'), join(uwsgi_path, str(sys.argv[2]) + '.ini'))
        uwsgi_config = ConfigParser()
        uwsgi_config.read(join(uwsgi_path, str(sys.argv[2]) + '.ini'))
        server_path = join(current_path.parent.parent, 'server')
        uwsgi_config.set('uwsgi', 'chdir', server_path)
        wsgi_path = join(server_path, 'server')
        uwsgi_config.set('uwsgi', 'wsgi-file', join(wsgi_path, 'wsgi.py'))
        uwsgi_config.set('uwsgi', 'logto', join(getcwd(), 'logs'))
        uwsgi_config.write(open(join(uwsgi_path, str(sys.argv[2]) + '.ini'), "wt"))

        if exists(join(supervisor_path, str(sys.argv[2]) + '.ini')) is False:
            shutil.copy2(join(file_path, 'supervisor.conf'), supervisor_path)
            rename(join(supervisor_path, 'supervisor.conf'), join(supervisor_path, str(sys.argv[2]) + '.conf'))
        supervisor_config = ConfigParser()
        supervisor_config.read(join(supervisor_path, str(sys.argv[2]) + '.conf'))
        if str(sys.argv[2]) != 'bomiot':
            supervisor_config.add_section(f'program:{sys.argv[2]}')
            supervisor_config.set(f'program:{sys.argv[2]}', 'user', 'root')
            supervisor_config.set(f'program:{sys.argv[2]}', 'command', 'daphne -b 0.0.0.0 -p 8008 bomiot.server.server.asgi:application')
            supervisor_config.set(f'program:{sys.argv[2]}', 'autostart', 'true')
            supervisor_config.set(f'program:{sys.argv[2]}', 'autorestart', 'true')
            supervisor_config.set(f'program:{sys.argv[2]}', 'startsecs', '0')
            supervisor_config.set(f'program:{sys.argv[2]}', 'stopwaitsecs', '0')
            supervisor_config.set(f'program:{sys.argv[2]}', 'redirect_stderr', 'true')
            supervisor_config.remove_setion('program:bomiot', 'chdir', server_path)
        supervisor_config.set(f'program:{sys.argv[2]}', 'directory', f'{getcwd()}')
        supervisor_config.set(f'program:{sys.argv[2]}', 'stdout_logfile',
                   f'{join(join(getcwd(), "logs"), "bomiot_supervisor_access.log")}')
        supervisor_config.set(f'program:{sys.argv[2]}', 'stdout_logfile',
                   f'{join(join(getcwd(), "logs"), "bomiot_supervisor_err.log")}')
        supervisor_config.write(open(join(supervisor_path, str(sys.argv[2]) + '.conf'), "wt"))

        print(f'Deploy project {str(sys.argv[2])} workspace success')
