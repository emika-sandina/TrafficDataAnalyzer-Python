#Author:E.S.Yaddehige
#Date:03/11/2023
#Student ID:20231380/w2120242
import csv
# Task A: Input Validation
#Getting the day,month and year in which the traffic data are required of.
def validate_date_input():
    #The program will be looped through a "while True" loop if the user enters a day less than 0 or more than 31 or if a string value is entered.
    days_in_a_month = [0,31,28,31,30,31,30,31,31,30,31,30,31]
    #0 th index in the list is 0 because the program does not allow to input 0 as the month.
    while True:
        try:
            day = int(input("Please enter the day of the survey in the format dd:"))
            if 1 <= day <= 31:
                break
            else:
                print("Out of range - values must be in the range 1 and 31.")
              
        except:
            print("Integer required")

    #The program will be looped through a "while True" loop if the user enters a month less than 0 or more than 12 or if a string value is entered.
    while True:
        try:
            month = int(input("Please enter the month of the survey in the format MM:"))
            if 1 <= month <= 12:
                break
            else:
                print("Out of range - values must be in the range 1 and 12.")
            
        except:
            print("Integer required")
    #The program will be looped through a "while True" loop if the user enters a year less than 2000 or more than 2024 or if a string value is entered.
    while True:
        try:
            year = int(input("Please enter the year of the survey in the format YY:"))
            if 2000 <= year <= 2024:
                break

            else:
                print("Out of range - values must be in the range 2000 and 2024.")

        except:
            print("Integer required")

    #Getting the maximum number of days in February as 29 if the entered year is a leap year.
    is_leap_year = (year%4==0)
    if is_leap_year == True:
        days_in_a_month[2] = 29

    #Looping the program to get the day again, if the user enters a day greater than the possible maximum number of days for the respective month.
    while day > days_in_a_month[month]:
        print(f"Invalid day.There are only {days_in_a_month[month]} days for the month you entered.")
        try:
            day = int(input("Please enter the day of the survey in the format dd:"))

        except:
            print("Integer Required")
        
    #Zero formatting is carried out so that there will be no errors in reading the file if the user enters a day or month less than 10. 
    day = f"{day:02d}"
    month = f"{month:02d}"

    #The file name is obtained through the day,month and year entered by the user
    file_path = f"traffic_data{day}{month}{year}.csv"
    date = f"{day}/{month}/{year}"
    #The file name is being returned to the caller
    return file_path,date

def validate_continue_input():
    #Looping the program if the user wants to load another set of data.
    while True:
        validation = input("Do you want to enter another dataset?(Y/N): ").strip().upper()
        if validation == "Y":
            return True
        elif validation == "N":
            print("Exiting the program, Thank You! ")
            return False
        else:
            print("Invalid input, Please enter Y or N")


# Task B: Processed Outcomes

#Reading the csv file row by row and appending to a list named vehicle_details
def process_csv_data(file_path):
    try:
        vehicle_details = []        
        read_csv = open(f"{file_path}", mode="r")
        #Reads all of the rows in the csv file
        reader = csv.DictReader(read_csv)
        for dataset in reader:
            vehicle_details.append(dataset)

        #Assignment of variables and additional lists to calculate time related values
        total_vehicles = len(vehicle_details)
        total_trucks = 0
        total_electric = 0
        total_twowheeled = 0
        bussesleaving_elm_heading_north = 0
        notleft_right = 0
        truck_percentage = 0
        total_bicycles = 0
        bicycles_perhour = 0
        over_speedlimit = 0
        only_elmavenue = 0
        only_hanleyhwy = 0
        elm_scooters = 0
        elm_scooter_percentage = 0
        peaktimes_hanleyhwy = 0
        peaktimecounter_hanley = 0
        times = []
        rain_hours = []

        #Going through the list containing all of the details using a for loop 
        for row in vehicle_details:
            if row['VehicleType'] == "Truck": #Getting the total truck count
                total_trucks += 1
            if row['elctricHybrid'] == "True": #Getting the count of total electric vehicles
                total_electric += 1
            if row['VehicleType'] == "Motorcycle" or row['VehicleType'] == "Scooter" or row['VehicleType']=="Bicycle": #Getting the count of two wheeled vehicles if they are either a motorcycle,scooter a bicycle
                total_twowheeled += 1
            if row['JunctionName'] == "Elm Avenue/Rabbit Road" and row['travel_Direction_out'] == "N" and row['VehicleType'] == "Buss": #Getting the count of buses leaving Elm Avenue and heading North direction 
                bussesleaving_elm_heading_north += 1
            if row['travel_Direction_in'] == row['travel_Direction_out']: #Getting the count of vehicles that went straight without turning left or right
                notleft_right += 1
            if float(row['VehicleSpeed']) > float(row['JunctionSpeedLimit']):#Getting the count of vehicles that went over the speed limit
                over_speedlimit += 1
            if row['JunctionName'] == "Elm Avenue/Rabbit Road": #Getting the count of total vehicles that went through Elm avenue.
                only_elmavenue += 1
            if row['JunctionName'] == "Hanley Highway/Westway": #Getting the count of total vehicles that went through Hanley Highway
                only_hanleyhwy += 1
            if row['JunctionName'] == "Elm Avenue/Rabbit Road" and row['VehicleType'] == "Scooter": #Getting the total number of scooters that went through Elm Avenue
                elm_scooters += 1
            if row['VehicleType'] == "Bicycle": #Getting the count of total number of bicycles
                total_bicycles += 1
            if row['JunctionName'] == "Hanley Highway/Westway": #Getting the hours that vehicles were observed in Hanley Highway 
                hour = int(row['timeOfDay'].split(":")[0])
                times.append(hour)
            if "Rain" in row['Weather_Conditions']: #Getting the hours that rain was observed during the day
                hour = int(row['timeOfDay'].split(":")[0])
                rain_hours.append(hour)
                       
        #The rain hours list is converted into a set so that it will be easier to calculate the hours of rain as the duplicate values will be eliminated.
        rain_hours = set(rain_hours)
        #Handling ZeroDivision errors which would happen if any one of the vehicle counts is 0.
        try:
            truck_percentage = round(total_trucks/total_vehicles*100)
        except ZeroDivisionError:
            truck_percentage = 0
        try:
            bicycles_perhour = round(total_bicycles/24)
        except ZeroDivisionError:
            bicycles_perhour = 0
        try:
            elm_scooter_percentage = round((elm_scooters/only_elmavenue)*100)
        except ZeroDivisionError:    
            elm_scooter_percentage = 0

        #The list is converted into a set to eliminate duplicate values and the values in the set are used to calculate the occurences of a particular value within the original list.
        #The most frequently occuring value will be consdiered as the busiest hour.

        busiest_hour = max(set(times), key=times.count)
        busiest_hour = int(busiest_hour)
        next_busiest_hour = str(int(busiest_hour) + 1)
        peaktimes_hanleyhwy = f"Between {busiest_hour}:00 and {next_busiest_hour}:00"

        #To calculate the most no.of vehicles seen in an hour in Hanley, a count of the number of vehicles gone during the peak hour is obtained.
        for values in times:
            if values == busiest_hour:
                peaktimecounter_hanley += 1

        #The list consists of all of the required information 
        outcomes = [file_path,total_vehicles,total_trucks,total_electric,total_twowheeled,bussesleaving_elm_heading_north,notleft_right,
                  truck_percentage,bicycles_perhour,over_speedlimit,only_elmavenue,only_hanleyhwy,
                  elm_scooter_percentage,peaktimecounter_hanley,peaktimes_hanleyhwy,len(rain_hours)]
        return outcomes

    #An error will be displayed to the user, if there is no file with the date given by the user
    except:
        print("Such file does not exist please enter a valid file name")
        return None

def display_outcomes(outcomes):
    #Here the results are only being displayed if the list named "outcomes" is created otherwise it will show an error message to the user.
    if outcomes:
        outcomes = f"""

data file selected is {outcomes[0]}

The total number of vehicles recorded for this date is {outcomes[1]}
The total number of trucks recorded for this date is {outcomes[2]}
The total number of electric vehicles for this date is {outcomes[3]}
The total number of two-wheeled vehicles for this date is {outcomes[4]}
The total number of Busses leaving Elm Avenue/Rabbit Road heading North is {outcomes[5]}
The total number of Vehicles through both junctions not turning left or right is {outcomes[6]}
The percentage of total vehicles recorded that are trucks for this date is {outcomes[7]}%
The average number of Bikes per hour for this date is {outcomes[8]}
The total number of Vehicles recorded as over the speed limit for this date is {outcomes[9]}
The total number of Vehicles recorded through Elm Avenue/Rabbit Road junction is {outcomes[10]}
The total number of vehicles recorded through Hanley Highway/Westway junction is {outcomes[11]}
{outcomes[12]}% of vehicles recorded through Elm Avenue/Rabbit Road are scooters.
The highest number of vehicles in an hour on Hanley Highway/Westway is {outcomes[13]}
The most vehicles through Hanley Highway/Westway were recorded between {outcomes[14]}
The number of hours of rain for this date is {outcomes[15]}
                
****************************************************
                """
        print(outcomes)
        return outcomes
    else:
        print("No results to be displayed")


# Task C: Save Results to Text File
def save_results_to_file(outcomes, file_name="results.txt"):
    with open(f"{file_name}","a") as text_file:
        text_file.write(f"{outcomes}")

    text_file.close()

# if you have been contracted to do this assignment please do not remove this line
file_path, date = validate_date_input()
outcomes = process_csv_data(file_path)
if outcomes:
    outcomes = display_outcomes(outcomes)
    save_results_to_file(outcomes,file_name="results.txt")

while validate_continue_input():
    file_path, date = validate_date_input()
    outcomes = process_csv_data(file_path)
    if outcomes:
        outcomes = display_outcomes(outcomes)
        save_results_to_file(outcomes,file_name="results.txt")



#References:
	#GeeksforGeeks. (2024, September 17). Python | Find most frequent element in a list. GeeksforGeeks. https://www.geeksforgeeks.org/python-find-most-frequent-element-in-a-list/
	#GeeksforGeeks. (2024a, June 20). Reading CSV files in Python. GeeksforGeeks. https://www.geeksforgeeks.org/reading-csv-files-in-python/?ref=header_outind




    