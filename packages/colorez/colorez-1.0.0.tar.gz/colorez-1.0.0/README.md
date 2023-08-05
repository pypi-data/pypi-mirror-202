# colorez

Simple addition of color to the builtin print and input functions

## Installation

Simply run `pip install colorez`. The PyPI package is at https://pypi.org/project/colorez/

## Example Usage

```python
from colorez import color_print, Color, color_input

color_print("This is red", color="red")
color_print("This is gold", color=178, end="\t")
color_print("This is pink", color="#ed0ecc")

print(Color("hi", 23, ["1", "2"], color="blue"), Color(0, 0, 255, color="blue"))
print("No color", Color(1, 2, 3, color="green"), "\t", Color("hello", color="orange"))

color_input(">", color="yellow")
```

![](https://github.com/CodingYuno/colorez/blob/main/example.png)
