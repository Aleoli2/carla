import json
import os
import sys

def calculate_folder_average(folder_path, prefix):
    
    sum_values = {"pedestrian": 0,"static": 0,"slight_collision": 0,"safety_stops": 0, "driving_time":0}
    sum_weighted_values = {"route_completion": 0.0,"infraction_penalty": 0.0,"driving_score": 0.0,"pedestrian_metric_mean": 0.0,
                           "robot_traj_metric": 0.0}
    total_length=0
    average = {"pedestrian": 0,"static": 0,"slight_collision": 0,"safety_stops": 0,"route_completion": 0.0,"infraction_penalty": 0.0,
               "driving_score": 0.0,"pedestrian_metric_mean": 0.0,"pedestrian_metric_min": 1.0,"robot_traj_metric": 0.0, "driving_time":0}
    #The metric pedestrian_metric_min is not averaged, we save the minimum value
    # Get the list of files in the folder
    files = [file for file in os.listdir(folder_path) if (file.startswith(prefix))]
    total_values = len(files)
    for file in files:
        file_path = os.path.join(folder_path, file)
        # Read the JSON file
        with open(file_path, 'r') as f:
            data = json.load(f)

            route_length = data["route_lenght"]
            total_length+=route_length

            for key in sum_values.keys():
                value = data[key]
                sum_values[key] += value

            for key in sum_weighted_values.keys():
                value = data[key]*route_length
                sum_weighted_values[key] += value

            if average["pedestrian_metric_min"]>data["pedestrian_metric_min"]:
                average["pedestrian_metric_min"]=data["pedestrian_metric_min"]
            
    print("Total lenght ",total_length)
    # Calculate the average
    if total_values > 0:
        for key in sum_values.keys():
            average[key] = sum_values[key]/(total_length/1000.0) #Calculate collisions per km 
        average["driving_time"]*=(total_length/1000.0) #Correct driving time
        for key in sum_weighted_values.keys():
            average[key] = sum_weighted_values[key]/total_length
        return average
    else:
        return None
    

# Check if command-line arguments are provided
if len(sys.argv) != 2:
    print("Usage: python script.py folder_prefix")
    sys.exit(1)

# Parse command-line arguments
folder, prefix = sys.argv[1].split("/")

# Calculate and display the average
average_result = calculate_folder_average(folder, prefix)

if average_result is not None:
    file_path = os.path.join(folder,"average", prefix+"_average.json")
    file = open(file_path,"w")
    json.dump(average_result,file,indent="\t")
    file.close()
    print(f"The average of values in the folder is: {average_result}")
else:
    print(f"No files with the specified folder and prefix were found.")