from fabric.api import *
from fabric.contrib import files
from fabric.operations import get, put, prompt
from fabric.context_managers import hide
from fabric.colors import blue, cyan, green, magenta, red, white, yellow
import yaml
from time import sleep
import warnings
import shutil
import os

# import from lib
from libs import git
from libs import mysql


"""
Set single host

env.hosts = ['abc.com']
env.key_filename = './key/abc.pem'
env.user = 'user'
"""

"""
Set group host

env.roledefs = {
    'Project_A': {
        'hosts': ['www1', 'www2', 'www3'],
        'key_filename': './key/www.pem',
        'user': 'www-user',
        'path': '~/source'
    },
    'Project_B': {
        'hosts': ['ns1', 'ns2'],
    }
}
"""

"""
Load from file env.yml
"""
with open("./env.yml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile)

env.roledefs = cfg

"""
Usage: $ fab role:h=staging
"""


@task
def role(h='staging'):
    global role
    role = h

    if not env.roledefs.has_key(h):
        print red("HOST NOT FOUND")
        return

    print yellow("Run with hosts: %(hosts)s, user: %(user)s" % env.roledefs[h])

    if env.roledefs[h].has_key('key_filename'):
        print yellow("Set chmod 400 for %s" % env.roledefs[h]['key_filename'])
        local("chmod 400 %s" % env.roledefs[h]['key_filename'])

    if env.roledefs[h].has_key('hosts'):
        print yellow("Set host %s" % env.roledefs[h]['hosts'])
        env.hosts = env.roledefs[h]['hosts']

    if env.roledefs[h].has_key('user'):
        print yellow("Set user %s" % env.roledefs[h]['user'])
        env.user = env.roledefs[h]['user']

    if env.roledefs[h].has_key('password'):
        print yellow("Set password ********")
        env.password = env.roledefs[h]['password']

    if env.roledefs[h].has_key('project'):
        print yellow("Set project %s" % env.roledefs[h]['project'])
        global project
        project = env.roledefs[h]['project']

    if env.roledefs[h].has_key('db'):
        print yellow("Set mysql host %s" % env.roledefs[h]['db']['host'])
        global db
        db = env.roledefs[h]['db']

"""
Show help
Usage: $ fab help
"""


@task
def help():
    print "Usage:"
    print yellow("<Deploy> : Deploy with branch")
    print "fab role:[ROLE] deploy:[BRANCH]"
    print yellow("<Test Host> : check connection to Server")
    print "fab role:[ROLE] test_host"
    print yellow("<Test> : Run test command in server")
    print "fab role:[ROLE] test:[BRANCH]"
    print yellow("<Remove folder>: Delete folder with branch")
    print "fab role:[ROLE] destroy:[BRANCH]"


"""
Test host active :
Usage: $ fab role:[ROLE] test_host
"""


@task
def test_host():
    warnings.simplefilter('ignore')
    # Test connection to host
    result = run("uname -a")
    if len(result) > 0:
        print yellow("Connected to host")
    else:
        print red("Connect is FAIL")
    
    print yellow(result)
    if 'db' in globals():
        global db
        mysql._connect(db)
        #mysql.command('show tables')

"""
Test host active :
Usage: $ fab role:[ROLE] test
"""


@task
def test(branch=''):
    print red("This function is used to test fabric")
    global project
    warnings.simplefilter('ignore')
    folder = branch.split('/')[-1]
    project_path = project['path'] + folder
    with cd(project_path):
        run("ls -la")
        git.tree()

"""
Usage: $ fab role:[ROLE] deploy:[BRANCH]
       $ fab role:[ROLE] deploy:branch=[BRANCH]
"""


@task
def deploy(branch='', source='', rebuild=False):
    print green("Start build project")
    global project
    warnings.simplefilter('ignore')
    if len(source) > 0:
    	folder = source
    else:
    	folder = branch.split('/')[-1]
    if len(folder) == 0:
        print red("The folder not found")
        return
    __config_ssh_key()
    run("mkdir -p %s" % project['path'])
    with cd(project['path']):
        with settings(hide('warnings', 'running', 'stdout', 'stderr'), warn_only=True):
            print yellow("RUN: pwd")
            print magenta(run("pwd"))
            if rebuild:
                print magenta("Rebuild again for branch %s" % branch)
                destroy(branch, source)
                print green("Start clone source from git for branch %s " % branch)
                git.command("clone", "--branch", branch, project['git'], folder)
            else:
                print yellow("RUN: ls -la | grep %s" % folder)
                result = run("ls -la | grep %s" % folder)
                if not result:
                    print magenta("Check exists source in %s" % folder) + red(": FAILED")
                    print green("Start clone source from git for branch %s " % branch)
                    git.command("clone", "--branch", branch, project['git'], folder)
                else:
                    print red("Check exists source in %s" % folder) + green(": OK")
                    print green("The folder for branch %s is exists" % branch)
    __build_project(branch, source)


"""
Usage: $ fab role:[ROLE] __build_project:[BRANCH]
       $ fab role:[ROLE] __build_project:branch=[BRANCH]
"""


@task
def __build_project(branch, source=''):
    global project
    if len(source) > 0:
        folder = source
    else:
        folder = branch.split('/')[-1]
    if len(folder) == 0:
        print red("The folder not found")
        return
    project_path = project['path'] + folder
    with cd(project_path):
        print yellow("RUN: pwd")
        print magenta(run("pwd"))
        git.command('fetch origin')
        git.command('reset', 'origin/' + branch, '--hard')
        git.branch()
        __update_source(branch, source)
        print yellow("RUN: ls -la")
        run("ls -la")
        git.branch()
        print green("Completed build project")


"""
Usage: $ fab role:[ROLE] __update_source:[BRANCH]
       $ fab role:[ROLE] __update_source:branch=[BRANCH]
"""


@task
def __update_source(branch, source=''):
    global project
    if len(source) > 0:
        folder = source
    else:
        folder = branch.split('/')[-1]
    if len(folder) == 0:
        print red("The folder not found")
        return
    project_path = project['path'] + folder
    with cd(project_path):
        with settings(hide('warnings', 'running', 'stdout', 'stderr'), warn_only=True):
            print yellow("RUN: rm -rf %s/uploads/" % project_path)
            sudo("rm -rf %s/uploads/" % project_path)
            print yellow("RUN: ln -s %s/uploads %s/uploads" % (project['shared_path'], project_path))
            sudo("ln -s %s/uploads %s/uploads" % (project['shared_path'], project_path))
            print yellow("RUN: chmod -R g+w %s%s" % (project_path, project['cache_source_path']))
            sudo("chmod -R g+w %s%s" % (project_path, project['cache_source_path']))
            print yellow("RUN: rm -rf %s/database/" % project_path)
            sudo("rm -rf %s/database/" % project_path)
            print yellow("RUN: rm -rf %s%s" % (project_path, project['logs_source_path']))
            sudo("rm -rf %s%s" % (project_path, project['logs_source_path']))
            print yellow("RUN: ln -s %s/data %s/data" % (project['shared_path'], project_path))
            sudo("ln -s %s/data %s/data" % (project['shared_path'], project_path))
            print yellow("RUN: ln -s %s/logs %s%s"% (project['shared_path'], project_path, project['logs_source_path']))
            sudo("ln -s %s/logs %s%s"% (project['shared_path'], project_path, project['logs_source_path']))
            htaccess_source_file = open('./config/.htaccess.sample', 'r')
            htaccess_destination_file = open('./config/.htaccess', 'w')
            for _line in htaccess_source_file:
                htaccess_destination_file.write(_line.replace('RewriteBase', '#RewriteBase'))
            htaccess_source_file.close()
            htaccess_destination_file.close()
            source_file = open('./config/config.php.sample', 'r')
            destination_file = open('./config/config.php', 'w')
            for line in source_file:
                destination_file.write(line.replace('ticket_branch_folder', folder))
            source_file.close()
            destination_file.close()
    config_folder = project_path + '/system/virtualpost/config/development'
    print yellow("RUN: Move file new config to folder")
    put("./config/config.php", config_folder + '/config.php')
    print yellow("RUN: Move file .htaccess to root folder")
    put("./config/.htaccess", '.htaccess')
    os.remove("./config/config.php")
    os.remove("./config/.htaccess")

"""
Usage: 
$ fab role:[ROLE] __config_ssh_key
"""


def __config_ssh_key():
    print yellow("Setup secret key and Git access key")
    # Set SSH key
    with settings(hide('warnings', 'running', 'stdout', 'stderr'), warn_only=True):
        result = run("ls -la ~/.ssh/ | grep id_rsa")

    if not result:
        print red("We need id_rsa , id_rsa.pub in folder:  ./key")
        put("./key/id_rsa", "~/.ssh/id_rsa")
        put("./key/id_rsa.pub", "~/.ssh/id_rsa.pub")
        sudo("chmod 400 ~/.ssh/id_rsa")
        sudo("chmod 400 ~/.ssh/id_rsa.pub")

"""
Usage: $ fab role:[ROLE] destroy:[BRANCH]
       $ fab role:[ROLE] destroy:branch=[BRANCH]
"""


@task
def destroy(branch='', source = ''):
    global project
    warnings.simplefilter('ignore')
    if len(source) == 0:
    	folder = branch.split('/')[-1]
    else:
        folder = source
    if len(folder) == 0:
        print red("The folder not found")
        return
    print green("Start remove folder")
    source = project['path'] + folder
    with cd(project['path']):
        with settings(hide('warnings', 'running', 'stdout', 'stderr'), warn_only=True):
            print magenta("Check exists folder source to delete")
            print yellow("RUN: ls -la | grep %s" % folder)
            result = run("ls -la | grep %s" % folder)
            if result:
                print yellow("RUN: rm -rf %s " % folder)
                sudo("rm -rf %s" % folder)
                print green("The folder %s was delete successfully" % folder)
            else:
                print green("The folder %s not exists on server" % folder)

    print green("Completed remove folder")
