from urllib import request, parse

data = parse.urlencode({ 'text': 'hello' }).encode()
req = request.Request("http://<address>:<port>/v1/sender/<token>", data=data)
request.urlopen(req)

