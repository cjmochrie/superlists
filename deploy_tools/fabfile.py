# This uses python 2.7 only
import random
from fabric.contrib.files import append, exists, sed
from fabric.api import env, local, run, prefix

REPO_URL = 'https://github.com/cjmochrie/superlists.git'
env.key_filename = 'Z:\Dropbox\Projects\droplet_server\cameron.ppk'


def deploy():

    host = env.host
    virtualenv_folder = '/home/{}/Envs/{}'.format(env.user, host)
    site_folder = '/home/{username}/sites/{host}'.format(username=env.user, host=host)
    source_folder = site_folder + '/source'
    _create_directory_structure_if_necessary(site_folder)
    _get_latest_source(source_folder)
    _update_settings(source_folder, env.host)
    _update_virtualenv(virtualenv_folder, source_folder, host)
    _update_static_files(virtualenv_folder, source_folder)
    _update_database(virtualenv_folder, source_folder)


def _create_directory_structure_if_necessary(site_folder):
    for subfolder in ('database', 'static', 'source'):
        run('mkdir -p {}/{}'.format(site_folder, subfolder))


def _get_latest_source(source_folder):
    if exists(source_folder + '/.git'):
        run('cd {} && git fetch'.format(source_folder))
    else:
        run('git clone {} {}'.format(REPO_URL, source_folder))
    current_commit = local('git log -n 1 --format=%H', capture=True)
    run('cd {} && git reset --hard {}'.format(source_folder, current_commit))


def _update_settings(source_folder, site_name):
    settings_path = source_folder + '/superlists/settings.py'
    sed(settings_path, 'DEBUG = True', 'DEBUG = False')
    sed(settings_path, 'ALLOWED_HOSTS =.+$', 'ALLOWED_HOSTS = ["{}"]'.format(site_name))
    secret_key_file = source_folder + '/superlists/secret_key.py'
    if not exists(secret_key_file):
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
        append(secret_key_file, "SECRET_KEY = '{}'".format(key))
    append(settings_path, '\nfrom .secret_key import SECRET_KEY')


def _update_virtualenv(virtualenv_folder, source_folder, env_name):

    with prefix('WORKON_HOME=~/Envs'):
        with prefix('export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3'):
            with prefix('source /usr/local/bin/virtualenvwrapper.sh'):

                if not exists(virtualenv_folder + '/bin/pip'):
                    run('mkvirtualenv --python=/usr/bin/python3 {}'.format(env_name))
                with prefix('workon {}'.format(env_name)):
                    run('{}/bin/pip install -r {}/requirements.txt'.
                        format(virtualenv_folder, source_folder))


def _update_static_files(virtualenv_folder, source_folder):
    run('cd {source_folder} && {virtualenv_folder}/bin/python3 '
        'manage.py collectstatic --noinput'.format(virtualenv_folder=virtualenv_folder,
                                                   source_folder=source_folder))


def _update_database(virtualenv_folder, source_folder):
    run('cd {source_folder} && {virtualenv_folder}/bin/python3 '
        'manage.py migrate --noinput'.format(source_folder=source_folder,
                                             virtualenv_folder=virtualenv_folder))
