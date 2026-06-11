##!/tools/pdtooling/packages/VirtPythonEnv/pkg_synopsys/bin/python3
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
import readline

import displayDRF
from tokenParse import tokenize, Tokenize_file, tokenize_file, Symbol, atom, is_list, is_symbol, parse

#from displayDRF import printStipple

import closure
import lispSupport
import tokenParse


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
                # Kommentar bis Ende des aktuellen Puffers -> input moeglicherweise unvollstaendig
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

        # character literal: #\ followed von mindestens einem Zeichen; das naechste
        # Zeichen soll nicht als Klammer gezaehlt werden (z.B. #\) )
        if ch == '#' and i+1 < n and s[i+1] == '\\':
            # ueberspringe "#\" und das folgende "Zeichen" (sofern vorhanden)
            i += 2
            if i < n:
                # Falls Folgezeichen eine escape-Sequenz oder Name ist, koennte man noch
                # spezialisierter behandeln; hier ueberspringen wir mindestens ein Zeichen.
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

        # normale Weiterzaehlung
        i += 1

    # Ende des Puffers: wenn paren==0 und nicht in String/Block-Comment,
    # koennte trotzdem nichts angefangen worden sein (z.B. nur Whitespace).
    if paren == 0 and not in_string and block_comment == 0:
        # evtl. kein top-level Ausdruck begonnen -> None (oder 0)
        # Wir geben None zurueck, damit der Aufrufer bei leerem/unschließendem Input weitere Zeilen erwartet.
        # return None
        #
        # if no parent no string or no blockcomment
        # we want to get the value of variables
        return i

    # ansonsten: unvollstaendig (offene Klammern, String oder Block-Comment)
    return None


        
def parse_and_run(main_env, token_generator, debug_level = 0, functionMode = False):
    parsed_lisp = parse(token_generator, program=list(), function_mode = functionMode)
    try:
        #print(parsed_lisp)
        closure.run(parsed_lisp, main_env)
    except TypeError as te:
        print(f"Error: {te}\n===============\n")
        if debug_level:
            lispSupport.print_lisp_recursive(parsed_lisp)
            traceback.print_exc()
            print(f"===============\n")
    except NameError as ne:
        print(f"Error: {ne}\n===============\n")
        if debug_level:
            lispSupport.print_lisp_recursive(parsed_lisp)
            traceback.print_exc()
            print(f"===============\n")
    except ValueError as ve:
        print(f"Error: {ve}\n===============\n")
        if debug_level:
            lispSupport.print_lisp_recursive(parsed_lisp)
            traceback.print_exc()
            print(f"===============\n")


def parse_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument("lispfiles", nargs="*")

    parser.add_argument("--display", dest="displayName", default = "", help="Selected display name")
    parser.add_argument("-d", "--drf", dest="displayDRF", default = None, help="Use displayDRF file")
    parser.add_argument("-m", "--map", dest="layerMap", default = None, help="Use layermap file")

    return parser.parse_args()


def lisp_interpreter(args, repl = True):
    debug_level = 1
    main_env = closure.Env()
    main_env.init_env()
    main_env.set("__.QUIT.__", not repl)
    program = Path(sys.argv[0])
    programpath = program.parent
    programname = program.name
    print(f"{programname} located in {programpath}")

    lispfiles = [programpath / Path("lispfile.lisp")]
    for lf in args.lispfiles:
        lispfiles.append(Path(lf).absolute())

    for lispfile in lispfiles:

        if lispfile.exists():
            #print(f"reading {lispfile}")
            #breakpoint()
            token_generator = tokenize_file(lispfile)
            parse_and_run(main_env, token_generator, debug_level)
        else:
            print(f"Can't find {lispfile} from here {os.getcwd()}")

    if main_env.get("__.QUIT.__"):
        return
        
    buffer = ""
    try:
        while not main_env.get("__.QUIT.__"):
            if buffer == "":
                prompt = "user> "
            else:
                prompt = "....> "

            line = input(prompt)
            buffer += "\n" + line

            while True:
                end_idx = first_complete_expr(buffer)
                if end_idx is None:
                    break
                expr_text = buffer[:end_idx].strip()
                buffer = buffer[end_idx:]
                #print(f"buffer '{buffer}'")

                if not expr_text:
                    if expr_text == "":
                        break
                    continue

                token_generator = tokenize(expr_text)
                parse_and_run(main_env, token_generator, debug_level)
                break
    except EOFError:
        print("EoF")
    

def main() -> None:
    errorstate = False
    args = parse_arguments()

    if not args.displayDRF:
        print("No display DRF given")
        errorstate = True
        
    if not args.layerMap:
        print("No layermap given")
        errorstate = True
        
    lisp_interpreter(args, repl = True)
    
if __name__ == '__main__':
    main()
