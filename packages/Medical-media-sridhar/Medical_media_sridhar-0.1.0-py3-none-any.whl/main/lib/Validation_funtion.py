class Validation_funtion:
    def check_bmi(self,weight:int,height:int):
        weight=int(weight)
        height=int(height)
        bmi=((weight)/(height/100)**2)
        if bmi <= 18.5:  
            print("Oops! You are underweight.")  
        elif bmi <= 24.9:  
            print("Awesome! You are healthy.")  
        elif bmi <= 29.9:  
            print("Eee! You are overweight.")  
        else:  
            print("Seesh! You are obese.")
    def heartbeat(self,age,gender,heartbeat):
        age=int(age)
        heartbeat=int(heartbeat)
        if(gender == 'male'):
            if(age>18 and age<25):
                if(heartbeat>62 and heartbeat <73):
                    print("Your Pulse Rate Status is Good")
                else:
                    print("Your Pulse Rate Status is Good")
            elif(age>26 and age<35):
                if(heartbeat>62 and heartbeat <73):
                    print("Your Pulse Rate Status is Good")
                else:
                    print("Your Pulse Rate Status is Good")
            elif(age>36 and age<45):
                if(heartbeat>63 and heartbeat <75):
                    print("Your Pulse Rate Status is Good")
                else:
                    print("Your Pulse Rate Status is Good")
            elif(age>46 and age<55):
                if(heartbeat>64 and heartbeat <76):
                    print("Your Pulse Rate Status is Good")
                else:
                    print("Your Pulse Rate Status is Good")
            elif(age>56 and age<65):
                if(heartbeat>62 and heartbeat <75):
                    print("Your Pulse Rate Status is Good")
                else:
                    print("Your Pulse Rate Status is Good")
            elif(age>=57):
                if(heartbeat>62 and heartbeat <73):
                    print("Your Pulse Rate Status is Good")
                else:
                    print("Your Pulse Rate Status is Good")
        
        
        if(gender == 'female'):
            if(age>18 and age<25):
                if(heartbeat>64 and heartbeat <80):
                    print("Your Pulse Rate Status is Good")
                else:
                    print("Your Pulse Rate Status is Good")
            elif(age>26 and age<35):
                if(heartbeat>62 and heartbeat <73):
                    print("Your Pulse Rate Status is Good")
                else:
                    print("Your Pulse Rate Status is Good")
            elif(age>36 and age<45):
                if(heartbeat>63 and heartbeat <75):
                    print("Your Pulse Rate Status is Good")
                else:
                    print("Your Pulse Rate Status is Good")
            elif(age>46 and age<55):
                if(heartbeat>64 and heartbeat <76):
                    print("Your Pulse Rate Status is Good")
                else:
                    print("Your Pulse Rate Status is Good")
            elif(age>56 and age<65):
                if(heartbeat>62 and heartbeat <75):
                    print("Your Pulse Rate Status is Good")
                else:
                    print("Your Pulse Rate Status is Good")
            elif(age>=57):
                if(heartbeat>64 and heartbeat <81):
                    print("Your Pulse Rate Status is Good")
                else:
                    print("Your Pulse Rate Status is Good")


    def bloodpressure(self,age,measuring_type,bloodpressure):
        age=int(age)
        bloodpressure=int(bloodpressure)
        if(measuring_type == 'systolic'):
            if(age>1 and age<5):
                if(bloodpressure>80 and bloodpressure <115):
                    print("Your Blood Pressure Rate Status is Good")
                else:
                    print("Your Blood Pressure Rate Status is Bad")
            elif(age>6 and age<13):
                if(bloodpressure>80 and bloodpressure <120):
                    print("Your Blood Pressure Rate Status is Good")
                else:
                    print("Your Blood Pressure Rate Status is Bad")
            elif(age>14 and age<18):
                if(bloodpressure>90 and bloodpressure <120):
                    print("Your Blood Pressure Rate Status is Good")
                else:
                    print("Your Blood Pressure Rate Status is Bad")
            elif(age>19 and age<40):
                if(bloodpressure>95 and bloodpressure <135):
                    print("Your Blood Pressure Rate Status is Good")
                else:
                    print("Your Blood Pressure Rate Status is Bad")
            elif(age>41 and age<60):
                if(bloodpressure>110 and bloodpressure <145):
                    print("Your Blood Pressure Rate Status is Good")
                else:
                    print("Your Blood Pressure Rate Status is Bad")
            elif(age>=61):
                if(bloodpressure>95 and bloodpressure <145):
                    print("Your Blood Pressure Rate Status is Good")
                else:
                    print("Your Blood Pressure Rate Status is Bad")
                    
        if(measuring_type == 'diastolic'):
            if(age>1 and age<5):
                if(bloodpressure>55 and bloodpressure <80):
                    print("Your Blood Pressure Rate Status is Good")
                else:
                    print("Your Blood Pressure Rate Status is Bad")
            elif(age>6 and age<13):
                if(bloodpressure>45 and bloodpressure <80):
                    print("Your Blood Pressure Rate Status is Good")
                else:
                    print("Your Blood Pressure Rate Status is Bad")
            elif(age>14 and age<18):
                if(bloodpressure>50 and bloodpressure <80):
                    print("Your Blood Pressure Rate Status is Good")
                else:
                    print("Your Blood Pressure Rate Status is Bad")
            elif(age>19 and age<40):
                if(bloodpressure>60 and bloodpressure <80):
                    print("Your Blood Pressure Rate Status is Good")
                else:
                    print("Your Blood Pressure Rate Status is Bad")
            elif(age>41 and age<60):
                if(bloodpressure>70 and bloodpressure <90):
                    print("Your Blood Pressure Rate Status is Good")
                else:
                    print("Your Blood Pressure Rate Status is Bad")
            elif(age>=61):
                if(bloodpressure>70 and bloodpressure <90):
                    print("Your Blood Pressure Rate Status is Good")
                else:
                    print("Your Blood Pressure Rate Status is Bad")

