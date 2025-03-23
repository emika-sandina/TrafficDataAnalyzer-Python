#Author: E.S.Yaddehige
#UOW/IIT ID: w2120242, 20231380
#Date of submission: 24/12/2024

import csv
import tkinter as tk

class HistogramApp:
    def __init__(self, date, traffic_data):
        """
        Initializes the histogram application with the traffic data and selected date.
        """
        self.date = date
        self.root = tk.Tk()
        self.traffic_data = traffic_data
        self.canvas = None  # Will hold the canvas for drawing

    def setup_window(self):
        """
        Sets up the Tkinter window and canvas for the histogram.
        """
        #Setting up a 720p window named "Histogram"
        self.root.geometry("1280x720")
        self.root.title("Histogram")

        #Setting up a canvas with a resolution of 720p to draw the histogram
        self.canvas = tk.Canvas(self.root,width=1280, height=720, bg="white")
        # Setup logic for the window and canvas

    def draw_histogram(self):
        """
        Draws the histogram with axes, labels, and bars.
        """
        elm_hourly_counts = self.traffic_data[0]
        hanley_hourly_counts = self.traffic_data[1]

        #Logic for drawing the x-axis of the histogram which includes the hours
        line_start = 30
        line_end = 1250
        self.canvas.create_line(line_start,600,line_end,600)
        self.canvas.create_text(620,650,text="Hours from 00:00 to 23:00",font=("Arial",16,"bold"))

    #Initializing the co-ordinates to display the hours

        #Creating a range from x=50 to x=1230 to display the hours in the canvas
        time_start = 50
        time_end = 1230

        #Since 00 is printed first and there are 23 numbers remaining, and 23 more gaps are required the number of pixels allocated for displaying time is divided by 23.
        time_gap = (time_end-time_start)//23

    #Initializeing the bar positions

        #Width of each bar is 20 pixels
        bar_width = 20

        #Initializing the colors for each bar and vehicle count texts.
        elm_color = "lightgreen"
        hanley_color = "red"

        #Initializing start and end points of a bar which displays counts of Elm avenue and Hanley Hwy.
        x1_elm = 30
        x2_elm = x1_elm+bar_width
        x1_hanley = x2_elm 
        x2_hanley = x1_hanley+bar_width
        
        #Since there should be 24 gaps, each gap is calculated by dividing the number of pixels allocated for the line by 24
        bar_gap = round((line_end-line_start)/24)

        #Scaler value is used to increase the size of the bar so that it is more clearer.
        max_count = max(max(elm_hourly_counts), max(hanley_hourly_counts))
        scaler_value = 400 / max_count
        
        for i in range(24):
        #Here it ensures all of the numbers from 00 to 23 gets printed by having a consistent gap among each number.    
            hour_txt = f"{i:02}"
            self.canvas.create_text(time_start, 620, text=hour_txt, font=("Arial", 10,"bold"))
            time_start += time_gap

        #Calculating the height of a bar of a particular hour based on the vehicle count by leaving equal gaps among them.(Elm Avenue)
            elm_height = elm_hourly_counts[i] * scaler_value

            #Creating bars according to the obtained height
            self.canvas.create_rectangle(x1_elm, 600 - elm_height, x2_elm, 600, fill=elm_color)
            
            #Writing the hourly counts on the center of the bars created.
            self.canvas.create_text(x1_elm+10,(600-elm_height)-10,text=elm_hourly_counts[i],font=("Arial",12),fill=elm_color)
            x1_elm += bar_gap
            x2_elm += bar_gap
        
        #Calculating the height of a bar of a particular hour based on the vehicle count by leaving equal gaps among them.(Hanley Highway)
            hanley_height = hanley_hourly_counts[i] * scaler_value

            #Creating bars according to the obtained height 
            self.canvas.create_rectangle(x1_hanley, 600 - hanley_height, x2_hanley, 600, fill=hanley_color)

            #Writing the hourly counts on the bars created
            self.canvas.create_text(x1_hanley+10,(600-(hanley_height)-10),text=hanley_hourly_counts[i],font=("Arial",12),fill=hanley_color)
            x1_hanley += bar_gap
            x2_hanley += bar_gap

            #Writing the text below the x axis.
            self.canvas.create_text(((line_end-line_start)/2)/2,30,text=f"Histogram of Vehicle Frequency per hour for {self.date}",font=("Arial",16),fill="#636363")
          # Drawing logic goes here

    def add_legend(self):
        """
        Adds a legend to the histogram to indicate which bar corresponds to which junction.
        """
        #Creating the legends and texts related to the legends.
        self.canvas.create_rectangle(40,50,60,70, fill="lightgreen")
        self.canvas.create_rectangle(40,80,60,100,fill="red")
        self.canvas.create_text(160,60,text="Elm Avenue/Rabbit Road",font=("Arial",11,"bold"),fill="#636363")
        self.canvas.create_text(160,90,text="Hanley Highway/Westway",font=("Arial",11,"bold"),fill="#636363")
         # Logic for adding a legend

    def run(self):
        """
        Runs the Tkinter main loop to display the histogram.
        """
        #Displaying the finalized canvas and window.
        self.setup_window()
        self.draw_histogram()
        self.add_legend()
        self.canvas.pack()
        self.root.mainloop()
        # Tkinter main loop logic


# Task E: Code Loops to Handle Multiple CSV Files
class MultiCSVProcessor:
    def __init__(self):
        """
        Initializes the application for processing multiple CSV files.
        """
        self.current_data = None

    def load_csv_file(self, file_path, date):
        """
        Loads a CSV file and processes its data.
        """
        try:
        #Creating dictionaries to store the counts relevant to each hour in each junction seperately.
            elm_hourly_counts = {hour:0 for hour in range(24)}
            hanley_hourly_counts = {hour:0 for hour in range(24)}

            with open(f"{file_path}","r") as csv_file:
                dataset = csv.DictReader(csv_file)
                for row in dataset:
                    #Getting Elm Avenue hourly counts
                    if row['JunctionName'] == "Elm Avenue/Rabbit Road":  
                        hour = int(row['timeOfDay'].split(":")[0])
                        elm_hourly_counts[hour] += 1

                    #Getting Hanley Hwy hourly counts
                    if row['JunctionName'] == "Hanley Highway/Westway": #if the junction name of the current row is Hanley Hwy, obtain the hour, and the count is increased relevant to that hour in the dictionary
                        hour = int(row['timeOfDay'].split(":")[0])
                        hanley_hourly_counts[hour] += 1

                #obtain the vehicle counts as lists.
                elm_hourly_counts = list(elm_hourly_counts.values())
                hanley_hourly_counts = list(hanley_hourly_counts.values())

            #Assigning the elm and hanley vehicle counts as the traffic_data
            traffic_data = [elm_hourly_counts,hanley_hourly_counts]
            return traffic_data #Returning the traffic_data
            #Processing the csv file and extracting the required data.

        #if the file is not found it will display an error message to the user and it will ask the user to continue or not.
        except FileNotFoundError:
            print("Such file does not exist, please enter a valid filename") 
          # File loading and data extraction logic

    def clear_previous_data(self):
        """
        Clears data from the previous run to process a new dataset.
        """
        self.current_data = None #Clearing the variable which contained the data
     #Clearing the traffic data object which contains the hanley and elm vehicle counts.
        print("Previous data has been cleared")

    def handle_user_interaction(self):
        """
        Handles user input for processing multiple files.
        """
         #Getting the date of the necessary file from the user.

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
        return file_path,date #Processing the necessary csv file based on the date and filepath
          # Logic for user interaction

    def process_files(self):
        """
        Main loop for handling multiple CSV files until the user decides to quit.
        """
        def continue_or_not():
            #Looping the program to load a new dataset
            while True:
                validation = input("Do you want to enter another dataset?(Y/N): ").strip().upper()
                if validation == "Y":
                    self.clear_previous_data() #Clear the earlier data if the user wants to move on to a new dataset.
                    return True
                elif validation == "N": #Exiting the program by giving an exit message if the user enters "N"
                    print("Exiting the program, Thank You! ")
                    exit()
                    return False
                else:
                    print("Invalid input, Please enter Y or N")
                #Loop logic for handling multiple files
                
        (file_path,date) = self.handle_user_interaction()
        traffic_data = self.load_csv_file(file_path,date)
        if traffic_data:
            self.current_data = traffic_data
            app = HistogramApp(date,traffic_data)
            app.run()

        #The program keeps on looping until the user enters "N"
        while continue_or_not():
            (file_path,date) = self.handle_user_interaction()
            traffic_data = self.load_csv_file(file_path,date)
            if traffic_data:
                app = HistogramApp(date,traffic_data)
                app.run()

 #Calling the processor
processor = MultiCSVProcessor()
processor.process_files()
#calling the necessary functions
