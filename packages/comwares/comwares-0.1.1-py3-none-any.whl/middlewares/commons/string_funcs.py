import re


def camel_to_snake(text: str):
    s = ''
    for letter in text:
        if letter.isupper():
            s += '_' + letter.lower()
        else:
            s += letter
    return s


if __name__ == '__main__':

    t = 'emRatingCode'
    print(camel_to_snake(t))
