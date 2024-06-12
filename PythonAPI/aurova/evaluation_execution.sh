#!/bin/bash

# Execution of the test automatically. The agent must be running in the docker.

# Function to handle interruption
function handle_interrupt {
    echo "Interrupt received. Ending processes..."

    kill -s SIGINT $pid1 $pid2

    exit 1
}

start_test=0
wait_launch=14
output=thinktwice
architecture=thinktwice
pedestrian_routes_prefix=routes/pedestrian_routes/

#Town01
# way_id=(6 8 9 10 11 12 14)
# pedestrian_routes=(Town01_evaluation1.xml Town01_evaluation2.xml Town01_evaluation3.xml Town01_evaluation4.xml Town01_evaluation4.xml Town01_evaluation4.xml  Town01_evaluation5.xml)

# Town02
# way_id=(1 2 3 4 5 6 7 8 9 10 11)
# pedestrian_routes=(Town02_evaluation1.xml Town02_evaluation1.xml Town02_evaluation1.xml Town02_evaluation1.xml Town02_evaluation1.xml Town02_evaluation1.xml Town02_evaluation1.xml Town02_evaluation1.xml Town02_evaluation2.xml Town02_evaluation2.xml Town02_evaluation2.xml)

#Town03
# way_id=(-1)
# pedestrian_routes=(Town03_evaluation1.xml)

#Town04
# way_id=(2 3 4 5)
# pedestrian_routes=(Town04_evaluation1.xml Town04_evaluation1.xml Town04_evaluation1.xml Town04_evaluation1.xml)

#Town05
way_id=(2 3 4 5 6 7 8)
pedestrian_routes=(Town05_evaluation1.xml Town05_evaluation1.xml Town05_evaluation1.xml Town05_evaluation1.xml Town05_evaluation1.xml Town05_evaluation1.xml Town05_evaluation1.xml)


for ((i=$start_test; i<${#way_id[@]}; i++))
do
    echo "Test way ${way_id[$i]}"

    # Execute the python files
    if [ "$architecture" = "ROS" ]; then
        map=/media/alolivas/MSI_500/aurova_carla/carla/PythonAPI/aurova/routes/Town01.xml
        roslaunch app_old nav_carla.launch map:=$map way:=${way_id[$i]} &
        pid1=$!

        sleep $wait_launch
        
        python pedestrians_fixed_routes.py --output $output -c --pedestrian_routes $pedestrian_routes_prefix${pedestrian_routes[$i]} --way_id ${way_id[$i]} &
        pid2=$!

    else
        python listener_agent.py --architecture $architecture --way_id ${way_id[$i]} &
        pid1=$!

        sleep $wait_launch

        python pedestrians_fixed_routes.py --output $output -s --pedestrian_routes $pedestrian_routes_prefix${pedestrian_routes[$i]} --way_id ${way_id[$i]} &
        pid2=$!
    fi

    # Wait the end of the route
    wait $pid2

    sleep $wait_launch

    kill -s SIGINT $pid1

    wait

    if [ "$architecture" = "ROS" ]; then
        wmctrl -a aurova_carla
        read -p "Change the close_loop and press enter"
    fi
  
done
wmctrl -a aurova_carla

