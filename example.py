from textexpressions import Grammar

class JSON(Grammar, start="document"):
    document = json_list 
    document = json_object

    json_value = rule( 
        json_list | json_object |
        json_string | json_number |
        json_true | json_false | 
        json_null
    )
    
    json_true = accept("true")
    json_false = accept("false")
    json_null = accept("null")

    @rule()
    def json_number(self):
        with self.optional():
            self.accept("-")
        with self.choice():
            with self.case():
                self.accept("0")
            with self.case():
                self.accept(*"12345689")
                with self.repeat():
                    self.accept(*"012345689")
        with self.optional():
            self.accept(".")
            with self.repeat():
                self.accept(*"012345689")
        with self.optional():
            self.accept("e", "E")
            with self.optional():
                self.accept("+", "-")
                with self.repeat():
                    self.accept(*"012345689")

    @rule()
    def json_string(self):
        self.accept("\"")
        with self.repeat(), self.choice():
            with self.case():
                self.accept("\\u")
                self.accept(*"0123456789abcedfABCDEF")
                self.accept(*"0123456789abcedfABCDEF")
                self.accept(*"0123456789abcedfABCDEF")
                self.accept(*"0123456789abcedfABCDEF")
            with self.case():
                self.accept("\\")
                self.accept(
                    "\"", "\\", "/", "b", 
                    "f", "n", "r", "t",
                )
            with self.case():
                self.accept(exclude=["\\", "\""])
        self.accept("\"")

    @rule()
    def json_list(self):
        self.accept("[")
        with self.repeat(max=1):
            self.json_value()
            with self.repeat(min=0):
                self.accept(",")
                self.json_value()
        self.accept("]")

    @rule()
    def json_object(self):
        self.accept("{")
        with self.optional():
            self.json_string()
            self.accept(":")
            self.json_value()
            with self.repeat(min=0):
                self.accept(",")
                self.json_string()
                self.accept(":")
                self.json_value()
        self.accept("}")

for name, value in JSON.rules.items():
    print(name, '<--', value,'.')
    print()

# build a recogniser, give it captures
# get back tree of (start, end, children) nodes, well something which exposes start,end and children 
