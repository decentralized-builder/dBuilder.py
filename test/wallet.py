import unittest

from dbuilder import Engine
from dbuilder.func.contract import Contract
from dbuilder.types import Slice


class SimpleWallet(Contract):
    def external_receive(
        self,
        in_msg: Slice,
    ) -> None:
        super(SimpleWallet, self).external_receive(
            in_msg,
        )
        signature = in_msg.load_bits_(512)
        cs = in_msg
        msg_seqno = cs.load_uint_(32)
        valid_until = cs.load_uint_(32)
        self.throw_if(35, valid_until <= self.now())
        ds = self.get_data().begin_parse()
        stored_seqno = ds.load_uint_(32)
        public_key = ds.load_uint_(256)
        ds.end_parse()
        self.throw_unless(33, msg_seqno == stored_seqno)
        self.throw_unless(
            34,
            self.check_signature(
                self.slice_hash(in_msg),
                signature,
                public_key,
            ),
        )
        self.accept_message()
        cs.touch_()
        self.begin_cell().store_uint(1, 23).store_uint(1, 43).end_cell()


class CompileTestCase(unittest.TestCase):
    def test_compile(self):
        t = Engine.patched(SimpleWallet)
        compiled = Engine.compile(t)
        print(compiled.to_func())


if __name__ == "__main__":
    unittest.main()
