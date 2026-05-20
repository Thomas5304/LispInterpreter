import lispSupport
from tokenParse import tokenize, tokenize_file, Symbol, atom, is_list, is_symbol, parse
import traceback
from pathlib import Path
from typing import Callable, Any, Iterable, Generator, TypeVar
import importlib

class Env:
    def __init__(self, parent = None):
        self.data = {}
        self.parent = parent

    def get(self, name):
        if name == "t":
            return True

        if name == "nil":
            return None

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
        self.set('function-mode', False)
        self.set('enable-function-mode',  lambda : self.set('function-mode', True))
        self.set('disable-function-mode', lambda : self.set('function-mode', False))
        self.set('format', lispSupport.lisp_format)
        self.set('string-append', lambda *args: ''.join(str(arg) for arg in args))
        self.set('print', print)
        self.set('list', lispSupport.create_list)
        self.set('cons', lispSupport.eval_append)
        self.set('append', lispSupport.eval_append)
        self.set('and', lambda a, b: a and b)
        self.set('or', lambda a, b: a or b)
        self.set('zip', lambda *a: list(zip(*a)))
        self.set('null', lambda a: len(a)==0)
        self.set('atom?', lambda a: "t" if not is_list(a) else "nil")
        self.set('integer?', lambda a: "t" if isinstance(a, int) else "nil")
        self.set('number?', lambda a: "t" if isinstance(a, float) else "nil")
        self.set('function?', lambda a: "t" if callable(a) else "nil")
        self.set('+'   , lispSupport.add)
        self.set('-'   , lispSupport.sub)
        self.set('*'   , lispSupport.mult)
        self.set('/'   , lispSupport.div)
        self.set('>='  , lispSupport.greaterequal)
        self.set('>'   , lispSupport.greater)
        self.set('<='  , lispSupport.lessequal)
        self.set('<'   , lispSupport.less)
        self.set('=='  , lispSupport.equal)
        self.set('!=', lambda a, b: not lispSupport.equal(a, b))
        self.set('not' , lambda x:  not x )
        self.set('car' , lispSupport.car)
        self.set('cdr' , lispSupport.cdr)
        self.set('print-env', lambda *args: print(str(self)))
        self.set('map', lispSupport.lisp_map)
        self.set('mapcar', lispSupport.lisp_mapcar)
        self.set('apply', lispSupport.lisp_apply)
        self.set('exit', lambda exit_code=0: exit(exit_code) if exit_code is not None else exit(0))
        self.set('function', lambda f: f)
        #self.set('debug', lambda debug_level=None: set_debug_level(debug_level))
        self.set('last-expr!', None)
        #self.set('symbol-name', symbol_name)
        self.set('intern', eval_intern)
        #self.set('length', lambda x: len(x) if is_list(x) else 0)

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

class FunctionBase:
    def __init__(self, closure, all_params) -> None:
        self.key_params = {}
        if '&rest' in all_params:
            idx = all_params.index('&rest')
            if idx>len(all_params)-2:
                SyntaxError(f"function with &rest is missing name for rest parameter")
            self.rest_name = all_params[idx+1]
            all_params = all_params[:-2]
        else:
            self.rest_name = None

        if '&key' in all_params:
            idx = all_params.index('&key')

            for kv in all_params[idx+1:]:
                if isinstance(kv, (tuple, list)):
                    k, v = kv
                    self.key_params[k] = v
                else:
                    self.key_params[kv] = None
            self.params = all_params[:idx]
            self.param_mode = "keys"
        else:
            self.params = all_params
            self.param_mode = "positional"
        self.optional = []

        self.closure = closure

    def bind_params(self, *args):
        env = Env(self.closure)
        i = 0
        arg_i = 0

        # ---------------------------
        # 1. Positional parameters
        # ---------------------------
        while i < len(self.params):
            if arg_i >= len(args):
                raise Exception("Missing positional argument")

            env.set(self.params[i], args[arg_i])
            i += 1
            arg_i += 1

        # ---------------------------
        # 2. Optional parameters
        # ---------------------------
        j = 0
        while j < len(self.optional):
            name, default = self.optional[j]

            if arg_i < len(args) and not is_keyword(args[arg_i]):
                env.set(name, args[arg_i])
                arg_i += 1
            else:
                env.set(name, default)

            j += 1

        # ---------------------------
        # 3. Keyword arguments
        # ---------------------------
        keywords = {}
        missing_keywords = set(k for k in self.key_params)

        while arg_i < len(args):
            if is_keyword(args[arg_i]):
                key = args[arg_i].lstrip(":")
                arg_i += 1

                if arg_i >= len(args):
                    raise Exception("Keyword without value")

                value = args[arg_i]
                arg_i += 1

                missing_keywords.discard(key)

                keywords[key] = value
            else:
                break  # no more keywords

        # ---------------------------
        # 3.1. Perhaps some keyword args are missing
        # ---------------------------
        for key in missing_keywords:
            #print(f"missing keyword: {key} set to default {self.key_params[key]}")
            keywords[key] = self.key_params[key]


        # assign keyword params
        for k,value in keywords.items():
                env.set(k, value)

        # ---------------------------
        # 4. Rest arguments
        # ---------------------------
        if self.rest_name:
            env.set(self.rest_name, args[arg_i:])
        elif arg_i < len(args):
            raise Exception("Too many arguments")

        return env


class FunctionDef(FunctionBase):
    def __init__(self, closure, all_params, body) -> None:
        super().__init__(closure, all_params)
        self.body = body

    def __call__(self, *values):
        new_env = self.bind_params(*values)
        return eval_lisp(new_env, self.body)


# Hilfsfunktionen zur Konversion (falls noetig)
def to_python(lisp_val):
    # einfache Identitaet; erweitere bei Bedarf (z.B. Symbol -> str, List -> tuple etc.)
    return lisp_val

def from_python(py_val):
    # einfache Identitaet; passe an, falls du spezielle Lisp-Typen brauchst
    return py_val

# Repraesentation fuer ein Lisp-Funktionsobjekt, das eine Python-Funktion aufruft
class PythonBridgeFunction(FunctionBase):
    def __init__(self, env, all_params, py_func):
        super().__init__(env, all_params)
        self.py_func = py_func

    def arity_ok(self, n):
        return n == len(self.params)

    # aufruf von Eval: args sind bereits evaluierte Lisp-Werte
    def __call__(self, *values):
        if not self.arity_ok(len(values)):
            raise TypeError(f"Expected {len(self.params)} args, got {len(values)}")
        py_args = [to_python(a) for a in values]
        result = self.py_func(*py_args)
        return from_python(result)


class Macro:
    def __init__(self, proc):
        self.proc = proc

    def expand(self, *raw_args):
        #print("Macro.expand 1:", raw_args)
        result = self.proc(*raw_args)
        #print("Macro.expand 2:", result)
        return result

def is_macro(x):return isinstance(x, Macro)


def symbol_name(env, symb):
    if isinstance(symb, Symbol):
        return str(symb)
    return symb

def eval_intern(name):
    if not isinstance(name, str):
        raise TypeError(f"{name} is not a string")
    return Symbol(name)

def is_keyword(kw):
    return isinstance(kw, str) and kw.startswith(':')

# Handler fuer die special form
def defun_python(env, lisp_name, params, py_name_sym, py_namespace=None):
    #print(f"defun_python")
    # py_name_sym kann ein Symbol sein; hier nehmen wir an, es ist der Name als string
    py_name = str(py_name_sym) if is_symbol else py_name_sym

    # Namespace, in dem wir python-Funktionen suchen (default: globals())
    ns = importlib.import_module(py_namespace) if py_namespace is not None else globals()

    py_func = getattr(ns, py_name)
    if py_func is None:
        raise NameError(f"Python function '{py_name}' not found in provided namespace")

    bridge = PythonBridgeFunction(env, params, py_func)
    env.set(lisp_name, bridge)


def macroexpand(env, ast, depth=-1):
    while (depth < 0 or depth > 0) and is_list(ast) and len(ast) > 0 and is_symbol(ast[0]):
        #print(f"macroexpand while {depth}: {ast}")
        depth = depth - 1
        head = ast[0]
        val = None
        try:
            val= env.get(head)
        except Exception:
            pass


        if is_macro(val):
            macro : Macro = val

            raw_args = ast[1:]

            #print(f"macroexpand {head} before: {raw_args}\n")

            #print(f"macro param: {', '.join(macro.proc.params)} rest: {macro.proc.rest_name} set to {raw_args}\n")
            ast = macro.expand(*raw_args)
            #if isinstance(ast, Env):
            #    raise TypeError("this is a Env")
            #print(f"macroexpand {head}  after: {ast}\n\n")

            continue

        else:
            break

    #print(f"after macroexpand {ast}")
    return ast


def eval_macroexpand(env, ast):
    return macroexpand(env, ast, depth=-1)
    
def eval_macroexpand_1(env, ast):
    return macroexpand(env, ast, depth=1)


def eval_dolist(env, spec, *body):
    var_name = spec[0]
    list_expr = spec[1]

    values:list = eval_lisp(env, list_expr)

    result = None

    for value in values:

        local_env = Env(parent=env)
        local_env.set(var_name, value)

        for form in body:
            result = eval_lisp(local_env, form)

    return result


def eval_cond(env, *clauses):
    for clause in clauses:
        test = clause[0]
        body = clause[1:]

        if test == "else" or eval_lisp(env, test):
            result = None

            for expr in body:
                result = eval_lisp(env, expr)

            return result

    return None


def print_and_eval(env, *args):
    toprint = lispSupport.print_lisp_recursive(*args)
    evaluated = eval_lisp(env, *args)
    print(f"{toprint} evaluates to {evaluated}")
    return evaluated

def create_lambda(env, *args):
    params, body = args
    return FunctionDef(env, params, body)

def define_function(env, name, params, body):
    try:
        #print(f"try to add function {name} ({params}) {body}")
        env.set(name, None)
        func = FunctionDef(env, params, body)
        if not env.overwrite(name, func):
            raise NameError(f"expecting function {name} in environtment")
    except NameError as ne:
        print(f"function {name} not defined: {ne}")
        traceback.print_exc()

def while_loop(env, cond_expr, *body_exprs):
    last_val = None
    while(eval_lisp(env, cond_expr)):
        try:
            for expr in body_exprs:
                last_val = eval_lisp(env, expr)
        except Exception as e:
            #print(e)
            traceback.print_exc()
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

def eval_quasiquote(env, expr):

    # atom
    if not isinstance(expr, (list, tuple)):
        return expr

    result = []

    for item in expr:

        # --------------------
        # ,x
        # --------------------

        if (
            isinstance(item, (list,tuple))
            and len(item) > 0
            and item[0] == "unquote"
        ):

            value = eval_lisp(env, item[1])
            result.append(value)

        # --------------------
        # ,@x
        # --------------------

        elif (
            isinstance(item, (list, tuple))
            and len(item) > 0
            and item[0] == "unquote-splicing"
        ):

            values = eval_lisp(env, item[1])

            if not isinstance(values, (list, tuple)):
                raise Exception(
                    f"unquote-splicing requires list {item[1]} -> {values}"
                )

            result.extend(values)

        # --------------------
        # normal recursion
        # --------------------

        else:
            result.append(
                eval_quasiquote(env, item)
            )

    return result


def quasiquote(env, ast, depth=0):
    """
    ast: AST node (atom or list)
    env: environment used to eval unquote parts
    depth: nesting level of quasiquote (1 = we are in quasiquote)
    Returns: AST with unquotes evaluated (for macro expansion)
    """
    #print(f"quasiquote {lispSupport.print_lisp_recursive(ast)}, depth:{depth}")
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
        ##print(f"for q {lispSupport.print_lisp_recursive(q)}")
        if isinstance(q, tuple) and q and q[0] == '__UNQUOTE_SPLICED__':
            spliced = q[1]
            if not isinstance(spliced, list):
                raise TypeError("unquote-splicing must evaluate to a list")
            result.extend(spliced)
        else:
            result.append(q)
    return result

def unquote(env, *args):
    result = eval_lisp(env, *args)
    return result

def load_and_parse_lisp_file(env, filename):
    filepath = Path(filename).absolute()
    if not filepath.exists():
        return "nil"

    parsed_lisp = parse(tokenize_file(filepath), program=list(), function_mode=env.get('function-mode'))

    return run(parsed_lisp, env)

    
def eval_include(env, filename):
    breakpoint()
    if isinstance(filename, str):
        pass
    if isinstance(filename, Symbol):
        filename = str(filename)

    print(f"filename: {filename}")
    filepath = Path(filename).absolute()
    if not filepath.exists():
        return "nil"

    parsed_lisp = parse(tokenize_file(filepath), program=list(), function_mode=env.get('function-mode'))
    return [parsed_lisp]


def eval(env, args):
    value = eval_lisp(env, args)
    return eval_lisp(env, value)


def eval_lisp(env, expression):
    specialforms = {
        'if':            ifthenelse,
        'define':        define,
        'let':           let,
        'lambda':        create_lambda,
        'defun':         define_function,
        'defun-python':  defun_python,
        'quote':         quote,
        'quasiquote':    eval_quasiquote,
        'unquote':       unquote,
        'eval':          eval,
        'begin':         begin,
        'set!':          overwrite,
        'load':          load_and_parse_lisp_file,
        'defmacro':      defmacro,
        'while':         while_loop,
        'print-eval':    print_and_eval,
        'cond':          eval_cond,
        'do-list':       eval_dolist,
        'symbol-name':   symbol_name,
        'macroexpand-1': eval_macroexpand_1,
        'macroexpand':   eval_macroexpand,
        'include':       eval_include,
    }
    try:
        if isinstance(expression, Symbol):
            if is_keyword(expression):
                return expression
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
        print(f"{ve}\n in {lispSupport.print_lisp_recursive(expression)}")
        #traceback.print_exc()
        raise
    except Exception as e:
        print(f"{e}\n in {lispSupport.print_lisp_recursive(expression)}")
        #traceback.print_exc()
        raise

def run(lisp_tree : list[Any], env:Env):
    for e in lisp_tree:
        try:
            env.set('last-expr!', eval_lisp(env, e))
        except ValueError as ve:
            print(f"{ve}\n in {lispSupport.print_lisp_recursive(e)}")
            #traceback.print_exc()
            raise
        except Exception as exc:
            print(f"{exc}\n in {lispSupport.print_lisp_recursive(e)}")
            #traceback.print_exc()
            raise
        
        if env.get('last-expr!') is not None:
            print(env.get('last-expr!'))

