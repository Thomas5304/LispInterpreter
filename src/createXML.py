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

