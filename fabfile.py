from fabric.api import *
from fabric.operations import run
from fabric.context_managers import cd
from fabric.api import env, prefix
from fabric.contrib.console import confirm


env.hosts = ['join.agiliq.com']
env.user = "join_agiliq"
env.directory = "~/jobs_env/jobs"
env.activate = 'source ~/jobs_env/bin/activate'
env.colorize_errors = True


def test():
    with settings(warn_only=True):
        result = local('python manage.py test api application user_profile',
                       capture=True)
    if result.failed and not confirm("Tests failed. Continue anyway?"):
        abort("Aborting at user request.")


def restart():
    print("Restarting Gunicorn...")
    run("~/gunicorn_restart.sh")
    print("Gunicorn Restarted...\n")


def syncdb():
    print("syncdb...")
    run("python manage.py syncdb")


def migrate():
    print("Migrating...")
    run("python manage.py migrate")


def install_requirements():
    print("Installing requirements..")
    run("pip install -r requirements.txt")


def pull():
    print("Pulling the latest code...")
    run("git pull")


def deploy():
    with cd(env.directory):
        with prefix(env.activate):
            pull()
            install_requirements()
            migrate()
            syncdb()
            restart()
