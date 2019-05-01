# -*- coding: utf-8 -*-
from fabric.api import run
from fabric.colors import blue, cyan, green, magenta, red, white, yellow


def _connect(connect):
    global db
    db = connect


def command(query):
    global db
    print yellow("RUN: '%s'" % query)
    run("mysql -h %s -u%s -p%s %s -e '%s'" %
        (db['host'], db['username'], db['password'], db['database'], query))


def _run():
    global db
    print yellow("Connect to MYSQL")
    run("mysql -h %s -u%s -p%s %s" %
        (db['host'], db['username'], db['password'], db['database']))
