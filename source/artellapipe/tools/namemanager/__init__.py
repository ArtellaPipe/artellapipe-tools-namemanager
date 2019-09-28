#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Initialization module for artellapipe-tools-namemanager
"""

import os
import inspect

import sentry_sdk
sentry_sdk.init("https://d50e6953c45b44609a9e88d3bc3064d8@sentry.io/1764141")

from tpPyUtils import importer

from artellapipe.utils import exceptions


class NameManager(importer.Importer, object):
    def __init__(self):
        super(NameManager, self).__init__(module_name='artellapipe.tools.namemanager')

    def get_module_path(self):
        """
        Returns path where tpNameIt module is stored
        :return: str
        """

        try:
            mod_dir = os.path.dirname(inspect.getframeinfo(inspect.currentframe()).filename)
        except Exception:
            try:
                mod_dir = os.path.dirname(__file__)
            except Exception:
                try:
                    import tpDccLib
                    mod_dir = tpDccLib.__path__[0]
                except Exception:
                    return None

        return mod_dir


def init(do_reload=False):
    """
    Initializes module
    """

    packages_order = []

    namemanager_importer = importer.init_importer(importer_class=NameManager, do_reload=False)
    namemanager_importer.import_packages(order=packages_order, only_packages=False)
    if do_reload:
        namemanager_importer.reload_all()

    create_logger_directory()


@exceptions.sentry_exception
def run(project, do_reload=False):
    """
    Run NameManager Tool
    :param project: ArtellaProject
    :param do_reload: bool
    :return: ArtellaManager
    """

    init(do_reload=do_reload)
    from artellapipe.tools.namemanager import namemanager
    win = namemanager.run(project=project)
    return win


def create_logger_directory():
    """
    Creates artellapipe-gui logger directory
    """

    artellapipe_logger_dir = os.path.normpath(os.path.join(os.path.expanduser('~'), 'artellapipe', 'logs'))
    if not os.path.isdir(artellapipe_logger_dir):
        os.makedirs(artellapipe_logger_dir)


def get_logging_config():
    """
    Returns logging configuration file path
    :return: str
    """

    return os.path.normpath(os.path.join(os.path.dirname(__file__), '__logging__.ini'))


def get_logging_level():
    """
    Returns logging level to use
    :return: str
    """

    if os.environ.get('ARTELLAPIPE_TOOLS_NAMEMANAGER_LOG_LEVEL', None):
        return os.environ.get('ARTELLAPIPE_TOOLS_NAMEMANAGER_LOG_LEVEL')

    return os.environ.get('ARTELLAPIPE_TOOLS_NAMEMANAGER_LOG_LEVEL', 'WARNING')
