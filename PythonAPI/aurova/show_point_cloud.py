import os
import open3d as o3d
import numpy as np
import time

def plot_point_cloud(folder_path):
    files = os.listdir(folder_path)
    num_files = len(files)

    # Crear una figura 3D
    vis = o3d.visualization.Visualizer()
    vis.create_window()
    
    for i in range(1, num_files + 1):
        file_name = f"{i}.npy"
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            file_path = os.path.join(folder_path, file_name)
            cloud = np.load(file_path)[:,:3]  # Cargar datos del archivo

            pcd = o3d.geometry.PointCloud()
            pcd.points = o3d.utility.Vector3dVector(cloud)
            if i%10==0:
                vis.destroy_window()
                o3d.visualization.draw_geometries([pcd])
                vis = o3d.visualization.Visualizer()
                vis.create_window()
            vis.add_geometry(pcd)
            # vis.update_geometry(pcd)
            vis.poll_events()
            vis.update_renderer()
            time.sleep(0.1)
            vis.remove_geometry(pcd)

    vis.destroy_window()

# Ruta de la carpeta que contiene los archivos de la nube de puntos
folder_path = '/home/alolivas/aurova-lab/labrobotica/dataset/CARLA_dataset/Town01_session1/lidar'  # Cambiar por la ruta correcta

plot_point_cloud(folder_path)