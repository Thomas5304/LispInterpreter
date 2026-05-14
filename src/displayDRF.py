import os
import pathlib

def createStipple(name, display, stipple):
    print(f"Stipple {display}/{name}\n")
    for row in stipple:
        for col in row:
            print("\u2588\u2588" if col else "  ", end="")
        print()

def createLPP(lpp_name, lpp_purpose):
    print(f"LPP({lpp_name}/{lpp_purpose})")