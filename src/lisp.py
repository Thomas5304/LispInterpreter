#!/tools/pdtooling/packages/VirtPythonEnv/pkg_synopsys/bin/python3
from cmath import isinf
from re import L
import textwrap
from enum import Enum, auto
from typing import Callable, Any, Iterable, Generator, TypeVar
from dataclasses import dataclass, field
import os
import sys
from pathlib import Path
import traceback
import argparse

from tokenParse import tokenize, tokenize_file, Symbol, atom, is_list, is_symbol, parse

from displayDRF import printStipple

import closure
import lispSupport


# Handler für die special form
def defun_python(env, lisp_name, params, py_name_sym, py_namespace=None):
    print(f"defun_python")
    # py_name_sym kann ein Symbol sein; hier nehmen wir an, es ist der Name als string
    py_name = str(py_name_sym) if is_symbol else py_name_sym

    # Namespace, in dem wir python-Funktionen suchen (default: globals())
    ns = py_namespace if py_namespace is not None else globals()

    py_func = ns.get(py_name)
    if py_func is None:
        raise NameError(f"Python function '{py_name}' not found in provided namespace")
    
    bridge = PythonBridgeFunction(env, params, py_func)
    env.set(lisp_name, bridge)
    
    
def macroexpand(env, ast):
    while is_list(ast) and len(ast) > 0 and is_symbol(ast[0]):
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



def eval_lisp(env, expression):
    specialforms = {
        'if':           ifthenelse,
        'define':       define,
        'let':          let,
        'lambda':       create_lambda,
        'defun':        define_function,
        'defun-python': defun_python,
        'quote':        quote,
        'quasiquote':   eval_quasiquote,
        'unquote':      unquote,
        'eval':         eval,
        'begin':        begin,
        'set!':         overwrite,
        'load':         load_and_parse_lisp_file,
        'defmacro':     defmacro,
        'while':        while_loop,
        'print-eval':   lispSupport.print_and_eval,
        'cond':         eval_cond,
        'do-list':      eval_dolist,
        'symbol-name':  closure.symbol_name,
    }
    try:
        if isinstance(expression, closure.Symbol):
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
        traceback.print_exc()
    except Exception as e:
        print(f"{e}\n in {lispSupport.print_lisp_recursive(expression)}")
        traceback.print_exc()


def run(lisp_tree : list[Any], env:closure.Env):
    for e in lisp_tree:
        env.set('last-expr!', eval_lisp(env, e))
    if env.get('last-expr!') is not None:
        print(env.get('last-expr!'))

def eval_dolist(env, spec, *body):
    var_name = spec[0]
    list_expr = spec[1]

    values:list = eval_lisp(env, list_expr)

    result = None

    for value in values:

        local_env = closure.Env(parent=env)
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
            print(e)
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

def define(env: closure.Env, *args):
    (var, value) = args
    env.set(var, eval_lisp(env, value))

def overwrite(env, var, value):
    return "t" if env.overwrite(var, value) else "nil"

def let(env: closure.Env, vars, *expressions):
    env = closure.Env(env)

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
    if not isinstance(expr, list):
        return expr

    result = []

    for item in expr:

        # --------------------
        # ,x
        # --------------------

        if (
            isinstance(item, list)
            and len(item) > 0
            and item[0] == "unquote"
        ):

            value = eval_lisp(env, item[1])
            result.append(value)

        # --------------------
        # ,@x
        # --------------------

        elif (
            isinstance(item, list)
            and len(item) > 0
            and item[0] == "unquote-splicing"
        ):

            values = eval_lisp(env, item[1])

            if not isinstance(values, list):
                raise Exception(
                    "unquote-splicing requires list"
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
    print(f"quasiquote {lispSupport.print_lisp_recursive(ast)}, depth:{depth}")
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
        print(f"for q {lispSupport.print_lisp_recursive(q)}")
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

    parsed_lisp = parse(tokenize_file(filepath), program=list())

    run(parsed_lisp, env)

    return "t"

def eval(env, args):
    value = eval_lisp(env, args)
    return eval_lisp(env, value)


def first_complete_expr(s: str):
    """
    Scans s from the left and returns the index at which the first complete
    S-form ends (exclusive). If no complete form is present, returns None.
    Accounts for:
    - parentheses ( )
    - "strings" with backslash escapes
    - line comments starting with ';' until EOL
    - block comments '#| ... |#' (nestable)
    - character literals '#\\x' (ignores the next character for parenthesis counting)
    """
    i = 0
    n = len(s)
    paren = 0
    in_string = False
    escape = False
    block_comment = 0
    while i < n:
        ch = s[i]

        # Wenn in String: nur auf " (ohne Escape) achten
        if in_string:
            if escape:
                escape = False
            elif ch == '\\':
                escape = True
            elif ch == '"':
                in_string = False
            i += 1
            continue

        # Wenn in block comment: erkenne |# und #|
        if block_comment > 0:
            # erkenne Beginn #| (wenn verschachteln)
            if ch == '#' and i+1 < n and s[i+1] == '|':
                block_comment += 1
                i += 2
                continue
            # erkenne Ende |#
            if ch == '|' and i+1 < n and s[i+1] == '#':
                block_comment -= 1
                i += 2
                continue
            i += 1
            continue

        # Nicht in String/Block-Comment
        if ch == ';':
            # zeilenkommentar: skip bis EOL
            # find next newline or end
            j = s.find('\n', i)
            if j == -1:
                # Kommentar bis Ende des aktuellen Puffers -> input möglicherweise unvollständig
                return None
            i = j + 1
            continue

        if ch == '"' :
            in_string = True
            i += 1
            continue

        # block comment start
        if ch == '#' and i+1 < n and s[i+1] == '|':
            block_comment += 1
            i += 2
            continue

        # character literal: #\ followed von mindestens einem Zeichen; das nächste
        # Zeichen soll nicht als Klammer gezählt werden (z.B. #\) )
        if ch == '#' and i+1 < n and s[i+1] == '\\':
            # überspringe "#\" und das folgende "Zeichen" (sofern vorhanden)
            i += 2
            if i < n:
                # Falls Folgezeichen eine escape-Sequenz oder Name ist, könnte man noch
                # spezialisierter behandeln; hier überspringen wir mindestens ein Zeichen.
                i += 1
            continue

        if ch == '(':
            paren += 1
        elif ch == ')':
            paren -= 1
            if paren < 0:
                # unbalancierte schließende Klammer -> die Form endet hier (Fehlerfall)
                return i+1
            # wenn paren == 0 und nicht in string/comment, die Form ist abgeschlossen:
            if paren == 0:
                # Ausdruck komplett: return Position nach dieser Klammer
                return i+1

        # normale Weiterzählung
        i += 1

    # Ende des Puffers: wenn paren==0 und nicht in String/Block-Comment,
    # könnte trotzdem nichts angefangen worden sein (z.B. nur Whitespace).
    if paren == 0 and not in_string and block_comment == 0:
        # evtl. kein top-level Ausdruck begonnen -> None (oder 0)
        # Wir geben None zurück, damit der Aufrufer bei leerem/unschließendem Input weitere Zeilen erwartet.
        return None

    # ansonsten: unvollständig (offene Klammern, String oder Block-Comment)
    return None


def parse_and_run(main_env, token_generator, debug_level = 0):
    try:
        parsed_lisp = parse(token_generator, program=list())
        run(parsed_lisp, main_env)
    except TypeError as te:
        print(f"Error: {te}\n===============\n")
        if debug_level:
            traceback.print_exc()
            print(f"===============\n")
    except NameError as ne:
        print(f"Error: {ne}\n===============\n")
        if debug_level:
            traceback.print_exc()
            print(f"===============\n")
    except ValueError as ve:
        print(f"Error: {ve}\n===============\n")
        if debug_level:
            traceback.print_exc()
            print(f"===============\n")

def main() -> None:
    debug_level = 0
    main_env = closure.Env()
    main_env.init_env()
    program = Path(sys.argv[0])
    programpath = program.parent
    programname = program.name
    print(f"{programname} located in {programpath}")

    parser = argparse.ArgumentParser()

    parser.add_argument("lispfiles", nargs="*")

    args = parser.parse_args()
    

    lispfiles = [programpath / Path("lispfile.lisp")]
    for lf in args.lispfiles:
        lispfiles.append(Path(lf).absolute())

    for lispfile in lispfiles:

        if lispfile.exists():
            token_generator = tokenize_file(lispfile)
            parse_and_run(main_env, token_generator, debug_level)
        else:
            print(f"Can't find {lispfile} from here {os.getcwd()}")


    buffer = ""
    try:
        while True:
            if buffer == "":
                prompt = "user> "
            else:
                prompt = "....> "

            line = input(prompt)
            buffer += line

            while True:
                end_idx = first_complete_expr(buffer)
                if end_idx is None:
                    break
                expr_text = buffer[:end_idx].strip()
                buffer = buffer[end_idx:]
                #print(f"buffer '{buffer}'")

                if not expr_text:
                    continue

                token_generator = tokenize(expr_text)
                parse_and_run(main_env, token_generator, debug_level)
                break
    except EOFError:
        print("EoF")

if __name__ == '__main__':
    main()
