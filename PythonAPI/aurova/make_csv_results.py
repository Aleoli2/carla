import json
import os
import sys

def write_table(output_file, folder_path):

    # Get the list of files in the folder
    files = [file for file in os.listdir(folder_path) if file.endswith(".json")]
    for file in files:
        file_path = os.path.join(folder_path, file)

        # Read the JSON file
        with open(file_path, 'r') as f:
            data = json.load(f)
            output_file.write("{},{:.2f},{:.2f},{:.2f},{:.2f},{:.2f},{:.2f},{:.2f},{:.3f},{:.3f}\n".format(
                file,data["driving_score"], data["route_completion"],
                data["infraction_penalty"], data["pedestrian"],
                data["static"], data["slight_collision"],
                data["safety_stops"], data["pedestrian_metric_mean"],
                data["robot_traj_metric"]
            ))
            

# Check if command-line arguments are provided
if len(sys.argv) != 2:
    print("Usage: python script.py folder")
    sys.exit(1)

# Parse command-line arguments
folder = sys.argv[1]

file_path = os.path.join(folder,"table.csv")
file = open(file_path,"w")
file.write("model,drivingScore,routeCompletation,infractionPenalty,pedestrian,static,slight,safetyStops,pedestrianMetricMean,robotTrajMetric\n")

# Calculate and display the average
average_result = write_table(file, folder)

file.close()