import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.spatial import distance
from scipy.stats import pearsonr

class CCM:
    def __init__(self, x, y, tau, E):
        self.x = x
        self.y = y
        self.tau = tau
        self.E = E
        self.L = len(x)
        self.M = self.shadow_manifold(self.y)
        self.t_steps, self.dists = self.get_distances(self.M)

    def shadow_manifold(self, data):
        M = {t: [] for t in range((self.E - 1) * self.tau, self.L)} 
        for t in range((self.E - 1) * self.tau, self.L):
            v_lag = [] 
            for t2 in range(0, self.E):
                v_lag.append(data[t - t2 * self.tau])
            M[t] = v_lag
        return M

    def get_distances(self, M):
        t_vec = [(k, v) for k, v in M.items()] 
        t_steps = np.array([i[0] for i in t_vec])
        vecs = np.array([i[1] for i in t_vec])
        dists = distance.cdist(vecs, vecs)
        return t_steps, dists

    def get_nearest_distances(self, t):
        t_ind = np.where(self.t_steps == t) 
        dist_t = self.dists[t_ind].squeeze() 
        nearest_inds = np.argsort(dist_t)[1:self.E + 2]
        nearest_timesteps = self.t_steps[nearest_inds] 
        nearest_distances = dist_t[nearest_inds]
        return nearest_timesteps, nearest_distances

    def predict(self, t, data_var):
        eps = 0.000001 
        t_ind = np.where(self.t_steps == t) 
        dist_t = self.dists[t_ind].squeeze() 
        nearest_timesteps, nearest_distances = self.get_nearest_distances(t)
        u = np.exp(-nearest_distances / np.max([eps, nearest_distances[0]])) 
        w = u / np.sum(u)

        var_true = data_var[t] 
        var_cor = np.array(data_var)[nearest_timesteps] 
        var_pre = (w * var_cor).sum() 
        return var_true, var_pre

    def causality(self):
        X_true_list = []
        X_pre_list = []
        for t in list(self.M.keys()): 
            var_true, var_pre = self.predict(t, self.x) 
            X_true_list.append(var_true)
            X_pre_list.append(var_pre)
        Xt, Xp = X_true_list, X_pre_list
        r = pearsonr(Xt, Xp)
        return r

