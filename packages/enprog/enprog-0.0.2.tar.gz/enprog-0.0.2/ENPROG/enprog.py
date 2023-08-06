import os
class EnProg:
    
    SYNTAX = {
    "PRINT": " print(",
    "SET": "",
    "TO": " = ",
    "IF": " if ",
    "THEN": ":",
    "ELSE": " else: ",
    "FOR": " for ",
    "IN": " in ",
    "RANGE": " range(",
    "WHILE": " while ",
    "NOT": " not ",
    "AND": " and ",
    "OR": " or ",
    "FUNCTION": " def ",
    "FUN": " def ",
    "STATIC": " @staticmethod ",
    "RETURN": " return ",
    "CLASS": " class ",
    "OBJECT": " class ",
    "INIT": " __init__ ",
    "SINGLEINIT": "  __init__(self)",
    "ATTRIBUTE": " self",
    "THIS": " self",
    "THIS.": "self.",
    "ATTRIBUTE.": "self.",
    "METHOD": " def ",
    "IS": " is ",
    "NONE": " None ",
    "NULL": " None ",
    "TRUE": " True ",
    "FALSE": " False ",
    "EQUALS": " == ",
    "NOT_EQUALS": " != ",
    "GREATER_THAN": " > ",
    "LESS_THAN": " < ",
    "GREATER_THAN_OR_EQUAL": " >= ",
    "LESS_THAN_OR_EQUAL": " <= ",
    "PLUS": " + ",
    "MINUS": " - ",
    "MULTIPLY": " * ",
    "DIVIDE": " / ",
    "MODULO": " % ",
    "INCREMENT": " += ",
    "DECREMENT": " -= ",
    "LENGTH": " len(",
    "SELF": " self ",
    "A": " ",
    "-F": "from",
    "-I": "import",
    "USING": "import",
    "PACKAGE": "import",
    "NAMED": " as ",
    "TOSTRING": "str(",
    "TOLIST": "list(",
    "STRING": "str(",
    "LIST": "list()",
    "CALL": "",
    "STDOUT": "print(",
    "CONSOLE.WRITE": "print(",
    "CONSOLE.LOG": "print("
}

    def __init__(self):
        pass

    @staticmethod
    def translate_program(program):
        translated_program = ""
        # Stack to keep track of open parentheses and open braces
        open_parentheses_stack = []
        open_braces_stack = []
        for line in program:
            line = line.strip()
            # If the line is empty or a comment, ignore it
            if not line or line.startswith("#" or '//' or '/*' or '*/' or '*comment'):
                continue
            if "init".upper() in line:
                line.replace("init", "def __init__(self, ")
            if "singleinit".upper() in line:
                line.replace("singleinit", "def __init__(self)")

            # Check if the line contains an opening brace
            if "{" in line:
                # If the line contains an opening brace, remove it and add an indent
                line = line.replace("{", "")
                translated_program += " " * (len(open_braces_stack) * 4) + line.strip() + ":\n"
                open_braces_stack.append("{")
                continue

            # Check if the line contains a closing brace
            if "}" in line:
                # If the line contains a closing brace, remove it and remove an indent
                line = line.replace("}", "")
                open_braces_stack.pop()
                translated_program += " " * (len(open_braces_stack) * 4) + line.strip() + "\n"
                continue

            # Translate each word in the line
            translated_line = ""
            words = line.split()

            for i, word in enumerate(words):
                # Check if the word is in the syntax dictionary
                found_word = False
                if word.upper() in EnProg.SYNTAX:
                    # If the word is in the syntax dictionary, append its translation
                    translated_line += EnProg.SYNTAX[word.upper()]
                    if "(" in EnProg.SYNTAX[word.upper()]:
                        open_parentheses_stack.append("(")
                        # Remove the space after the opening parenthesis
                        translated_line = translated_line.rstrip()  # strip the trailing whitespace
                    found_word = True
                if not found_word:
                    # If the word is not in any of the syntax dictionaries, just append it as is
                    translated_line += word

                # If the next word is not the last one and is not a keyword, add a space
                if i < len(words) - 1 and words[i + 1].upper() not in EnProg.SYNTAX:
                    translated_line += " "

            translated_program += " " * (len(open_braces_stack) * 4) + translated_line.strip() + '\n'

            # Close parentheses if there are any open ones
            while len(open_parentheses_stack) > 0:
                translated_program += ")"
                open_parentheses_stack.pop()

            # Add a newline after each line
            translated_program += "\n"
        return translated_program

    @staticmethod
    def run_program(file_path):
        with open(file_path, "r") as f:
            program = f.readlines()

        translated_code = EnProg.translate_program(program)

        # Redirect stdout to a string buffer
        import io
        stdout_buffer = io.StringIO()
        import sys
        sys.stdout = stdout_buffer

        # Execute the program
        exec(translated_code)

        # Restore stdout and return the output
        sys.stdout = sys.__stdout__
        return stdout_buffer.getvalue()

    @staticmethod
    def check_syntax(code):
        bracket_stack = []
        errors = []
        for i, char in enumerate(code):
            if char == "(":
                bracket_stack.append(("(", i))
            elif char == ")":
                if len(bracket_stack) == 0 or bracket_stack[-1][0] != "(":
                    errors.append(("Mismatched closing parenthesis", i))
                else:
                    bracket_stack.pop()
            for keyword, value in EnProg.SYNTAX:
                if code[i:i+len(value)] == value:
                    if keyword == "THIS" and ("class " not in code[:i] or "self" not in code[:i]):
                        errors.append(("Invalid use of 'this'", i))
                    elif keyword == "STATIC" and "class " not in code[:i]:
                        errors.append(("Invalid use of '@staticmethod'", i))
                    elif keyword in ["OBJECT", "INIT", "SINGLEINIT", "ATTRIBUTE", "SELF", "METHOD"] and "class " not in code[:i]:
                        errors.append((f"Invalid use of '{keyword.lower()}'", i))
                    elif keyword in ["A", "-F", "-I", "USING", "PACKAGE", "NAMED"] and "import " not in code[:i]:
                        errors.append((f"Invalid use of '{keyword.lower()}'", i))
                    elif keyword in ["PRINT", "SET", "LENGTH", "TOSTRING", "TOLIST"] and i > 0 and code[i-1].isalnum():
                        errors.append((f"Missing whitespace before '{value.strip()}'", i))
                    elif keyword in ["IF", "FOR", "WHILE"] and i > 0 and code[i-1].isalnum():
                        errors.append((f"Missing whitespace before '{value.strip()}'", i))
                    elif keyword in ["THEN", "ELSE", "IN", "EQUALS", "NOT_EQUALS", "GREATER_THAN", "LESS_THAN", "GREATER_THAN_OR_EQUAL", "LESS_THAN_OR_EQUAL", "PLUS", "MINUS", "MULTIPLY", "DIVIDE", "MODULO", "INCREMENT", "DECREMENT", "TO"] and (i == 0 or not code[i-1].isspace()):
                        errors.append((f"Missing whitespace after '{value.strip()}'", i))
        if len(bracket_stack) > 0:
            errors.append(("Unclosed opening parenthesis", bracket_stack[-1][1]))
        return errors
    @staticmethod
    def getPackage(package_path):
        with open (package_path, 'r', encoding='utf-8') as f:
            script = f.readlines()
        code = EnProg.translate_program(script)
        script_path = os.path.realpath(__file__)
        script_dir = os.path.dirname(script_path)
        print(script_dir)
        with open(f"{script_dir}\\packages\\EnProgCache.py", "w", encoding="utf-8")as f:
            f.write(code)
        return f"{script_dir}\\packages\\EnProgCache.py"
    @staticmethod
    def importPackage(file_path, class_name):
        import_file_path = EnProg.getPackage(file_path)

        with open(import_file_path, 'r') as f:
            script_code = f.read()

        imported_globals = {}
        exec(script_code, imported_globals)

        # Check if the requested class is defined in the imported script
        if class_name not in imported_globals:
            raise ValueError(f"{class_name} is not defined in the imported file")

        # Create an instance of the requested class
        instance = imported_globals[class_name]()

        return instance
