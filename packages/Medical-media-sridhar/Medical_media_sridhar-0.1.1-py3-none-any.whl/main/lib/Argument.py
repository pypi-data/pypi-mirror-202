import sys
class Argument:
    def __init__(self,args):
        self.args=args
        self.command=[]
        self.option=[]
        self.option_values = {}
        for arg in self.args:
            if '-' in arg:
                if '=' in arg:
                    pairs = arg.split('=')
                    self.option_values[pairs[0]] = pairs[1] 
                    self.option.append(pairs[0])
            
                else:
                    self.option.append(arg)
            else:
                self.command.append(arg)

    def hasOption(self,options:list): 
        user_options=set(self.option)
        required_option=set(options)
        return list(required_option & user_options)
        
    def hasCommand(self,commands:list):
        user_command=set(self.command)
        required_command=set(commands)
        return list(required_command & user_command)

    def getoptionvalue(self, option, default=None):
        if option in self.option_values:
            return self.option_values[option]
        else:
            return default 

    
 

    



        