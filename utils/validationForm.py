
import re


def validationEmail(email):
    return re.match("[^@]+@[^@]+\.[^@]+", email) is not None
