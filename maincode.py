Welcome to the COVID-19 Symptom Checker!
Please answer the following questions with either "yes" or "no"

list = (" ")

travel = input("Have you recently travelled? ")
print(travel)

if travel.starswith("y"):
print("low risk")

work = input ("Are you an essential worker? ")
print(work)

if work.starswith("y"):
print("medium")

contact = input ("Have you been in contact with someone who has either travelled and/or is an essential worker AND is now sick? ")
print(contact)

if contact.starswith("y"):
print("medium")

exposure = input ("Have you been in contact with anyone who was known to have the coronavirus or have been exposed to it (COVID-19)? ")
print(contact)

if exposure.starswith("y"):
print("high")

symptoms = input("Are you experiencing any ONE of the following symptoms: fever, cough, sore throat, runny nose, shortness or breath or difficulty breathing, chills, repeated shaking with chills, muscle pain, headache, sore throat, new loss of taste or smell")
print(fever)

if symptoms.starswith("y"):
print("low")

symptomstwo = input("Are you experiencing TWO OR MORE of the following symptoms: fever, cough, sore throat, runny nose, shortness or breath or difficulty breathing, chills, repeated shaking with chills, muscle pain, headache, sore throat, new loss of taste or smell")
print(symptoms)

if symptomstwo.starswith("y"):
print("high")

symptomshigh = input("If you are experiencing trouble breathing, persistent pain or pressure in the chest, new confusion or inability to arouse, bluish lips or face - please call 911")
print(symptomshigh)

if symptoms.starswith("y"):
print("extremely high")

Please contact your medical care provider if you are experiencing symptoms and have been judged to be at medium or high risk for more than 2 questions
