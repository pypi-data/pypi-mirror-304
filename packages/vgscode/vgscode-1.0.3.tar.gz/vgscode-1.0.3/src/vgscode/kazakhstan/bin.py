def gBIN(str_input=""):
    if str_input:
        str_input = str(str_input) if isinstance(str_input, (int, float)) else str_input
        
        if not isinstance(str_input, str) or len(str_input) > 11 or not str_input.isdigit():
            raise ValueError("Input value must be a 'string'/number of 0 to 11 digits")
        
        if len(str_input) >= 4:
            month = int(str_input[2:4])
            if month < 1 or month > 12:
                raise ValueError("The 3rd and 4th digits must represent a valid month (01-12)")
        
        if len(str_input) >= 5:
            fifth_digit = int(str_input[4])
            if fifth_digit not in [4, 5, 6]:
                raise ValueError("The 5th digit must be 4, 5, or 6")
        
        if len(str_input) >= 6:
            sixth_digit = int(str_input[5])
            if sixth_digit not in [0, 1, 2, 3]:
                raise ValueError("The 6th digit must be 0, 1, 2, or 3")
        
        result = str_input
    else:
        result = ""
    
    import random
    
    while len(result) < 11:
        if len(result) == 2:
            month = str(random.randint(1, 12)).zfill(2)
            result += month
        elif len(result) == 4:
            result += str(random.randint(4, 6))
        elif len(result) == 5:
            result += str(random.randint(0, 3))
        else:
            result += str(random.randint(0, 9))
    
    main_code = [int(d) for d in result]
    
    weights1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    weights2 = [3, 4, 5, 6, 7, 8, 9, 10, 11, 1, 2]
    
    def calculate_sum(code, weights):
        return sum(digit * weight for digit, weight in zip(code, weights))
    
    control_digit = calculate_sum(main_code, weights1) % 11
    
    if control_digit == 10:
        control_digit = calculate_sum(main_code, weights2) % 11
    
    if control_digit == 10:
        control_digit = 0
    
    return result + str(control_digit)

def vBIN(str_input):
    str_input = str(str_input) if isinstance(str_input, (int, float)) else str_input
    
    if len(str_input) != 12:
        return False
    
    try:
        code = [int(d) for d in str_input]
    except ValueError:
        return False
    
    month = int(str_input[2:4])
    if month < 1 or month > 12:
        return False
    
    fifth_digit = code[4]
    if fifth_digit not in [4, 5, 6]:
        return False
    
    sixth_digit = code[5]
    if sixth_digit not in [0, 1, 2, 3]:
        return False
    
    main_code = code[:11]
    control_digit_from_str = code[11]
    
    weights1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    weights2 = [3, 4, 5, 6, 7, 8, 9, 10, 11, 1, 2]
    
    def calculate_sum(code, weights):
        return sum(digit * weight for digit, weight in zip(code, weights))
    
    control_digit = calculate_sum(main_code, weights1) % 11
    
    if control_digit == 10:
        control_digit = calculate_sum(main_code, weights2) % 11
    
    if control_digit == 10:
        control_digit = 0
    
    return control_digit == control_digit_from_str