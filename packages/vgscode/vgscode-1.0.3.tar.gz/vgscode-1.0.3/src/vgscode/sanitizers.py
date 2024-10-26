def sNumberToString(input_value):
    if isinstance(input_value, (int, float)):
        return str(input_value)
    elif isinstance(input_value, str):
        return input_value
    else:
        raise TypeError(f"Expected a 'string'/number but received a {type(input_value).__name__}")

def sTrimStart(input_str):
    i = 0
    while i < len(input_str) and input_str[i].isspace():
        i += 1
    return input_str[i:]

def sTrimEnd(input_str):
    i = len(input_str) - 1
    while i >= 0 and input_str[i].isspace():
        i -= 1
    return input_str[:i + 1]

def sTrimBoth(input_str):
    start = 0
    while start < len(input_str) and input_str[start].isspace():
        start += 1
    
    str_no_leading = input_str[start:]
    
    end = len(str_no_leading) - 1
    while end >= 0 and str_no_leading[end].isspace():
        end -= 1
    
    return str_no_leading[:end + 1]

#https://blog.stevenlevithan.com/archives/faster-trim-javascript

def sTrimAll(input_str):
    return ''.join(input_str.split())

def sRemoveNonDigits(input_str):
    return ''.join(char for char in input_str if char.isdigit())