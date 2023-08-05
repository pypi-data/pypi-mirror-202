import sys
from main.lib.Argument import Argument
from main.lib.Command_help import Command_help
from main.lib.Validation_funtion import Validation_funtion
Validation_funtion=Validation_funtion()
Command_help=Command_help()
Argument=Argument(sys.argv)
class Validation_command:
    def bmi(self):
        if(Argument.hasCommand(['bmi'])):
            if(Argument.hasOption(['-weight']) and Argument.hasOption(['-height']) ):
                weight=Argument.getoptionvalue('-weight')
                height=Argument.getoptionvalue('-height')
                Validation_funtion.check_bmi(weight,height)
            if(Argument.hasOption(['--help']) or Argument.hasOption(['-h'])):
                        Command_help.bmi()

                
    def heartbeat(self):
        if(Argument.hasCommand(['heartbeat'])):
            if(Argument.hasOption(['-heartbeat']) and Argument.hasOption(['-age']) and Argument.hasOption(['-gender'])):
                age=Argument.getoptionvalue('-age')
                gender=Argument.getoptionvalue('-gender')
                heartbeat=Argument.getoptionvalue('-heartbeat')
                Validation_funtion.heartbeat(age,gender,heartbeat)
            if(Argument.hasOption(['--help']) or Argument.hasOption(['-h'])):
                        Command_help.heartbeat()
        

    def bloodpressure(self):
        if(Argument.hasCommand(['bloodpressure'])):
            if(Argument.hasOption(['-bloodpressure']) and Argument.hasOption(['-age']) and Argument.hasOption(['-measuring_type'])):
                age=Argument.getoptionvalue('-age')
                measuring_type=Argument.getoptionvalue('-measuring_type')
                bloodpressure=Argument.getoptionvalue('-bloodpressure')
                Validation_funtion.bloodpressure(age,measuring_type,bloodpressure)
            if(Argument.hasOption(['--help']) or Argument.hasOption(['-h'])):
                        Command_help.bloodpressure()
            

