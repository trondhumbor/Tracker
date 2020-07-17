

def _parse_method(s):
    return {
        b"i": _parse_integer,
        b"l": _parse_list,
        b"d": _parse_dictionary
    }.get(s, _parse_bstring)

def _parse_bstring(data, idx):
    colon = data.index(b":", idx)
    length = int(data[idx:colon].decode("utf-8"))
    baseOffset = colon + 1
    bstring = bytes(data[baseOffset:baseOffset + length])
    return bstring, baseOffset + length

def _parse_integer(data, idx):
    length = 0
    while data[idx + 1 + length] != ord(b"e"):
        length += 1
    baseOffset = idx + 1
    integer = int(data[baseOffset:baseOffset+length])
    return integer, baseOffset + length + 1

def _parse_list(data, idx):
    lst = []
    idx += 1
    while data[idx] != ord(b"e"):
        char = data[idx:idx+1]
        value, idx = _parse_method(char)(data, idx)
        lst.append(value)
    return lst, idx + 1

def _parse_dictionary(data, idx):
    dct = {}
    idx += 1
    while data[idx] != ord(b"e"):
        key, idx = _parse_bstring(data, idx)
        char = data[idx:idx + 1]
        value, idx = _parse_method(char)(data, idx)
        dct[key] = value
    return dct, idx + 1

def bdecode(data):
    char = data[0:1]
    return _parse_method(char)(data, 0)[0]

if __name__ == "__main__":
    print(bdecode(b"d3:cow3:moo4:spam4:eggse"))
    print(bdecode(b"d4:spaml1:a1:bee"))
    print(bdecode(b"l4:blahi1234e4:spame"))
    print(bdecode(b"4:blah"))
    print(bdecode(b"i1234e"))
