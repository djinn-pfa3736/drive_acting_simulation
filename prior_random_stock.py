import sys
import random
import numpy as np
import cv2
import matplotlib.pyplot as plt

from drive_act_class import *

import pdb

class PriorOperator(Operator):
    pass

    def get_order(self):
        hit_flag = False
        if(0 < len(self.stock)):
            for i in range(0, len(self.stock)):
                order = self.stock[i]
                if(order.gender == 'female'):
                    hit_flag = True
                    del self.stock[i]
                    break
            if(hit_flag == False):
                order = self.stock.pop()
        else:
            order = -1
        return order

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
        operator = PriorOperator(max_stock, area)

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
                # print(j)
                for op in operators:
                    add_flag = op.add_order(order)
                    if(add_flag == True):
                        full_flag = False
                        del_elms.append(order)
                        break
                if(full_flag == True):
                    # pdb.set_trace()
                    break

            # if(0 < len(del_elms)):
            #     pdb.set_trace()
            for elm in del_elms:
                calling_orders.remove(elm)

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
