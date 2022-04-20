"""

    PATH MANAGER UTILITY.
    Utilities for managing paths and folders.

"""

from argparse import Namespace
from os import mkdir, getenv


def create_directory(dir_name):
    """
    Create a directory. If the directory already exists, then do nothing.
    Args:
        dir_name: The path for the directory to be created

    """
    try:
        mkdir(dir_name)
    except:
        pass


def get_base_path():
    """
    Gets the base path for the database files
    Returns:    a string representing the base folder for the database files

    """
    db_path_env = getenv('DB_PATH', 'unset')
    if db_path_env == 'unset':
        create_directory('data')
        create_directory('data/temp')
        create_directory('data/temp/temp_folder')
        base_path = 'data/'
    else:
        # exploit path binding of docker
        create_directory('db')
        create_directory('db/temp')
        create_directory('db/temp/temp_folder')
        base_path = 'db/'
    return base_path


def get_db_paths():
    """
    Compute the values for db_path, temp_dir, temp_db1_path e temp_db1_path.
    If there is an env variable DB_PATH defining the path, then it is used as destination.
    Otherwise, a default path is used.
    Returns:    Namespace containing the values for db_path, temp_dir, temp_db1_path e temp_db1_path

    """
    base_path = get_base_path()
    args = Namespace()

    args.__setattr__('db_path', base_path + 'varianthunter.db')

    args.__setattr__('temp_tree', base_path + 'temp/')
    args.__setattr__('temp_dir', base_path + 'temp/temp_folder/')
    args.__setattr__('temp_db1_path', base_path + 'temp/temp_table1.db')
    args.__setattr__('temp_db2_path', base_path + 'temp/temp_table2.db')
    return args


db_paths = get_db_paths()
"""
    Namespace containing the values for db_path, temp_dir, temp_db1_path e temp_db1_path
"""

db_path = db_paths.db_path
"""
    Path to the main database
"""
