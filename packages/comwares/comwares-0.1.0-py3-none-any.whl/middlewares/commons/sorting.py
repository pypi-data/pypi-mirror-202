import json


def sort_nested_dict(d: dict, key: str):
    res = sorted(d.items(), key=lambda x: x[1][key])
    return res


if __name__ == '__main__':

    from pprint import pprint

    d = {
        '500192': {'price': 12.19, 'diff': -2.5},
        '600381': {'price': 10.19, 'diff': -1.5},
        '128178': {'price': 15.19, 'diff': -0.5},
        '129812': {'price': 12.69, 'diff': 1.5},
    }

    pprint(sort_nested_dict(d, key='diff'))
