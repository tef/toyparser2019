from textexpressions import Grammar, Node

class JSON(Grammar, start="document"):
    document = json_list | json_object

    json_value = ( 
        json_list | json_object |
        json_string | json_number |
        json_true | json_false | 
        json_null
    )
    
    json_true = literal("true")
    json_false = literal("false")
    json_null = literal("null")

    def json_number(self):
        with self.optional():
            self.literal("-")
        with self.choice():
            with self.case():
                self.literal("0")
            with self.case():
                self.any_literal(*"12345689")
                with self.repeat():
                    self.any_literal(*"012345689")
        with self.optional():
            self.literal(".")
            with self.repeat():
                self.any_literal(*"012345689")
        with self.optional():
            self.any_literal("e", "E")
            with self.optional():
                self.any_literal("+", "-")
                with self.repeat():
                    self.any_literal(*"012345689")

    def json_string(self):
        self.literal("\"")
        with self.repeat():
            with self.repeat():
                self.any_literal_except("\"","\\")
            with self.optional():
                self.literal("\\")
                with self.choice():
                    with self.case():
                        self.any_literal(
                            "\"", "\\", "/", "b", 
                            "f", "n", "r", "t",
                        )
                    with self.case():
                        self.literal("u")
                        self.any_literal(*"0123456789abcedfABCDEF")
                        self.any_literal(*"0123456789abcedfABCDEF")
                        self.any_literal(*"0123456789abcedfABCDEF")
                        self.any_literal(*"0123456789abcedfABCDEF")
        self.literal("\"")

    def json_list(self):
        self.literal("[")
        with self.optional():
            self.json_value()
            with self.repeat(min=0):
                self.literal(",")
                self.json_value()
        self.literal("]")

    def json_object(self):
        self.literal("{")
        with self.optional():
            self.json_string()
            self.literal(":")
            self.json_value()
            with self.repeat(min=0):
                self.literal(",")
                self.json_string()
                self.literal(":")
                self.json_value()
        self.literal("}")

for name, value in JSON.__dict__.items():
    if name.startswith('_'): continue
    print(name, value)
    if isinstance(value, Node):
        for r in value.rules:
            print('\t', r)
