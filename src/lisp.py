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
            return 't'
        if self.parent is None:
            #print("no parent, returning False")
            return 'nil'
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

class FunctionDef:
    def __init__(self, closure, params, body, call_interpreter) -> None:
        self.closure = closure
        self.params = params
        self.body = body
        self.call_interpreter = call_interpreter

    def __call__(self, *values):
        new_env = Env(self.closure)
        for name, value in zip(self.params, values):
            new_env.set(name, value)
        return self.call_interpreter(new_env, self.body)
        
def lisp_format(fmt, *args):
    try:
        return fmt.format(*args)
    except Exception as e:
        raise ValueError(f"format Fehler: {e}")
        def create_list(self, args):
            return list(args)
    
def greater(args):
    a, b = args
    #print(f"{a=} > {b=}")
    ret = True if a>b else None
    #print(f"{ret=}")
    return ret

def greaterequal(args):
    a, b = args
    #print(f"{a=} >= {b=}")
    ret = True if a>=b else None
    #print(f"{ret=}")
    return ret

def less(args):
    a, b = args
    #print(f"{a=} < {b=}")
    ret = True if a<b else None
    #print(f"{ret=}")
    return ret

def lessequal(args):
    a, b = args
    #print(f"{a=} <= {b=}")
    ret = True if a<=b else None
    #print(f"{ret=}")
    return ret

def equal(args):
    a, b = args
    #print(f"{a=} == {b=}")
    ret = True if a==b else None
    #print(f"{ret=}")
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
        raise ValueError("car expects non empty list")
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

class LispInterpreter:

    def __init__(self):
        self.env = Env()
        self.env.set('format', lisp_format)
        self.env.set('string-append', lambda *args: ''.join(str(arg) for arg in args))
        self.env.set('print', print)
        self.env.set('list', create_list)
        self.env.set('+'   , add)
        self.env.set('-'   , sub)
        self.env.set('*'   , mult)
        self.env.set('/'   , div)
        self.env.set('>='  , greaterequal)
        self.env.set('>'   , greater)
        self.env.set('<='  , lessequal)
        self.env.set('<'   , less)
        self.env.set('=='  , equal)
        self.env.set('car' , car)
        self.env.set('cdr' , cdr)
        self.env.set('map', lisp_map)
        self.env.set('print-env', lambda *args: print(str(self.env)))

        self.functionplaceholder = FunctionDef(self.env, None, None, self.run_rec)

        self.specialforms = {
            'if': self.ifthenelse,
            'define': self.define,
            'let': self.let,
            'lambda': self.create_lambda,
            'defun': self.define_function,
            #'map': self.map,
            'quote': self.qoute,
            'quasiquote': self.quasiqoute,
            'unquote': self.unqoute,
            'eval': self.eval,
            'begin': self.begin,
            'set!': self.overwrite
        }
        self.functions = {

        }

    def run_rec(self, env:Env, expression):
        #print(f"{expression=}")
        
        if isinstance(expression, Symbol):
            return env.get(expression)
            
        if isinstance(expression, str):
            return expression

        if isinstance(expression, (float,int)):
            return expression

        if not isinstance(expression, (list, tuple)):
            raise ValueError(f"invalid value {expression}")

        function = expression[0]
        args = expression[1:]

        if isinstance(function, list):
            function = self.run_rec(env, function)

        if function in self.specialforms:
            return self.specialforms[function](env, *args)


        values = [self.run_rec(env, arg) for arg in args]
        #print(f"{values=}")

        if isinstance(function, (int, float)):
            return [function, *values]

        if function in self.functions.keys():
            return self.functions[function](*values)
        else:
            if isinstance(function, str):
                func = env.get(function)
            else:
                func = function
            if isinstance(func, FunctionDef):
                new_env = Env(func.closure)
                for name, value in zip(func.params, values):
                    new_env.set(name, value)

                return self.run_rec(new_env, func.body)
            elif callable(func):
                #print(values)
                return func(*values)
            else:
                raise ValueError(f"unknown function {function}")

    def run(self, lisp_tree : list[Any], keep_env = False):
        env : Env = Env(self.env)
        #print(f"run starts with {str(env)=}")
        ret = None
        for e in lisp_tree:
            ret = self.run_rec(env, e)
        #print(f"{str(env)=}")
        if keep_env and not env.empty():
            self.env = env
            #print(f"keep {str(self.env)=}")
        
        return ret

    def create_lambda(self, env, *args):
        params, body = args
        return FunctionDef(env, params, body, self.run_rec)

    def define_function(self, env, *args):
        try:
            name, params, body = args
            #env.set(name, self.functionplaceholder)
            func = FunctionDef(env, params, body, self.run_rec)
            env.set(name, func)
        except NameError as ne:
            print(f"function {name} not defined: {ne}")


    def begin(self, env, *args):
        _, expressions = args
        ret = None
        for expression in expressions:
            ret = self.run_rec(env, expression)
        return ret

    def ifthenelse(self, env, *args):
        condition, true_branch, false_branch = args
        cond_result = self.run_rec(env, condition)
        #print(f"{cond_result=}")
        if cond_result is not None:
            return self.run_rec(env, true_branch)
        else:
            return self.run_rec(env, false_branch)

    def define(self, env: Env, *args):
        (var, value) = args
        env.set(var, self.run_rec(env, value))

    def overwrite(self, env, var, value):
        return env.overwrite(var, value)
    


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


    def qoute(self, env, args):
        return args

    
    def quasiqoute(self, env, args):
        if not isinstance(args, list):
            return args
        values = args   
        if len(values)>0 and values[0]=="unqoute":
            return self.run_rec(env, values[1])
        return [self.quasiqoute(env, val) for val in values]
        
    def unqoute(self, env, args):
        (result,) = self.run_rec(env, args)
        return result
        
    def eval(self, env, args):
        value = self.run_rec(env, args)
        return self.run_rec(env, value)
        
def main() -> None:
    program = Path(sys.argv[0])
    programpath = program.parent
    programname = program.name
    print(f"{programname} located in {programpath}")
    lispfile = programpath / Path("lispfile.lisp")
    
    interpreter = LispInterpreter()
    if lispfile.exists():
        parsed_lisp = parse(tokenize_file(lispfile))

        interpreter.run(parsed_lisp, keep_env=True)
    else:
        print(f"Can't find {lispfile} from here {os.getcwd()}")
        exit(1)
    
    
    testcases = {
        "testcase1" : textwrap.dedent("""\
        (my-func 1 2 ( + 1 2 )
        """),
        "testcase2": textwrap.dedent("""\
        (my-func 1 2 3 (my-func 4 5 (+ 3 3)))
        (+ 10 (* 3 6))
        """),
        "testcase3": textwrap.dedent("""\
        (my-func 1 2 3 (my-func 4 5 (+ 3 3))))
        """),
        "testcase4": """\
    (define a 10)
    (define addN
        (lambda (n)
            (lambda (x) (+ x n)
            )
        )
    )
    (list (let ((a 2) (b 3 )) (+ 1 a b (* 2 2) (if nil (/ 2 1) (+ 3 2))) (+ a b)) 10)""",

    "testcase5": """\
    (define a 10)
    (defun test (m) (lambda (x) (* m x)))
    (define addN
        (lambda (n)
            (lambda (x) (+ x n)
            )
        )
    )
    (define add5 (addN 5))
    (define mul10 (test 10))
    ((add5 a) (mul10 3))
    (map (lambda (v) (* 3.14 v)) (10 12 14))
    """,
    "testcase6": """\
    (defun fib (x)
        (if (>= x 3)
            (car (cdr (print
                (
                    x 
                    (+ 
                        (fib (- x 1))
                        (fib (- x 2))
                    )
                )
            )))
            (print 1)
        )
    )
    (print (map (lambda (x) (list x (fib x))) (3 4 5 6 7 8 9 10 11 12)))
        """,
    "testcase7": """\
    (defun sqr (x) (x (* x x)))
    (map sqr (4 5))
    """,
    "testcase8": """\
(defun double (x) (* 2 x))
(define lst '(1 2 3 4 5))
(print lst " -> " (map double lst))
((lambda (x) (* 3 x)) 3)
    """,
    
    "testcase9": """(let ((b 10)( a `( + 1 2 (+ 2 1) 4)))
        (print a)
        (print a (car a) (cdr a))
        (print (eval a))
        )""",
    "testcase10": """\
        (define print (lambda (a) '(print a)))
        (define a "Thomas Dilling")
        (define b "Hallo ")
        (define c 10)
        (print (string-append b a " " c) )
        (print (format "{} ist {} Jahre alt!" a 59))
        """,
        }
    number_of_testcases = len(testcases)
    while True:
        test_case = input(f"testcase: ")
        if test_case=="exit":
            exit(0)
        if test_case not in testcases:
            if test_case.startswith("load "):
                filepath = Path(test_case[5:].strip())
                
                with open(filepath)as filehandle:
                    lisp_lines = "".join(filehandle.readlines())
                    token_generator = tokenize(lisp_lines)
            else:
                lisp_lines = test_case
                if lisp_lines.strip() == "":
                    continue 
                token_generator = tokenize(lisp_lines)
        else:
            lisp_lines = testcases[test_case]
            token_generator = tokenize(lisp_lines)

        if False:
            try:
                print(f"test case:\n{lisp_lines}\n-----------\n")
                parsed_lisp = parse(token_generator, program=list())
                
                print(interpreter.run(parsed_lisp, keep_env=True))
            except NameError as ne:
                print(ne)
        else:
            print(f"test case:\n{lisp_lines}\n-----------\n")
            parsed_lisp = parse(token_generator, program=list())
                
            print(interpreter.run(parsed_lisp, keep_env=True))
        print("===============")
        
if __name__ == '__main__':
    main()
