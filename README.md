# PySwitch
Switch case statemant for Python 3

## Usage example
```python
def foo(option: int) -> str:
    @Switch(option)
    def switcher(switch):
        @switch.case(1)
        def one():
            return "One"

        @switch.case(2)
        def two():
            return "Two"

        @switch.case(Default)
        def default():
            return "Not is one or two"

    return switcher()


foo(1)
>>> One
foo(2)
>>> Two
foo(3)
>>> Not one or two
```
