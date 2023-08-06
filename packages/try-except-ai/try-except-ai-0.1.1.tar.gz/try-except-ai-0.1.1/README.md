# TryExceptAI

A Python package to handle exceptions and suggest resolutions using OpenAI.

## Installation

Install the package using [Poetry](https://python-poetry.org/):

```bash
poetry add try-except-ai
```

## Usage
Add `export OPENAI_API_KEY={your openai api key here}` to your .zshrc or .bash_profile file.

Then test it with the following

```python
from try_except_ai import TryExceptAI

def test_function():
    try:
        # Code that might raise an exception
        result = 1 / 0
        print(result)
    except Exception as e:
        TryExceptAI().handle_exception(e)

if __name__ == "__main__":
    test_function()

```

## License
This project is licensed under the MIT License. See the LICENSE file for details.

