#!/tools/pdtooling/packages/VirtPythonEnv/pkg_synopsys/bin/python3
from cmath import isinf
from re import L
from tokenize import Token
import textwrap
from enum import Enum, auto
from typing import Callable, Any, Iterable, Generator
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
    if not isinstance(func, LispInterpreter.FunctionDef) and not callable(func):
        raise TypeError(f"map: can't call func {func}")
        
    for nr, lst in enumerate(args):
        if not isinstance(lst, list):
            raise TypeError(f"map: element at {nr} is not a list")
    result = []
    
    for items in zip(*args):
        value = func(*items)
        result.append(value)
        
    return result

def cond(*args):
    pass

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
        

class LispInterpreter:
    class FunctionDef:
        def __init__(self, closure, params, body, call_interpreter) -> None:
            self.closure = closure
            self.params = params
            self.body = body
            self.call_interpreter = call_interpreter


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
            return self.call_interpreter.run_rec(new_env, self.body)

    class Macro:
        def __init__(self, proc):
            self.proc = proc

        def expand(self, *raw_args):
            result = self.proc(*raw_args)
            #print("Macro.expand:", result)
            return result

    def is_macro(x):return isinstance(x, LispInterpreter.Macro)
    
    def macroexpand(env, ast):
        while is_list(ast) and len(ast) > 0 and is_symbol(ast[0]):
            head = ast[0]
            try:
                val = env.get(head)
            except Exception:
                val = None

            if LispInterpreter.is_macro(val):
                macro = val

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

    def __init__(self, debug_level=0):
        self.debug_level = debug_level
        self.last_value = None
        self.env = Env()
        self.env.set('nil', False)
        self.env.set('t', True)
        self.env.set('format', lisp_format)
        self.env.set('string-append', lambda *args: ''.join(str(arg) for arg in args))
        self.env.set('print', print)
        self.env.set('list', create_list)
        self.env.set('cons', lambda l, a: l.append(a))
        self.env.set('and', lambda a, b: a and b)
        self.env.set('or', lambda a, b: a or b)
        self.env.set('zip', lambda *a: list(zip(*a)))
        self.env.set('null', lambda a: "t" if a==[] or a=="nil" else "nil")
        self.env.set('+'   , add)
        self.env.set('-'   , sub)
        self.env.set('*'   , mult)
        self.env.set('/'   , div)
        self.env.set('>='  , greaterequal)
        self.env.set('>'   , greater)
        self.env.set('<='  , lessequal)
        self.env.set('<'   , less)
        self.env.set('=='  , equal)
        self.env.set('not' , lambda x: not x)
        self.env.set('car' , car)
        self.env.set('cdr' , cdr)
        self.env.set('map', lisp_map)
        self.env.set('print-env', lambda *args: print(str(self.env)))
        self.env.set('exit', lambda exit_code=0: exit(exit_code) if exit_code is not None else exit(0))
        self.env.set('debug', lambda debug_level=None: self.set_debug_level(debug_level))
        self.env.set('set!', lambda v: "t" if self.overwrite(v) else "nil")
        self.env.set('last-expr!', None)

        self.specialforms = {
            'if': self.ifthenelse,
            'define': self.define,
            'let': self.let,
            'lambda': self.create_lambda,
            'defun': self.define_function,
            'quote': self.quote,
            'quasiquote': self.quasiquote,
            'unquote': self.unquote,
            'eval': self.eval,
            'begin': self.begin,
            #'set!': self.overwrite,
            'load': self.load_and_parse_lisp_file,
            'defmacro': self.defmacro,
            'while': self.while_loop,
        }
        self.functions = {

        }
        
    def set_debug_level(self, debug_level = None):
        if debug_level is not None:
            self.debug_level = debug_level
        return self.debug_level
        
    def run_rec(self, env:Env, expression):
        try:
            if self.debug_level:
                print(f"{expression=}")

            if isinstance(expression, Symbol):
                return env.get(expression)

            if isinstance(expression, str):
                return expression

            if isinstance(expression, (float,int)):
                return expression

            if not isinstance(expression, (list, tuple)):
                raise ValueError(f"invalid value {expression}")

            expression = LispInterpreter.macroexpand(env, expression)

            function = expression[0]
            args = expression[1:]

            if isinstance(function, list):
                function = self.run_rec(env, function)

            if function in self.specialforms:
                return self.specialforms[function](env, *args)


            values = [self.run_rec(env, arg) for arg in args]
            if self.debug_level:
                print(f"{    values=}")

            #if isinstance(function, (int, float)):
            #    return [function, *values]

            if function in self.functions.keys():
                return self.functions[function](*values)
            else:
                if isinstance(function, str):
                    func = env.get(function)
                else:
                    func = function
                if isinstance(func, LispInterpreter.FunctionDef):
                    return func(*values)
                elif callable(func):
                    #print(values)
                    return func(*values)
                else:
                    raise ValueError(f"unknown function {function}")
        except ValueError as ve:
            print(f"{ve}\n in {print_lisp_recursive(expression)}")
        except Exception as e:
            print(f"{e}\n in {print_lisp_recursive(expression)}")

            
    def run(self, lisp_tree : list[Any], keep_env = False):
        if keep_env:
            env = self.env
        else:
            env : Env = Env(self.env)
        #print(f"run starts with {str(env)=}")
        for e in lisp_tree:
            self.env.set('last-expr!', self.run_rec(env, e))
        if self.env.get('last-expr!') is not None:
            print(self.env.get('last-expr!'))
        #print(f"{str(env)=}")
        

    def create_lambda(self, env, *args):
        params, body = args
        return LispInterpreter.FunctionDef(env, params, body, self)

    def define_function(self, env, *args):
        try:
            name, params, body = args
            #print(f"try to add function {name} ({params}) {body}")
            env.set(name, None)
            func = LispInterpreter.FunctionDef(env, params, body, self)
            if not env.overwrite(name, func):
                raise NameError(f"expecting function {name} in environtment")
        except NameError as ne:
            print(f"function {name} not defined: {ne}")

    def while_loop(self, env, cond_expr, *body_exprs):
        last_val = None
        while(self.run_rec(env, cond_expr)):
            try:
                for expr in body_exprs:
                    last_val = self.run_rec(env, expr)
            except Exception as e:
                print(e)
        return last_val

    def defmacro(self, env, name, params, body):
        proc = LispInterpreter.FunctionDef(env, params, body, self)
        env.set(name, LispInterpreter.Macro(proc))

    def begin(self, env, *args):
        _, expressions = args
        ret = None
        for expression in expressions:
            ret = self.run_rec(env, expression)
        return ret

    def ifthenelse(self, env, condition, true_branch, false_branch = None):
        cond_result = self.run_rec(env, condition)
        if cond_result is not None and (cond_result == "t" or cond_result == True):
            return self.run_rec(env, true_branch)
        elif false_branch is not None:
            return self.run_rec(env, false_branch)
        return "nil"

    def define(self, env: Env, *args):
        (var, value) = args
        env.set(var, self.run_rec(env, value))

    def overwrite(self, env, var, value):
        return "t" if env.overwrite(var, value) else "nil"
    


    def let(self, env: Env, vars, *expressions):
        env = Env(env)

        for var in vars:
            self.define(env, *var)

        ret = None

        for expression in expressions:
            ret = self.run_rec(env, expression)

        env = env.parent

        return ret

    def map(self, env, *args):
        func = self.run_rec(env, args[0])
        list_of_values = self.run_rec(env, args[1:])
        
        if len(list_of_values)==1:
            return [self.run_rec(env, [func, value]) for value in values]
        return [None]


    def quote(self, env, args):
        return args


    def quasiquote(self, env, ast, depth=1):
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
            return ['quasiquote', self.quasiquote(env, ast[1], depth+1)]

        # Handle unquote only when depth == 1 (i.e. this quasiquote level)
        if is_symbol(ast[0]) and ast[0] == 'unquote':
            if depth == 1:
                # evaluate the inner expression in env and return the result (AST)
                return self.run_rec(env, ast[1])
            else:
                # inside deeper quasiquote: treat as literal unquote form
                return ['unquote', self.quasiquote(env, ast[1], depth-1)]

        # Handle unquote-splicing, only valid inside list context when depth == 1
        if is_symbol(ast[0]) and ast[0] == 'unquote-splicing':
            if depth == 1:
                # evaluate to a list that will later be spliced
                return ('__UNQUOTE_SPLICED__', self.run_rec(env, ast[1]))
            else:
                return ['unquote-splicing', self.quasiquote(env, ast[1], depth-1)]

        # General list processing: iterate elements, handle splicing markers
        result = []
        for elem in ast:
            q = self.quasiquote(env, elem, depth)
            # If element returned a special splicing marker, splice its value into result
            if isinstance(q, tuple) and q and q[0] == '__UNQUOTE_SPLICED__':
                spliced = q[1]
                if not isinstance(spliced, list):
                    raise TypeError("unquote-splicing must evaluate to a list")
                result.extend(spliced)
            else:
                result.append(q)
        return result

    def oldquasiquote(self, env, *args):
        if not isinstance(args, list):
            return args
        values = args   
        if len(values)>0 and values[0]=="unquote":
            return self.run_rec(env, values[1:])
        return [self.quasiquote(env, val) for val in values]
        
    def unquote(self, env, *args):
        result = self.run_rec(env, *args)
        return result

    def load_and_parse_lisp_file(self, env, filename):
        filepath = Path(filename).absolute()
        if not filepath.exists():
            return "nil"

        parsed_lisp = parse(tokenize_file(filepath), program=list())

        self.run(parsed_lisp, keep_env = True)
        
        return "t"
        
    def eval(self, env, args):
        value = self.run_rec(env, args)
        return self.run_rec(env, value)
        
def main() -> None:
    program = Path(sys.argv[0])
    programpath = program.parent
    programname = program.name
    print(f"{programname} located in {programpath}")

    lispfiles = [programpath / Path("lispfile.lisp"),
                programpath / "macro.l"]

    interpreter = LispInterpreter()

    for lispfile in lispfiles:
    
        if lispfile.exists():
            try:
                parsed_lisp = parse(tokenize_file(lispfile))

                interpreter.run(parsed_lisp, keep_env=True)
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
        if interpreter.debug_level:
            prompt = f"testcase: "
        test_case = input(prompt)
        
        token_generator = tokenize(test_case)

        if interpreter.debug_level:
            print(f"test case:\n{test_case}\n-----------\n")

        try:
            parsed_lisp = parse(token_generator, program=list())

            interpreter.run(parsed_lisp, keep_env=True)
            if interpreter.debug_level:
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
