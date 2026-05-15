import os
import pathlib
from dataclasses import dataclass
from collections import defaultdict

@dataclass
class Layer:
    name: str

        
@dataclass
class Purpose:
    purpose: str


@dataclass
class Stipple:
    display:str
    stippleName: str
    stippleMatrix: list[list[str]]

    def __str__(self):
        result = f"{self.display} {self.stippleName}\n"
        for row in self.stippleMatrix:
            for col in row:
                result += "\u2588\u2588" if col else "  "
            result+="\n"
        return result


@dataclass
class LPP:
    def __init__(self, layer, purpose, stippleName):
        self.layer = layer
        self.purpose = purpose
        self.stippleName = stippleName


stipples = defaultdict(dict)
layer_names = {}
purpose_names = {}
lpps={}

def createStipple(name, display, stipple):
    stipples[name][display] = Stipple(display, name, stipple)
    print(stipples[name][display])


def createLayer(layer):
    if layer in layer_names:
        raise KeyError(f"Layer {layer} already defined!")
    layer_names[layer] = Layer(layer)


def getLayer(layer):
    if layer not in layer_names:
        raise KeyError(f"Layer {layer} not defined!")
    return layer_names[layer]


def createPurpose(purpose):
    if purpose in purpose_names:
        raise KeyError(f"Purpose {purpose} already defined!")
    purpose_names[purpose] = Layer(purpose)


def getPurpose(purpose):
    if purpose not in purpose_names:
        raise KeyError(f"Purpose {purpose} not defined!")
    return purpose_names[purpose]


def createLPP(lpp_layer, lpp_purpose, stippleName = None):
    print(f"LPP({lpp_layer}/{lpp_purpose} {stippleName if stippleName else '-no stipple-'})")
    lpp = (lpp_layer, lpp_purpose)
    error = False
    try:
        getLayer(lpp_layer)
    except KeyError as ke:
        print(ke)
        error = True
    try:
        getPurpose(lpp_purpose)
    except KeyError as ke:
        print(ke)
        error = True
    if error:
        print(f"fail to create LPP({lpp_layer}/{lpp_purpose})")

    if lpp in lpps:
        raise KeyError("LPP({lpp_layer}/{lpp_purpose}) already defined")

    if stippleName:
        if stippleName not in stipples:
            print(f"stipple {stippleName} not found")
        else:
            print(f"  for displays {', '.join(stipples[stippleName].keys())}")

    lpps[lpp] = LPP(lpp_layer, lpp_purpose, stippleName)
    
    return not error