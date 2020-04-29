print("Welcome to the COVID-19 Symptom Checker! Please answer the following questions with either 'YES' or 'NO' ")

list = (" ")

travel = input("Have you recently travelled? ")
if travel.startswith("y"):
    print("low risk")
else:
    print("minimal to no risk")

work = input ("Are you an essential worker? ")
if work.startswith("y"):
    print("medium risk")
else:
    print("minimal to no risk")

contact = input ("Have you been in contact with someone who has either travelled and/or is an essential worker AND is now sick? ")
if contact.startswith("y"):
    print("medium risk")
else:
    print("minimal to no risk")

exposure = input ("Have you been in contact with anyone who was known to have the coronavirus or have been exposed to it (COVID-19)? ")
if exposure.startswith("y"):
    print("high risk")
else:
    print("minimal to no risk")

symptoms = input("Are you experiencing any ONE of the following symptoms: fever, cough, sore throat, runny nose, shortness or breath or difficulty breathing, chills, repeated shaking with chills, muscle pain, headache, sore throat, new loss of taste or smell ")
if symptoms.startswith("y"):
    print("low risk")
else:
    print("minimal to no risk")

symptomstwo = input("Are you experiencing TWO OR MORE of the following symptoms: fever, cough, sore throat, runny nose, shortness or breath or difficulty breathing, chills, repeated shaking with chills, muscle pain, headache, sore throat, new loss of taste or smell ")
if symptomstwo.startswith("y"):
    print("high risk")
else:
    print("minimal to no risk")

symptomshigh = input("If you are experiencing trouble breathing, persistent pain or pressure in the chest, new confusion or inability to arouse, bluish lips or face - please call 911 ")
if symptoms.startswith("y"):
    print("extremely high risk")
else:
    print("minimal to no risk")

print("Please contact your medical care provider if you are experiencing symptoms and have been judged to be at medium or high risk for more than 2 questions ")
