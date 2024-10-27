from os.path import join, exists
from os import makedirs, getcwd, rename
import shutil
from pathlib import Path
from .init import create_file
from configparser import ConfigParser
import sys

config = ConfigParser()

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
        uwsgi_path = join(deploy_path, 'deploy')
        supervisor_path = join(deploy_path, 'supervisor')
        if exists(join(uwsgi_path, str(sys.argv[2]) + '.ini')) is False:
            shutil.copy2(join(file_path, 'uwsgi.ini'), uwsgi_path)
            rename(join(uwsgi_path, 'uwsgi.ini'), join(uwsgi_path, str(sys.argv[2]) + '.ini'))
        config.read(join(uwsgi_path, str(sys.argv[2]) + '.ini'))
        server_path = join(current_path.parent.parent, 'server')
        config.set('uwsgi', 'chdir', server_path)
        wsgi_path = join(server_path, 'server')
        config.set('uwsgi', 'wsgi-file', join(wsgi_path, 'wsgi.py'))
        config.set('uwsgi', 'logto', join(getcwd(), 'logs'))
        config.write(open(join(uwsgi_path, str(sys.argv[2]) + '.ini'), "wt"))

        if exists(join(supervisor_path, str(sys.argv[2]) + '.ini')) is False:
            shutil.copy2(join(file_path, 'supervisor.conf'), supervisor_path)
            rename(join(supervisor_path, 'supervisor.conf'), join(supervisor_path, str(sys.argv[2]) + '.conf'))
        config.read(join(supervisor_path, str(sys.argv[2]) + '.conf'))
        if str(sys.argv[2]) != 'bomiot':
            config.add_section(f'program:{sys.argv[2]}')
            config.set(f'program:{sys.argv[2]}', 'user', 'root')
            config.set(f'program:{sys.argv[2]}', 'command', 'daphne -b 0.0.0.0 -p 8008 bomiot.server.server.asgi:application')
            config.set(f'program:{sys.argv[2]}', 'autostart', 'true')
            config.set(f'program:{sys.argv[2]}', 'autorestart', 'true')
            config.set(f'program:{sys.argv[2]}', 'startsecs', '0')
            config.set(f'program:{sys.argv[2]}', 'stopwaitsecs', '0')
            config.set(f'program:{sys.argv[2]}', 'redirect_stderr', 'true')
            config.remove_setion('program:bomiot', 'chdir', server_path)
        config.set(f'program:{sys.argv[2]}', 'directory', f'{getcwd()}')
        config.set(f'program:{sys.argv[2]}', 'stdout_logfile',
                   f'{join(join(getcwd(), "logs"), "bomiot_supervisor_access.log")}')
        config.set(f'program:{sys.argv[2]}', 'stdout_logfile',
                   f'{join(join(getcwd(), "logs"), "bomiot_supervisor_err.log")}')
        config.write(open(join(supervisor_path, str(sys.argv[2]) + '.conf'), "wt"))

        print(f'Deploy project {str(sys.argv[2])} workspace success')
