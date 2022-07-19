from dbuilder.ast import Node, Printer, Statement
from dbuilder.ast.utils import _type_name


class Method(Node):
    statements: list[Statement] = []
    active_statement: list[Statement] = []

    def __init__(self, name, args, annotations):
        super().__init__()
        self.name = name
        self.args = args
        self.annotations = annotations
        self.statements = []
        self.active_statement = []

    def add_statement(self, statement):
        if len(self.active_statement) > 0:
            active = self.active_statement[0]
            active.add_statement(statement)
            if statement.activates():
                self.active_statement.insert(0, statement)
        else:
            self.statements.append(statement)
            if statement.activates():
                self.active_statement.insert(0, statement)

    def end_statement(self, statement):
        self.active_statement.remove(statement)

    def _get_specs(self):
        sd = self.annotations.get("_method")
        if not sd:
            return ""
        res = []
        if sd["impure"]:
            res.append("impure")
        if sd["inline"]:
            res.append("inline")
        elif sd["inline_ref"]:
            res.append("inline_ref")
        elif sd["method_id"]:
            if sd["method_id_v"]:
                res.append("method_id(%d)" % sd["method_id_v"])
            else:
                res.append("method_id")
        if len(res) == 0:
            return ""
        return " ".join(res) + " "

    def print_func(self, printer: Printer):
        type_namer = lambda x: "{type} {name}".format(
            type=_type_name(x[0]),
            name=x[1],
        )
        tupler = lambda x: (self.annotations[x], x)
        arg_defs = list(map(type_namer, map(tupler, self.args)))
        printer.print(
            "{output} {name}({args}) {specs}{{",
            output=_type_name(self.annotations["return"]),
            name=self.name,
            args=", ".join(arg_defs),
            specs=self._get_specs(),
            o="{",
        )
        printer.incr_indent()
        for s in self.statements:
            s.print_func(printer)
        printer.decr_indent()
        printer.print("}}")
