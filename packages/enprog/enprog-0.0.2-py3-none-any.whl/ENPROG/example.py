from enprog import EnProg

# Import the module and assign it to a variable
example_module = EnProg.importPackage("D:\\Projects\\ENPROG\\examplescript.ep", "Example")

# Use the Example class from the imported module
example_module.singleinit()
print(example_module.age)

