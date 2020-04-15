"""
Switch

To implements switch case statement

Example:
>>> def foo(option: int) -> str:
>>>    @Switch(option)
>>>    def switcher(switch):
>>>        @switch.case(1)
>>>        def one():
>>>            return "One"
>>>
>>>        @switch.case(2)
>>>        def two():
>>>            return "Two"
>>>
>>>        @switch.case(Default)
>>>        def default():
>>>            return "Not is one or two"
>>>
>>>    return switcher()
>>>
>>>
>>> foo(1)
>>> One
>>> foo(2)
>>> Two
>>> foo(3)
>>> Not one or two
"""

import functools
from typing import Callable, Any, Dict, cast

AnyFunc = Callable[[], Any]
Cases = Dict[Any, AnyFunc]
SwitchFunc: type = Callable[[Any], AnyFunc]


class SwitchException(Exception):
    """ Bse Switch exception """


class DuplicatedCaseException(SwitchException):
    """ Error for cases when are duplicated """


class Default:
    """ Used to default case """

    @staticmethod
    def do_nothing() -> None:
        """ Do nothing """


class Switch:
    """ Decorator imitates switch case in other languages.
    Giving a value and returning the case or default

    :param value: any object to compare in the cases
    :return AnyFunc: function that resolve the case
    """
    def __init__(self, value: Any):
        self.value = value
        self.cases: Cases = dict()

    def __call__(self, func: SwitchFunc) -> AnyFunc:

        @functools.wraps(func)
        def with_switch(*args, **kwargs) -> AnyFunc:
            args = args + (self,)
            func(*args, **kwargs)
            return self._resolve()
        return with_switch

    def case(self, case_value: Any) -> Callable[[AnyFunc], AnyFunc]:
        """ Case for a switch case statement,
        Giving a "case" value and a to add this case to the group

        :param case_value:
        :return: returns a Callable of each case
        """
        def decorator(func: AnyFunc) -> AnyFunc:
            """
            :param func: Execution function for the case
            :return AnyFunc: func
            :raise CaseError: When have a duplicated case
            """
            if case_value in self.cases.keys():
                raise DuplicatedCaseException(f"Case must be unique. '{case_value}' is duplicated")
            self.cases[case_value] = func
            return func

        return decorator

    def _resolve(self) -> AnyFunc:
        """ Resolve the case for that situation.

        :return AnyFunc: the Callable for this case
        """
        return self.cases.get(
            self.value,
            self.cases.get(Default, Default.do_nothing)
        )()
