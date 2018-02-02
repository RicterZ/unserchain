import os
import itertools
from pprint import pprint

from unserchain.php_types import *
from unserchain.parser import parser
from unserchain.checker import check_function, check_method
from unserchain.php_info import get_magic_method, get_class_ctx
from unserchain.logger import logger


def register_functions(info):
    for type_, defined_info in info:
        if type_ == FUNCTION:
            RUNTIME_FUNCTION[defined_info['name']] = defined_info


def build_chains(context):
    if not context['evil_methods']:
        return

    result_dict = {}
    for method, chain in context['evil_methods'].items():
        result = []
        for i in chain:
            if isinstance(chain, list):
                while isinstance(i, list) and len(i) == 1:
                    i = i[0]
                result.append(i)
            else:
                if chain not in result:
                    result = [chain]

        chain = result
        result_dict[method] = chain

    entry_keys = [k for k in result_dict.keys() if k not in itertools.chain(*result_dict.values())]

    def output_map(map_, k, ret=None):
        if ret is None:
            ret = []
        if k in map_:
            ret.append(k)
            # map_[k][0] ignore others chain
            return output_map(map_, map_[k][0], ret)
        else:
            ret.append(k)
            return ret

    for k in entry_keys:
        chain_list = output_map(result_dict, k)
        logger.info('Class %s ' % context['class'] + ' -> '.join(chain_list))

def check(result):
    for type_, info in result:
        if type_ == CLASS:
            ctx = get_class_ctx(info)
            for node_info in get_magic_method(info):
                logger.debug(node_info['name'])
                ctx['chains'][node_info['name']] = []
                check_method(node_info, ctx=ctx)

            build_chains(context=ctx)
            # logger.info('Class %s: %s' % (info['name'], ret))


def main():
    # path = r'C:\Users\ricterzheng\Downloads\wordpress'
    path = os.path.join(os.path.dirname(__file__), '../resources')
    for root, _, files in os.walk(path):
        for filename in files:
            if filename.endswith('.php'):
                php_file = os.path.abspath(os.path.join(root, filename))
                result = parser(php_file)
                result = [i for i in result if i]

                register_functions(result)
                for name, func_info in RUNTIME_FUNCTION.items():
                    check_function(func_info)
                check(result)


if __name__ == '__main__':
    main()
