import pandas as pd
import numpy as np

from collections import defaultdict

from haversine import haversine, Unit

class ProximityCalculator():
    def __init__(self, log1) -> None:
        """
        log1: numpy array with values: ,id,row,col,time, time_delta(s) ,lng,lat
        """
        self.server_time = 0
        self.log1 = log1
        self.log2 = []
        self.log1_start_time = pd.Timestamp(str(log1[0][4]))
        self.log2_start_time = 0
        self.log1_index = 0
        self.log2_index = 0
        self.distances = []

    def is_contact_2_mins(self, minutes):
        if len(self.distances) < minutes*60:
            return False
        size = minutes*60

        for i in range(size-1, 0, -1):
            if self.distances[i][2] != self.distances[i-1][2] +pd.Timedelta(seconds=1):
                return False
        
        return True

    def calculate_proximity(self, log2):

        self.log2 = log2
        self.log2_start_time = pd.Timestamp(str(log2[0][4]))
        self.server_time = 0
        self.log1_index = 0
        self.log2_index = 0
        self.distances = []
        proximity_map = defaultdict(set)
        if self.log1_start_time > self.log2_start_time:
            self.server_time = self.log1_start_time
            while self.log2_index < len(self.log2) and pd.Timestamp(str(self.log2[self.log2_index][4])) < self.log1_start_time:
                self.log2_index += 1
        else:
            self.server_time = self.log2_start_time
            while self.log1_index < len(self.log1) and self.log2_start_time > pd.Timestamp(str(self.log1[self.log1_index][4])):
                self.log1_index += 1

        # print(type(self.server_time))
        # print(self.log1[self.log1_index][5], self.log2[self.log2_index][5])
        while self.log2_index < len(self.log2) and self.log1_index < len(self.log1):
           
            if pd.Timestamp(str(self.log1[self.log1_index][4])) == pd.Timestamp(str(self.log2[self.log2_index][4])):
                user1 = (float(self.log1[self.log1_index][7]), float(self.log1[self.log1_index][6]))
                user2 = (float(self.log2[self.log2_index][7]), float(self.log2[self.log2_index][6]))
                # print(user1, user2)
                dist = haversine(user1, user2, unit=Unit.METERS)

                if dist <= 2:
                    if self.distances and  self.distances[-1][2] + pd.Timedelta(seconds=1) == self.server_time:
                        if self.is_contact_2_mins(15):
                            # print("15 min contact between %s and %s is: %i at time:%s" %(self.log1[0][1],self.log2[0][1], dist, str(self.server_time)))
                            proximity_map[int(self.log1[0][1])].add(int(self.log2[0][1]))
                        # print("dist between %s and %s is: %i, at time: %s" %(self.log1[0][1],self.log2[0][1], dist, str(self.server_time)))
                    self.distances.append((self.log1[0][1],self.log2[0][1], self.server_time, dist))

            self.log1_index += 1
            self.log2_index += 1
            self.server_time = self.server_time + pd.Timedelta(seconds=1)
        
        return proximity_map

def main():
    proximity_map = defaultdict(set)


    for i in range(8,108):
        for j in range(i+1, 108):
            # i = 9
            # j = 13
            # print(i, j)
            id_10_data = pd.read_csv("C:\\Users\\mahno\\Documents\\Thesis\\Code\\server\\data\\log_logs_%i.csv" %(i))
            id_12_data = pd.read_csv("C:\\Users\\mahno\\Documents\\Thesis\\Code\\server\\data\\log_logs_%i.csv" %(j))

            id_10_arr = id_10_data.to_numpy()
            id_12_arr = id_12_data.to_numpy()
            # print(id_10_arr)

            pc = ProximityCalculator(id_10_arr, id_12_arr)
            pc.calculate_proximity(proximity_map)
    
    print(proximity_map)
                

if __name__ == "__main__":
    main()