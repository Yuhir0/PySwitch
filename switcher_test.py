import unittest
from .switcher import Switch, Default, DuplicatedCaseException


class SwitchTest(unittest.TestCase):

    def test_01_correct_case(self):
        @Switch(1)
        def switch(s):
            @s.case(1)
            def one():
                return 1

        self.assertEqual(switch(), 1)

    def test_02_default_value(self):
        @Switch(2)
        def switch(s):
            @s.case(1)
            def one():
                return 1

        self.assertEqual(switch(), None)

    def test_03_custom_default(self):
        @Switch(2)
        def switch(s):
            @s.case(1)
            def one():
                return 1

            @s.case(Default)
            def default():
                return 0

        self.assertEqual(switch(), 0)

    def test_04_duplicated_case_exception(self):
        @Switch(2)
        def switch(s):
            @s.case(1)
            def one():
                return 1

            @s.case(1)
            def one2():
                return 1

        with self.assertRaises(DuplicatedCaseException):
            switch()


if __name__ == '__main__':
    unittest.main()
