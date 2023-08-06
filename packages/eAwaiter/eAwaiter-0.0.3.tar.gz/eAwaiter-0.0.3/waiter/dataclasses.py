"""
eAsistentUser
=============

eAsistentUser class is used for creating and accessing uer's data.
For examples and in depth usage, take a look at our documentation.
<https://dasadweb.com/documentation/eAwaiter>
"""

from dataclasses import dataclass
from datetime import datetime

@dataclass
class eAsistentUser():
    """
    username, password => user's eAsistent credentials
    disliked_foods, favourite_foods => 
        array of foods (str spelled exactly as in eAsistent)
    preferred_menu, default_menu =>
        integers of menu options
        0 = odjava (sign off)
        1-6 = meal options

        1 ... Topli Mesni
        2 ... Topli Brezmesni
        3 ... Hladni Mesni
        4 ... Hladni Brezmesni
        5 ... Solatni
        6 ... Šport
    overwrite_unchangable =>
        user is unable to change meals < 7 days in advance
        when True:
            this option will try to change even if < 7 days in advance
    """
    username: str
    password: str

    disliked_foods: list
    favourite_foods: list

    preferred_menu: int
    default_menu: int

    overwrite_unchangable: bool

@dataclass
class eAsistentMeal():
    """
    meal_text => contents of meal
    meal_id => id of meal (not same as eAsistentUser menu)
    date => date of menu
    changable => true if > 8 days in advance
    selected => true if meal selected
    """
    meal_text: str
    meal_id: str
    date: datetime
    changable: bool
    selected: bool

"""
Created By:

|~| ._ _'|
_)|<| (_ |
"""

