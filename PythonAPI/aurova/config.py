#Config file for variables used by multiple files

PATH_DATASET = "/home/alolivas/aurova-lab/labrobotica/dataset/CARLA_dataset/Town05_experiment2_session"
ROUTE_FILENAME = "./routes/Town01.xml"
PEDESTRIANS_ROUTES_FILE="routes/pedestrian_routes/Town01_evaluation1.xml"
WAY_ID = 6 #None first way. The robot starts in the first node of the way.

PENALTY_COLLISION_SLIGHT=0.9
PENALTY_COLLISION_STATIC=0.65
PENALTY_COLLISION_PEDESTRIAN=0.5
PENALTY_OFF_ROAD=0.7 #In this case the penalty is on "cars" road driving, except pedestrian crossing. Therefore, we penalize every crossed road line.
TIME_DISTANCE_COEFFICIENT = 3 #Coefficient for determining the max trajectory time
MAX_TIME_LOCAL_MINIMUM = 30 #Seconds
MINIMUM_DISTANCE = 3.0
DISTANCE2PEDESTRIAN = 1.0 #Distance to the pedestrian in the direction of movement to consider that it has been avoided.
PATH_RESULTS ="/media/alolivas/MSI_500/aurova_carla/carla/PythonAPI/aurova/results_no_runner/"

#Ackermann control configuration
MAX_SPEED=1.3 # m/s
MAX_STEERING_ANGLE = 24 # degrees
KP = 2.0
KI = 0.5
KD = 0.5

DEG2RAD = 3.1415927/180.0
FPS=10