#!/tools/pdtooling/packages/VirtPythonEnv/pkg_synopsys/bin/python3
from typing import Callable, Any, Iterable, Generator, TypeVar, Protocol
from dataclasses import dataclass, field
import os
import sys
from pathlib import Path
import traceback



def tokenize(s: str)->Generator[str, None, None]:
    i = 0
    while i < len(s):
        c = s[i]

        if c == ';':
            while i < len(s) and s[i] != '\n':
                i+=1
            continue

        # whitespace
        if c.isspace():
            i += 1
            continue

        # Klammern
        if c in '()':
            yield c
            i += 1
            continue

        # unquote /unquote-splice
        if c in ",":
            if s[i+1] =='@':
                c+='@'
                i+=1
            yield c
            i += 1
            continue
        # quote / function-quote
        if c in "#":
            if s[i+1] =="'":
                c+="'"
                i+=1
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

            i += 1  # schliessendes "
            value = value.replace("\\n","\n").replace("\\t", "\t")
            yield ('STRING', value)
            continue

        # SYMBOL / ZAHL
        start = i
        while i < len(s) and not s[i].isspace() and s[i] not in '()\'`,"':
            i += 1

        yield s[start:i]

def tokenize_file(filename: Path)->Generator[str, None, None]:
    with open(filename, "r", encoding="utf-8", errors="ignore") as filehandle:
        for line in filehandle.readlines():
            yield from tokenize(line)

class Tokenize_file:
    def __init__(self, filename):

        if isinstance(filename, Path):
            self.filename = filename
        else:
            self.filename = Path(filename)


    def __call__(self):
        with open(self.filename) as filehandle:
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

def parse(tokens, program = list(), function_mode=False):
    class TokenStream:
        def __init__(self, generator):
            self.gen = [generator]
            self.buffer = None

        def next(self):
            if self.buffer is not None:
                token = self.buffer
                self.buffer = None
                return token
            if False:
                while True:
                    try:
                        return next(self.gen[-1])
                    except EOFError:
                        self.pop()
                        continue
                return None
            return next(self.gen[-1])

        def peek(self):
            if self.buffer is None:
                self.buffer = next(self.gen[-1])
            return self.buffer

        def get_dir(self):
            if isinstance(self.gen, Tokenize_file):
                return self.gen[-1].parent
            return Path(os.getcwd())

        def include(self, new_generator):
            print(f"include {new_generator}")
            self.gen.append(new_generator)

        def pop(self):
            print(f"pop include")
            if len(self.gen)>1:
                self.gen.pop()
            raise ValueError("No further tokenizer")

    def parse_stream(token_stream, function_mode = False):
        token = token_stream.next()

        #print(token)

        if token == '(':
            lst = []
            while token_stream.peek() != ')':
                lst.append(parse_stream(token_stream))
            _ = token_stream.next()  # ')'
            return lst

        elif token == ')':
            raise SyntaxError("Unexpected )")

        elif token == "'":
            return ['quote', parse_stream(token_stream)]

        elif token == '`':
            return ['quasiquote', parse_stream(token_stream)]

        elif token == ',':
            return ['unquote', parse_stream(token_stream)]

        elif token == ',@':
            return ['unquote-splicing', parse_stream(token_stream)]

        elif token == "#'":
            return ['function', parse_stream(token_stream)]

        else:
            if function_mode and token_stream.peek() == '(':
                lst = [atom(token)]
                #print(f"parser in function mode: correcting {token}(")
                _ = token_stream.next() # consume (
                while token_stream.peek() != ')':
                    lst.append(parse_stream(token_stream))
                _ = token_stream.next()  # ')'
                return (lst)
            else:
                return atom(token)

    #print(f"Parser Mode: {'function_mode' if function_mode else 'S-Expression'}")
    stream = TokenStream(tokens)
    try:
        while True:
            program.append(parse_stream(stream, function_mode))
    except StopIteration:
        return program
