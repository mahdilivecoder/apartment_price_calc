class validate_data_entry:
    """
    This class validate all input that come from user all inputs should filled by integers
    __set__ represent setter function and _set_name_ just relate called function to __set__.
    """
    def __set_name__(self,owner,name):
        self.name=name
    def __get__(self,instance,owner):
        return instance.__dict__[self.name]
    def __set__(self,instance,value):
        value=float(value)
        if int(value)==value:
            if self.name=="parking":
                if value<6:
                  instance.__dict__[self.name]=int(value)
                else:
                    raise ValueError("The value is incorrect!")
            else:  
                instance.__dict__[self.name]=int(value)
            if self.name=="type":
                if value==0:
                    instance.__dict__[self.name]==value
                else:
                    raise ValueError("You Should enter value between 0-0 !")
        else:
            raise TypeError("You should enter an integer!")