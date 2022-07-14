from typing import List

from dbuilder.ast import IfFlow, Contract, Method, Node, Statement


class CallStacks(object):
    contracts = {}
    calls: List = []
    functions = set()
    __instance = None
    current_contract: Contract = None

    @staticmethod
    def get_instance() -> "CallStacks":
        if CallStacks.__instance is None:
            CallStacks()
        return CallStacks.__instance

    def __init__(self):
        if CallStacks.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            CallStacks.__instance = self

    @staticmethod
    def add(call):
        CallStacks.get_instance().calls.append(call)
        return len(CallStacks.get_instance().calls) - 1

    @staticmethod
    def insert(call, pos=-1):
        if pos == -1:
            CallStacks.add(call)
            return
        CallStacks.get_instance().calls.insert(pos, call)

    @staticmethod
    def get_stack() -> str:
        x = ""
        for call in CallStacks.get_instance().calls:
            x += str(call) + "\n"
        return x

    @staticmethod
    def declare_contract(name):
        CallStacks.current_contract = Contract(name)
        CallStacks.contracts[name] = CallStacks.current_contract

    @staticmethod
    def get_contract(name):
        return CallStacks.contracts[name]

    @staticmethod
    def declare_method(name, args):
        m = Method(name, args)
        CallStacks.current_contract.add_method(m)

    @staticmethod
    def add_statement(type, *args):
        s = Statement(type, args)
        CallStacks.current_contract.add_statement(s)
        return s.node_id()

    @staticmethod
    def return_(entity):
        CallStacks.add_statement(Statement.RETURN, entity)

    @staticmethod
    def end_method(method):
        CallStacks.current_contract.end_method(method)

    @staticmethod
    def begin_if(cond):
        nif = IfFlow()
        nif.iff(cond)
        CallStacks.current_contract.add_statement(nif)
        return nif.node_id()

    @staticmethod
    def else_if(id, cond=None):
        nif: IfFlow = Node.find(id)
        if cond:
            nif.iff(cond)
        else:
            nif.else_()

    @staticmethod
    def end_if(id):
        nif: IfFlow = Node.find(id)
        CallStacks.current_contract.current_method.end_statement(nif)

    @staticmethod
    def call_(name, *args, operand=None):
        if operand:
            CallStacks.add_statement(
                Statement.METHOD_CALL, name, operand, *args)
        else:
            CallStacks.add_statement(Statement.FUNC_CALL, name, *args)