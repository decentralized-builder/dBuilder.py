import unittest

from dbuilder import Engine
from dbuilder.func.contract import Contract
from dbuilder.types import Slice


class Arithmetics(Contract):
    def external_receive(
        self,
        in_msg: Slice,
    ) -> None:
        super(Arithmetics, self).external_receive(
            in_msg,
        )
        v = in_msg.load_uint_(8)
        _ = v + 2
        _ = v / 2
        _ = v - 2
        _ = v * 2
        _ = 2 + v
        _ = 2 / v
        _ = 2 - v
        _ = 2 * v
        _ = ~v
        _ = -v
        _ = v <= 2
        _ = v < 2
        _ = v > 2
        _ = v >= 2
        _ = v == 2
        _ = v != 2
        _ = v | 2
        _ = v & 2
        _ = 2 | v
        _ = 2 & v


class CompileTestCase(unittest.TestCase):
    def test_compile(self):
        t = Engine.patched(Arithmetics)
        compiled = Engine.compile(t)
        print(compiled.to_func())


if __name__ == "__main__":
    unittest.main()
