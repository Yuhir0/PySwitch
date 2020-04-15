import unittest
from switcher import Switch, Default, DuplicatedCaseException


def switch_func(options: int):
    @Switch(options)
    def switch(s):
        @s.case(1)
        def one():
            return 1
    return switch()


def switch_with_default(options: int):
    @Switch(options)
    def switch(s):
        @s.case(Default)
        def default():
            return 0
    return switch()


class SwitchTest(unittest.TestCase):
    def test_01_correct_case(self):
        self.assertEqual(switch_func(1), 1)

    def test_02_default_value(self):
        self.assertEqual(switch_func(2), None)

    def test_03_custom_default(self):
        self.assertEqual(switch_with_default(1), 0)

    def test_04_duplicated_case_exception(self):
        @Switch(2)
        def switch(s):
            @s.case(1)
            def one():
                """ Do nothing """

            @s.case(1)
            def one2():
                """ Do nothing """

        with self.assertRaises(DuplicatedCaseException):
            switch()
