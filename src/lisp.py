from re import L
from statemachine import StateMachine
import textwrap
from enum import Enum, auto
from typing import Callable, Any, Iterable, Generator
from dataclasses import dataclass, field
from pathlib import Path

class LispState(Enum):
    START = auto()
    LIST = auto()
    EOF = auto()

class LispEvent(Enum):
    OPEN = auto()
    ELEMENT = auto()
    CLOSE = auto()
    EOF = auto()

class MissingElementError(Exception):
    def __init__(self, msg : str):
        super().__init__(msg)

class BadStackError(Exception):
    def __init__(self, msg : str):
        super().__init__(msg)

@dataclass
class LispCtx:
    lisp_stack: list[Any] = field(default_factory=list)
    element : Any|None = None

    def depth(self) -> int:
        return len(self.lisp_stack)

    def actual_lisp_list(self) -> list[Any]:
        if len(self.lisp_stack) == 0:
            raise MissingElementError("Missing list on stack")
        return self.lisp_stack[-1]

    def new_actual_lisp_list(self) -> None:
        self.lisp_stack.append(list())

    def pop_actual_lisp_list(self) -> list[Any]:
        if len(self.lisp_stack) == 0:
            raise MissingElementError("Missing element on stack")
        return self.lisp_stack.pop()

    def close_actual_lisp_list(self) -> None:
        act_list = self.pop_actual_lisp_list()
        if len(self.lisp_stack) == 0:
            raise MissingElementError("Missing list on stack")
        self.lisp_stack[-1].append(act_list)

    def new_element(self) -> None:
        if self.element is None:
            raise MissingElementError("Element is None")
        self.actual_lisp_list().append(self.element)
        self.element = None

@dataclass
class LispParser:
    lisp : LispCtx
    state : LispState = LispState.START
    debug : int = False

    def handle(self, event: LispEvent) -> None:
        if self.debug:
            print(f"State {self.state} Event {event} Element = {self.lisp.element if self.lisp.element is not None else 'None'}")
            print(f"     pre {self.lisp.depth()}")
        self.state = lisp_sm.handle(self.lisp, self.state, event)
        if self.debug:
            print(f"    post {self.lisp.depth()}")
            print(f"         {len(self.lisp.actual_lisp_list()) if self.lisp.depth()>0 else 'no top'}")

    def parse(self, token_stream:Iterable[str]):
        for token in token_stream:
            if token == "(":
                self.handle(LispEvent.OPEN)
            elif token == ")":
                self.handle(LispEvent.CLOSE)
            else:
                self.lisp.element = token
                self.handle(LispEvent.ELEMENT)

        self.handle(LispEvent.EOF)

        return self.lisp.pop_actual_lisp_list()

lisp_sm : StateMachine[LispState, LispEvent, LispCtx] = StateMachine()

@lisp_sm.transition(LispState.START, LispEvent.OPEN, LispState.LIST)
def start_list(ctx:LispCtx):
    ctx.new_actual_lisp_list()
    ctx.new_actual_lisp_list()

@lisp_sm.transition(LispState.START, LispEvent.EOF, LispState.EOF)
def start_list(ctx:LispCtx):
    ctx.new_actual_lisp_list()

@lisp_sm.transition(LispState.LIST, LispEvent.OPEN, LispState.LIST)
def new_list(ctx:LispCtx):
    ctx.new_actual_lisp_list()

@lisp_sm.transition((LispState.START,LispState.LIST), LispEvent.EOF, LispState.EOF)
def end_of_file(ctx:LispCtx):
    if ctx.depth() < 1:
        raise BadStackError(f"To many ')' in lisp expression ({ctx.depth()})")
    if ctx.depth() > 1:
        raise BadStackError(f"To many '(' in lisp expression ({ctx.depth()})")

@lisp_sm.transition(LispState.LIST, LispEvent.ELEMENT, LispState.LIST)
def new_element(ctx:LispCtx):
    ctx.new_element()

@lisp_sm.transition(LispState.LIST, LispEvent.CLOSE, LispState.LIST)
def close_list(ctx:LispCtx):
    ctx.close_actual_lisp_list()

def tokenize(lisp_expression:str)->Generator[str, None, None]:
    for token in lisp_expression.replace("(", " ( ").replace(")"," ) ").split():
        try:
            token = int(token)
        except Exception:
            try:
                token = float(token)
            except Exception:
                pass
        yield token

def tokenize_file(filename: Path)->Generator[str, None, None]:
    with open(filename) as filehandle:
        for line in filehandle.readlines():
            yield from tokenize(line)

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
        raise NameError(f"unbound symbol: {name}  -- {self}")

    def set(self, name, value):
        self.data[name] = value

    def __str__(self):
        ret = ""
        if self.parent is not None:
            ret += str(self.parent)
        return ret + str(self.data)

class FunctionDef:
    def __init__(self, closure, params, body) -> None:
        self.closure = closure
        self.params = params
        self.body = body


class LispInterpreter:

    def __init__(self, lisp_tree : list[Any]):
        self.lisp_tree = lisp_tree
        self.specialforms = {
            'if': self.ifthenelse,
            'define': self.define,
            'let': self.let,
            'lambda': self.create_lambda,
            'defun': self.define_function,
            'map': self.map,
        }
        self.functions = {
            'begin': self.begin,
            'list': self.create_list,
            '+': self.add,
            '-': self.sub,
            '*': self.mult,
            '/': self.div,
            '>=': self.greaterequal,
            '>': self.greater,
            '<=': self.lessequal,
            '<': self.less,
            '==': self.equal,
        }

    def run_rec(self, env:Env, expression: list[Any]):
        #print(expression)
        if isinstance(expression, str):
            new_expression = env.get(expression)

            return new_expression

        if isinstance(expression, (float,int)):
            return expression

        if not isinstance(expression, list):
            raise ValueError(f"invalid value {expression}")

        function = expression[0]
        args = expression[1:]

        if isinstance(function, list):
            function = self.run_rec(env, function)

        if function in self.specialforms:
            return self.specialforms[function](env, args)


        values = [self.run_rec(env, arg) for arg in args]

        if isinstance(function, (int, float)):
            return [function, *values]

        if function in self.functions.keys():
            return self.functions[function](values)
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
            else:
                raise ValueError(f"unknown function {function}")

    def run(self):
        env : Env = Env()
        ret = None
        for e in self.lisp_tree:
            ret = self.run_rec(env, e)
        return ret

    def create_lambda(self, env, args):
        params, body = args
        return FunctionDef(env, params, body)

    def define_function(self, env, args):
        name, params, body = args
        func = FunctionDef(env, params, body)
        env.set(name, func)


    def begin(self, env, args):
        _, expressions = args
        ret = None
        for expression in expressions:
            ret = self.run_rec(env, expression)
        return ret

    def ifthenelse(self, env, args):
        condition, true_branch, false_branch = args
        cond_result = self.run_rec(env, condition)
        #print(f"{cond_result=}")
        if cond_result is not None:
            return self.run_rec(env, true_branch)
        else:
            return self.run_rec(env, false_branch)

    def define(self, env: Env, args):
        var, value = args
        env.set(var, self.run_rec(env, value))

    def let(self, env: Env, args):
        env = Env(env)
        vars, *expressions = args

        for var in vars:
            self.define(env, var)

        ret = None

        for expression in expressions:
            ret = self.run_rec(env, expression)

        env = env.parent

        return ret

    def create_list(self, args):
        return list(args)

    def map(self, env, args):
        func, values = args
        return [self.run_rec(env, [func, value]) for value in values]

    def greater(self, args):
        a, b = args
        #print(f"{a=} > {b=}")
        ret = True if a>b else None
        #print(f"{ret=}")
        return ret

    def greaterequal(self, args):
        a, b = args
        #print(f"{a=} >= {b=}")
        ret = True if a>=b else None
        #print(f"{ret=}")
        return ret

    def less(self, args):
        a, b = args
        #print(f"{a=} < {b=}")
        ret = True if a<b else None
        #print(f"{ret=}")
        return ret

    def lessequal(self, args):
        a, b = args
        #print(f"{a=} <= {b=}")
        ret = True if a<=b else None
        #print(f"{ret=}")
        return ret

    def equal(self, args):
        a, b = args
        #print(f"{a=} == {b=}")
        ret = True if a==b else None
        #print(f"{ret=}")
        return ret

    def add(self, args):
        return sum(args)

    def mult(self, args):
        result = 1
        for arg in args:
            result *= arg
        return result

    def sub(self, args):
        l = len(args)
        if l == 0:
            raise ValueError("sub with no argument")
        if l == 1:
            return -args[0]
        result = args[0]
        for arg in args[1:]:
            result -= arg
        return result

    def div(self, args):
        l = len(args)
        if l == 0:
            raise ValueError("sub with no argument")
        result = args[0]
        for arg in args:
            result /= arg
        return result

def main() -> None:
    lisp_lines0 = textwrap.dedent("""\
        (my-func 1 2 ( + 1 2 )
        """)
    lisp_lines1 = textwrap.dedent("""\
        (my-func 1 2 3 (my-func 4 5 (+ 3 3)))
        (+ 10 (* 3 6))
        """)
    lisp_lines2 = textwrap.dedent("""\
        (my-func 1 2 3 (my-func 4 5 (+ 3 3))))
        """)
    lisp_lines3 = """\
    (define a 10)
    (define addN
        (lambda (n)
            (lambda (x) (+ x n)
            )
        )
    )
    (list (let ((a 2) (b 3 )) (+ 1 a b (* 2 2) (if nil (/ 2 1) (+ 3 2))) (+ a b)) 10)"""

    lisp_lines4 = """\
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
    """
    lisp_lines5 = """\
    (defun fib (x)
        (if (>= x 3)
            (+ (fib (- x 1)) (fib (- x 2)))
            1
        )
    )
    (map (lambda (x) (list x (fib x))) (3 4 5 6 7 8 9 10 11 12))
        """
    lisp_lines6 = """\
    (defun sqr (x) (x (* x x)))
    (map sqr (4 5))
    """
    lisp_lines7 = """\
(defun double (x) (* 2 x))
(map double (1 2 3 4))
((lambda (x) (* 3 x)) 3)
    """
    parser : LispParser = LispParser(lisp = LispCtx())

    parsed_lisp = parser.parse(tokenize(lisp_lines5))
    print(f"{parsed_lisp=}")

    interpreter = LispInterpreter(parsed_lisp)
    print(f"interpreter.run({parsed_lisp})={interpreter.run()}")

    exit(0)

    ctx = LispCtx()
    print(f"ctx {ctx.depth}")

    exit(0)
    lispfile = Path("./src/lispfile.lisp").absolute()
    if lispfile.exists():
        #for token in tokenize_file(lispfile):
        #    print(token)
        parsed_lisp = parser.parse(tokenize_file(lispfile))
        print(parsed_lisp)
    else:
        print(f"Can't find {lispfile}")
        exit(1)

if __name__ == '__main__':
    main()
