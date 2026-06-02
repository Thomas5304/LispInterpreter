import os
import pathlib
from dataclasses import dataclass
from collections import defaultdict
import functools
from dillingUtils import Layertable, LayertableParser


class XMLBuilder:
    def __init__(self):
        self.lines = []
        self.level = 0

    def __call__(self, tag, **attrs):
        """Ermoeglicht den Aufruf des Objekts als Context Manager."""
        return XMLElement(self, tag, attrs)

    def text(self, content):
        """Fuegt einfachen Textinhalt hinzu."""
        indent = "  " * self.level
        self.lines.append(f"{indent}{content}")

    def short(self, tag, content, **attrs):
        indent = "  " * self.level
        attr_str = " " + "".join([f' {k}="{v}"' for k, v in attrs.items()])
        if isinstance(content, (int, float)):
            content = str(content)
        if content and len(content)>0:
            self.lines.append(f"{indent}<{tag}{attr_str}>{content}</{tag}>")
        else:
            self.lines.append(f"{indent}<{tag}{attr_str} />")

    def comment(self, text):
        indent = "  " * self.level
        self.lines.append(f"{indent}<!-- {text} -->")


    def __str__(self):
        return "\n".join(self.lines)

class XMLElement:
    def __init__(self, builder, tag, attrs):
        self.builder = builder
        self.tag = tag
        # Attribute in XML-Format umwandeln (z.B. id="123")
        self.attr_str = "".join([f' {k}="{v}"' for k, v in attrs.items()])

    def __enter__(self):
        # Oeffnendes Tag mit Einrueckung
        indent = "  " * self.builder.level
        self.builder.lines.append(f"{indent}<{self.tag}{self.attr_str}>")
        self.builder.level += 1
        return self.builder

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Schliessendes Tag
        self.builder.level -= 1
        indent = "  " * self.builder.level
        self.builder.lines.append(f"{indent}</{self.tag}>")



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

def print_pattern_line(line):
    pattern = ""
    for c in line:
        pattern += "*" if c else "."
    return pattern

def print_pattern_line_with_tag(line, presuffix= "", indent = ""):
    pattern = prefix(presuffix, indent=indent)
    pattern+= print_pattern_line(line)
    return pattern+suffix(presuffix) # same row


def print_matrix(matrix, matrixtag = "", rowtag="", indent = ""):
    result = prefix(matrixtag, indent=indent)+"\n"
    for row in matrix:
        result += print_pattern_line_with_tag(row, rowtag, indent+"  ")
        result +="\n"
    return result+suffix(matrixtag, indent=indent)

def gen_matrix(matrix, xml, tag):
    for row in matrix:
        xml.short(tag, print_pattern_line(row))


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

layertable = None
displayNames = set()
colors = defaultdict(dict)
stipples = defaultdict(dict)
linestyles = defaultdict(dict)
layer_names = {}
purpose_names = {}
lpps={}
displaypackets = defaultdict(dict)



def createLayertable(file):
    global layertable
    layertable = Layertable(file)

    parser = LayertableParser(layertable)
    parser.read_file()
    #print(layertable)


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
    displaypackets[name][display] = DisplayPacket(display = display,
                                                  packetName = name,
                                                  stippleName = stippleName,
                                                  lineStyleName = lineStyleName,
                                                  fillColor = fillColor,
                                                  outlineColor = outlineColor,
                                                  fillStyle = fillStyle)

def getDisplayPacket(name, display):
    return displaypackets[name][display]

def createColor(name, display, red, green, blue, visible = True):
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
    print(f"{prefix(nameTag, indent+'  ')}{stipple.stippleName}{suffix(nameTag)}", file = filehandle)
    print(f"{prefix(orderTag, indent+'  ')}1{suffix(orderTag)}", file = filehandle)
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
    print(print_pattern_line_with_tag(linestyle.linePattern, "pattern", indent=indent+"  "), file = filehandle)
    print(f"{prefix(nameTag, indent+'  ')}{linestyle.lineStyleName}{suffix(nameTag)}", file = filehandle)
    print(f"{prefix(orderTag, indent+'  ')}1{suffix(orderTag)}", file = filehandle)
    print(f"{suffix(linestyleTag,indent)}", file = filehandle)

def genLayerColor(color:Color):
    return f"#{color.red:02X}{color.green:02X}{color.blue:02X}"

def genDefinePacket(packet:DisplayPacket, filehandle, indent=""):
    pass


def getKlayoutInternalPattern(pattern):
    if pattern == "solid":
        return "I0"
    elif pattern == "blank":
        return "I1"
    return "I0"

def getKlayoutCustomOrInternalPattern(collection, pattern):
    try:
        return f"C{collection[pattern]}"
    except KeyError:
        pass

    if pattern == "solid":
        return "I0"
    elif pattern == "blank":
        return "I1"

    return "I0"




class UnionFind:
    def __init__(self, elements):
        # Each element is its own parent (its own set)
        self.parent = {el: el for el in elements}
        self.rank = {el: 0 for el in elements}
        self.num_sets = len(elements)

    def find(self, i):
        # Path compression: make nodes point directly to the root
        if self.parent[i] == i:
            return i
        self.parent[i] = self.find(self.parent[i])
        return self.parent[i]

    def union(self, i, j):
        root_i = self.find(i)
        root_j = self.find(j)

        if root_i != root_j:
            # Union by rank: attach the smaller tree under the larger tree
            if self.rank[root_i] < self.rank[root_j]:
                self.parent[root_i] = root_j
            elif self.rank[root_i] > self.rank[root_j]:
                self.parent[root_j] = root_i
            else:
                self.parent[root_i] = root_j
                self.rank[root_j] += 1
            self.num_sets -= 1
            return True
        return False

    def get_equivalence_classes(self):
        """Returns a dictionary of root: [elements] representing classes."""
        classes = {}
        for element in self.parent:
            root = self.find(element)
            if root not in classes:
                classes[root] = []
            classes[root].append(element)
        return classes


def generate_lyp(lyphandle, displayName = None):
    #genCustomDitherPatterns(stipples, lyphandle, indent= "", displayName="")
    #genCustomLineStyles(linestyles, lyphandle, indent= "", displayName="")

    if not displayName:
        if len(displayNames)==1:
            displayName = list(displayNames)[0]
    if not displayName:
        raise KeyError("No display name")

    lyp = XMLBuilder()

    stippleToCMap = {}
    linestyleToCMap = {}

    def genPacketName(lpp):
        return f"P_{lpp.layer}_{lpp.purpose}"

    stippleCounter = 0
    for stipplename, displaystipples in stipples.items():
        if displayName not in displaystipples:
            continue
        stipple = displaystipples[displayName]
        stippleToCMap[stipple.stippleName] = stippleCounter
        stippleCounter += 1


    lineStyleCounter = 0
    for linestylename, displaylinestyle in linestyles.items():
        if displayName not in displaylinestyle:
            #print(f"{displayName} not in {displaylinestyle}")
            continue
        linestyle = displaylinestyle[displayName]
        linestyleToCMap[linestyle.lineStyleName] = lineStyleCounter
        lineStyleCounter += 1


    with lyp("layer-properties"):
        for lpp in layertable.all_layername_purposes():
            #print(lpp)


            with lyp("properties"):
                # Data


                lpp_gdsdt = layertable.layerno_datatype_for(lpp)

                # create
                lyp.short("name", f"{lpp.layer}_{lpp.purpose} ({lpp_gdsdt.layerno}/{lpp_gdsdt.datatype})")


                lyp.short("source", f"{lpp_gdsdt.layerno}/{lpp_gdsdt.datatype}")

                if genPacketName(lpp) not in displaypackets:
                    continue
                if displayName not in displaypackets[genPacketName(lpp)]:
                    continue

                lpp_displaypacket = displaypackets[genPacketName(lpp)][displayName]
                lpp_fill_color = colors[lpp_displaypacket.fillColor][displayName]
                lpp_frame_color = colors[lpp_displaypacket.outlineColor][displayName]
                lpp_linestyle = linestyles[lpp_displaypacket.lineStyleName][displayName]



                lyp.short("fill-color", genLayerColor(lpp_fill_color))
                lyp.short("frame-color", genLayerColor(lpp_frame_color))
                lyp.short("dither-pattern", getKlayoutCustomOrInternalPattern(stippleToCMap, lpp_displaypacket.stippleName))
                lyp.short("line-style", getKlayoutCustomOrInternalPattern(linestyleToCMap, lpp_linestyle.lineStyleName))


                lyp.short("width", lpp_linestyle.lineSize)

                lyp.short("visible", "true")
                lyp.short("transparent", "false")
                lyp.short("marked", "false")
                lyp.short("xfill", "false" if lpp_displaypacket.fillStyle!="X" else "true")
                lyp.short("animation", 0)

        for stipplename, displaystipples in stipples.items():
            if displayName not in displaystipples:
                continue
            stipple = displaystipples[displayName]
            with lyp("custom-dither-pattern"):
                with lyp("pattern"):
                    gen_matrix(stipple.stippleMatrix, lyp, "line")
                    lyp.short("name", stipple.stippleName)
                    try:
                        lyp.short("order", stippleToCMap[lpp_displaypacket.stippleName])
                    except:
                        pass

        for linestylename, displaylinestyle in linestyles.items():
            if displayName not in displaylinestyle:
                continue
            linestyle = displaylinestyle[displayName]
            with lyp("custom-line-style"):
                with lyp("pattern"):
                    lyp.short("line", print_pattern_line(linestyle.linePattern))
                    lyp.short("name", linestyle.lineStyleName)
                    try:
                        lyp.short("order", linestyleToCMap[lpp_linestyle.lineStyleName])
                    except KeyError as ke:
                        print(linestylename, ke)




    print(lyp, file = lyphandle)


def main():
    pass

if __name__ == "__main__":
    main()
