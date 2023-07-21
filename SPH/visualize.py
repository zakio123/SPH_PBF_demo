import open3d as o3d
import numpy as np
import sys
import time
arg = sys.argv
# 点群データの読み込み
point_clouds = np.load(f'data/result_{arg[2]}_{arg[1]}.npy')

# Open3DのPointCloudオブジェクトを作成
pcd_fluids = o3d.geometry.PointCloud()
pcd_wall = o3d.geometry.PointCloud()
pcd_stick = o3d.geometry.PointCloud()
n = 0.5
points = [[0, 0, 0],[n, 0, 0],[0, n, 0],[n, n, 0],[0, 0, n],[n, 0, n],[0, n, n],[n, n, n],]

#print(points)
lines = [[0, 1],[0, 2],[1, 3],[2, 3],[4, 5],[4, 6],[5, 7],[6, 7],[0, 4],[1, 5],[2, 6],[3, 7],]
colors = [[1, 0, 0] for i in range(len(lines))]
line_set = o3d.geometry.LineSet(
        points=o3d.utility.Vector3dVector(points),
        lines=o3d.utility.Vector2iVector(lines),)
line_set.colors = o3d.utility.Vector3dVector(colors)

# 可視化ウィンドウを作成
vis = o3d.cpu.pybind.visualization.Visualizer()

vis.create_window()
vis.add_geometry(line_set)
pcd_wall.points = o3d.utility.Vector3dVector(point_clouds[0][int(arg[2]):len(point_clouds[0])-6])
pcd_wall.paint_uniform_color([1,0.9,0.9])
vis.add_geometry(pcd_wall)
# アニメーションフレームごとの処理
pcd_fluids.paint_uniform_color([16/255,156/255,16/255])
time.sleep(5)
for i, points in enumerate(point_clouds):
    # 点群データをPointCloudオブジェクトにセット
    pcd_fluids.points = o3d.utility.Vector3dVector(points[0:int(arg[2])])
    # 点群を可視化
    vis.add_geometry(pcd_fluids)
    # 可視化ウィンドウを更新
    vis.update_geometry(pcd_fluids)
    vis.poll_events()
    vis.update_renderer()
vis.destroy_window()

