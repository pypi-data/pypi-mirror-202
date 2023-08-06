import os
import inspect


def init_script():
    import sys
    from os.path import dirname
    root_path = dirname(dirname(dirname(__file__)))
    sys.path.append(root_path)


def get_root_dir(root_dir_name):
    return os.getcwd()[:os.getcwd().find(root_dir_name) + len(root_dir_name)]


def change_to_root_dir(root_dir_name):
    root_path = get_root_dir(root_dir_name)
    os.chdir(root_path)
    # print('Working dir has been set as: ' + root_path)


def get_cur_func_name():
    return inspect.stack()[1][3]

