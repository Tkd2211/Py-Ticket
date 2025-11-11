# GET USER INPUT
def get_input(
    prompt="input: ",
    input_type="str",
    required=False,
    give_parameters=False,
    error_prompt=None,
):
    if give_parameters:
        print('get_input(prompt="input: ", type="str", required=False)')
        return None

    while True:
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
            except ValueError:
                if error_prompt == None:
                    print("Not an integer value")
                else:
                    print(error_prompt)
                continue
        
        elif input_type == "float":
            try:
                value = float(input(prompt).strip())
            except ValueError:
                if error_prompt == None:
                    print("Not a floating point value")
                else:
                    print(error_prompt)
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
