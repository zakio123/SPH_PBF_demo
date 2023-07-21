import sys
import os
import math
import numpy
# 定数たち

particle_size = 0.01
AX = 0.2
AY = 0.5
AZ = 0.2
ALL_AREA = [AX,AY,AZ]
WALL_AREA = [AX,AY-0.32,AZ]

# 領域の分割数
divide_x = int(AX / (2 * particle_size))
divide_y = int(AY / (2 * particle_size))
divide_z = int(AZ / (2 * particle_size))
dx = 2 * particle_size
dy = 2 * particle_size
dz = 2 * particle_size
suc = False
arg = sys.argv
if (len(arg) == 4):
    name = arg[3]
    r_file_name = f'data/result_{name}.npy'
    v_file_name = f'data/result_V_{name}.npy'
    u_file_name = f'data/result_U_{name}.npy'
    N_f = int(arg[1])
    iter = int(arg[2])
    suc = True
if (len(arg) == 3):
    N_f = int(arg[1])
    iter = int(arg[2])
if (len(arg) == 2):
    N_f = int(arg[1])    
    iter = 100
if (len(arg) == 1):
    N_f = 1000
    iter = 100
#シミュレーションの設定パラメータ
dt = 0.001

N_ball = 0
V = 1

nx = WALL_AREA[0] / particle_size
ny = WALL_AREA[1] / particle_size
nz = WALL_AREA[2] / particle_size
px = int((int(nx) - 8) / 2)
py = int(ny) - 4
pz = int(nz) - 8
h = particle_size * 1.5
stiffness = 100
density0 = 1000
viscosity = 1
mass_pa = particle_size * particle_size * particle_size * density0

h_2 = h * h
k_0 = 0
myu = 1
gravity = 9.8



C_spiky = 45 / (math.pi * math.pow(h,6))
C_grav = gravity
C_dens = 315 / (64 * math.pi * math.pow(h,9))
gamma = 3.0
N_wall = (nx * nz) * 4 + (nz * (ny - 4)) * 4 * 2 + ((nx - 8) * (ny - 4)) * 4 * 2
square = divide_x * divide_y
box = divide_z * square
near = [0,-1,1,-divide_x,divide_x,-1-divide_x,-1+divide_x,1-divide_x,1+divide_x,
        0+square,-1+square,1+square,-divide_x+square,divide_x+square,-1-divide_x+square,-1+divide_x+square,1-divide_x+square,1+divide_x+square,
        0-square,-1-square,1-square,-divide_x-square,divide_x-square,-1-divide_x-square,-1+divide_x-square,1-divide_x-square,1+divide_x-square]
m = 0.01 * h * h