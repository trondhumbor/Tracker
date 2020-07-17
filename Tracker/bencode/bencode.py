
def _parse_method(s):
    if type(s) in (bytes, str):
        return _encode_bstring
    elif type(s) == int:
        return _encode_integer
    elif type(s) == list:
        return _encode_list
    elif type(s) == dict:
        return _encode_dictionary

    raise ValueError("Couldn't bencode type {}".format(type(s)))

def _encode_bstring(data):
    if type(data) == str:
        data = data.encode("utf-8")
    return str(len(data)).encode("utf-8") + b":" + data

def _encode_integer(data):
    return b"i" + str(data).encode("utf-8") + b"e"

def _encode_list(data):
    return b"l" + b"".join(_parse_method(value)(value) for value in data) + b"e"

def _encode_dictionary(data):
    return b"d" + b"".join(_encode_bstring(k) + _parse_method(v)(v) for k, v in data.items()) + b"e"

def bencode(data):
    return _parse_method(data)(data)

if __name__ == "__main__":
    print(bencode({"failure reason": "Not enough query parameters provided"}))
    print(bencode({b'cow': b'moo', b'spam': b'eggs'}))
    print(bencode({b'spam': [b'a', b'b']}))
    print(bencode([b'blah', 1234, b'spam']))
    print(bencode(b'blah'))
    print(bencode(1234))
