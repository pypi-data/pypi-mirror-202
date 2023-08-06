# Universal Date Parser

an universal date parser for python, which can parse date string from different formats and localization (including
Excel dates) into datetime object and more.

## Installation

### via Github

```bash
pip install git+https://github.com/guangyu-he/universal_date_parser
```

### via PyPI

```bash
pip install universal-date-parser
```

## Usage

- initializing parser instance
- use method to get the result

## Arguments

- **date_in_str**: the date string to be parsed
- **date_format** (optional): the format of the date string, default is "guess", which means it will guess the format
    - "guess": guess the format
    - others: date formats supported by datetime.strptime()
- **locale** (optional): the locale of the date string, default is None, which means it will guess the localization
  format

## Methods

- **to_datetime**(): return datetime object
- **to_date**(): return date object
- **to_time**(): return time object
- **to_date_str**(_date_format_): return date string, by default, the format is "YYYY-MM-DD"
- **to_str**(_date_format_): return the date time string, by default, the format is "YYYY-MM-DD HH:MM:SS"
- **to_timestamp**(): return the timestamp object

## Examples

```python
from universal_date_parser import DateParser

date_string = "06/07/1995"
a = DateParser(date_string, locale="de_DE")
print(a.to_date_str())
# >>> 1995-07-06
print(a.to_str())
# >>> 1995-07-06 00:00:00
print(a.to_date_str(date_format="%d.%m.%Y"))
# >>> 06.07.1995

date_string = "06/07/1995"
a = DateParser(date_string, locale="en_US")
print(a.to_date_str())
# >>> 1995-06-07

date_string = "06/07/1995"
a = DateParser(date_string, date_format="%d/%m/%Y")
print(a.to_date_str())
# >>> 1995-07-06

date_string = "Jun/06/1995"
a = DateParser(date_string)
print(a.to_date_str())
# >>> 1995-06-06

date_string = "06/Juni/1995"
a = DateParser(date_string, locale="de_DE")
print(a.to_date_str())
# >>> 1995-06-06
```

## Updates Log

### v0.0.1

#### initial upload

- first version

### v0.0.2

#### update

- description and setup updates

### v0.0.2.1

#### bug fix

- fix long desc error in setup.py while installing 

## Support

feel free to check source code in <a href="https://github.com/guangyu-he/universal_date_parser">GitHub</a>, you are
welcome
to leave any comments.

2022&copy;Guangyu He, for further support please contact author. <br>
Email: <a href="mailto:me@heguangyu.net">me@heguangyu.net</a>
