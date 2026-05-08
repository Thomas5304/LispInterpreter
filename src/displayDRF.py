import os
import pathlib

def printStipple(name, display, stipple):
    print(f"Stipple {display}/{name}\n")
    for row in stipple:
        for col in row:
            print("\u2588\u2588" if col else "  ", end="")
        print()

