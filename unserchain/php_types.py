
# types
CLASS = 'Class'
METHOD = 'Method'
FUNCTION = 'Function'
EVAL = 'Eval'
CLASS_VARIABLES = 'ClassVariables'

# statements
BLOCK = 'Block'
IF = 'If'
RETURN = 'Return'
FOREACH = 'Foreach'
SWITCH = 'Switch'
ASSIGNMENT = 'Assignment'
ELSE = 'Else'

# op
TERNARY_OP = 'TernaryOp'
BINARY_OP = 'BinaryOp'
UNARY_OP = 'UnaryOp'

# action
FUNCTION_CALL = 'FunctionCall'
METHOD_CALL = 'MethodCall'

# others
DANGEROUS_FUNCTIONS = [
    'exec', 'shell_exec', 'call_user_func', 'call_user_func_array', 'file_put_contents', 'file_get_contents',
    'popen', 'readfile', 'passthru', 'proc_open',
]

MAGIC_METHODS = [
    '__construct', '__destruct', '__call', '__callStatic', '__get', '__set', '__isset', '__unset',
    '__sleep', '__wakeup', '__toString', '__invoke', '__set_state', '__clone', '__debugInfo',
]

RUNTIME_FUNCTION = {}
USER_DEFINED_DANGEROUS_FUNCTION = []
PARSED_FUNCTION = []
