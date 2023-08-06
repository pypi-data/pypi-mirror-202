special_chars = {
    "b'\\t'": '\t',
    "b'\\r'": '\n',
    "b'\\x07'": '|',
    "b'\\xc4'": 'Ä',
    "b'\\xe4'": 'ä',
    "b'\\xdc'": 'Ü',
    "b'\\xfc'": 'ü',
    "b'\\xd6'": 'Ö',
    "b'\\xf6'": 'ö',
    "b'\\xdf'": 'ß',
    "b'\\xa7'": '§',
    "b'\\xb0'": '°',
    "b'\\x82'": '‚',
    "b'\\x84'": '„',
    "b'\\x91'": '‘',
    "b'\\x93'": '“',
    "b'\\x96'": '-',
    "b'\\xb4'": '´',
    "b' '": " ",
    "b'.'": ".",
    "b':'": ":",
    "b'/'": "/"
}


def get_string(path):
    string = ''
    with open(path, 'rb') as stream:
        stream.seek(2560) # Offset - text starts after byte 2560
        current_stream = stream.read(1)
        while not (str(current_stream) == "b'\\xfa'"):
            #print(str(current_stream))
            if str(current_stream) in special_chars.keys():
                string += special_chars[str(current_stream)]
                #print(str(current_stream) ,special_chars[str(current_stream)])
            else:
                try:
                    char = current_stream.decode('UTF-8')
                    if char.isalnum():
                        string += char
                except UnicodeDecodeError:
                    string += ''
            current_stream = stream.read(1)
    return string