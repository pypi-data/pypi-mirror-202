import base64


def save_b64_string_as_pdf(b64_string, filename='tmp.pdf'):
    with open(filename, 'wb') as f:
        f.write(base64.b64decode(b64_string))
        print(f'Saved base64 content to: {filename}')


if __name__ == '__main__':
    b64_str = 'JVBERi0xLjQKJeLjz9MKNCAwIG9iago8PC9MZW5ndGggNjIyL0ZpbHRlci9GbGF0ZURlY29kZT4+c3RyZWFtCnicnZXNbtpAEMdXP' \
              'fopRuolqZrN7vpj19woHxGpcBK8lCTKxQIHXIEJBpRjH6BSH7GP0VulzhoHCCHBja2Vd2bH/994mF1m1gw49XxgeONEgm1T3wfOfer' \
              '60J/A6fU9h/oUrqwra2Z90RYDoWzqgh5YDZ07zRBwjitnOMcQvpIDrijjIFyP2g7oiXXaRB8DfY/hOrMYtc0FjxbLX+icFZNsaB2' \
              'FcToAPa0c6+/oHeIwbyCBYzyCD2MdhzLxhPW3qfuJQbXdgAr0oiR9zJLhaAHtKOvH0RK+RovROI7TvbnsUG23oL4Nq9bryBIKevF8' \
              'ATfTZTqEzqAMQHilALWWvkFCLRonD9EiS6Iy2lyW0g51VZtS1aplRJkql/BFN9Adk3M3aOlGHXJK+J7fnwnq44Nz08NFA6itBhCeh' \
              '52+N4umwx0mBOOCM7xq78HL/INdTn31jH6YckDYo7gzlUMlf0X3NnnA+vlC2HZJSVtRwVeir2hejqZpjKp3R67D745Bus6JSbocwMe' \
              'OcjFzPAKKYohdAOmSgLSIJg1SJ0BCnFVzK0QLfvz69rfktwhzzDhqfdgIdO2gmih8S9o4rlHcCSv/I62ocp+U5Y7wJcnIlAzIkvTJA' \
              'qUDEpEJiXFWwVEjI1xPyBzXJrgyR98UPWkRlaLf+DiB3sefv/sfgj/kM7nYicjXg0+Emnsr8U0bU8mUdLFDsbeok/cgswF3nhRUycIc' \
              'W+HLSLPz+SZyZe5GcsptIyIdE7kysSlfSKIG9zaBK3Md+EadhVBmywq57hb0ec9L3Q23P30NXRfBNf9iQkqqbCjQJ8UzixH/D5tUaYk' \
              'KZW5kc3RyZWFtCmVuZG9iago2IDAgb2JqCjw8L1R5cGUvUGFnZS9NZWRpYUJveFswIDAgMjgzLjUgMjgzLjVdL1Jlc291cmNlczw8L' \
              '0ZvbnQ8PC9GMSAxIDAgUi9GMiAzIDAgUj4+L1hPYmplY3Q8PC9YZjEgMiAwIFI+Pj4+L0NvbnRlbnRzIDQgMCBSL1BhcmVudCA1IDA' \
              'gUj4+CmVuZG9iagoxIDAgb2JqCjw8L1R5cGUvRm9udC9TdWJ0eXBlL1R5cGUxL0Jhc2VGb250L0hlbHZldGljYS9FbmNvZGluZy9Xa' \
              'W5BbnNpRW5jb2Rpbmc+PgplbmRvYmoKNyAwIG9iago8PC9UeXBlL0ZvbnREZXNjcmlwdG9yL0FzY2VudCA4ODAvQ2FwSGVpZ2h0IDg' \
              '4MC9EZXNjZW50IC0xMjAvRmxhZ3MgNi9Gb250QkJveCBbLTI1IC0yNTQgMTAwMCA4ODBdL0ZvbnROYW1lL1NUU29uZy1MaWdodC9JdG' \
              'FsaWNBbmdsZSAwL1N0ZW1WIDkzL1N0eWxlPDwvUGFub3NlKAEFAgIEAAAAAAAAACk+Pj4+CmVuZG9iago4IDAgb2JqCjw8L1R5cGU' \
              'vRm9udC9TdWJ0eXBlL0NJREZvbnRUeXBlMC9CYXNlRm9udC9TVFNvbmctTGlnaHQvRm9udERlc2NyaXB0b3IgNyAwIFIvVyBbMVsy' \
              'MDddMTNbMjM4XTE1WzIzOF0xOFs0NjJdMjFbNDYyXTI3WzIzOF0zNFs2ODRdMzZbNjk1IDczOSA1NjMgNTExXTQyWzMxOF00Nls4O' \
              'TYgNzU4IDc3MiA1NDRdNTJbNDY1IDYwNyA3NTNdNTdbNjQ3XTU5WzYwN102Nls0MTddNjhbNDI3IDUyOSA0MTVdNzNbNTE4IDI0MV0' \
              '3OFs3OTMgNTI3IDUyNF04M1szMzggMzM2IDI3NyA1MTddXS9EVyAxMDAwL0NJRFN5c3RlbUluZm88PC9SZWdpc3RyeShBZG9iZSkvT' \
              '3JkZXJpbmcoR0IxKS9TdXBwbGVtZW50IDQ+Pj4+CmVuZG9iagozIDAgb2JqCjw8L1R5cGUvRm9udC9TdWJ0eXBlL1R5cGUwL0Jhc2' \
              'VGb250L1NUU29uZy1MaWdodC1VbmlHQi1VQ1MyLUgvRW5jb2RpbmcvVW5pR0ItVUNTMi1IL0Rlc2NlbmRhbnRGb250c1s4IDAgUl0+' \
              'PgplbmRvYmoKMiAwIG9iago8PC9UeXBlL1hPYmplY3QvU3VidHlwZS9Gb3JtL1Jlc291cmNlczw8Pj4vQkJveFswIDAgMTI0LjggMj' \
              'RdL0Zvcm1UeXBlIDEvTWF0cml4IFsxIDAgMCAxIDAgMF0vTGVuZ3RoIDE4OC9GaWx0ZXIvRmxhdGVEZWNvZGU+PnN0cmVhbQp4nI1S' \
              'OxKEIAztPYUnyCQhBDjQrr33L1aEGcyz2bHQF3yfJPDO13MeW38J+a62n59NyfoB1Ynt+nriClg00MXjaSEoNOqE7jL9hmG6yrPgd2' \
              'FJJoZIKYFoyhRTpOHy6IIhtkUPKxAro2nWW2FRskdYIbYLxT/cgoPHQIWBX9CwRLnSoOmKhtVAocIq201Yo29jsCtjc9w2M+AEKYQz' \
              'rpxfd0YEWWLQvsgY6AojKqisL3ed9/VP/N1+1UeYagplbmRzdHJlYW0KZW5kb2JqCjUgMCBvYmoKPDwvVHlwZS9QYWdlcy9Db3VudC' \
              'AxL0tpZHNbNiAwIFJdPj4KZW5kb2JqCjkgMCBvYmoKPDwvVHlwZS9DYXRhbG9nL1BhZ2VzIDUgMCBSPj4KZW5kb2JqCjEwIDAgb2Jq' \
              'Cjw8L1Byb2R1Y2VyKCkvQ3JlYXRpb25EYXRlKEQ6MjAyMDEyMTAxNjE1NTcrMDgnMDAnKS9Nb2REYXRlKEQ6MjAyMDEyMTAxNjE1N' \
              'TcrMDgnMDAnKT4+CmVuZG9iagp4cmVmCjAgMTEKMDAwMDAwMDAwMCA2NTUzNSBmIAowMDAwMDAwODUxIDAwMDAwIG4gCjAwMDAwMDE' \
              '2MTEgMDAwMDAgbiAKMDAwMDAwMTQ4NyAwMDAwMCBuIAowMDAwMDAwMDE1IDAwMDAwIG4gCjAwMDAwMDE5NTcgMDAwMDAgbiAKMDAw' \
              'MDAwMDcwNCAwMDAwMCBuIAowMDAwMDAwOTM5IDAwMDAwIG4gCjAwMDAwMDExMzAgMDAwMDAgbiAKMDAwMDAwMjAwOCAwMDAwMCBuIA' \
              'owMDAwMDAyMDUzIDAwMDAwIG4gCnRyYWlsZXIKPDwvU2l6ZSAxMS9Sb290IDkgMCBSL0luZm8gMTAgMCBSL0lEIFs8MGU3NjJlNjY' \
              '1YWEzZGEyNjA4MTBlZjAyMTJiNjVmNGY+PDBlNzYyZTY2NWFhM2RhMjYwODEwZWYwMjEyYjY1ZjRmPl0+PgolLQpzdGFydHhyZWYKM' \
              'jE1NgolJUVPRgo='
    save_b64_string_as_pdf(b64_str)
