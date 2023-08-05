#! /usr/bin/python
import sys
from .lib.Argument import Argument
# import *
from .lib.Validation_command import Validation_command
from .lib.Help import Help
Help=Help()
# main.helloworld()
Validation_command=Validation_command()
Argument=Argument(sys.argv)

def main():
    if((Help.Availale_contents())==True):
        if(len(sys.argv)>1):
            if(Argument.hasCommand(['bmi'])):
                Validation_command.bmi()
            if(Argument.hasCommand(['heartbeat'])):
                Validation_command.heartbeat()
            if(Argument.hasCommand(['bloodpressure'])):
                Validation_command.bloodpressure()
            if((sys.argv[1] == '--help') or (sys.argv[1] == '-h')):
                Help.help(sys.argv[0])
            
        else:
            Help.help(sys.argv[0])
    else:
        Help.help(sys.argv[1])

if __name__ == "__main__":
    main()






