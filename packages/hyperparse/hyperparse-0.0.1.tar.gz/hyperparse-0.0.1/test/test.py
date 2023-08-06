import unittest
import sys
import os
import argparse
sys.path.append(".")

class TestHyperParse(unittest.TestCase):

    def test_basic(self):
        os.environ["usermode"] = "a=1,b,c=[1,2,3],d=4,e=3.2,f=itud,g=False"
        from hyperparse import usermode
        self.assertDictEqual(usermode, {'a': 1, 'b': None, 'c': [1, 2, 3], 'd': 4, 'e': 3.2, 'f': 'itud', 'g': False})

    def test_argparse(self):
        os.environ["usermode"] = "a=1,b,c=[1,2,3],d=4,e=3.2,f=itud,g=False"
        from hyperparse import usermode, set_hyper
        parser = argparse.ArgumentParser()
        parser.add_argument('--a', type=int, default=5)
        parser.add_argument('--f', type=str, default="hello")
        args = parser.parse_args()
        set_hyper(usermode, args)
        self.assertEqual(args.a, 1)
        self.assertEqual(args.f, "itud")

    def test_func(self):
        os.environ["usermode"] = "a=1,b,c=[1,2,3],d=4,e=3.2,f=itud,g=False"
        from hyperparse import usermode, set_hyper
        a = 5
        f = "stk"
        set_hyper(usermode)
        self.assertEqual(a, 1)
        self.assertEqual(f, "itud")

    def test_func_strname(self):
        os.environ["usermode"] = "a=1,b,c=[1,2,3],d=4,e=3.2,f=itud,g=False"
        from hyperparse import set_hyper
        a = 5
        f = "stk"
        set_hyper("usermode")
        self.assertEqual(a, 1)
        self.assertEqual(f, "itud")

if __name__ == '__main__':
    unittest.main()