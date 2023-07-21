from const import *
import numpy as np
class Partial:
    def __init__(self,r,v=np.zeros(3),f=np.zeros(3),d=0.0,p=0.0,n=0,a=1,u=np.zeros(3),neg=[],area = 0):
        self.r = r
        self.v = v
        self.u = u
        self.f = f
        self.n = n
        self.d = d
        self.p = p
        self.a = a
        self.neg = neg
        self.area = area

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

def init(suc):
    partial_list = []
    # 流体粒子の生成
    if (suc):
        r_data = np.load(r_file_name)
        u_data = np.load(u_file_name)
        v_data = np.load(v_file_name)
        r_last = r_data[len(r_data)-1]
        for i in range(N_f):
            r = r_last[i]
            v = v_data[i]
            u = u_data[i]
            f = np.zeros(3)
            neg = []
            partial = Partial(r=r,v=v,f=f,d=0.0,p=0.0,n=i,a=1,u=u,neg=neg,area=0)
            partial.checkarea()
            partial_list.append(partial)
            
    else :
        for i in range(N_f):
            r = np.array([particle_size * (4 + int(i % px)),particle_size * (10 + int ((i / (px * pz)))),particle_size * (4 + int ((i % (px * pz)) / px))])
            v = np.zeros(3)
            u = np.zeros(3)
            f = np.zeros(3)
            neg = []
            partial = Partial(r=r,v=v,f=f,d=0.0,p=0.0,n=i,a=1,u=u,neg=neg,area=0)
            partial.checkarea()
            partial_list.append(partial)
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
                neg =[]
                v = np.zeros(3)
                u = np.zeros(3)
                f = np.zeros(3)
                wall = Partial(r=r,v=v,u=u,f=f,d=0.,p=0.,n=count,a=0,neg=neg,area=0)
                wall.checkarea()
                count += 1
                partial_list.append(wall)
    print(count)
    # 某粒子の生成
    x = int(nx / 2)
    y = int(ny / 2)
    z = int(nz)
    
    # for i in range(N_ball):
    #     r = np.array([(x + 0.5) * particle_size,(y + 0.5) * particle_size,(z-i) * particle_size])
    #     v = np.array([0,0,0])
    #     u = np.zeros(3)
    #     f = np.array([0,7.5,0])
    #     wall = Partial(r=r,v=v,u=u,f=f,d=0.,p=0.,n=count,a=1,neg=neg,area=0)
    #     wall.checkarea()
    #     count += 1
    #     partial_list.append(wall)
    return partial_list