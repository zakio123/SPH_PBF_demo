import numpy as np
import math
from const import *
class Particle:
    def __init__(self,r,v = np.zeros(3), r_pre=np.zeros(3),f=np.array([0,-9.8,0]),d=0.0,n=0,a=1,neighbor=[],area = 0,l=0.0):
        self.r = r
        self.f = f
        self.n = n
        self.d = d
        self.r_pre = r_pre
        self.neighbor = neighbor
        self.area = area
        self.l = l
        self.v = v

    def checkarea(self):
        r = self.r 
        area_x = 0
        area_y = 0
        area_z = 0
        for n in range(divide_x):
            if (r[0] > dx * n):
                area_x = n
            else :
                break
        for n in range(divide_y):
            if (r[1] > dy * n):
                area_y = n
            else :
                break
        for n in range(divide_z):
            if (r[2] > dz * n):
                area_z = n
            else :
                break
        self.area = int(area_x + area_y * divide_x + area_z * square)
    
    def update_predict_positon(self):
        self.v += self.f * dt
        self.r_pre = self.r + self.v * dt
        self.checkarea_pre()
        return self
    
    def update_positon_velocity(self):
        self.v = (self.r_pre - self.r) / dt
        self.r = self.r_pre
        return self
    def checkarea_pre(self):
        r = self.r_pre
        area_x = 0
        area_y = 0
        area_z = 0
        for n in range(divide_x):
            if (r[0] > dx * n):
                area_x = n
        for n in range(divide_y):
            if (r[1] > dy * n):
                area_y = n
        for n in range(divide_z):
            if (r[2] > dz * n):
                area_z = n
        self.area = int(area_x + area_y * divide_x + area_z * square)
    
    def kernel(self,particle):
        c = 315 / (64 * math.pi * math.pow(h,9))
        r = self.r_pre - particle.r_pre
        dist = r[0] * r[0] + r[2] * r[2] + r[1] * r[1]
        x = h_2 - dist
        if (x < 0):
            return 0
        else :
            return c * math.pow(x,3)
    
    def kernel_gr(self,particle):
        c = - 45 / (math.pi * math.pow(h,6))
        r = self.r_pre - particle.r_pre
        dist = np.sqrt(r[0] * r[0] + r[1] * r[1] + r[2] * r[2]); 
        x = h - dist
        if (x < 0):
            return 0
        else :
            return (c * math.pow(x,2) / dist) * r
    
    def consist(self):
        return self.d / density0 - 1
    
def init(suc):
    particle_list = []
    # 流体粒子の生成
    if (suc):
        r_data = np.load(r_file_name)
        v_data = np.load(v_file_name)
        r_last = r_data[len(r_data)-1]
        for i in range(N_f):
            r = r_last[i]
            v = v_data[i]
            r_pre = r_last[i]
            f = np.array([0,-9.8,0])
            neighbor = []
            particle = Particle(r=r,v=v,f=f,r_pre = r_pre,d=0.0,n=i,neighbor=neighbor,area=0,l=0)
            particle.checkarea()
            particle_list.append(particle)
            
    else :
        for i in range(N_f):
            r = np.array([particle_size * (4 + int(i % px)),particle_size * (10 + int(i / (px * pz))),particle_size * (4 + int (i % (px * pz) / px))])
            v = np.zeros(3)
            u = np.zeros(3)
            r_pre = np.zeros(3)
            f=np.array([0,-9.8,0])
            neighbor = []
            particle = Particle(r=r,v=v,f=f,r_pre = r_pre,d=0.0,n=i,neighbor=neighbor,area=0,l=0)
            particle.checkarea()
            particle_list.append(particle)
    
    # 壁粒子の生成
    count = N_f
    for k in range(int(ny)):
        for j in range(int(nz)):
            for i in range(int(nx)):
                if (k < 4):
                    r = np.array([i * particle_size,k * particle_size,j * particle_size ])
                else :
                    if ((i > 3 and i < nx - 4) and (j > 3 and j < nz - 4)):
                        continue
                    else :
                        r = np.array([i * particle_size,k * particle_size,j * particle_size ])
                neighbor =[]
                v = np.zeros(3)
                f = np.zeros(3)
                r_pre = r
                wall = Particle(r=r,f=f,v=v,r_pre = r_pre,d=0.,n=count,neighbor=neighbor,area=0,l=0)
                wall.checkarea()
                count += 1
                particle_list.append(wall)
    
    # 棒粒子の生成
    x = int(nx / 2)
    y = int(ny / 2)
    z = int(nz)
    for i in range(N_ball):
        r = np.array([(x + 0.5) * particle_size,(y + 0.5) * particle_size,(z-i) * particle_size])
        v = np.array([0,0,0])
        u = np.zeros(3)
        f = np.array([0,0,0])
        stick = Particle(r=r,f=f,d=0,n=count,a=1,neighbor=neighbor,area=0)
        stick.checkarea()
        count += 1
        particle_list.append(stick)
    return particle_list
