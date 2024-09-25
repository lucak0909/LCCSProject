import numpy as np
import csv
import time
import matplotlib.pyplot as plt
import pandas as pd
from project_functions import checkBPM

# Initializing Variables
minsElapsed = 1
startTime = int(time.monotonic())
loopTime = 0
currentBPM = 0
BPM_list = []
interval = 5
interval_average_BPM = 0
interval_slope = 0
slope_diff = 0
avg_BPM_list = []
val_diff = []
numRows = 0

dataset = "\Artefact\dataset.csv"  # declaring dataset name
datasetHeader = ["Time_Elapsed", "Heart_Rate", "Average_BPM", "Stress_Level"]  # Initializing list of dataset headers
file = open(dataset, "w")  # Creates dataset
data = csv.writer(file)  # Initializes csv.write() function as a variable
data.writerow(datasetHeader)  # Writes the dataset with column headers
file.close()  # Saves the dataset and leaves "write" mode, so it can append later

print("\n" * 10)
#  Programme title and instructions
print("\n\t\tStress Management Device\n"
      "\t\t------------------------\n\n"
      "Press 'A' on the MicroBit to display your stress levels.\n"
      "Press 'B' on the MicroBit to ask a 'what if' question.\n\n"
      "NOTE: PRESS BUTTON IN RAPID SUCCESSION TO ENSURE IT IS REGISTERED\n\n\n\n")

# Primary loop in which the programme runs indefinitely
while True:
    loopTime = int(time.monotonic())  # finds the current time to 0 decimal places

    time.sleep(0.98)  # delay to stop each ms to be counted in each second with the time of each loop taken into account

    currentBPM = int(checkBPM())  # initialized currentBPM by calling function in "project_functions.py" to read serial

    """On a MicroBit Button press, the program will "serial write" 1111 for button "A" or 2222 for button "B", this 
    number is out of any realistic heartrate and therefore on a button "A" press, the if statement below recognizes 
    this executes its contents"""
    if currentBPM == 1111:
        question = input("\n\t\t What Data Would You Like to Graph?\n"
                         "\n\t\t------------------------------------\n\n"
                         "[1] Heart Rate Against Time\n"
                         "[2] Stress Levels Against Time\n\n"
                         "Answer: ")

        # The below while loop is a form of input validation to ensure the programme won't end unintentionally
        while question not in ["1", "2"]:
            question = input("\nPlease enter either of the below options ('1' or '2'):\n"
                             "-----------------------------------------------------\n\n"
                             "[1] Heart Rate Against Time\n"
                             "[2] Stress Levels Against Time\n\n"
                             "Answer: ")

        # Checks user input and executes accordingly
        if question == "1":
            # This if statement ensures heart rate is only able to be graphed once enough data has been collected
            if minsElapsed >= 6:
                # Using the "pandas" package, the programme creates dictionary using each header's contents as a list
                df = pd.read_csv(dataset, usecols=datasetHeader)
                print("\nContents in csv file:", df)
                # Using the matplotlib package:
                plt.title("Heart Rate Over Time")  # Creating graph title 
                plt.bar(df.Time_Elapsed, df.Heart_Rate, color='#7242f5', edgecolor='black')
                plt.xlabel("Time Elapsed (mins)")  # Labelling x-axis
                plt.ylabel("Heart Rate (beats per minute)")  # Labelling y-axis
                plt.show()  # Displays the graph
            else:
                print("\nNot enough data has been collected!\nPlease wait at least 5 minutes to graph heart rate.\n")

        # Checks user input and executes accordingly
        elif question == "2":
            # This if statement ensures stress is only able to be graphed once enough data has been collected
            if minsElapsed >= 21:
                df = pd.read_csv(dataset, usecols=datasetHeader)
                print("Contents in csv file:", df)
                plt.title("Stress Levels Over Time")
                plt.bar(df.Time_Elapsed, df.Stress_Level, color='#7242f5', edgecolor='black')
                plt.xlabel("Time Elapsed (mins)")
                plt.ylabel("Stress Level")
                plt.show()
            else:
                print("\nNot enough data has been collected!\n"
                      "Please wait until 20 minutes has passed to graph stress levels\n")

    elif currentBPM == 2222:  # Executes on a button "B" press
        # This if statement ensures 'what if' questions are only able to be asked once enough data has been collected
        if minElapsed <= 11:
            print("\nNot enough data has been collected!\n"
                  "Please wait until 10 minutes has passed to allow for accurate analysis of your data.\n")
        else:
            question = input("\n\t\t What Question Would You Like to Ask?\n"
                             "\t\t--------------------------------------\n\n"
                             "[1] What would my average and maximum heart rate be if I became athletic? \n"
                             "[2] What should my heart rate be if I am doing light to moderate exercise? \n\n"
                             "Answer: ")

            # The below while loop is a form of input validation to ensure the programme won't end unintentionally
            while question not in ["1", "2"]:
                question = input("\nPlease enter either of the below options ('1' or '2'):\n"
                                 "-----------------------------------------------------\n\n"
                                 "[1] What would my average and maximum heart rate be if I became athletic? \n"
                                 "[2] What should my heart rate be if I am doing light to moderate exercise? \n\n"
                                 "Answer: ")

            # Checks user input and executes accordingly
            if question == "1":
                gender = input("\nEnter Your Gender (m/f): ")  # 'What if' parameter no.1: gender (string)
                while gender not in ["m", "f"]:  # While loop to validate 'what if' question parameter
                    gender = input("\nPlease enter either 'm' for male or 'f' for female: ")
                    gender = gender.lower()

                age = input("\nEnter Your Age: ")
                # While loop to validate 'what if' question parameters by ensuring the age is input as a digit
                while not age.isdigit():
                    age = input("\nPlease enter your age in integer form: ")
                age = int(age)  # 'What if' Question parameter no.2: age (integer)

                # Using the "pandas" package, the programme creates dictionary using each header's contents as a list
                df = pd.read_csv(dataset, usecols=datasetHeader)  # 'What if' parameter no.3 heart rate (integer)
                # Finds sum of the contents of heart rate column and divides by the number of rows to find the average
                avg = int(sum(df.Heart_Rate) / numRows)

                # Changes the average heart rate based on your gender
                if gender == "m":
                    avg = avg * 0.6
                elif gender == "f":
                    avg = avg * 0.7

                maxHR = 220 - age  # Using the common formula to find the user's max heart rate 

                print(f"\nYour average heart rate would be {avg} BPM if you were athletic."
                      f"\nYour maximum heart rate would be {maxHR} BPM if you were athletic.\n\nTo reach "
                      f"this level of cardiovascular fitness, you should attempt to focus on cardio when exercising."
                      f"\nBy doing this you are exercising your heart by forcing your heart rate to increase,"
                      f"\nwhich strengthen the muscles in your heart, thus reducing heart rate.\n")

            # Checks user input and executes accordingly
            if question == "2":
                gender = input("\nEnter Your Gender (m/f): ")  # 'What if' Question parameter no.1: gender (string)
                while gender not in ["m", "f"]:  # Validation loop
                    gender = input("\nPlease enter either 'm' for male or 'f' for female: ")
                    gender = gender.lower()

                age = input("\nEnter Your Age: ")
                while not age.isdigit():  # Validation loop
                    age = input("\nPlease enter your age in integer form: ")
                age = int(age)  # 'What if' Question parameter no.2: age (integer)

                # formula to find maximum heart rate
                maxHR = 220 - age
                target_low = maxHR * 0.5
                target_high = maxHR * 0.85

                df = pd.read_csv(dataset, usecols=datasetHeader)  # 'What if' parameter no.3: heart rate (integer)
                avg = int(sum(df.Heart_Rate) / numRows)  # Finding user's average heart rate
                max_hr = int(max(df.Heart_Rate) + (avg * 0.3))  # Finds highest heart rate stored in the dataset
                min_hr = int(min(df.Heart_Rate))  # Finds lowest heart rate stored in the dataset

                # Changes heart rate range based on gender parameter
                if gender == "m":
                    target_high -= 2
                    target_low -= 2
                elif gender == "f":
                    target_high += 2
                    target_low += 2

                max_diff = abs(target_high - max_hr)
                min_diff = abs(target_low - min_hr)

                print("\n\t\tAnswer\n\t\t------\n\n"
                      f"Your heart rate if you are doing light to moderate exercise should be within the range of "
                      f"{np.round(target_low, 0)} - {np.round(target_high, 0)} BPM.\n"
                      f"Your heart rate is currently in the range of {min_hr} - {max_hr} BPM.\n\n")

                # The below if statements print different answers to "what if" questions based on the user's input
                if max_hr > target_high:
                    print(f"Your maximum heart rate is {max_diff} higher than it should be when doing moderate exercise"
                          f",\nand your minimum heart rate is {min_diff} higher than it should be when doing moderate "
                          f"exercise.\n\n")

                    if max_diff > 10:
                        print("This is an unhealthy range in terms of cardiovascular fitness.\n"
                              "The recommended range will reduce stress and the likelihood of heart related issues "
                              "in the future.\nTo achieve this level of cardiovascular fitness, you should \n"
                              "attempt to focus on cardio when exercising.\n"
                              "By doing this you are exercising your heart by forcing your heart rate to increase,\n"
                              "which strengthen the muscles in your heart, thus reducing heart rate.\n\n")
                    elif max_diff <= 10:
                        print("This is a healthy range in terms of cardiovascular fitness, \n"
                              "However, there is room for improvement.\nThe recommended range "
                              "will reduce stress and the likelihood of heart related issues in the future.\n"
                              "To achieve this level of cardiovascular fitness, you should \n"
                              "attempt to focus on cardio when exercising.\n"
                              "By doing this you are exercising your heart by forcing your heart rate to increase,\n"
                              "which strengthen the muscles in your heart, thus reducing heart rate.\n\n")

                elif max_hr <= target_high:
                    print(f"Your maximum heart rate is {max_diff} below what is recommended,\n"
                          f"and your minimum heart rate is {min_diff} below what is recommended.\n"
                          f"This is a very healthy range in terms of cardiovascular fitness, \n"
                          f"Keep up the good work!\n\n")

    # This statement below finds the programme's runtime (in seconds) and executes the below code every minute
    if np.round((loopTime - startTime + 1), 0) % 60 == 0:

        # Put BPM into list to find average
        BPM_list.append(currentBPM)

        if minsElapsed % 5 == 0:  # Executes every 5 minutes

            interval_average_BPM = sum(BPM_list) / interval  # Finds the user's average BPM over the last 5 minutes
            avg_BPM_list.append(interval_average_BPM)  # Places this average into a separate list

            BPM_list.clear()  # Empties the first list to find next 5-minute average

            if minsElapsed % 10 == 0:  # Executes every 10 minutes

                interval_slope = (avg_BPM_list[1] - avg_BPM_list[
                    0]) / interval  # Finds the slope between the two average BPM values from the past 10 mins
                interval_slope = np.round(interval_slope, 2)  # Rounds this value to two decimal places

                avg_BPM_list.clear()  # Clears the list of average heart rates to find next 10 minute slope

                val_diff.append(interval_slope)  # Places the average heart rate's rate of change into a list

                if len(val_diff) > 1:  # Once there is multiple values in the above list then the below code is executed
                    # Finds the displacement of two consecutive slope values and takes this to be the stress level
                    slope_diff = abs(val_diff[-1] - val_diff[-2])
                    # If the program detects a large change in stress then it executes the below code
                    if slope_diff > 4:
                        # Warns the user of their stress level and suggests ways of reducing this stress
                        print(
                            "\n\n\n\t\t WARNING\n"
                            "\t\t---------\n"
                            "Your stress level has increased!\n\nTo reduce your stress use the '4-7-8' deep "
                            "breathing exercise.\n\nMethod:\n"
                            "Inhale for 4 seconds | Hold your breath for 7 seconds | Exhale for 8 seconds"
                            "\n\nAnother method to reduce stress is to exercise, as this releases endorphins "
                            "which help to the lower cortisol levels responsible for stress.\n\n")

        #  Every time the programme loops:
        file = open(dataset, "a")  # Initializes "file" as the CSV dataset in "append" mode
        data = csv.writer(file)  # Initializes csv.write() function as a variable
        data.writerow([minsElapsed, currentBPM, interval_slope,
                       slope_diff])  # Writes the next empty row with all current values to be stored
        file.close()  # Closes and Saves the dataset
        numRows += 1  # Adds 1 to a variable which indicates the number of rows in the dataset (excluding the header)

        print(f"\nCurrent Heart Rate: {currentBPM} BPM")  # Prints the user's current heart rate each minute
        minsElapsed += 1  # Adds 1 to a variable which indicates the programmes runtime in minutes
