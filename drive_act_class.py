import sys
import random
import numpy as np
import cv2
import matplotlib.pyplot as plt

import pdb

class Operator:
    def __init__(self, max_stock, area):
        self.max_stock = max_stock
        self.drivers = []
        self.stock = []
        self.area = area
        self.ratio_vec = []

    def set_drivers(self, drivers):
        self.drivers = drivers

    def add_order(self, order):
        if(len(self.stock) < self.max_stock):
            self.stock.append(order)
            add_flag = True
        else:
            add_flag = False

        return add_flag
        # pdb.set_trace()

    def get_order(self):
        if(0 < len(self.stock)):
            order = self.stock.pop()
        else:
            order = -1
        return order

    def check_empty_driver(self):
        empty_idx = -1
        for i in range(0, len(self.drivers)):
            driver = self.drivers[i]
            if(driver.state == 0):
                empty_idx = i
                break
        return empty_idx

    def assign_order(self):

        driver_idx = self.check_empty_driver()
        if(driver_idx != -1):
            order = self.get_order()
            if(order != -1):
                self.drivers[driver_idx].set_order(order)
                self.drivers[driver_idx].update_state()

    def upload_ratio(self, ratio_val):
        self.ratio_vec.append(ratio_val)

class Driver:
    def __init__(self, state, x, y, plane_x, plane_y, operator):
        self.state = state
        self.x = x
        self.y = y
        self.plane_x = plane_x
        self.plane_y = plane_y
        self.operator = operator

        self.total_drive = 0
        self.act_drive = 0

    def update_state(self):
        self.state += 1
        self.state = self.state % 3

    def set_order(self, order):
        if(self.state == 0):
            self.order = order
            set_flag = True
        else:
            set_flag = False
        return set_flag

    def update_position(self):

        if(self.state == 1 or self.state == 2):
            self.total_drive += 1
        if(self.state == 2):
            self.act_drive += 1

        if(self.state == 0):
            if(random.random() > 0.5):
                diff_x = 1
            else:
                diff_x = -1

            if(random.random() > 0.5):
                diff_y = 1
            else:
                diff_y = -1
        elif(self.state == 1):
            shop_pos = self.order.dest[0]
            diff_x = shop_pos[0] - self.x
            diff_y = shop_pos[1] - self.y

            if(diff_x != 0):
                diff_x = diff_x / abs(diff_x)

            if(diff_y != 0):
                diff_y = diff_y / abs(diff_y)

            if(diff_x == 0 and diff_y == 0):
                self.update_state()

        else:
            home_pos = self.order.dest[1]
            diff_x = home_pos[0] - self.x
            diff_y = home_pos[1] - self.y

            if(diff_x != 0):
                diff_x = diff_x / abs(diff_x)

            if(diff_y != 0):
                diff_y = diff_y / abs(diff_y)

            if(diff_x == 0 and diff_y == 0):
                self.update_state()
                self.operator.upload_ratio(self.act_drive / self.total_drive)
                self.act_drive = 0
                self.total_drive = 0

        self.x = self.x + diff_x
        if(self.x < 0):
            self.x = 0
        elif(self.plane_x < self.x):
            self.x = self.plane_x

        self.y = self.y + diff_y
        if(self.y < 0):
            self.y = 0
        elif(self.plane_y < self.y):
            self.y = self.plane_y


class OrderGenerator:
    def __init__(self, sim_time, plane_x, plane_y, gender_ratio,
                    male_weight, female_weight,
                    number_up_len,
                    number_keep_len, number_down_len):

        self.plane_x = plane_x
        self.plane_y = plane_y
        self.gender_ratio = gender_ratio
        self.male_weight = male_weight
        self.female_weight = female_weight

        self.order_ratio_vec = []
        x = 0
        dx = np.floor(number_up_len/number_down_len)
        for i in range(0, sim_time):
            if(i < number_up_len):
                x += 1
                self.order_ratio_vec.append(x)
            elif(number_up_len < i and i < number_up_len + number_keep_len):
                self.order_ratio_vec.append(x)
            elif(number_up_len + number_keep_len < i and i < number_up_len + number_keep_len + number_down_len):
                x -= dx
                self.order_ratio_vec.append(x)
            else:
                self.order_ratio_vec.append(0)

        self.order_ratio_vec = np.array(self.order_ratio_vec)
        self.order_ratio_vec = self.order_ratio_vec / np.max(self.order_ratio_vec)

        # pdb.set_trace()

    def get_order_ratio(self, time):
        return self.order_ratio_vec[time]

    def generate_order(self):
        gender_prob = random.random()
        if(gender_prob < self.gender_ratio):
            gender = 'male'
        else:
            gender = 'female'

        if(gender == 'male'):
            bias = np.floor(self.male_weight*random.random())
            shop_x = np.floor(random.random()*self.plane_x)
            if(self.plane_x < shop_x):
                shop_x = self.plane_x
            shop_y = np.floor(random.random()*self.plane_y)
            if(self.plane_y < shop_y):
                shop_y = self.plane_y
            home_x = np.floor(random.random()*self.plane_x + bias)
            if(self.plane_x < home_x):
                home_x = self.plane_x
            home_y = np.floor(random.random()*self.plane_y + bias)
            if(self.plane_y < home_y):
                home_y = self.plane_y
        else:
            bias = np.floor(self.female_weight*random.random())
            shop_x = np.floor(random.random()*self.plane_x)
            if(self.plane_x < shop_x):
                shop_x = self.plane_x
            shop_y = np.floor(random.random()*self.plane_y)
            if(self.plane_y < shop_y):
                shop_y = self.plane_y
            home_x = np.floor(random.random()*self.plane_x + bias)
            if(self.plane_x < home_x):
                home_x = self.plane_x
            home_y = np.floor(random.random()*self.plane_y + bias)
            if(self.plane_y < home_y):
                home_y = self.plane_y

        dest = [[shop_x, shop_y], [home_x, home_y]]
        order = Order(gender, dest)
        return order

class Order:
    def __init__(self, gender, dest):
        self.gender = gender
        self.dest = dest

if __name__ == "__main__":

    sim_time = int(sys.argv[1])
    plane_x = int(sys.argv[2])
    plane_y = int(sys.argv[3])
    area_diff_x = int(sys.argv[4])
    area_diff_y = int(sys.argv[5])
    max_stock = int(sys.argv[6])
    operator_num = int(sys.argv[7])
    driver_num = int(sys.argv[8])

    number_up_len = int(sys.argv[9])
    number_keep_len = int(sys.argv[10])
    number_down_len = int(sys.argv[11])

    order_generator = OrderGenerator(sim_time, plane_x, plane_y,
                                     1/3, 20, 10,
                                     number_up_len, number_keep_len,
                                     number_down_len)
    operators = []
    for i in range(0, operator_num):
        left_up_x = np.floor(random.random()*plane_x)
        left_up_y = np.floor(random.random()*plane_y)
        right_down_x = left_up_x + area_diff_x
        if(plane_x < right_down_x):
            right_down_x = plane_x
        right_down_y = left_up_y + area_diff_y
        if(plane_y < right_down_y):
            right_down_y = plane_y
        area = [[left_up_x, left_up_y], [right_down_x, right_down_y]]
        operator = Operator(max_stock, area)

        drivers = []
        for j in range(0, driver_num):
            x = np.floor(plane_x*random.random())
            y = np.floor(plane_y*random.random())
            driver = Driver(0, x, y, plane_x, plane_y, operator)
            drivers.append(driver)
        operator.set_drivers(drivers)
        operators.append(operator)

    unit_size = 15
    calling_orders = []
    total_order_count = 0
    for i in range(0, sim_time):

        image = np.zeros((unit_size*plane_x, unit_size*plane_y, 3))
        inv_idx = np.where(image == 0)
        image[inv_idx] = 255

        print("*** SIMULATION COUNT: " + str(i) + " ***")
        order_dec = random.random()
        order_ratio = order_generator.get_order_ratio(i)
        if order_dec < order_ratio:
            # pdb.set_trace()
            total_order_count += 1
            order = order_generator.generate_order()
            operator_idx = int(np.floor(len(operators)*random.random()))
            add_flag = operators[operator_idx].add_order(order)
            if(add_flag == False):
                calling_orders.append(order)


        del_elms = []
        if(0 < len(calling_orders)):
            for j in range(0, len(calling_orders)):
                order = calling_orders[j]
                full_flag = True
                for op in operators:
                    add_flag = op.add_order(order)
                    if(add_flag == True):
                        full_flag = False
                        del_elms.append(order)
                        break
                if(full_flag == True):
                    break

            # if(0 < len(del_elms)):
            #     pdb.set_trace()
            for elm in del_elms:
                calling_orders.remove(elm)

        # print(len(calling_orders))
        for j in range(0, len(operators)):
            operator = operators[j]
            operator.assign_order()
            for k in range(0, len(operators[j].drivers)):
                driver = operator.drivers[k]
                driver.update_position()

                if(driver.state == 0):
                    cv2.rectangle(image, (int(driver.x)*unit_size, int(driver.y)*unit_size), ((int(driver.x) + 2)*unit_size, (int(driver.y) + 2)*unit_size), (0, 0, 0), -1)
                elif(driver.state == 1):
                    cv2.rectangle(image, (int(driver.x)*unit_size, int(driver.y)*unit_size), ((int(driver.x) + 2)*unit_size, (int(driver.y) + 2)*unit_size), (50, 98, 255), -1)
                elif(driver.state == 2):
                    cv2.rectangle(image, (int(driver.x)*unit_size, int(driver.y)*unit_size), ((int(driver.x) + 2)*unit_size, (int(driver.y) + 2)*unit_size), (255, 0, 0), -1)

        """
        states = np.asarray([operators[i].cars[j].state for i in range(0, num_operators) for j in range(0, num_cars_per_op)])
        idx0 = np.where(states == 0)
        idx1 = np.where(states == 1)
        idx2 = np.where(states == 2)
        count0_vec.append(len(states[idx0]))
        count1_vec.append(len(states[idx1]))
        count2_vec.append(len(states[idx2]))
        """

        file_name = "sim" + format(i, '0>5') + ".png"
        cv2.imwrite(file_name, image)

    eff_ratio_vec = []
    total_stock = 0
    total_processing = 0
    for op in operators:
        eff_ratio_vec = eff_ratio_vec + op.ratio_vec
        total_stock += len(op.stock)
        for dv in op.drivers:
            if(dv.state != 0):
                total_processing += 1
    print("Processed Order Count: " + str(len(eff_ratio_vec)))
    print("Processed Efficienty : " + str(sum(eff_ratio_vec)/len(eff_ratio_vec)))
    print("Total Order COunt    : " + str(total_order_count))
    print("Length of Callings   : " + str(len(calling_orders)))
    print("Number of Stocks     : " + str(total_stock))
    print("Number of Processings: " + str(total_processing))

    # pdb.set_trace()
