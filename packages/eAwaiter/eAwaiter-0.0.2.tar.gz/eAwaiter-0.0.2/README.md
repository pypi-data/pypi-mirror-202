![eAwaiter banner](https://github.com/5KRC1/5KRC1/blob/main/images/eAwaiter/eAwaiter-banner.png "eAwaiter banner")
# eAwaiter
eAwaiter is a Python package that can change your eAsistent meals automatically.

## Description
eAwaiter is supposed to help with changing meals in eAsistent. Meals are "changable" only 7 days in advance. Therefore, waiter's service looks for any disliked foods and favourite foods and changes meals few weeks in future. I can also help manually changing meals and more.

eAwaiter's service (and more) is used in [eAmenu](https://github.com/5KRC1/eAmenu) android app.

## Install & Run
If you are changing the code or using it locally, you can easily install and run it with the following commands:
- Clone the project
```bash
git clone https://github.com/5KRC1/eAwaiter && cd eAmenu
```
- Setup Python venv
```bash
python -m venv env && source env/bin/activate
```
- Install dependencies
```bash
pip install -r requirements.txt
```
- Run the example provided under "Usage"
```bash
python examples/example.py
```

## Usage
install with pip
```bash
pip install git+https://github.com/5KRC1/eAwaiter.git
```

examples:
- service
```python
from waiter.waiter import Waiter

# Init Waiter
username = "__your_username__"
password = "__your_password__"

default_menu = "1"
preferred_menu = "2"
favourite_foods = ["pica", "špageti"]
disliked_foods = ["Cheder", "hrenovko", "osličev", "oslič"]
overwrite = False

waiter = Waiter(
  username=username,
  password=password,
  default_menu=default_menu,
  favourite_foods=favourite_foods,
  disliked_foods=disliked_foods,
  preferred_menu=preferred_menu,
  orevwrite_unchangable=overwrite
)

# Run service
waiter.service()
```

- get meals
```python
from waiter.waiter import Waiter

# Init Waiter
username = "__your_username__"
password = "__your_password__"

waiter = Waiter(
  username=username,
  password=password
)

# Get meals
meals = waiter.get_meals()
```

- change a meal
```python
from datetime import datetime
from waiter.waiter import Waiter

# Init Waiter
username = "__your_username__"
password = "__your_password__"

waiter = Waiter(
  username=username,
  password=password
)

action = "prijava"
meal_id = "__meal_id__"
date = datetime(2023, 3, 29)  # (year, month, day)

# Change a meal
changed = waiter.prijava_odjava(
  action=action,
  meal_id=meal_id,
  date=date
)
```

For more information check out the documentation [here](https://dasadweb.com/documentation/eAwaiter).

## Contribute
