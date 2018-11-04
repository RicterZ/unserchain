import os
import phply.phplex
import phply.phpparse
from phply.phpparse import make_parser
from unserchain.logger import logger


def export(items):
    result = []
    if items:
        for item in items:
            if hasattr(item, 'generic'):
                item = item.generic(with_lineno=True)
            result.append(item)

    return result


def parser(filename):
    if not os.path.exists(filename):
        return {}

    with open(filename) as f:
        code = f.read()

    reload(phply.phplex)
    logger.debug('Parse file: %s' % filename)
    return export(make_parser().parse(code, lexer=phply.phplex.lexer, tracking=True))
