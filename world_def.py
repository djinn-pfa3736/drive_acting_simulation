import sys
import random

import numpy as np
import pandas as pd

import cv2
import matplotlib.pyplot as plt

import pickle
import json
import glob

import pdb

import map_def
import order_def
import operator_def
import driver_def
import tactics_def

class World:
    def __init__(self, map_file, demands_distribution_pickle, \
        temporal_distribution_pickle, total_order_num, operator_file_list, simulation_start):

        tactics = [tactics_def.in_house_random, tactics_def.totally_random, tactics_def.in_house_nearest, \
            tactics_def.totally_nearest, tactics_def.in_house_home_nearest, tactics_def.totally_home_nearest]

        self.simulation_count = 0
        self.map = map_def.Map(map_file, demands_distribution_pickle)

        with open(temporal_distribution_pickle, 'rb') as f:
            self.temporal_distribution = pickle.load(f)

        self.operators = []
        for operator_file in operator_file_list:
            operator = operator_def.Operator(operator_file, tactics)
            self.operators.append(operator)

        self.simulation_length = simulation_length
        self.simulation_start = simulation_start

        self.phone_queue = []
        self.appli_queue = []

        self.phone_cancelled_num = 0
        self.appli_cancelled_num = 0

        self.order_time_points = np.floor(self.temporal_distribution.sample(total_order_num)) % (24*60)

    def initialize_simulation(self, operators, simulation_length, simulation_start, total_order_num):
        self.operators = operators

        self.simulation_count = 0

        self.simulation_length = simulation_length
        self.simulation_start = simulation_start

        self.phone_queue = []
        self.appli_queue = []

        self.phone_cancelled_num = 0
        self.appli_cancelled_num = 0

        self.order_time_points = np.floor(self.temporal_distribution.sample(total_order_num)) % (24*60)

    def get_individuals(self):
        return self.operators

    def take_a_step(self):
        current_time = (self.simulation_start + self.simulation_count) % (24*60)
        hour = np.floor(current_time/60)
        min = current_time%60
        print("*** Simulation Count: " + str(self.simulation_count).zfill(5) + "(" + str(current_time) + "=" + str(int(hour)) + ":" + str(min) + ")" + " ***")

        order_count = np.sum(np.where(self.order_time_points == current_time, True, False))
        for i in range(order_count):
            order = self.map.generate_order(current_time)
            if random.random() < appli_ratio:
                self.appli_queue.append(order)
            else:
                self.phone_queue.append(order)

        for operator in self.operators:
            operator.check_switch(current_time)

        # Phone accept process
        to_be_removed = []
        random_idx = random.sample(range(len(self.phone_queue)), len(self.phone_queue))

        for idx in random_idx:
            order = self.phone_queue[idx]
            # Random calling model
            called = random.randrange(0, len(self.operators))
            assign_result = self.operators[called].assign_order(current_time, self.operators, order)
            if assign_result == 0:
                print((order.generated_time, current_time))
                to_be_removed.append(order)

        for removed_order in to_be_removed:
            self.phone_queue.remove(removed_order)

        # Phone deadline process
        to_be_removed = []
        for order in self.phone_queue:
            if order.deadline_length < current_time - order.generated_time:
                to_be_removed.append(order)
                self.phone_cancelled_num += 1

        for removed_order in to_be_removed:
            self.phone_queue.remove(removed_order)

        # Application deadline process
        to_be_removed = []
        for order in self.appli_queue:
            if order.deadline_length < current_time - order.generated_time:
                to_be_removed.append(order)
                self.appli_cancelled_num += 1

        for removed_order in to_be_removed:
            self.appli_queue.remove(removed_order)
            removed_order.dedline_length = random.randint(10, 20)
            removed_order.generated_time = current_time
            self.phone_queue.append(removed_order)

        for operator in self.operators:
            for driver in operator.drivers:
                self.appli_queue = driver.drive(self.appli_queue, current_time)

        self.simulation_count += 1

    def report(self):
        efficiency_list = []
        operator_wait_time = []
        for operator in self.operators:
            driver_wait_time = []
            for driver in operator.drivers:
                efficiency_list.append(driver.total_drive/driver.total_move)
                wait_time = []
                for processed_order in driver.processed_orders:
                    wait_time.append(processed_order.process_start_time - processed_order.generated_time)
                driver_wait_time.append(wait_time)
            operator_wait_time.append(driver_wait_time)

        return efficiency_list, operator_wait_time, self.phone_cancelled_num, self.appli_cancelled_num

if __name__ == "__main__":

    map_file = sys.argv[1]
    demands_distribution_pickle = sys.argv[2]
    temporal_distribution_pickle = sys.argv[3]
    total_order_num = int(sys.argv[4])
    appli_ratio = float(sys.argv[5])

    # 50,000[m/hour]/60 = 833.333...[m/min]

    # simulation_start = 0
    simulation_start = 21*60
    simulation_length = 6*60

    # Size of spatial size of demands distribution is (564, 332)
    tmp = np.zeros((55, 35))
    tmp += 1
    tmp_df = pd.DataFrame(tmp)
    tmp_df.to_csv('map_file.csv', header=False, index=False)

    operator_file_list = glob.glob('operator_*.json')

    random.seed(0)
    world = World(map_file, demands_distribution_pickle, temporal_distribution_pickle, total_order_num, operator_file_list, simulation_start)
    simulation_count = 0
    while simulation_count < simulation_length:
        world.take_a_step()
        simulation_count += 1

    efficiency_list, operator_wait_time, phone_cancelled_num, appli_cancelled_num = world.report()
    pdb.set_trace()
