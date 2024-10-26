# colortruck


## Examples of How To Use 

Create intput with green prompt and output with blue

```python
from colortruck import Truckcolors

clt=Truckcolors()
a=input(clt.GREEN+'Input something: ')
print(clt.BLUE+"Hello beatyfull truck")
# clt.reset can be added or not. after the program ends, your terminal will be reset in color.
print(clt.RESET)

# There are many other colors waiting for you to discover.

```
If you are going to convert python code to .exe you should add exe_cover()
```python
from colortruck import Truckcolors


clt=Truckcolors()
clt.exe_cover()
a=input(clt.GREEN+'Input something: ')
print(clt.BLUE+"Hello beatyfull truck")
print(clt.RESET)
```

