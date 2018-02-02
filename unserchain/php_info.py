from unserchain.php_types import *


def get_function(get_name):
    """get user-defined functions

    :param name: function name
    :return dict of function information
    """
    for name, func_info in RUNTIME_FUNCTION.items():
        if name == get_name:
            return func_info
    return False


def get_magic_method(class_info):
    """get magic method in the class

    :param class_info: class node information
    :return: node information of magic method
    """
    for node_type, node_info in class_info['nodes']:
        if node_type == METHOD and node_info['name'] in MAGIC_METHODS:
            yield node_info


def get_class_ctx(class_info):
    """

    :param class_info:
    :return: context dict
    """
    ret = {
        'class': class_info['name'],
        'evil_methods': {},
        'parsed_methods': [],
        'methods': {},
        'vars': {},
        'chains': {},
    }
    for node_type, node_info in class_info['nodes']:
        if node_type == METHOD:
            ret['methods'][node_info['name']] = node_info

    return ret