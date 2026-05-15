import os
import pathlib
from dataclasses import dataclass

@dataclass
class Layer:
    def __init__(self, name) -> None:
        self.name = name

        
@dataclass
class Purpose:
    def __init__(self, purpose) -> None:
        self.purpose = purpose


@dataclass
class LPP:
    def __init__(self, layer, purpose, stippleName):
        self.layer = layer
        self.purpose = purpose
        self.stippleName = stippleName

    
layer_names = {}
purpose_names = {}
lpps={}

def createStipple(name, display, stipple):
    print(f"Stipple {display}/{name}\n")
    for row in stipple:
        for col in row:
            print("\u2588\u2588" if col else "  ", end="")
        print()

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
    print(f"LPP({lpp_layer}/{lpp_purpose})")
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

    lpps[lpp] = LPP(lpp_layer, lpp_purpose, stippleName)
    
    return not error