import math
import numpy as np
from multiprocessing import Pool
from const import *
from particle import init 
from util import kernel,distance

if __name__ == '__main__':
    partial_list = init(suc)
    result = []
    #　密度場と圧力の計算
    def updata_pressure(i):
        n = i.n
        i.d = 0.0
        i.neg = []
        for k in near:
            darea = i.area + k
            if (darea < 0):
                continue
            if (darea >= box):
                continue
            else :
                for m in area_particle[darea]:
                    j = partial_list[m]
                    dw = kernel(C_dens,i.r,j.r)
                    if (dw > 0):
                        i.neg.append(j.n)
                        i.d += dw * mass_pa
        if (i.d > density0):
            i.p = k_0 * (i.d - density0) + stiffness * (i.d - density0)
        else :
            i.p =  k_0 * (i.d - density0)
        return i

    def updata_f(i):
        sum_press = np.zeros(3)
        sum_visco = np.zeros(3)
        for n in i.neg:
            j = partial_list[n]
            dist = distance(i.r,j.r)
            r_ij = i.r - j.r
            if (j.n != i.n):
                #TODO
                r = np.sqrt(dist)
                if (r == 0):
                    print(i.r,j.r,i.n,j.n)
                v_ji = j.v - i.v
                tmp = h - np.sqrt(dist)
                interact_press = mass_pa * (j.p / (j.d * j.d) + i.p / (i.d * i.d))
                sum_press +=  C_spiky * interact_press * (tmp * tmp / r) * r_ij
                tmp_ = r_ij.dot((tmp * tmp / r) * r_ij)
                sum_visco += C_spiky * mass_pa * (2 * myu) * tmp_  * v_ji / (j.d * i.d * (m + dist)) 
        i.f = sum_press + sum_visco + np.array([0,-C_grav,0])
        return i
    
    def updata_pos(i):
            i.u += i.f * dt
            i.r += i.u * dt 
            i.v = i.a * (i.u + 0.5 * i.f * dt)
            i.checkarea()
            return i
    
    for i in range(N_f):
        partial_list[i].u = np.zeros(3)
    U = np.zeros((N_f+int(N_wall)+N_ball,3))
    V = np.zeros((N_f+int(N_wall)+N_ball,3))
    for k in range(iter):
        print(k)
        R = np.zeros((N_f+int(N_wall)+N_ball,3))
        
        area_particle = []
        for _ in range(box):
            area_particle.append([])
        #粒子の位置、速度、変位の結果を保存
        for i in partial_list:
            n = i.n
            R[n] = i.r
            V[n] = i.v
            U[n] = i.u
            area_particle[i.area].append(n)
        with Pool(12) as p:
            partial_list = p.map(updata_pressure, partial_list)
        #　粒子に働く力fの更新
        fluids = partial_list[0:N_f]
        with Pool(12) as p:
            fluids = p.map(updata_f, fluids)
        
        # 位置の更新
        with Pool(12) as p:
            fluids = p.map(updata_pos, fluids)
        partial_list[0:N_f] = fluids
        
        # 棒の処理
        # for i in partial_list[N_f+int(N_wall):N]:
        #     i.u += i.f * dt
        #     i.r += i.u * dt
        #     i.v = i.a * (i.u + 0.5 * i.f * dt)
        #     if (i.r[1] > (nx-4) * particle_size):
        #         i.r[1] = 2 * (nx-4) * particle_size - i.r[1]
        #         i.v = (-1) * i.v
        #     if (i.r[1] < 4 * particle_size):
        #         i.r[1] = 2 * 4 * particle_size - i.r[1]
        #         i.v = (-1) * i.v
        #     i.checkarea()
        result.append(R)
        
        if (k % 50 == 0):
            np.save(f'data/result_{N_f}_{k}',result)
            np.save(f'data/result_U_{N_f}_{k}',U)
            np.save(f'data/result_V_{N_f}_{k}',V)
    if (suc):
        name = arg[3]
        file_name = f'data/result_{name}.npy'
        data = np.load(file_name)
        iter = iter + len(data)
        result = np.concatenate([data, result])
    
    np.save(f'data/result_{N_f}_{iter}',result)
    np.save(f'data/result_U_{N_f}_{iter}',U)
    np.save(f'data/result_V_{N_f}_{iter}',V)