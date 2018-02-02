from functools import wraps
from pprint import pprint

from php_info import get_function
from unserchain.php_types import *
from unserchain.logger import logger


def context(f):
    @wraps(f)
    def wrapper(*args, **kwargs):

        if 'ctx' in kwargs:
            ctx = kwargs['ctx']
            ret = f(*args, ctx=ctx)
        else:
            ret = f(*args, **kwargs)

        if ret and 'ctx' in kwargs:
            # print 'RET', ret
            if 'name' in args[0]:
                if args[0]['name'] in kwargs['ctx']['chains']:
                     kwargs['ctx']['chains'][args[0]['name']].append(ret)

        return ret

    return wrapper


@context
def check_eval(node_info, **kwargs):
    return 'eval'


@context
def check_block(node_info, **kwargs):
    ret_list = []
    for node_type, node in node_info['nodes']:
        checke_func = CHECKER_MAP.get(node_type)
        if checke_func:
            ret = checke_func(node, **kwargs)
            if ret:
                ret_list.append(ret)

    return ret_list


@context
def check_function_call(node_info, **kwargs):
    """check function call

    :return str or None
    """
    if node_info['name'] in DANGEROUS_FUNCTIONS or node_info['name'] in USER_DEFINED_DANGEROUS_FUNCTION:
        logger.debug('Dangerous function call detected: %s' % node_info['name'])
        return node_info['name']

    if node_info['name'] not in PARSED_FUNCTION:
        PARSED_FUNCTION.append(node_info['name'])
        func = get_function(node_info['name'])
        if not func:
            return

        check_function(func)
        return check_function_call(node_info)


@context
def check_function(info, **kwargs):
    ret_list = []
    for _ in info['nodes']:
        if not _:
            continue
        t, i = _
        check_func = CHECKER_MAP.get(t)
        if check_func:
            ret = check_func(i, **kwargs)
            if ret:
                ret_list.append(ret)
                USER_DEFINED_DANGEROUS_FUNCTION.append(info['name'])

    return ret_list


@context
def check_method_call(node_info, ctx=None):
    if ctx is not None:
        if isinstance(node_info['name'], str):
            logger.debug('Method call: %s' % node_info['name'])

        if isinstance(node_info['name'], str):
            if node_info['name'] in ctx['evil_methods']:
                return node_info['name']

        if not node_info['name'] in ctx['parsed_methods']:
            if isinstance(node_info['name'], str):
                ctx['parsed_methods'].append(node_info['name'])
                check_method(ctx['methods'].get(node_info['name']), ctx=ctx)
                return check_method_call(node_info, ctx=ctx)


@context
def check_method(node_info, ctx=None):
    """check magic method

    :param node_info: magic method node information
    :param ctx: class context
    :return:
    """
    if ctx is not None:
        ret_list = []
        if not node_info:
            return

        for _ in node_info['nodes']:
            if not _:
                continue
            t, i = _
            check_func = CHECKER_MAP.get(t)
            if check_func:
                ret = check_func(i, ctx=ctx)
                if ret:
                    ret_list.append(ret)
                    # do something else
                    ctx['evil_methods'][node_info['name']] = ret

        return ret_list


@context
def check_expr(node_info, **kwargs):
    # pprint(node_info)
    pass


@context
def check_foreach(node_info, **kwargs):
    """
    node_info["node"]: The main block
    node_info["expr"]: expr

    :param node_info:
    :param kwargs:
    :return:
    """
    return check_common_by_keyword(FOREACH, node_info, **kwargs)


@context
def check_assignment(node_info, **kwargs):
    """
    node_info["expr"]: the expr

    :param node_info:
    :param kwargs:
    :return:
    """
    return check_common_by_keyword(ASSIGNMENT, node_info, **kwargs)


@context
def check_else(node_info, **kwargs):
    return check_common_by_keyword(ELSE, node_info, **kwargs)


@context
def check_if(node_info, **kwargs):
    """
    node_info['elseifs']: list of if nodes
    node_info['else_']: Else node
    node_info['node']: main block
    node_info['expr']: the expr of `if (expr)`
    """
    return check_common_by_keyword(IF, node_info, **kwargs)


@context
def check_ternary_op(node_info, **kwargs):
    """
    node_info['expr']: the expr
    node_info['iffalse']: false block
    node_info['iftrue']: true block

    :param node_info:
    :param kwargs:
    :return:
    """
    return check_common_by_keyword(TERNARY_OP, node_info, **kwargs)


@context
def check_return(node_info, **kwargs):
    return check_common_by_keyword(RETURN, node_info, **kwargs)


@context
def check_common_by_keyword(node_type, node_info, **kwargs):
    ret_list = []
    for i in KEYWORD_MAP.get(node_type, []):
        try:
            type_, info = node_info.get(i)
            check_func = CHECKER_MAP.get(type_)
            if check_func:
                ret = check_func(info, **kwargs)
                if ret:
                    ret_list.append(ret)
        except (TypeError, ValueError) as e:
            pass

    return ret_list


KEYWORD_MAP = {
    TERNARY_OP: ('expr', 'iffalse', 'iftrue'),
    IF: ('node', 'expr', 'else_'),
    ELSE: ('node', ),
    FOREACH: ('node', 'expr'),
    ASSIGNMENT: ('expr', 'node'),
    RETURN: ('node', )
}


CHECKER_MAP = {
    METHOD_CALL: check_method_call,
    BLOCK: check_block,
    FUNCTION_CALL: check_function_call,
    IF: check_if,
    EVAL: check_eval,
    METHOD: check_method,
    FUNCTION: check_function,
    FOREACH: check_foreach,
    ASSIGNMENT: check_assignment,
    TERNARY_OP: check_ternary_op,
    ELSE: check_else,
    RETURN: check_return,
}


