import lispSupport
import traceback

print_exc_level = 0

def set_print_exc_level(level):
    global print_exc_level

    print_exc_level = level

def print_exc():
    if print_exc_level > 0:
        traceback.print_exc()

debug_level = 0

def set_debug_level(level):
    global debug_level

    debug_level = level

def print_exception_errorprint_exception_error(parsed_lisp, exc):
    print(f"Error: {exc}\n===============\n")
    #breakpoint()
    lispSupport.print_lisp_recursive(parsed_lisp)
    print_exc()