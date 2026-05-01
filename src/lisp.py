#!/tools/pdtooling/packages/VirtPythonEnv/pkg_synopsys/bin/python3
from cmath import isinf
from re import L
from tokenize import Token
import textwrap
from enum import Enum, auto
from typing import Callable, Any, Iterable, Generator, TypeVar
from dataclasses import dataclass, field
import os
import sys
from pathlib import Path
import traceback


def oldtokenize(lisp_expression:str)->Generator[str, None, None]:
    s = lisp_expression.replace("(", " ( ").replace(")"," ) ").replace("'", " ' ")
    s = s.replace("`", " ` ").replace("'", " ' ")

    for token in s.split():
        yield token

def tokenize(s: str):
    i = 0
    while i < len(s):
        c = s[i]

        # whitespace
        if c.isspace():
            i += 1
            continue

        # Klammern
        if c in '()':
            yield c
            i += 1
            continue

        # quote / quasiquote / unquote
        if c in "'`,":
            yield c
            i += 1
            continue

        # STRING
        if c == '"':
            i += 1
            start = i
            value = ""

            while i < len(s):
                if s[i] == '"' and s[i-1] != '\\':
                    break
                value += s[i]
                i += 1

            i += 1  # schließendes "
            yield ('STRING', value)
            continue

        # SYMBOL / ZAHL
        start = i
        while i < len(s) and not s[i].isspace() and s[i] not in '()\'`,"':
            i += 1

        yield s[start:i]

def tokenize_file(filename: Path)->Generator[str, None, None]:
    with open(filename) as filehandle:
        for line in filehandle.readlines():
            yield from tokenize(line)

class Symbol(str):
    pass

def atom(token):
    if isinstance(token, tuple):
        return token[1]
    try:
        return int(token)
    except:
        try:
            return float(token)
        except:
            return Symbol(token)  # Symbol (z. B. '+', 'x')

def is_list(x):return isinstance(x,list)
def is_symbol(x):return isinstance(x,Symbol)

def parse(tokens, program = list()):
    class TokenStream:
        def __init__(self, generator):
            self.gen = generator
            self.buffer = None

        def next(self):
            if self.buffer is not None:
                token = self.buffer
                self.buffer = None
                return token
            return next(self.gen)

        def peek(self):
            if self.buffer is None:
                self.buffer = next(self.gen)
            return self.buffer

    def parse_stream(token_stream):
        token = token_stream.next()

        #print(token)

        if token == '(':
            lst = []
            while token_stream.peek() != ')':
                lst.append(parse_stream(token_stream))
            _ = token_stream.next()  # ')'

            #print(f"close list {lst}")
            return lst

        elif token == ')':
            raise SyntaxError("Unerwartetes )")

        elif token == "'":
            return ['quote', parse_stream(token_stream)]

        elif token == '`':
            return ['quasiquote', parse_stream(token_stream)]

        elif token == ',':
            return ['unquote', parse_stream(token_stream)]

        else:
            return atom(token)

    stream = TokenStream(tokens)
    try:
        while True:
            program.append(parse_stream(stream))
    except StopIteration:
        return program

class Env:
    def __init__(self, parent = None):
        self.data = {}
        self.parent = parent

    def get(self, name):
        if name in self.data:
            return self.data[name]
        if self.parent is not None:
            return self.parent.get(name)
        raise NameError(f"unbound symbol: {name}")

    def set(self, name, value):
        self.data[name] = value

    def init_env(self, debug_level=0):
        self.debug_level = debug_level
        self.set('nil', False)
        self.set('t', True)
        self.set('format', lisp_format)
        self.set('string-append', lambda *args: ''.join(str(arg) for arg in args))
        self.set('print', print)
        self.set('list', create_list)
        self.set('cons', lambda l, a: l.append(a))
        self.set('and', lambda a, b: a and b)
        self.set('or', lambda a, b: a or b)
        self.set('zip', lambda *a: list(zip(*a)))
        self.set('null', lambda a: "t" if a==[] or a=="nil" else "nil")
        self.set('atom?', lambda a: "t" if not is_list(a) else "nil")
        self.set('integer?', lambda a: "t" if isinstance(a, int) else "nil")
        self.set('number?', lambda a: "t" if isinstance(a, float) else "nil")
        self.set('function?', lambda a: "t" if callable(a) else "nil")
        self.set('+'   , add)
        self.set('-'   , sub)
        self.set('*'   , mult)
        self.set('/'   , div)
        self.set('>='  , greaterequal)
        self.set('>'   , greater)
        self.set('<='  , lessequal)
        self.set('<'   , less)
        self.set('=='  , equal)
        self.set('not' , lambda x: not x)
        self.set('car' , car)
        self.set('cdr' , cdr)
        self.set('print-env', lambda *args: print(str(self)))
        self.set('map', lisp_map)
        self.set('mapcar', lisp_mapcar)
        self.set('apply', lisp_apply)
        self.set('exit', lambda exit_code=0: exit(exit_code) if exit_code is not None else exit(0))
        #self.set('debug', lambda debug_level=None: set_debug_level(debug_level))
        self.set('last-expr!', None)

    def overwrite(self, name, value):
        if name in self.data.keys():
            #print(f"found {name=} old value={self.data[name]}")
            self.data[name] = value
            return True
        if self.parent is None:
            #print("no parent, returning False")
            return False
        #print("search in parent")
        return self.parent.overwrite(name, value)


    def empty(self):
        if len(self.data) == 0:
            return True
        return False

    def __str__(self):
        ret = ""
        if self.parent is not None:
            ret += str(self.parent)
        return ret + str(self.data)


def lisp_format(fmt, *args):
    try:
        return fmt.format(*args)
    except Exception as e:
        raise ValueError(f"format Fehler: {e}")

def create_list(self, args):
     return list(args)

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


def cond(*args):
    pass

#(print-eval (apply + 20 30 '(1 2 3 4 5)))

def print_lisp_recursive(expression):
    if isinstance(expression, Symbol):
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



class FunctionDef:
    def __init__(self, closure, params, body) -> None:
        self.closure = closure
        self.params = params
        self.body = body


    def bind_params(self, *args):
        new_env =Env(self.closure)
        if '&rest' in self.params:
            idx = self.params.index('&rest')
            before = self.params[:idx]
            if idx+1 > len(self.params):
                raise SyntaxError("&rest needs a following parameter name")
            rest_name = self.params[idx+1]
            if len(args) < len(before):
                raise TypeError("missing arguments")
            for name, val in zip(before, args[:len(before):]):
                new_env.set(name,val)
            new_env.set(rest_name, list(args[len(before):]))
        else:
            if len(args) != len(self.params):
                raise TypeError(f"wrong number of arguments, expecting {len(self.params)} got {len(args)}")

            for name, val in zip(self.params, args):
                new_env.set(name, val)
        return new_env

    def __call__(self, *values):
        new_env = self.bind_params(*values)
        return eval_lisp(new_env, self.body)

class Macro:
    def __init__(self, proc):
        self.proc = proc

    def expand(self, *raw_args):
        result = self.proc(*raw_args)
        #print("Macro.expand:", result)
        return result

def is_macro(x):return isinstance(x, Macro)

def macroexpand(env, ast):
    while is_list(ast) and len(ast) > 0 and is_symbol(ast[0]):
        head = ast[0]
        try:
            val:Symbol|list|Macro|FunctionDef|None = env.get(head)
        except Exception:
            val:Symbol|list|Macro|FunctionDef|None = None

        if is_macro(val):
            macro : Macro = val

            raw_args = ast[1:]

            #print(f"macroexpand {head} before: {raw_args}\n")

            #print(f"macro param: {macro.proc.params} set to {raw_args}\n")
            ast = macro.expand(*raw_args)
            if isinstance(ast, Env):
                raise TypeError("this is a Env")
            #print(f"macroexpand {head}  after: {ast}\n\n")

            continue

        else:
            break

    #print(f"after macroexpand {ast}")
    return ast



def print_and_eval(env, *args):
    toprint = print_lisp_recursive(*args)
    evaluated = eval_lisp(env, *args)
    print(f"{toprint} evaluates to {evaluated}")
    return evaluated

def eval_lisp(env:Env, expression):
    specialforms = {
        'if':         ifthenelse,
        'define':     define,
        'let':        let,
        'lambda':     create_lambda,
        'defun':      define_function,
        'quote':      quote,
        'quasiquote': quasiquote,
        'unquote':    unquote,
        'eval':       eval,
        'begin':      begin,
        'set!':       overwrite,
        'load':       load_and_parse_lisp_file,
        'defmacro':   defmacro,
        'while':      while_loop,
        'print-eval': print_and_eval,
    }
    try:
        if isinstance(expression, Symbol):
            return env.get(expression)

        if isinstance(expression, str):
            return expression

        if isinstance(expression, (float,int)):
            return expression

        if not isinstance(expression, (list, tuple)):
            raise ValueError(f"invalid value {expression}")

        expression = macroexpand(env, expression)

        function = expression[0]
        args = expression[1:]

        if isinstance(function, list):
            function = eval_lisp(env, function)

        if function in specialforms:
            return specialforms[function](env, *args)


        values = [eval_lisp(env, arg) for arg in args]

        if isinstance(function, str):
            func = env.get(function)
        else:
            func = function
        if isinstance(func, FunctionDef):
            return func(*values)
        elif callable(func):
            return func(*values)
        else:
            raise ValueError(f"unknown function {function}")
    except ValueError as ve:
        print(f"{ve}\n in {print_lisp_recursive(expression)}")
    except Exception as e:
        print(f"{e}\n in {print_lisp_recursive(expression)}")


def run(lisp_tree : list[Any], env:Env):
    for e in lisp_tree:
        env.set('last-expr!', eval_lisp(env, e))
    if env.get('last-expr!') is not None:
        print(env.get('last-expr!'))



def create_lambda(env, *args):
    params, body = args
    return FunctionDef(env, params, body)

def define_function(env, *args):
    name, params, body = args
    try:
        #print(f"try to add function {name} ({params}) {body}")
        env.set(name, None)
        func = FunctionDef(env, params, body)
        if not env.overwrite(name, func):
            raise NameError(f"expecting function {name} in environtment")
    except NameError as ne:
        print(f"function {name} not defined: {ne}")

def while_loop(env, cond_expr, *body_exprs):
    last_val = None
    while(eval_lisp(env, cond_expr)):
        try:
            for expr in body_exprs:
                last_val = eval_lisp(env, expr)
        except Exception as e:
            print(e)
    return last_val

def defmacro(env, name, params, body):
    proc = FunctionDef(env, params, body)
    env.set(name, Macro(proc))

def begin(env, *args):
    expressions = args
    ret = None
    for expression in expressions:
        ret = eval_lisp(env, expression)
    return ret

def ifthenelse(env, condition, true_branch, false_branch = None):
    cond_result = eval_lisp(env, condition)
    if cond_result is not None and (cond_result == "t" or cond_result == True):
        return eval_lisp(env, true_branch)
    elif false_branch is not None:
        return eval_lisp(env, false_branch)
    return "nil"

def define(env: Env, *args):
    (var, value) = args
    env.set(var, eval_lisp(env, value))

def overwrite(env, var, value):
    return "t" if env.overwrite(var, value) else "nil"

def let(env: Env, vars, *expressions):
    env = Env(env)

    for var in vars:
        define(env, *var)

    ret = None

    for expression in expressions:
        ret = eval_lisp(env, expression)

    # The new env is deleted automatically
    # env = env.parent

    return ret



def quote(env, args):
    return args


def quasiquote(env, ast, depth=1):
    """
    ast: AST node (atom or list)
    env: environment used to eval unquote parts
    depth: nesting level of quasiquote (1 = we are in quasiquote)
    Returns: AST with unquotes evaluated (for macro expansion)
    """
    # atoms: just return quoted atom as-is (symbols/numbers)
    if not is_list(ast):
        return ast

    # empty list stays empty
    if len(ast) == 0:
        return []

    # If head is 'quasiquote', increase depth and recurse into its body
    if is_symbol(ast[0]) and ast[0] == 'quasiquote':
        # (quasiquote X) -> treat inner with depth+1
        return ['quasiquote', quasiquote(env, ast[1], depth+1)]

    # Handle unquote only when depth == 1 (i.e. this quasiquote level)
    if is_symbol(ast[0]) and ast[0] == 'unquote':
        if depth == 1:
            # evaluate the inner expression in env and return the result (AST)
            return eval_lisp(env, ast[1])
        else:
            # inside deeper quasiquote: treat as literal unquote form
            return ['unquote', quasiquote(env, ast[1], depth-1)]

    # Handle unquote-splicing, only valid inside list context when depth == 1
    if is_symbol(ast[0]) and ast[0] == 'unquote-splicing':
        if depth == 1:
            # evaluate to a list that will later be spliced
            return ('__UNQUOTE_SPLICED__', eval_lisp(env, ast[1]))
        else:
            return ['unquote-splicing', quasiquote(env, ast[1], depth-1)]

    # General list processing: iterate elements, handle splicing markers
    result = []
    for elem in ast:
        q = quasiquote(env, elem, depth)
        # If element returned a special splicing marker, splice its value into result
        if isinstance(q, tuple) and q and q[0] == '__UNQUOTE_SPLICED__':
            spliced = q[1]
            if not isinstance(spliced, list):
                raise TypeError("unquote-splicing must evaluate to a list")
            result.extend(spliced)
        else:
            result.append(q)
    return result

def oldquasiquote(env, *args):
    if not isinstance(args, list):
        return args
    values = args
    if len(values)>0 and values[0]=="unquote":
        return eval_lisp(env, values[1:])
    return [quasiquote(env, val) for val in values]

def unquote(env, *args):
    result = eval_lisp(env, *args)
    return result

def load_and_parse_lisp_file(env, filename):
    filepath = Path(filename).absolute()
    if not filepath.exists():
        return "nil"

    parsed_lisp = parse(tokenize_file(filepath), program=list())

    run(parsed_lisp, env)

    return "t"

def eval(env, args):
    value = eval_lisp(env, args)
    return eval_lisp(env, value)

def main() -> None:
    debug_level = 0
    main_env = Env()
    main_env.init_env()
    program = Path(sys.argv[0])
    programpath = program.parent
    programname = program.name
    print(f"{programname} located in {programpath}")

    lispfiles = [programpath / Path("lispfile.lisp"),
                programpath / "macro.l"]

    for lispfile in lispfiles:

        if lispfile.exists():
            try:
                parsed_lisp = parse(tokenize_file(lispfile))

                run(parsed_lisp, main_env)
            except TypeError as te:
                print(f"Error: {te}\n===============\n")
                traceback.print_exc()
                print(f"===============\n")
            except NameError as ne:
                print(f"Error: {ne}\n===============\n")
                traceback.print_exc()
                print(f"===============\n")
            except ValueError as ve:
                print(f"Error: {ve}\n===============\n")
                traceback.print_exc()
                print(f"===============\n")
        else:
            print(f"Can't find {lispfile} from here {os.getcwd()}")



    while True:
        prompt = ""
        if debug_level:
            prompt = f"testcase: "
        test_case = input(prompt)

        token_generator = tokenize(test_case)

        if debug_level:
            print(f"test case:\n{test_case}\n-----------\n")

        try:
            parsed_lisp = parse(token_generator, program=list())

            run(parsed_lisp, main_env)
            if debug_level:
                print("===============")
        except TypeError as te:
            print(f"Error: {te}\n===============\n")
            traceback.print_exc()
            print(f"===============\n")
        except NameError as ne:
            print(f"Error: {ne}\n===============\n")
            traceback.print_exc()
            print(f"===============\n")
        except ValueError as ve:
            print(f"Error: {ve}\n===============\n")
            traceback.print_exc()
            print(f"===============\n")

if __name__ == '__main__':
    main()
