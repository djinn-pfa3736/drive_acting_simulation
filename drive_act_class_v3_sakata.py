import sys
import random	#OpenCV module
import numpy as np
import cv2
import matplotlib.pyplot as plt

import pdb  #debuger module

# add ksakata
def angle_between(p1, p2):
    ang1 = np.arctan2(*p1[::-1])
    ang2 = np.arctan2(*p2[::-1])
    return (ang1 - ang2)

##Class difinition
class Operator:
    def __init__(self, operator_id, area, tactics):
        self.operator_id = operator_id
        self.field_id = field_id
        self.area = area
        self.drivers = []
        self.tactics = tactics
        self.tactics_update_schedule

        self.cum_order_count = 0
        self.cum_passing_count = 0

    def set_drivers(self, drivers):
        self.drivers = drivers

    def set_tactics(self, tactics):
        self.tactics = tactics

    def assign_order(self, current_time, whole_operators, order):
        operator_id, driver_id = self.tactics(self.operator_id, whole_operators, order)
        if driver_id != -1:
            order.process_start_time = current_time
            whole_operators[operator_id].drivers[driver_id].set_order(order)
            if operator_id == self.operator_id:
                self.cum_order_count += 1
            else:
                self.cum_passing_count += 1

            return 0
        else:
            return -1

class Driver:
    def __init__(self, driver_id, operator_id, state, current_position, waiting_position, waiting_size, waiting_tactics):

        self.driver_id = driver_id
        self.operator = operator_id
        self.state = state
        self.current_position = current_position
        self.waiting_position = waiting_position
        self.waiting_size = waiting_size
        self.waiting_tactics = waiting_tactics

        self.order = null
        self.total_drive = 0
        self.act_drive = 0
        self.total_drive_list = []
        self.act_drive_list = []

    def set_state(self, state):
        self.state = state

    def set_order(self, order):
        if self.state == 0:
            self.order = order
            set_flag = True
        else:
            set_flag = False
        return set_flag

    def update_position(self):

        if self.state == 1 or self.state == 2:
            self.total_drive += 1
        if self.state == 2:
            self.act_drive += 1

        if self.state == 0:
            dx, dy = self.waiting_tactics()

        elif self.state == 1:
            shop_position = self.order.shop_position
            dx = shop_position[0] - self.current_position[0]
            dy = shop_position[1] - self.current_position[1]

            if dx != 0:
                dx = dx / abs(dx)

            if dy != 0:
                dy = dy / abs(dy)

            if dx == 0 and dy == 0:
                self.set_state(2)

        elif self.state == 2:
            home_position = self.order.home_position
            dx = home_position[0] - self.current_position[0]
            dy = home_position[1] - self.current_position[1]

            if dx != 0:
                dx = dx / abs(dx)

            if dy != 0:
                dy = dy / abs(dy)

            if dx == 0 and dy == 0:
                self.set_state(0)
                self.total_drive_list.append(total_drive)
                self.act_ratio_list.append(act_drive)
                self.act_drive = 0
                self.total_drive = 0

        self.current_position + [dx, dy]

class Order:
    def __init__(self, shop_position, home_position, generated_time, deadline):
        self.shop_position = shop_position
        self.home_position = home_position
        self.generated_time = generated_time
        self.deadline_length = deadline_length
        self.process_start_time = -1
        self.process_end_time = -1

class Map:
    def __init__(self, shop_distribution, home_distribution):
        self.shop_distribution = shop_distribution
        self.home_distribution = home_distribution

    def generate_order(self, simulation_time, deadline):
        shop_position = self.sample_shop_position()
        home_position = self.sample_home_position()
        order = Order(shop_position, home_position, simulation_time, deadline)

        return order

    def sample_shop_position(self):

        # Not implemented yet
        pass

    def sample_home_position(self):

        # Not implemented yet
        pass

class World:
    def __init__(self, map, operators, drivers, lambda_parameter_list, simulation_last_time, tactics_update_list, deadline_distribution):
        self.map = map
        self.operators = operators
        self.drivers = drivers
        self.lambda_parameter_list = lambda_parameter_list
        self.simulation_last_time = simulation_last_time
        self.tactics_update_list = tactics_update_list
        self.deadline_distribution = deadline_distribution

        self.simulation_time = 0
        self.order_queue = []
        self.not_processed_order = 0

        def update_state(self):
            # Not implemented yet
            pass

class Tactics:
    @classmethod
    def in_house_random(cls, operator_id, whole_operators, order):
        # add ksakata
        drivers = whole_operators[operator_id].drivers
        driver_states = [drivers[i].state for i in range(0, len(drivers))]# get draivers states
        empty_index = np.where(driver_states == 0, True, False)
        if np.sum(empty_index) == 0:
            return -1, -1
        else:
          dice = list(range(0, len(drivers)))
          random_select_drivers_index = np.random.choice(dice,dice)# create random index of drivers

          count = 0
          while(count < len(drivers)):
                random_index = random_select_drivers_index[count]# select of random drivers id
                if drivers[random_index].state != 0:
                    drivers[nearest_index] = 100000   # ???�v�m�F
                else:
                    return operator_id, nearest_index
                count += 1

    @classmethod
    def totally_random(cls, operator_id, whole_operators, order):
        # add ksakata
        select_of_operators_id = np.random.choice(len(whole_operators))# select of random oprators_id
        drivers = whole_operators[select_of_operators_id].drivers
        driver_states = [drivers[i].state for i in range(0, len(drivers))]# get draivers states
        empty_index = np.where(driver_states == 0, True, False)
        if np.sum(empty_index) == 0:
            return -1, -1
        else:
          dice_of_drivers = list(range(0, len(drivers)))
          random_select_drivers_index = np.random.choice(dice_of_drivers,dice_of_drivers)# create random index of drivers

          count = 0
          while(count < len(drivers)):
                random_index = random_select_drivers_index[count]# select of random drivers id
                if drivers[random_index].state != 0:
                    drivers[nearest_index] = 100000   # ???�v�m�F
                else:
                    return operator_id, nearest_index
                count += 1

    @classmethod
    def in_house_nearest(cls, operator_id, whole_operators, order):
        drivers = whole_operators[operator_id].drivers
        driver_states = [drivers[i].state for i in range(0, len(drivers))]
        empty_index = np.where(driver_states == 0, True, False)
        if np.sum(empty_index) == 0:
            return -1, -1
        else:
            shop_position = order.shop_position
            positions = [drivers[i].current_position for i in range(0, len(drivers))]
            distances = [sum(abs(shop_position - positions[i])) for i in range(0, len(drivers))]

            count = 0
            while(count < len(drivers)):
                nearest_index = np.argmin(distances)
                if drivers[nearest_index].state != 0:
                    #drivers[nearest_index] = 100000   # ???�m�F
                    # add ksakata
                    distances[nearest_index] = 100000  # �I���Ώۂ̋����ɑ傫�Ȓl�������ď��O�����ق������������H
                else:
                    return operator_id, nearest_index
                count += 1

    @classmethod
    def totally_nearest(cls, operator_id, whole_operators, order):
        # add ksakata
        # init
        drivers_ids      = np.zeros(len(whole_operators))
        operator_ids     = np.zeros(len(whole_operators))
        nearest_distance = np.zeros(len(whole_operators))

        # change operators
        for n in range(0, len(whole_operators)):
            drivers = whole_operators[n].drivers# get drivers
            driver_states = [drivers[i].state for i in range(0, len(drivers))]
            empty_index = np.where(driver_states == 0, True, False)
            if np.sum(empty_index) == 0:
                return -1, -1
            else:
                shop_position = order.shop_position
                positions = [drivers[i].current_position for i in range(0, len(drivers))]
                distances = [sum(abs(shop_position - positions[i])) for i in range(0, len(drivers))]

                count = 0
                while(count < len(drivers)):
                    nearest_index = np.argmin(distances)
                    if drivers[nearest_index].state != 0:
                        #drivers[nearest_index] = 100000   # ???�m�F
                        distances[nearest_index] = 100000   # �I���Ώۂ̋����ɑ傫�Ȓl�������ď��O�����ق������������H
                    else:
                        drivers_ids[n]  = nearest_index
                        operator_ids[n] = n
                        nearest_distances = distances[count]
                    count += 1

        totally_nearest_index = np.argmin(nearest_distance)
        operator_id           = operator_ids[totally_nearest_index]
        drivers_id            = drivers_ids[totally_nearest_index]
        return operator_id, drivers_id


    @classmethod
    def in_house_home_nearest(cls, operator_id, whole_operators, order):
        # add ksakata
        drivers = whole_operators[operator_id].drivers
        driver_states = [drivers[i].state for i in range(0, len(drivers))]
        empty_index = np.where(driver_states == 0, True, False)
        if np.sum(empty_index) == 0:
            return -1, -1
        else:
            shop_position = order.shop_position
            home_position = order.home_position
            house_positions = [diver[i].waiting_position for i in range(0,len(drivers))]

            positions = [drivers[i].current_position for i in range(0, len(drivers))]
            shop_distances = [sum(abs(shop_position - positions[i])) for i in range(0, len(drivers))]
            house_current_distances = [sum(abs(house_positions[i] - positions[i])) for i in range(0,len(drivers))]
            house_home_distances = [sum(abs(house_positions[i] - home_position)) for i in range(0,len(drivers))]

            # Step1  house_current_distances > house_home_distances : ���݈ʒu��house�̋��������Ahouse��home�̋����̕���������
            d_distances = [(house_current_distances[i] - house_home_distances[i]) for i in range(0,len(drivers))]

            # Step2 calc of inner product : theta_house_current_home < theta_th(parameter = pi/4�`sqrt(3)/2*pi���炢?)
            # Not implemented yet
            count = 0
            while(count < len(drivers)):

                # Step3 ���苗���ȓ��ň���house���牓��driver���I��
                farther_index = np.argmax(house_current_distances)
                if drivers[nearest_index].state != 0:
                    #drivers[nearest_index] = 100000   # ???�m�F
                    house_current_distances[farther_index] = 100000  # �I���Ώۂ̋����ɑ傫�Ȓl�������ď��O�����ق������������H
                else:
                    p1 = home_position - positions[count]
                    p2 = house_positions[count] -  positions[count]
                    angle = angle_between(p1, p2)

                    # Step4 Dot product calculation
                    if (angle < np.pi/8) or (angle > np.pi*(15/8)): # parameter
                        return operator_id, farther_index
                    else:
                        pass
                count += 1

    @classmethod
    def totally_home_nearest(cls, operator_id, whole_operators, order):
        # add ksakata
        # init
        drivers_ids        = np.zeros(len(whole_operators))
        operator_ids       = np.zeros(len(whole_operators))
        most_far_distances = np.zeros(len(whole_operators))

        # change operators
        for n in range(0, len(whole_operators)):
            # add ksakata
            drivers = whole_operators[operator_id].drivers
            driver_states = [drivers[i].state for i in range(0, len(drivers))]
            empty_index = np.where(driver_states == 0, True, False)
            if np.sum(empty_index) == 0:
                return -1, -1
            else:
                shop_position = order.shop_position
                home_position = order.home_position
                house_positions = [diver[i].waiting_position for i in range(0,len(drivers))]

                positions = [drivers[i].current_position for i in range(0, len(drivers))]
                shop_distances = [sum(abs(shop_position - positions[i])) for i in range(0, len(drivers))]
                house_current_distances = [sum(abs(house_positions[i] - positions[i])) for i in range(0,len(drivers))]
                house_home_distances = [sum(abs(house_positions[i] - home_position)) for i in range(0,len(drivers))]

                # Step1  house_current_distances > house_home_distances : ���݈ʒu��house�̋��������Ahouse��home�̋����̕���������
                d_distances = [(house_current_distances[i] - house_home_distances[i]) for i in range(0,len(drivers))]

                # Step2 calc of inner product : theta_house_current_home < theta_th(parameter = pi/4�`sqrt(3)/2*pi���炢?)
                # Not implemented yet
                count = 0
                while(count < len(drivers)):

                    # Step3 ���苗���ȓ��ň���house���牓��driver���I��
                    farther_index = np.argmax(house_current_distances)
                    if drivers[nearest_index].state != 0:
                        #drivers[nearest_index] = 100000   # ???�m�F
                        house_current_distances[farther_index] = 100000  # �I���Ώۂ̋����ɑ傫�Ȓl�������ď��O�����ق������������H
                    else:
                        p1 = home_position - positions[count]
                        p2 = house_positions[count] -  positions[count]
                        angle = angle_between(p1, p2)

                        # Step4 Dot product calculation
                        if (angle < np.pi/8) or (angle > np.pi*(15/8)): # parameter
                            drivers_ids[n]     = farther_index
                            operator_ids[n]    = n
                            most_far_distances = distances[count]
                            return operator_id, nearest_index
                        else:
                            pass

                    count += 1
        # max
        totally_mast_far_index = np.argmax(most_far_distances)
        operator_id           = operator_ids[totally_mast_far_index]
        drivers_id            = drivers_ids[totally_mast_far_index]
        return operator_id, drivers_id

## main



## EOF
