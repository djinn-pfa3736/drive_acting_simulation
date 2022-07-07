import sys
import random

import numpy as np
import pandas as pd

import cv2
import matplotlib.pyplot as plt

import pickle

import pdb

# Number of working drivers per day
# np.mean([15, 13, 20, 22, 17, 15, 28, 30, 28, 30, 32, 21, 24, 27]) = 23

class Driver:
    def __init__(self, home_coord, max_stock_len):
        self.coord = home_coord
        self.home_coord = home_coord

        self.max_stock_len = max_stock_len
        self.current_stock_len = 0

        self.state = 0
        self.shop_coord = []
        self.dest_coord = []
        self.stock = []

        self.appli_matching_num = 0
        self.processed_num = 0

    def get_order(self, order):
        if len(self.stock) < self.max_stock_len:
            self.stock.append(order)
            # print("=== Order matched!! ===")
            return True
        return False

    def set_order(self):
        if 0 < len(self.stock):
            order = self.stock[0]
            self.stock.remove(order)
            self.shop_coord = order.shop_coord
            self.dest_coord = order.dest_coord
            self.state = 1
            return True
        return False

    def drive_type1(self, appli_queue):
        if self.state == 0:
            if not self.set_order():
                if 0 < len(appli_queue):
                    self.appli_matching_num += 1
                    self.get_order(appli_queue[0])
                    appli_queue.remove(appli_queue[0])

            delta = self.coord - self.home_coord

        if self.state == 1:
            delta = self.coord - self.shop_coord

        elif self.state == 2:
            delta = self.coord - self.dest_coord

        delta_x = delta_y = 0
        if 0 < delta[0]:
            delta_x = -1
        elif delta[0] < 0:
            delta_x = 1

        if 0 < delta[1]:
            delta_y = -1
        elif delta[1] < 0:
            delta_y = 1

        self.coord = self.coord + np.array([delta_x, delta_y])
        if delta_x == 0 and delta_y == 0:
            if self.state == 2:
                self.processed_num += 1
            self.switch_state()

        return appli_queue

    def drive_type2(self, appli_queue):
        if self.state == 0:
            if not self.set_order():
                if 0 < len(appli_queue):
                    self.appli_matching_num += 1
                    self.get_order(appli_queue[0])
                    appli_queue.remove(appli_queue[0])

            delta = self.coord - self.home_coord

        if self.state == 1:
            delta = self.coord - self.shop_coord

        elif self.state == 2:
            delta = self.coord - self.dest_coord
            if 0 < len(appli_queue):
                if self.get_order(appli_queue[0]):
                    self.appli_matching_num += 1
                    appli_queue.remove(appli_queue[0])

        delta_x = delta_y = 0
        if 0 < delta[0]:
            delta_x = -1
        elif delta[0] < 0:
            delta_x = 1

        if 0 < delta[1]:
            delta_y = -1
        elif delta[1] < 0:
            delta_y = 1

        self.coord = self.coord + np.array([delta_x, delta_y])
        if delta_x == 0 and delta_y == 0:
            if self.state == 2:
                self.processed_num += 1
            self.switch_state()

        return appli_queue


    def switch_state(self):
        # pdb.set_trace()
        if self.state == 0:
            pass
        else:
            self.state += 1
            self.state = self.state % 3

class Order:
    def __init__(self, shop_coord, dest_coord, generated_time, deadline_length):
        self.shop_coord = shop_coord
        self.dest_coord = dest_coord
        self.generated_time = generated_time
        self.deadline_length = deadline_length
        self.process_start_time = -1
        self.process_end_time = -1

if __name__ == "__main__":

    trial_num = int(sys.argv[1])

    grid_size_x = int(sys.argv[2])
    grid_size_y = int(sys.argv[3])

    driver_num = int(sys.argv[4])
    max_stock_len = int(sys.argv[5])

    total_order_num = int(sys.argv[6])

    appli_ratio = float(sys.argv[7])

    drive_type = int(sys.argv[8])

    # 50,000[m/hour]/60 = 833.333...[m/min]

    with open('kde.pickle', 'rb') as f:
        kde = pickle.load(f)

    simulation_start = 17*60
    simulation_length = 12*60

    order_count_vec = []
    appli_matching_ratio_vec = []
    processed_ratio_vec = []
    trial_count = 0
    while trial_count < trial_num:

        appli_cancelled_num = phone_cancelled_num = 0
        appli_order_num = 0
        total_order_count = 0

        # Random sampling model for application
        order_time_vec = np.floor(kde.sample(total_order_num)) % (24*60)

        drivers = []
        for i in range(0, driver_num):
            home_coord = [random.randrange(0, grid_size_x), random.randrange(0, grid_size_y)]
            drivers.append(Driver(np.array(home_coord), max_stock_len))

        phone_queue = []
        appli_queue = []
        simulation_count = 0
        while simulation_count < simulation_length:

            time = (simulation_start + simulation_count) % (24*60)
            hour = np.floor(time/60)
            min = time%60
            print("*** Simulation Count: " + str(simulation_count).zfill(5) + "(" + str(time) + "=" + str(int(hour)) + ":" + str(min) + ")" + " ***")
            order_count = np.sum(np.where(order_time_vec == time, True, False))
            total_order_count += order_count
            for i in range(0, order_count):
                shop_coord = [random.randrange(0, grid_size_x), random.randrange(0, grid_size_y)]
                dest_coord = [random.randrange(0, grid_size_x), random.randrange(0, grid_size_y)]
                order = Order(np.array(shop_coord), np.array(dest_coord), simulation_count, 10)
                if random.random() < appli_ratio:
                    appli_queue.append(order)
                    appli_order_num += 1
                    # print("+++ Application order occured!! +++")
                else:
                    phone_queue.append(order)

            to_be_removed = []
            for order in phone_queue:

                """
                if order.deadline_length < simulation_count - order.generated_time:
                    to_be_removed.append(order)
                    phone_cancelled_num += 1
                else:
                    # Random calling model
                    called = random.randrange(0, len(drivers))
                    if drivers[called].get_order(order):
                        # pdb.set_trace()
                        to_be_removed.append(order)
                """

                # Random calling model
                called = random.randrange(0, len(drivers))
                if drivers[called].get_order(order):
                    # pdb.set_trace()
                    to_be_removed.append(order)

            for removed_order in to_be_removed:
                phone_queue.remove(removed_order)

            to_be_removed = []
            for order in appli_queue:
                if order.deadline_length < simulation_count - order.generated_time:
                    to_be_removed.append(order)
                    appli_cancelled_num += 1

            for removed_order in to_be_removed:
                appli_queue.remove(removed_order)
                phone_queue.append(removed_order)

            for driver in drivers:
                if drive_type == 0:
                    appli_queue = driver.drive_type1(appli_queue)
                elif drive_type == 1:
                    appli_queue = driver.drive_type2(appli_queue)

            simulation_count += 1

        # pdb.set_trace()
        order_count_vec.append(total_order_count)

        appli_matching_ratio = np.sum([driver.appli_matching_num for driver in drivers])/appli_order_num
        appli_matching_ratio_vec.append(appli_matching_ratio)

        processed_ratio = np.sum([driver.processed_num for driver in drivers])/total_order_count
        processed_ratio_vec.append(processed_ratio)

        trial_count += 1

    df = pd.DataFrame({'processed':processed_ratio_vec, 'application_matched':appli_matching_ratio_vec})
    df.to_csv("result.csv")

    print("Processed ratio           : " + str(round(np.mean(processed_ratio_vec), 3)) + " ± " + str(round(np.sqrt(np.var(processed_ratio_vec)), 3)))
    print("Application matching ratio: " + str(round(np.mean(appli_matching_ratio_vec), 3)) + " ± " + str(round(np.sqrt(np.var(appli_matching_ratio_vec)), 3)))

"""
Model1:
Processed ratio           : 0.662 ± 0.024
Application matching ratio: 0.225 ± 0.068

Model2:
Processed ratio           : 0.664 ± 0.022
t = -0.44569, df = 196.78, p-value = 0.6563
Application matching ratio: 0.260 ± 0.071
t = -3.5874, df = 197.72, p-value = 0.000421
"""
