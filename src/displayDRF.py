import os
import pathlib
from dataclasses import dataclass
from collections import defaultdict
import functools

@dataclass
class Layer:
    name: str


@dataclass
class Purpose:
    purpose: str

def prefix(pf, indent = ""):
    if pf!="":
        return indent + f"<{pf}>"
    return indent


def suffix(sf, indent = ""):
    if sf!="":
        return indent + f"</{sf}>"
    return indent

def print_pattern_line(line, presuffix= "", indent = ""):
    pattern = prefix(presuffix, indent=indent)
    for c in line:
        pattern += "*" if c else "."
    return pattern+suffix(presuffix) # same row


def print_matrix(matrix, matrixtag = "", rowtag="", indent = ""):
    result = prefix(matrixtag, indent=indent)+"\n"
    for row in matrix:
        result += print_pattern_line(row, rowtag, indent+"  ")
        result +="\n"
    return result+suffix(matrixtag, indent=indent)


@dataclass
class Stipple:
    display:str
    stippleName: str
    stippleMatrix: list[list[str]]

    def __str__(self):
        result = f"Stipple {self.display} {self.stippleName}\n"
        result += print_matrix(self.stippleMatrix)
        return result


@dataclass
class LineStyle:
    display:str
    lineStyleName: str
    lineSize: int
    linePattern: list[str]

    def __str__(self):
        result = f"LineStyle {self.display} {self.lineStyleName} {self.lineSize}\n"
        for c in self.linePattern:
            result += f"*" if c else "."
        return result

@dataclass
class DisplayPacket:
    display: str
    packetName: str
    stippleName: str
    lineStyleName: str
    fillColor: str
    outlineColor: str
    fillStyle: str

@dataclass
class Color:
    display: str
    colorName: str
    red: int
    green: int
    blue: int
    visible: bool

@dataclass
class LPP:
    def __init__(self, layer, purpose, stippleName):
        self.layer = layer
        self.purpose = purpose
        self.stippleName = stippleName

displayNames = set()
colors = defaultdict(dict)
stipples = defaultdict(dict)
linestyles = defaultdict(dict)
layer_names = {}
purpose_names = {}
lpps={}
displaypackets = {}

def createDisplay(displayName):
    displayNames.add(displayName)
    #print(f"displayName: {displayName}")


def createStipple(name, display, stipple):
    stipples[name][display] = Stipple(display, name, stipple)
    #print(stipples[name][display])

def createLineStyle(name, display, lineSize, linePattern):
    linestyles[name][display] = LineStyle(display, name, lineSize, linePattern)
    #print(linestyles[name][display])

def createDisplayPacket(name, display, stippleName, lineStyleName, fillColor, outlineColor, fillStyle=None):
    displaypackets[name][display] = DisplayPacket(display=display,
            packetName=name,
            stippleName=stippleName,
            lineStyleName=lineStyleName,
            fillColor=fillColor,
            outlineColor=outlineColor,
            fillStyle=fillStyle)


def createColor(name, display, red, green, blue, visible):
    colors[name][display] = Color(display, name, int(red), int(green), int(blue), visible=True)

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

def genCustomDitherPatterns(stipples, filehandle, displayName = None, indent = ""):
    """print all stipples in custom-dither-pattern"""

    if not displayName:
        if len(displayNames)==1:
            displayName = list(displayNames)[0]
    if not displayName:
        raise KeyError("No display name")

    for stippleName, stipplesForName in stipples.items():
        stipple = stipplesForName[displayName]
        genCustomDitherPatternsForDisplay(stipple, filehandle, indent)

def genCustomDitherPatternsForDisplay(stipple:Stipple, filehandle, indent=""):

    stippleTag = "custom-dither-pattern"
    nameTag = "name"
    orderTag = "order"

    print(f"{prefix(stippleTag,indent)}", file = filehandle)
    print(print_matrix(stipple.stippleMatrix, "pattern", "line", indent=indent+"  "), file = filehandle)
    print(f"{prefix(nameTag, indent+"  ")}{stipple.stippleName}{suffix(nameTag)}")
    print(f"{prefix(orderTag, indent+"  ")}1{suffix(orderTag)}")
    print(f"{suffix(stippleTag,indent)}", file = filehandle)


def genCustomLineStyles(linestyles, filehandle, displayName = None, indent = ""):
    """print all linestyles in custom-line-styles"""

    if not displayName:
        if len(displayNames)==1:
            displayName = list(displayNames)[0]
            if not displayName:
                raise KeyError("No display name")
    for linestyleName, linestylesForName in linestyles.items():
        linestyle = linestylesForName[displayName]
        genCustomLineStylesForDisplay(linestyle, filehandle, indent)


def genCustomLineStylesForDisplay(linestyle:LineStyle, filehandle, indent=""):
    linestyleTag = "custom-line-style"
    nameTag = "name"
    orderTag = "order"

    print(f"{prefix(linestyleTag,indent)}", file = filehandle)
    print(print_pattern_line(linestyle.linePattern, "pattern", indent=indent+"  "), file = filehandle)
    print(f"{prefix(nameTag, indent+"  ")}{linestyle.lineStyleName}{suffix(nameTag)}")
    print(f"{prefix(orderTag, indent+"  ")}1{suffix(orderTag)}")
    print(f"{suffix(linestyleTag,indent)}", file = filehandle)

def genLayerColor(color:Color, colortag, filehandle, indent=""):
    colorInHex = f"#{color.red:02X}{color.green:02X}{color.blue:02X}"
    print(f"{prefix(colortag)}{colorInHex}{suffix(colortag)}")

def genDefinePacket(packet:DisplayPacket, filehandle, indent=""):
    pass

def generate_lyp(lyphandle):
    genCustomDitherPatterns(stipples, lyphandle, indent= "", displayName="")
    genCustomLineStyles(linestyles, lyphandle, indent= "", displayName="")
