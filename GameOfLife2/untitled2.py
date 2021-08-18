
def var2str(variable):

    return [global_var for global_var in globals() if id(variable) == id(globals()[global_var])]

variable = 1
a = 1
print(var2str(variable))