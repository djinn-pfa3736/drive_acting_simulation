import pandas as pd
import pickle
import numpy as np
import random

import order_def

class Map:
    def __init__(self, map_file, demands_distribution_pickle):
        valid_area = pd.read_csv(map_file, header=None)
        self.valid_area = valid_area.values
        with open(demands_distribution_pickle, 'rb') as f:
            self.distribution = pickle.load(f)
        self.generated_orders = 0

    def get_shape(self, map_file, demands_distribution_pickle):
        return valid_area.shape

    def generate_order(self, current_time):
        # Not completed

        self.generated_orders += 1
        width, height = self.valid_area.shape

        while True:
            shop_coord_x = int(np.floor(random.uniform(1, width)))
            shop_coord_y = int(np.floor(random.uniform(1, height)))

            if self.valid_area[shop_coord_x, shop_coord_y] == 1:
                break

        while True:
            dest_coord_x = int(np.floor(random.uniform(1, width)))
            dest_coord_y = int(np.floor(random.uniform(1, height)))

            if self.valid_area[dest_coord_x, dest_coord_y] == 1:
                break

        generated_time = current_time
        deadline_length = random.randint(10, 20)

        order = order_def.Order([shop_coord_x, shop_coord_y], [dest_coord_x, dest_coord_y], generated_time, deadline_length)
        return order
