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

def in_house_random(operator_id, whole_operators, order):
    # add ksakata
    drivers = whole_operators[operator_id].drivers
    driver_states = [drivers[i].state for i in range(len(drivers))]
    if len(driver_states) == 1:
        if driver_states[0] == 0:
            empty_idx = [True]
        else:
            empty_idx = [False]
    else:
        empty_idx = np.where(driver_states == 0, True, False)

    if np.sum(empty_idx) == 0:
        return -1, -1
    else:
        shuffled_idx_driver = random.sample(range(len(drivers)), len(drivers))

        for idx in shuffled_idx_driver:
            if drivers[idx].state == 0:
                return operator_id, idx

        return -1, -1

def totally_random(operator_id, whole_operators, order):
    # add ksakata
    shuffled_idx_operator = random.sample(np.arange(len(drivers)), len(drivers))
    for operator_idx in shuffled_idx_operator:
        drivers = whole_operators[operator_idx].drivers
        driver_states = [drivers[i].state for i in range(0, len(drivers))]
        if len(driver_states) == 1:
            if driver_states[0] == 0:
                empty_idx = [True]
            else:
                empty_idx = [False]
        else:
            empty_idx = np.where(driver_states == 0, True, False)

        if np.sum(empty_idx) == 0:
            continue
        else:
            shuffled_idx_driver = random.sample(range(len(drivers)), len(drivers))

            for idx in shuffled_idx_driver:
                if drivers[idx].state == 0:
                    return operator_id, idx

    return -1, -1

def in_house_nearest(operator_id, whole_operators, order):
    drivers = whole_operators[operator_id].drivers
    driver_states = [drivers[i].state for i in range(0, len(drivers))]

    if len(driver_states) == 1:
        if driver_states[0] == 0:
            empty_idx = [True]
        else:
            empty_idx = [False]
    else:
        empty_idx = np.where(driver_states == 0, True, False)

    if np.sum(empty_idx) == 0:
        return -1, -1
    else:
        shop_position = order.shop_coord
        driver_positions = [drivers[i].coord for i in range(0, len(drivers))]
        distances = [np.sqrt(np.sum((shop_position - driver_positions[i])**2)) for i in range(len(drivers))]

        sorted_idx_list = np.argsort(distances)
        for idx in sorted_idx_list:
            if drivers[idx].state == 0:
                return operator_id, idx

        return -1, -1

def totally_nearest(operator_id, whole_operators, order):
    # add ksakata
    shop_position = order.shop_position
    distances = []
    empty_idx_list = []
    operators_idx_list = []
    drivers_idx_list = []
    drivers_list = []
    for idx in range(len(whole_operators)):
        drivers = whole_operators[idx].drivers
        drivers_list = drivers_list + drivers

        driver_states = [drivers[i].state for i in range(0, len(drivers))]
        if len(driver_states) == 1:
            if driver_states[0] == 0:
                empty_idx = [True]
            else:
                empty_idx = [False]
        else:
            empty_idx = np.where(driver_states == 0, True, False)

        empty_idx_list = empty_idx_list + empty_idx

        driver_positions = [drivers[i].coord for i in range(0, len(drivers))]
        tmp = [np.sqrt(np.sum((shop_position - driver_positions[i])**2)) for i in range(len(drivers))]
        distances = distances + tmp

        operators_idx_list = operators_idx_list + [idx]*len(drivers)
        drivers_idx_list = drivers_idx_list + range(len(drivers))

    if np.sum(empty_idx_list) == 0:
        return -1, -1
    else:
        sorted_idx_list = np.argsort(distances)
        for idx in sorted_idx_list:
            if drivers_list[idx].state == 0:
                return operators_idx_list[idx], drivers_idx_list[idx]

        return -1, -1

def in_house_home_nearest(operator_id, whole_operators, order):
    # add ksakata
    drivers = whole_operators[operator_id].drivers
    driver_states = [drivers[i].state for i in range(len(drivers))]
    if len(driver_states) == 1:
        if driver_states[0] == 0:
            empty_idx = [True]
        else:
            empty_idx = [False]
    else:
        empty_idx = np.where(driver_states == 0, True, False)

    if np.sum(empty_idx) == 0:
        return -1, -1
    else:
        shop_position = order.shop_coord
        dest_position = order.dest_coord

        driver_positions = [drivers[i].coord for i in range(0, len(drivers))]
        home_positions = [drivers[i].home_coord for i in range(len(drivers))]

        shop_distances = np.array([np.sqrt(np.sum((shop_position - driver_positions[i])**2)) for i in range(0, len(drivers))])
        home_distances = np.array([np.sqrt(np.sum((dest_position - home_positions[i])**2)) for i in range(0,len(drivers))])

        metric = shop_distances + home_distances
        sorted_idx_list = np.argsort(metric)
        for idx in sorted_idx_list:
            if drivers[idx].state == 0:
                return operator_id, idx

        return -1, -1

def totally_home_nearest(operator_id, whole_operators, order):
    # add ksakata
    shop_position = order.shop_coord
    dest_position = order.dest_coord

    metrics = []
    empty_idx_list = []
    operators_idx_list = []
    drivers_idx_list = []
    drivers_list = []
    for idx in range(len(whole_operators)):
        drivers = whole_operators[idx].drivers
        drivers_list = drivers_list + drivers

        driver_states = [drivers[i].state for i in range(0, len(drivers))]
        if len(driver_states) == 1:
            if driver_states[0] == 0:
                empty_idx = [True]
            else:
                empty_idx = [False]
        else:
            empty_idx = np.where(driver_states == 0, True, False)

        empty_idx_list = empty_idx_list + empty_idx

        driver_positions = [drivers[i].coord for i in range(0, len(drivers))]
        home_positions = [drivers[i].home_coord for i in range(0, len(drivers))]
        shop_distances = np.array([np.sqrt(np.sum((shop_position - driver_positions[i])**2)) for i in range(len(drivers))])
        home_distances = np.array([np.sqrt(np.sum((dest_position - home_positions[i])**2)) for i in range(0,len(drivers))])
        metric = shop_distances + home_distances
        metrics = metrics + metric

        operators_idx_list = operators_idx_list + [idx]*len(drivers)
        drivers_idx_list = drivers_idx_list + range(len(drivers))

    if np.sum(empty_idx_list) == 0:
        return -1, -1
    else:
        sorted_idx_list = np.argsort(metrics)
        for idx in sorted_idx_list:
            if drivers_list[idx].state == 0:
                return operators_idx_list[idx], drivers_idx_list[idx]

        return -1, -1

tactics = [in_house_random, totally_random, in_house_nearest, totally_nearest, in_house_home_nearest, totally_home_nearest]

class World:
    def __init__(self, map_file, demands_distribution_pickle, occuring_distribution_pickle, total_order_num, operator_file_list, simulation_start):

        self.simulation_count = 0
        self.map = Map(map_file, demands_distribution_pickle)

        with open(occuring_distribution_pickle, 'rb') as f:
            self.occuring_distribution = pickle.load(f)

        self.operators = []
        for operator_file in operator_file_list:
            operator = Operator(operator_file)
            self.operators.append(operator)

        self.simulation_length = simulation_length
        self.simulation_start = simulation_start

        self.phone_queue = []
        self.appli_queue = []

        self.phone_cancelled_num = 0
        self.appli_cancelled_num = 0

        self.order_time_points = np.floor(self.occuring_distribution.sample(total_order_num)) % (24*60)

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
        print(random_idx)
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


class Order:
    def __init__(self, shop_coord, dest_coord, generated_time, deadline_length):
        self.shop_coord = shop_coord
        self.dest_coord = dest_coord
        self.generated_time = generated_time
        self.deadline_length = deadline_length
        self.process_start_time = -1
        self.process_end_time = -1

class Operator:
    def __init__(self, operator_file):

        with open(operator_file) as f:
            df = json.load(f)
        self.operator_id = df['operator_id']
        self.home_coord = df['home_coord']

        self.drivers = []
        for driver_info in df['driver_list']:
            driver_id = driver_info['driver_id']
            driver_home_coord_x = int(self.home_coord[0] + np.floor(random.uniform(-5, 6)))
            driver_home_coord_y = int(self.home_coord[1] + np.floor(random.uniform(-5, 6)))
            stock_size = driver_info['stock_size']
            driver = Driver(driver_id, [driver_home_coord_x, driver_home_coord_y], stock_size)
            self.drivers.append(driver)

        self.stock_size = df['stock_size']

        self.switch_schedule = []
        self.distribution_list = []
        for schedule_info in df['dist_schedule']:
            self.switch_schedule.append(schedule_info['time'])
            self.distribution_list.append(schedule_info['distribution'])

        self.distribution = []
        self.current_distribution_idx = 0

        self.cum_order_count = 0
        self.cum_passing_count = 0

    def check_switch(self, current_time):
        if self.current_distribution_idx < len(self.switch_schedule):
            if current_time == self.switch_schedule[self.current_distribution_idx]:
                self.switch_distribution()

    def switch_distribution(self):
        self.distribution = self.distribution_list[self.current_distribution_idx]
        self.current_distribution_idx += 1

    def assign_order(self, current_time, whole_operators, order):
        random_val = random.random()
        cum_dist = np.cumsum(self.distribution)

        for i in range(len(cum_dist)):
            selected_tactics_idx = i
            if random_val <= cum_dist[i]:
                break
        operator_id, driver_id = tactics[selected_tactics_idx](self.operator_id, whole_operators, order)
        # print(selected_tactics_idx)
        if driver_id != -1:
            set_result = whole_operators[operator_id].drivers[driver_id].set_order(order, current_time)
            return 0
        else:
            return -1

class Driver:
    def __init__(self, driver_id, home_coord, stock_size):
        self.driver_id = driver_id
        self.home_coord = np.array(home_coord)

        self.coord = self.home_coord

        self.stock_size = stock_size
        self.stock = []

        self.state = 0
        self.shop_coord = []
        self.dest_coord = []

        self.appli_matching_num = 0
        self.processed_num = 0

        self.total_move = 0
        self.total_drive = 0
        self.total_empty = 0

        self.current_order = None
        self.processed_orders = []

    def get_order_to_stock(self, order, current_time):
        if len(self.stock) < self.stock_size:
            order.process_start_time = current_time
            self.stock.append(order)
            return 0
        return -1

    def set_order(self, order, current_time):
        if order is None:
            if 0 < len(self.stock):
                order = self.stock[0]
                self.stock.remove(order)
                order.process_start_time = current_time
                self.current_order = order
                self.shop_coord = order.shop_coord
                self.dest_coord = order.dest_coord
                self.state = 1
                return 0
            return -1
        else:
            if self.state == 0:
                order.process_start_time = current_time
                self.current_order = order
                self.shop_coord = order.shop_coord
                self.dest_coord = order.dest_coord
                self.state = 1
                return 0
            elif state == 2:
                return self.get_order_to_stock(order, current_time)
            else:
                return -1

    def drive(self, appli_queue, current_time):
        self.total_move += 1
        if self.state == 0:
            self.total_empty += 1
            if self.set_order(None, None) == -1: # Get order from stock
                if 0 < len(appli_queue):
                    self.appli_matching_num += 1
                    self.get_order_to_stock(appli_queue[0], current_time)
                    appli_queue.remove(appli_queue[0])

            delta = self.coord - self.home_coord

        if self.state == 1:
            delta = self.coord - self.shop_coord

        elif self.state == 2:
            self.total_drive += 1
            delta = self.coord - self.dest_coord
            if 0 < len(appli_queue):
                distances = [np.sum(np.abs(appli_queue[i].shop_coord - self.dest_coord)) for i in range(len(appli_queue))]
                nearest_idx = np.argmin(distances) # Currently only nearest tactics is implemented
                order = appli_queue[nearest_idx]
                if self.get_order_to_stock(order, current_time) == 0:
                    self.appli_matching_num += 1
                    appli_queue.remove(order)

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
                self.current_order.process_end_time = current_time
                self.processed_orders.append(self.current_order)
                self.current_order = None
            self.switch_state()

        return appli_queue

    def switch_state(self):
        # pdb.set_trace()
        if self.state == 0:
            pass
        else:
            self.state += 1
            self.state = self.state % 3

if __name__ == "__main__":

    map_file = sys.argv[1]
    demands_distribution_pickle = sys.argv[2]
    occuring_distribution_pickle = sys.argv[3]
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
    world = World(map_file, demands_distribution_pickle, occuring_distribution_pickle, total_order_num, operator_file_list, simulation_start)
    simulation_count = 0
    while simulation_count < simulation_length:
        world.take_a_step()
        simulation_count += 1

    efficiency_list, operator_wait_time, phone_cancelled_num, appli_cancelled_num = world.report()
    pdb.set_trace()
