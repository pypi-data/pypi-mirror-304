# What is it?

textextent is a Python library for customizing print statements in a different variety of ways.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

```bash
pip install textextent
```

## Usage

```python
import textextent

# prints out "Hello World! This is a test sentence!" in the color blue while also being bolded.
textextent.colorPrint("Hello World! This is a test sentence!", "Blue", "Bold")

# prints out "Hello World! This is a test sentence!" in a rainbow pattern.
textextent.colorPrint("Hello World! This is a test sentence!", "Rainbow")

# prints out "Hello World! This is a test sentence!" while under a typewriter effect.
textextent.typewritePrint("Hello World! This is a test sentence!")

```

## License

[MIT](https://choosealicense.com/licenses/mit/)