from .color import color
from .logger import log

def changelogs():
# Log the latest update version
    log(f"{color('Lumtina', 'red')} Latest Update: 0.2.2")

# Log the changes made in this version
    log(f'''{color('Lumtina', 'red')} Added:
 [ + ] Added Math Functions (add, subtract, multiply, divide, power, factorial, is_even, is_odd)
 [ + ] Modified the README
 [ - ] Fixed Bugs
    ''')

    log(f"{color('Lumtina', 'red')} Previous Update 0.2.1")

# Log the changes made in this version
    log(f'''{color('Lumtina', 'red')} Added:
 [ + ] Added ascii converter
 [ - ] Fixed Bugs
    ''')





