def gIIN(str_input=""):
    import random

    if isinstance(str_input, (int, float)):
        str_input = str(str_input)
    
    if str_input:
        if not isinstance(str_input, str):
            raise ValueError("Input value must be a string or a number")
        if len(str_input) > 11:
            raise ValueError("Input string must not exceed 11 digits")
        if not str_input.isdigit():
            raise ValueError("Input string must contain only digits")
        
        if len(str_input) >= 5:
            fifth_digit = int(str_input[4])
            if fifth_digit not in [0, 1, 2, 3]:
                raise ValueError("The 5th digit must be 0, 1, 2, or 3")
        
        result = str_input
    else:
        result = ""
    
    while len(result) < 11:
        if len(result) == 4:
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

def vIIN(str_input):
    str_input = str(str_input) if isinstance(str_input, (int, float)) else str_input
    
    if len(str_input) != 12:
        return False
    
    try:
        code = [int(d) for d in str_input]
    except ValueError:
        return False
    
    fifth_digit = code[4]
    if fifth_digit not in [0, 1, 2, 3]:
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