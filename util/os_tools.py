import os
from functools import wraps

def os_check(func):
    """
    decorate a function and check if the os is supported or not.
    if we pass function without args it just check the os and runs the function.
    if we pass function with args it's check os and runs function with it's @decorators values like(print ....)
    """
    @wraps(func)
    def inner(args=None):
        if os.name=="nt":
            os.system("cls")
            if args!=None:
                print("Based On the entered data the price of apartment would be around:\n\t")
                func(args)
            elif args==None:
                func()
        elif os.name=="posix":
            if args!=None:
                os.system("clear")
                print("Based On the entered data the price of apartment would be around:\n\t")
                func(args)
            elif args==None:
                func()
        else:
            raise OSError("We just support windows and linux!")
    return inner