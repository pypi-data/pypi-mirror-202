from typing import Union
from pathlib import Path

def toString(path:Union[Path,str])->str:    
    if not(path.endswith(".doc")):
        raise TypeError("must be .doc file")
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
                "b'\\x95'": '-',
                "b' '": " ",
                "b'.'": ".",
                "b':'": ":",
                "b'/'": "/",
                "b'('": "(",
                "b')'": ")",
            }
    return _get_string(special_chars,path)

def _get_string(special_chars:dict,path:Union[Path,str])->str:
            string = ''
            with open(path, 'rb') as stream:
                stream.seek(2560) # Offset - text starts after byte 2560
                current_stream = stream.read(1)
                while not (str(current_stream) == "b'\\xfa'"):
                    if str(current_stream) in special_chars.keys():
                        string += special_chars[str(current_stream)]
                    else:
                        try:
                            char = current_stream.decode('UTF-8')
                            if char.isalnum():
                                string += char
                        except UnicodeDecodeError:
                            string += ''
                            print(str(current_stream))
                    current_stream = stream.read(1)
                return string