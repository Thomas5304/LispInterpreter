import lispSupport

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
        self.set('format', lispSupport.lisp_format)
        self.set('string-append', lambda *args: ''.join(str(arg) for arg in args))
        self.set('print', print)
        self.set('list', lispSupport.create_list)
        self.set('cons', lispSupport.eval_append)
        self.set('append', lispSupport.eval_append)
        self.set('and', lambda a, b: a and b)
        self.set('or', lambda a, b: a or b)
        self.set('zip', lambda *a: list(zip(*a)))
        self.set('null', lambda a: "t" if a==[] else "nil")
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

    def __call__(self, *values):
        new_env = self.bind_params(*values)
        return eval_lisp(new_env, self.body)

class FunctionDef(FunctionBase):
    def __init__(self, closure, all_params, body) -> None:
        super().__init__(closure, all_params)
        self.body = body

    def __call__(self, *values):
        new_env = self.bind_params(*values)
        return eval_lisp(new_env, self.body)



# Hilfsfunktionen zur Konversion (falls nötig)
def to_python(lisp_val):
    # einfache Identität; erweitere bei Bedarf (z.B. Symbol -> str, List -> tuple etc.)
    return lisp_val

def from_python(py_val):
    # einfache Identität; passe an, falls du spezielle Lisp-Typen brauchst
    return py_val

# Repräsentation für ein Lisp-Funktionsobjekt, das eine Python-Funktion aufruft
class PythonBridgeFunction(FunctionBase):
    def __init__(self, env, all_params, py_func):
        super().__init__(env, all_params)
        self.py_func = py_func

    def arity_ok(self, n):
        return n == len(self.params)

    # aufruf von Eval: args sind bereits evaluierte Lisp-Werte
    def __call__(self, *values):
        if not self.arity_ok(len(values)):
            raise TypeError(f"Expected {len(self.param_names)} args, got {len(values)}")
        py_args = [to_python(a) for a in values]
        result = self.py_func(*py_args)
        return from_python(result)


class Macro:
    def __init__(self, proc):
        self.proc = proc

    def expand(self, *raw_args):
        result = self.proc(*raw_args)
        #print("Macro.expand:", result)
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

