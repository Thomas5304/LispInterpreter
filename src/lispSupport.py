
import tokenParse
import closure


def lisp_format(fmt, *args):
    try:
        return fmt.format(*args)
    except Exception as e:
        raise ValueError(f"format Fehler: {e}")

def greater(a, b):
    ret = True if a>b else None
    return ret

def greaterequal(a, b):
    ret = True if a>=b else None
    return ret

def less(a, b):
    ret = True if a<b else None
    return ret

def lessequal(a, b):
    ret = True if a<=b else None
    return ret

def equal(a, b):
    ret = True if a==b else None
    return ret

def add(*args):
    if any(isinstance(arg, str) for arg in args):
        return ''.join(str(arg) for arg in args)
    try:
        return sum(args)
    except TypeError as te:
        print(f"{te} {args}")
        traceback.print_exc()

def mult(*args):
    result = 1
    for arg in args:
        result *= arg
    return result

def sub(*args):
    l = len(args)
    if l == 0:
        raise ValueError("sub with no argument")
    if l == 1:
        return -args[0]
    result = args[0]
    for arg in args[1:]:
        result -= arg
    return result

def div(*args):
    l = len(args)
    if l == 0:
        raise ValueError("sub with no argument")
    result = args[0]
    for arg in args:
        result /= arg
    return result

def car(args):
    if not isinstance(args, list) or len(args)==0:
        raise ValueError("car expects non empty list")
    return args[0]

def cdr(args):
    if not isinstance(args, list) or len(args)==0:
        return 'nil'
    return args[1:]

def create_list(*args):
    return list(args)

def eval_append(lst, *args):
    for arg in args:
        if isinstance(arg, list):
            lst.extend(arg)
        else:
            lst.append(arg)
    return lst

def lisp_map(func, *args):
    if not isinstance(func, FunctionDef) and not callable(func):
        raise TypeError(f"map: can't call func {func}")

    for nr, lst in enumerate(args):
        if not isinstance(lst, list):
            raise TypeError(f"map: element at {nr} is not a list")
    result = []

    for items in zip(*args):
        value = func(*items)
        result.append(value)

    return result

def lisp_mapcar(func, *lists):
    # Prüfe: mindestens eine Liste
    if len(lists) == 0:
        raise TypeError("mapcar braucht mindestens eine Liste")

    # stoppe, wenn irgendeine Liste leer ist
    result = []
    # Annahme: Listen werden als Python-Listen repräsentiert
    while all(lst for lst in lists):  # leere Liste == [] falsy
        # aktuelle Köpfe
        heads = [lst[0] for lst in lists]

        val = func(*heads)

        result.append(val)
        # advance lists
        lists = [lst[1:] for lst in lists]
    return result

def lisp_apply(func, *args):
    # args: optional vorangestellte Argumente, das letzte Argument muss eine Liste sein
    if len(args) == 0:
        raise TypeError("apply braucht mindestens ein Argument: die Argumentliste")
    arglist = args[-1]
    prefix = list(args[:-1])

    #print(f"{arglist=}")
    #print(f"{prefix=}")

    if not isinstance(arglist, list):
        raise TypeError("apply: letztes Argument muss eine Liste sein")

    full_args = prefix + list(arglist)

    # func kann ein Python-callable (builtin) oder eine Closure sein
    return func(*full_args)

#(print-eval (apply + 20 30 '(1 2 3 4 5)))

def print_lisp_recursive(expression):
    if isinstance(expression, tokenParse.Symbol):
        return expression
    elif isinstance( expression, str):
        return f'"{expression}"'
    elif isinstance( expression, (int, float, str)):
        return str(expression)
    elif isinstance(expression, (tuple, list)):
        ret = "("
        for e in expression:
            ret+=print_lisp_recursive(e)+" "
        ret.rstrip()
        ret += ")"
        return ret
    return "???"


