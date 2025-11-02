#GET USER INPUT
def get_input(prompt="input: ", type="str", required=False, give_parameters=False):
    if give_parameters:
        print("get_input(prompt=\"input: \", type=\"str\", required=False)")
        return None
    
    while True:
        if type == "str":
            value = input(prompt).strip()
        elif type == "int":
            try:
                value = int(input(prompt))
            except ValueError:
                print("Not an integer value")
                continue
        elif type == "float":
            try:
                value = float(input(prompt))
            except ValueError:
                print("Not a floating point value")
                continue
        else:
            raise ValueError(f"Invalid type '{type}' passed to get_input(). Valid types: 'str', 'int', 'float'.")

        if required and (value == "" or value is None):
            print("This is a required field")
            continue

        return value

#Example_of_use

def use_example():
    num=get_input("Whats the number yo? ",type="int",required=True)
    print("The number you typed is:", num)

if __name__=="__main__":
    use_example()