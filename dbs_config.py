#!/usr/bin/python
from configparser import ConfigParser


def config(filename='dbs.ini', section='postgresql'):

    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    # get section
    db = {}

    # Check if postgresql parser exists
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]

    # return error if a param is called that is not listed in the init file
    else:
        raise Exception('Section {0} not fround in the {1} file'. format(section,filename))

    return db
