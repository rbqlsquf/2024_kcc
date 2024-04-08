message = ""

with open("output_answer.txt", "r") as f:
    lines = f.readlines()
    for line in lines:
        if line == "\n":
            continue
        if "Reference documents" in line:
            print(message)
            message = ""
        message = message + line
