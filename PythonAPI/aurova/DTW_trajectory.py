#Calculate the similarity between two trajectories, saving the metric in the second json file.
import sys
import os
import numpy as np
import json
from dtaidistance import dtw_ndim
from utils import *


def main(exp1, exp2, route_file):
    with open(exp1+".json","r") as fp1, open(exp2+".json","r") as fp2:
        data1=json.load(fp1)
        data2=json.load(fp2)
    traj1=np.loadtxt(exp1+"_trajectory.csv",delimiter=",")
    traj2=np.loadtxt(exp2+"_trajectory.csv",delimiter=",")

    #Compare the same route completation
    route = ReadRouteFromXML(route_file)
    route_length=[]
    for id in range(1,len(route["way"])):
        node, previous=route["way"][id], route["way"][id-1]
        x, y=route["nodes"][node][0]-route["nodes"][previous][0], route["nodes"][node][1]-route["nodes"][previous][1]
        route_length.append(math.sqrt(x**2+y**2))
    total_length = sum(route_length)
    percentage = [lenght/total_length for lenght in route_length]
    
    if data2["route_completion"]<data1["route_completion"]:
        for id,n in enumerate(percentage):
            if data1["route_completion"]<n:
                node = route["way"][id]
                target = np.array(route["nodes"][node])*(data2["route_completion"]/n)
                break
        for i in range(len(traj1)-1,0,-1):
            dist=math.sqrt((traj1[i][0]-target[0])**2+(traj1[i][1]-target[1])**2)
            if dist<2.0:
                traj1=traj1[:i]
                break
    elif data1["route_completion"]<data2["route_completion"]:
        for id,n in enumerate(percentage):
            if data1["route_completion"]<n:
                node = route["way"][id]
                target = np.array(route["nodes"][node])*(data1["route_completion"]/n)
                break
        for i in range(len(traj2)-1,0,-1):
            dist=math.sqrt((traj2[i][0]-target[0])**2+(traj2[i][1]-target[1])**2)
            if dist<2.0:
                traj2=traj2[:i]
                break
    d = dtw_ndim.distance(traj1, traj2)
    print("Dynamic time warping(DTW) ",d)
    data2["DTW"]=d
    with open(exp2+".json","w") as fp:
        json.dump(data2,fp, indent="\t")

if __name__ == "__main__":
    if (len(sys.argv)<4):
        print("USAGE: python DTW_trajectory.py experiment_name1 experiment_name2 route_file\n\t"+
              "There must be the files experiment_name.json and experiment_name_trajectory.csv")
        exit(0)
    exp1, exp2=sys.argv[1], sys.argv[2]
    route_file=sys.argv[3]
    if(not os.path.exists(exp1+".json") or not os.path.exists(exp1+"_trajectory.csv")
       or not os.path.exists(exp2+".json") or not os.path.exists(exp2+"_trajectory.csv")
       or not os.path.exists(route_file)):
        print("USAGE: python DTW_trajectory.py ground_truth experiment_name route_file\n\t"+
              "There must be the files experiment_name.json and experiment_name_trajectory.csv\n\t")
        exit(0)
    main(exp1,exp2, route_file)