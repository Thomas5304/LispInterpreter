import os
import pathlib
from dataclasses import dataclass, field
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

    def short(self, tag, content = "", **attrs):
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
    order: int

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
    order: int

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
    
def genLPPGroups(layertable):
    lpp_groups  = defaultdict(list)
    for lpp in layertable.all_layername_purposes():
        if lpp.layer in lpp_groups:
            lpp_groups[lpp.layer].append(lpp)
        elif lpp.purpose in lpp_groups:
            lpp_groups[lpp.purpose].append(lpp)
        else:
            lpp_groups[lpp.layer].append(lpp)
    return lpp_groups



def createDisplay(displayName):
    displayNames.add(displayName)
    #print(f"displayName: {displayName}")


def createStipple(name, display, stipple):
    stipples[name][display] = Stipple(display, name, stipple, -1)
    #print(stipples[name][display])

def createLineStyle(name, display, lineSize, linePattern):
    linestyles[name][display] = LineStyle(display, name, lineSize, linePattern, -1)
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

def getKlayoutCustomPattern(collection, display, pattern):
    return f"C{collection[pattern][display].order}"
    


def getKlayoutCustomOrInternalPattern(collection, display, pattern):
    try:
        return getKlayoutCustomPattern(collection, display, pattern)
    except KeyError:
        pass

    return getKlayoutInternalPattern(pattern)

def generate_lpp(lyp, tag, displayName, lpp):
    def genPacketName(lpp):
        return f"P_{lpp.layer}_{lpp.purpose}"

    with lyp(tag):
        # Data
        
        
        lpp_gdsdt = layertable.layerno_datatype_for(lpp)
        
        # create
        lyp.short("name", f"{lpp.layer}_{lpp.purpose} ({lpp_gdsdt.layerno}/{lpp_gdsdt.datatype})")
        
        
        lyp.short("source", f"{lpp_gdsdt.layerno}/{lpp_gdsdt.datatype}")
        
        if genPacketName(lpp) not in displaypackets:
            return
        if displayName not in displaypackets[genPacketName(lpp)]:
            return
        
        lpp_displaypacket = displaypackets[genPacketName(lpp)][displayName]
        lpp_fill_color = colors[lpp_displaypacket.fillColor][displayName]
        lpp_frame_color = colors[lpp_displaypacket.outlineColor][displayName]
        
        lyp.short("fill-color", genLayerColor(lpp_fill_color))
        lyp.short("frame-color", genLayerColor(lpp_frame_color))
        lyp.short("dither-pattern", getKlayoutCustomOrInternalPattern(stipples,
                                                                      displayName,
                                                                      lpp_displaypacket.stippleName if lpp_displaypacket.fillStyle!="X"
                                                                      else "blank"))
        lyp.short("line-style", getKlayoutCustomOrInternalPattern(linestyles, displayName, lpp_displaypacket.lineStyleName))
        
        
        lyp.short("width", 1)
        
        lyp.short("visible", "true")
        lyp.short("transparent", "false")
        lyp.short("marked", "false")
        lyp.short("xfill", "false" if lpp_displaypacket.fillStyle!="X" else "true")
        lyp.short("animation", 0)

   

def generate_lyp(lyphandle, displayName = None):

    if not displayName:
        if len(displayNames)==1:
            displayName = list(displayNames)[0]
    if not displayName:
        raise KeyError("No display name")

    lyp = XMLBuilder()


    stippleToCMap = {}
    stippleCounter = 0
    for stipplename, displaystipples in stipples.items():
        if displayName not in displaystipples:
            continue
        stipple = displaystipples[displayName]
        stipple.order = stippleCounter
        stippleCounter += 1



    lineStyleCounter = 0
    for linestylename, displaylinestyle in linestyles.items():
        if displayName not in displaylinestyle:
            #print(f"{displayName} not in {displaylinestyle}")
            continue
        linestyle = displaylinestyle[displayName]
        linestyle.order = lineStyleCounter
        lineStyleCounter += 1


    with lyp("layer-properties"):
        grouping = True
        if grouping:
            lpp_groups = genLPPGroups(layertable)
            for groupname, lpp_list in lpp_groups.items():
                if len(lpp_list) == 1:
                    generate_lpp(lyp, "properties", displayName, lpp_list[0])
                else:
                    with lyp("properties"):
                        lyp.short("name", groupname)
                        lyp.short("source")
                        lyp.short("frame-color")
                        lyp.short("fill-color")
                        lyp.short("frame-brightness", 0)
                        lyp.short("fill-brightness", 0)
                        lyp.short("dither-pattern")
                        lyp.short("line-style")
                        lyp.short("valid", "true")
                        lyp.short("visible", "true")
                        lyp.short("transparent", "false")
                        lyp.short("width")
                        lyp.short("marked", "false")
                        lyp.short("xfill", "false")
                        lyp.short("animation", 0)
                        lyp.short("expanded", "true")
                        for lpp in lpp_list:
                            generate_lpp(lyp, "group-members", displayName, lpp)
        else:
            for lpp in layertable.all_layername_purposes():
                generate_lpp(lyp, "properties", displayName, lpp)

        for stipplename, displaystipples in stipples.items():
            if displayName not in displaystipples:
                continue
            stipple = displaystipples[displayName]
            with lyp("custom-dither-pattern"):
                with lyp("pattern"):
                    gen_matrix(stipple.stippleMatrix, lyp, "line")
                    lyp.short("name", stipple.stippleName)
                    lyp.short("order", stipple.order)
                    

        for linestylename, displaylinestyle in linestyles.items():
            if displayName not in displaylinestyle:
                continue
            linestyle = displaylinestyle[displayName]
            with lyp("custom-line-style"):
                lyp.short("line", print_pattern_line(linestyle.linePattern))
                lyp.short("name", linestyle.lineStyleName)
                try:
                    lyp.short("order", linestyle.order)
                except KeyError as ke:
                    print(linestylename, ke)




    print(lyp, file = lyphandle)


def main():
    pass

if __name__ == "__main__":
    main()
