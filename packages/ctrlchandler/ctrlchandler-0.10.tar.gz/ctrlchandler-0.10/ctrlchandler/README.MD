# Like atexit but for ctrl+c

### Tested against Windows 10 / Python 3.10 / Anaconda 

## pip install ctrlchandler


```python
# atexit
import atexit
def printx(bu=12, ba=3223):
    print(bu, ba)
    print('ciao')
atexit.register(printx, bu='nice', ba='ba')
exit()
nice ba
ciao
Process finished with exit code 0
```

```python
from ctrlchandler import set_console_ctrl_handler


def printx(bu=12, ba=3223):
    print(bu, ba)
    print('ciao')


set_console_ctrl_handler(returncode=1, func=printx, bu=12011, ba=32231111)
while True:
    pass


After pressing ctrl+c
^C12011 32231111
ciao
Process finished with exit code 1
```