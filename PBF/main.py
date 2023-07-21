import math
import numpy as np
from multiprocessing import Pool
from const import *
from particle import init,Particle
import time 

if __name__ == '__main__':
    particle_area = []
    def update_neighbor(i):
        i.neighbor = []
        for k in near:
            darea = i.area + k
            if (darea < 0):
                continue
            if (darea >= box):
                continue
            else :
                for m in particle_area[darea]:
                    j = particle_list[m]
                    dist = np.linalg.norm(i.r_pre - j.r_pre)
                    if (dist < h):
                        i.neighbor.append(j.n)
        return i
    
    def naive_neighbor(i):
        i.neighbor = []
        for j in particle_list:
            dist = np.linalg.norm(i.r_pre - j.r_pre)
            if (dist < h):
                i.neighbor.append(j.n)            
        return i
    
    def update_density(i):
        i.d = 0.0
        for n_j in i.neighbor:
            j = particle_list[n_j]
            dw = i.kernel(j)
            i.d += dw * mass_pa
        return i
    
    # ラムダの計算
    def update_lambda(i):
        sum = 0.
        for n_k in i.neighbor:
            k = particle_list[n_k]
            tmp_sum = np.zeros(3)
            if (i.n == n_k):
                for n_j in i.neighbor:
                    if (n_j == i.n):
                        continue
                    j = particle_list[n_j]
                    
                    tmp_sum += i.kernel_gr(j) * k.r_pre
            else :
                tmp_sum += - i.kernel_gr(k) * k.r_pre
            sum += tmp_sum[0] * tmp_sum[0] + tmp_sum[1] * tmp_sum[1] + tmp_sum[2] * tmp_sum[2]
        sum = sum / density0
        i.l = - (i.consist() / (sum + 0.1))
        return i
    
    edge_x = (nx - 4) * particle_size - 0.005
    edge_y = (ny - 4) * particle_size - 0.005
    edge_z = (nz - 4) * particle_size - 0.005
     
    c_ = 315 / (64 * math.pi * math.pow(h,9))
    delta_q = 0.2 * 0.2 * h_2
    x = h_2 - delta_q
    w_q = c_ * math.pow(x,3)
    # 位置の更新
    def update_position(i):
        delta = 0.0
        k = - 0.1
        for n_j in i.neighbor:
            if (n_j == i.n):
                continue
            j = particle_list[n_j]
            tmp = i.kernel(j) / w_q
            s = k * math.pow(tmp,4)
            delta += (j.l + i.l ) * i.kernel_gr(j)
        i.r_pre += delta / density0
        # 壁との衝突処理
        if (i.r_pre[0] < 0.035):
            i.r_pre[0] = 0.07 - i.r_pre[0]
        if (i.r_pre[1] < 0.035):
            i.r_pre[1] = 0.07 - i.r_pre[1]
        if (i.r_pre[2] < 0.035):
            i.r_pre[2] = 0.07 - i.r_pre[2]
        if (i.r_pre[0] > edge_x):
            i.r_pre[0] = edge_x * 2 - i.r_pre[0]
        if (i.r_pre[2] > edge_z):
            i.r_pre[2] = edge_z * 2 - i.r_pre[2]
        return i
    
    particle_list = init(suc)
    result = []
    V = np.zeros((N_f+int(N_wall)+N_ball,3))
    for iter in range(ITER):
        
        print("iter",iter)
        particle_area = []
        R = np.zeros((N_f+int(N_wall)+N_ball,3))
        for _ in range(box):
            particle_area.append([])
        #粒子の位置、速度、変位の結果を保存
        for i in particle_list:
            n = i.n
            R[n] = i.r
            V[n] = i.v
            particle_area[i.area].append(n)
        fluids = particle_list[0:N_f]

        with Pool(16) as p:    
            fluids = p.map(Particle.update_predict_positon,fluids)
        particle_list[0:N_f] = fluids
        t_start = time.time()
        with Pool(16) as p:    
            particle_list = p.map(naive_neighbor, particle_list)
        t_end = time.time()
        print("{}:{}",N_wall + N_f,t_end - t_start)
        for _ in range(20):
            with Pool(16) as p:
                particle_list = p.map(update_density,particle_list)
            with Pool(16) as p:
                particle_list = p.map(update_lambda,particle_list)
            fluids = particle_list[0:N_f]
            with Pool(16) as p:
                fluids = p.map(update_position,fluids)
            particle_list[0:N_f] = fluids
        fluids = particle_list[0:N_f]
        with Pool(16) as p:    
            fluids = p.map(Particle.update_positon_velocity,fluids)
        particle_list[0:N_f] = fluids
        print(time.time()-t_start)
        print(particle_list[100].r)
        result.append(R)
        if (iter % 50 == 0):
            np.save(f'result_{iter}_{N_f}',result)
            np.save(f'result_V_{iter}_{N_f}',V)
    np.save(f'result_{ITER}_{N_f}',result)
    np.save(f'result_V_{ITER}_{N_f}',V)
