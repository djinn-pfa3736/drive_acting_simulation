import sys
import random
import numpy as np
import cv2

import matplotlib.pyplot as plt
import pdb

class Primary:
    state = 0
    """
    0: Waiting
    1: Moving to get order
    2: Moving to salbage secondary
    3: No secondary
    """
    x = 0
    y = 0
    dest_x = 0
    dest_y = 0

    sec_count = 0
    move_random = 0
    move_total = 0

    def __init__(self, init_x, init_y, num_secs):
        self.x = init_x
        self.y = init_y
        self.sec_count = num_secs

    def set_dest(self, dest_x, dest_y):
        self.dest_x = dest_x
        self.dest_y = dest_y

    def move(self, grid_size, secondary_queue):
        if (self.state == 0):

            # No order process
            dir = random.randrange(0, 5)

            if(dir == 1):
                self.y -= 1
            elif(dir == 2):
                self.x -= 1
            elif(dir == 3):
                self.y += 1
            elif(dir == 4):
                self.x += 1

            self.move_random += 1

        else:

            # Move one step to destination
            move_flag = 0
            if(self.dest_x != self.x):
                self.x += (self.dest_x - self.x)/np.abs(self.dest_x - self.x)
                move_flag = 1
                self.move_total += 1
            if(self.dest_y != self.y):
                self.y += (self.dest_y - self.y)/np.abs(self.dest_y - self.y)
                move_flag = 1
                self.move_total += 1

            if(move_flag == 0):

                # When current position of primary is at destination
                if(self.state == 1):

                    # Primary is moving to put secondary
                    if(0 < self.sec_count):
                        self.state = 0
                        sec = secondary_queue.dequeue()
                        sec.x = self.x
                        sec.y = self.y
                        dest_x = int(random.randrange(0, grid_size))
                        dest_y = int(random.randrange(0, grid_size))
                        sec.set_dest(dest_x, dest_y)
                        sec.state = 1
                        secondary_queue.enqueue(sec)
                        self.sec_count -= 1
                    if(self.sec_count == 0):
                        self.state = 3
                else:

                    # Primary is moving to salbage secondary
                    sec, secondary_queue = secondary_queue.find_and_remove(self.x, self.y)
                    self.sec_count += 1
                    self.state = 0
                    sec.state = 0
                    secondary_queue.enqueue(sec)

    def calc_dist(self, x, y):
        dist = np.sqrt((self.x - x)**2 + (self.y - y)**2)
        return dist

class Secondary:

    state = 0
    """
    0: Waiting to be set order
    1: Moving to destination
    2: Waiting to be salbaged
    """

    x = 0
    y = 0
    dest_x = 0
    dest_y = 0

    move_total = 0

    def __init__(self, init_x, init_y):
        self.x = init_x
        self.y = init_y

    def set_dest(self, dest_x, dest_y):
        self.dest_x = dest_x
        self.dest_y = dest_y

    def move(self, grid_size, salbage_list):
        if(self.state == 1):
            move_flag = 0
            if(self.dest_x != self.x):
                self.x += (self.dest_x - self.x)/np.abs(self.dest_x - self.x)
                move_flag = 1
                self.move_total += 1
            if(self.dest_y != self.y):
                self.y += (self.dest_y - self.y)/np.abs(self.dest_y - self.y)
                move_flag = 1
                self.move_total += 1

            if(move_flag == 0):
                self.state = 2
                salbage_list.push([self.x, self.y])

class SalbagePointList:

    def __init__(self):
        self.coords_list = []

    def get_len(self):
        return len(self.coords_list)

    def push(self, coords):
        self.coords_list.append(coords)

    def pop(self):
        return self.coords_list.pop()

class PrimaryList:

    primaries = []

    def __init__(self, num_prims, num_secs):
        for i in range(0, num_prims):
            init_x = int(random.randrange(0, grid_size))
            init_y = int(random.randrange(0, grid_size))
            prim = Primary(init_x, init_y, num_secs)
            self.primaries.append(prim)

    def get(self, idx):
        return self.primaries[idx]

    def get_order(self, order_prob):
        num_prims = len(self.primaries)
        prob = random.uniform(0.0, 1.0)

        if(prob < order_prob):
            dest_x = random.randrange(0, grid_size)
            dest_y = random.randrange(0, grid_size)

            dist_vec = []
            for i in range(0, num_prims):
                primary = self.primaries[i]
                dist_vec.append(primary.calc_dist(dest_x, dest_y))

            ord = np.argsort(dist_vec)
            for idx in ord:
                primary = self.primaries[idx]
                if(primary.state == 0 and 0 < primary.sec_count):
                    primary.set_dest(dest_x, dest_y)
                    primary.state = 1
                    break

    def set_salbage(self, salbage_list):
        for i in range(0, len(self.primaries)):
            prim = self.primaries[i]
            if(prim.state == 0 or prim.state == 3):
                if(0 < salbage_list.get_len()):
                    dist_vec = []
                    for coords in salbage_list.coords_list:
                        dist = prim.calc_dist(coords[0], coords[1])
                        dist_vec.append(dist)

                    ord = np.argsort(dist_vec)
                    for idx in ord:
                        coords = salbage_list.coords_list[idx]
                        prim.state = 2
                        prim.set_dest(coords[0], coords[1])
                        break
                    salbage_list.coords_list.pop(idx)

class SecondaryQueue:

    queue = []

    def __init__(self):
        self.queue = []

    def random_gen(self, num_total):
        for i in range(0, num_total):
            sec = Secondary(-1, -1)
            self.queue.append(sec)

    def get(self, idx):
        return self.queue[idx]

    def get_len(self):
        return len(self.queue)

    def enqueue(self, sec):
        self.queue.append(sec)

    def dequeue(self):
        return self.queue.pop(0)

    def find_and_remove(self, x, y):
        sec = Secondary(-1, -1)
        new_queue = SecondaryQueue()
        for i in range(0, len(self.queue)):
            tmp = self.queue[i]
            if(tmp.x == x and tmp.y == y):
                sec = tmp
            else:
                new_queue.enqueue(tmp)

        return sec, new_queue

args = sys.argv
num_prims = int(args[1])
num_secs = int(args[2])
grid_size = int(args[3])
sim_count = int(args[4])
busy_max = int(args[5])
supply_const = float(args[6])
plot_flag = int(args[7])

primary_list = PrimaryList(num_prims, num_secs)

secondary_queue = SecondaryQueue()
secondary_queue.random_gen(num_prims*num_secs)

salbage_list = SalbagePointList()

busy_num = 0

order_supply = supply_const*num_prims*num_secs
order_prob = order_supply/sim_count

count0_vec = [num_prims]
count1_vec = [0]
count2_vec = [0]

for i in range(0, sim_count):
    print("*** Simulating " + str(i) + "-th Step ***")

    if(plot_flag == 1):
        unit_size = 10
        image = np.zeros((unit_size*grid_size, unit_size*grid_size, 3))
        inv_idx = np.where(image == 0)
        image[inv_idx] = 255

    primary_list.get_order(order_prob)
    primary_list.set_salbage(salbage_list)

    for j in range(0, num_prims):
        primary = primary_list.get(j)
        primary.move(grid_size, secondary_queue)

        if(plot_flag == 1):
            if(primary.state == 0):
                cv2.rectangle(image, (int(primary.x)*unit_size, int(primary.y)*unit_size), ((int(primary.x) + 2)*unit_size, (int(primary.y) + 2)*unit_size), (0, 0, 0), -1)
            elif(primary.state == 1):
                cv2.rectangle(image, (int(primary.x)*unit_size, int(primary.y)*unit_size), ((int(primary.x) + 2)*unit_size, (int(primary.y) + 2)*unit_size), (50, 98, 255), -1)
            elif(primary.state == 2):
                cv2.rectangle(image, (int(primary.x)*unit_size, int(primary.y)*unit_size), ((int(primary.x) + 2)*unit_size, (int(primary.y) + 2)*unit_size), (255, 0, 0), -1)
            elif(primary.state == 3):
                cv2.rectangle(image, (int(primary.x)*unit_size, int(primary.y)*unit_size), ((int(primary.x) + 2)*unit_size, (int(primary.y) + 2)*unit_size), (0, 0, 255), -1)

    # pdb.set_trace()

    for j in range(0, secondary_queue.get_len()):
        secondary = secondary_queue.get(j)
        secondary.move(grid_size, salbage_list)


        if(plot_flag == 1):
            """
            if(secondary.state == 0):
                cv2.rectangle(image, (int(secondary.x)*unit_size, int(secondary.y)*unit_size), ((int(secondary.x) + 2)*unit_size, (int(secondary.y) + 2)*unit_size), (0, 0, 0), -1)
            elif(secondary.state == 1):
                cv2.rectangle(image, (int(secondary.x)*unit_size, int(secondary.y)*unit_size), ((int(secondary.x) + 2)*unit_size, (int(secondary.y) + 2)*unit_size), (25, 25, 255), -1)
            elif(secondary.state == 2):
                cv2.rectangle(image, (int(secondary.x)*unit_size, int(secondary.y)*unit_size), ((int(secondary.x) + 2)*unit_size, (int(secondary.y) + 2)*unit_size), (0, 255, 0), -1)
            """
            if(secondary.state == 1):
                cv2.circle(image, (int(secondary.x)*unit_size + int(unit_size/2), int(secondary.y)*unit_size + int(unit_size/2)), int(unit_size/2), (25, 25, 255), -1)
            elif(secondary.state == 2):
                cv2.circle(image, (int(secondary.x)*unit_size + int(unit_size/2), int(secondary.y)*unit_size + int(unit_size/2)), int(unit_size/2), (0, 255, 0), -1)
    if(plot_flag == 1):
        file_name = "sim" + format(i, '0>5') + ".png"
        cv2.imwrite(file_name, image)

move_primary = 0
for j in range(0, num_prims):
    primary = primary_list.get(j)
    move_primary += primary.move_total
move_secondary = 0
for j in range(0, secondary_queue.get_len()):
    secondary = secondary_queue.get(j)
    move_secondary += secondary.move_total
print(move_secondary/(move_primary + move_secondary))
