# imports for ref_number_generator
from random import choice
from string import digits, ascii_uppercase
from datetime import date


def anonymous_ref_number_generator():
    date_str = date.today().strftime('%d%m%y')
    random_str = "".join([choice(digits) for x in range(2)]) + \
        "".join([choice(ascii_uppercase) for x in range(2)])
    return "UN{}-{}".format(date_str, random_str)


def ref_number_generator():
    date_str = date.today().strftime('%d%m%y')
    random_str = "".join([choice(ascii_lowercase) for x in range(2)]) + \
        "".join([choice(digits) for x in range(2)])
    return "VA{}-{}".format(date_str, random_str)
