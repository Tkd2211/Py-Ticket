# GET USER INPUT
def get_input(
    prompt="input: ",
    input_type="str",
    required=False,
    give_parameters=False,
    error_prompt=None,
    negative_value_allowed=False,
):
    # To make specifed error prompt a priority over generic error prompt
    priority_error_prompt = error_prompt
    
    if give_parameters:
        print('get_input(prompt="input: ", type="str", required=False)')
        return None
    while True:
        ValueError_prompt = None
        if input_type == "str":
            try:
                value = input(prompt).strip()
            except Exception:
                if error_prompt == None:
                    print("Not an integer value")
                else:
                    print(error_prompt)
                continue

        elif input_type == "int":
            try:
                value = int(input(prompt).strip())
                if value < 0 and negative_value_allowed == False:
                    ValueError_prompt = "This field does not take negative values"
                    raise ValueError(ValueError_prompt)
            except ValueError:
                error_prompt = priority_error_prompt
                if ValueError_prompt and error_prompt == None:
                    error_prompt = ValueError_prompt
                if error_prompt == None:
                    print("Not an integer value")
                else:
                    print(error_prompt)
                    error_prompt = None
                continue
        
        elif input_type == "float":
            try:
                value = float(input(prompt).strip())
                if value < 0 and negative_value_allowed == False:
                    ValueError_prompt = "This field does not take negative values"
                    raise ValueError(ValueError_prompt)
            except ValueError:
                error_prompt = priority_error_prompt
                if ValueError_prompt and error_prompt == None:
                    error_prompt = ValueError_prompt
                if error_prompt == None:
                    print("Not a floating point value")
                else:
                    print(error_prompt)
                    error_prompt = None
                continue
        
        else:
            raise ValueError(
                f"Invalid type '{input_type}' passed to get_input(). Valid input_types: 'str', 'int', 'float'."
            )

        if required and (value == "" or value is None):
            print("This is a required field")
            continue

        return value


# Example_of_use
def use_example():
    num = get_input(
        "Whats the number? ", input_type="int", required=True, error_prompt="Bad"
    )
    print("The number you typed is:", num)


if __name__ == "__main__":
    use_example()
