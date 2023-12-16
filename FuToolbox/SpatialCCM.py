import numpy as np
import pandas as pd

class SpatialCCM:
    def __init__(self, x, y, tau, E,lon,lat):
        self.x=x
        self.y=y
        self.lon_values=lon
        self.lat_values=lat
        self.E = E
        self.tau=tau
        self.L = len(x[:,0,0])
        self.result_array = np.zeros(x.shape)
    def calculate(self):
        for i in tqdm(range(len(self.lon_values))):
            for j in tqdm(range(len(self.lat_values))):
                data_x = self.x[:, j, i].values
                data_y = self.y[:, j, i].values
                ccm1 = CCM(data_x, data_y,self.tau,self.E)
                cc=ccm1.causality()[0]
                self.result_array[:, j, i] = cc
        return self.result_array