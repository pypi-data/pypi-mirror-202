import sys
from main.lib.Argument import Argument
Argument=Argument(sys.argv)
class Help:
    def Availale_contents(self):
        if(Argument.hasCommand(['bmi'])):
            return True
        if(Argument.hasCommand(['heartbeat'])):
            return True
        if(Argument.hasCommand(['bloodpressure'])):
            return True
        if(Argument.hasOption(['--help']) or Argument.hasOption(['-h'])):
            return True

            
    def help(self,filename):
        print(f"Usage: {filename} [Options]...")
        print("Options  are :")
        print("bmi                                        Show's the BMI status of our Body")
        print("heartbeat                                  Show's the Pulse Rate of our Heart")
        print("bloodpressure                              Show's the Blood Pressure Rate of our Body")


        
