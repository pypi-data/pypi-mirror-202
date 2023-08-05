import sys
class Command_help:
    def bmi(self):
        print("{} <bmi> -weight=<Our Weight> -height=<Our Weight>".format(sys.argv[0]))
        print("Options  are :")
        print("-weight          Represents the Weight of our body")
        print("-height          Represents the height of our body")
        print("If we want to find our BMI of our body means must reprsenets the Height and Weight of our body")
    def heartbeat(self):
        print("{} <heartbeat> -gender=<Gender> -age=<Age> -heartbeat=<Heart beat>".format(sys.argv[0]))
        print("Options  are :")
        print("-gender          Gender")
        print("-age             Represents the Age of Human")
        print("-heartbeat       Represents the rate of our Pulse")
    def bloodpressure(self):
        print("{} <bloodpressure> -bloodpressure=<BloodPressure> -age=<Age> -measuring_type=<Which Type>".format(sys.argv[0]))
        print("Options  are :")
        print("-bloodpressure         Represents the BloodPressure rate or status of our body")
        print("-age                   Represents the Age of Human")
        print("-measuring_type        Represents the Which type of our body")

