import sys
import random
import numpy as np
import cv2

import matplotlib.pyplot as plt
import pdb

running_secondaries = []

class Request:
    x = 0
    y = 0

    def __init__(self, init_x, init_y):
        self.x = init_x
        self.y = init_y

class Primary:

    state = 0
    """ 0: 搬送可能(注文受け付け中) """
    """ 1: Secondary搬送中 """
    """ 2: Secondary回収中 """
    move_total = 0
    move_fee = 0
    move_random = 0
    x = 0
    y = 0
    dest_x = 0
    dest_y = 0

    secondary_list = []

    def __init__(self, init_x, init_y, num_sec):
        self.x = init_x
        self.y = init_y
        for(i in range(num_sec)):
            sec = new Secondary(init_x, init_y)
            self.secondary_list.append(sec)

    def set_dest(self, dest_x, dest_y):



        gexn72da
        gexn72da
        gexn72da

        self.dest_x = dest_x
        self.dest_y = dest_y

    def move(self, grid_size):

        if(self.state == 0):
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

        elif(self.state == 1):
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
                if(self.state == 1):
                    sec = pop(self.secondary_list)
                    dest_x = int(random.randrange(0, grid_size))
                    dest_y = int(random.randrange(0, grid_size))
                    sec.set_dest(dest_x, dest_y)
                    running_secondaries.append(sec)
                    if(len(self.secondary_list) == 0):
                        self.state = 2
                elif(self.state == 2):
                    self.state = 0

    def calc_dist(self, x, y):
        dist = np.sqrt((self.x - x)**2 + (self.y - y)**2)
        return dist


class Secondary:

    state = 0
    """ 0: 移動中 """
    """ 1: 搬送中 """
    """ 2: 待機中 """
    move_total = 0
    move_fee = 0
    x = 0
    y = 0
    dest_x = 0
    dest_y = 0

    def __init__(self, init_x, init_y):
        self.x = init_x
        self.y = init_y

    def set_dest(self, dest_x, dest_y):
        self.dest_x = dest_x
        self.dest_y = dest_y

    def move(self, grid_size):

        if self.state == 1:
            move_flag = 0
            if(self.dest_x != self.x):
                self.x += (self.dest_x - self.x)/np.abs(self.dest_x - self.x)
                move_flag = 1
                if(self.state == 1):
                    self.move_total += 1
                elif(self.state == 2):
                    self.move_total += 1
                    self.move_fee += 1
            if(self.dest_y != self.y):
                self.y += (self.dest_y - self.y)/np.abs(self.dest_y - self.y)
                move_flag = 1
                if(self.state == 1):
                    self.move_total += 1
                elif(self.state == 2):
                    self.move_total += 1
                    self.move_fee += 1

            if(move_flag == 0):
                if(self.state == 1):
                    self.state = 2
                    dest_x = int(random.randrange(0, grid_size))
                    dest_y = int(random.randrange(0, grid_size))
                    self.set_dest(dest_x, dest_y)
                elif(self.state == 2):
                    self.state = 0

    def calc_dist(self, x, y):
        dist = np.sqrt((self.x - x)**2 + (self.y - y)**2)
        return dist



args = sys.argv
num_cars = int(args[1])
grid_size = int(args[2])
sim_count = int(args[3])
busy_max = int(args[4])
supply_const = float(args[5])
plot_flag = int(args[6])

primaries = []
secondaries = []
busy_num = 0

for i in range(0, num_cars):
    init_x = int(random.randrange(0, grid_size))
    init_y = int(random.randrange(0, grid_size))
    car = Primary(init_x, init_y)
    primaries.append(car)

order_supply = supply_const*num_cars
order_prob = order_supply/sim_count

count0_vec = [num_cars]
count1_vec = [0]
count2_vec = [0]

for i in range(0, sim_count):
    print("*** Simulating " + str(i) + "-th Step ***")

    prob = random.uniform(0.0, 1.0)
    if(prob < order_prob):
        dest_x = random.randrange(0, grid_size)
        dest_y = random.randrange(0, grid_size)

        dist_vec = []
        for j in range(0, num_cars):
            primary = primaries[j]
            dist_vec.append(car.calc_dist(dest_x, dest_y))

        accept_flag = 0
        ord = np.argsort(dist_vec)
        for car_idx in ord:
            car = cars[car_idx]
            if(car.state == 0):
                car.set_dest(dest_x, dest_y)
                car.state = 1
                accept_flag = 1
                break
                # pdb.set_trace()

        if(accept_flag == 0):
            busy_num += 1

    if(plot_flag == 1):
        unit_size = 10
        image = np.zeros((unit_size*grid_size, unit_size*grid_size, 3))
        inv_idx = np.where(image == 0)
        image[inv_idx] = 255

    for j in range(0, num_cars):
        car = cars[j]
        if(car.state == 0):
            car.random_walk()
        else:
            car.move(grid_size)

        if(plot_flag == 1):
            if(car.state == 0):
                cv2.rectangle(image, (int(car.x)*unit_size, int(car.y)*unit_size), ((int(car.x) + 2)*unit_size, (int(car.y) + 2)*unit_size), (0, 0, 0), -1)
            elif(car.state == 1):
                cv2.rectangle(image, (int(car.x)*unit_size, int(car.y)*unit_size), ((int(car.x) + 2)*unit_size, (int(car.y) + 2)*unit_size), (50, 98, 255), -1)
            elif(car.state == 2):
                cv2.rectangle(image, (int(car.x)*unit_size, int(car.y)*unit_size), ((int(car.x) + 2)*unit_size, (int(car.y) + 2)*unit_size), (255, 0, 0), -1)

    states = np.asarray([cars[i].state for i in range(0, num_cars)])
    idx0 = np.where(states == 0)
    idx1 = np.where(states == 1)
    idx2 = np.where(states == 2)
    count0_vec.append(len(states[idx0]))
    count1_vec.append(len(states[idx1]))
    count2_vec.append(len(states[idx2]))

    if(plot_flag == 1):
        file_name = "sim" + format(i, '0>5') + ".png"
        cv2.imwrite(file_name, image)

dx = 1
scale_y = 8
margin = 50
height = scale_y*num_cars

prev_dx = margin
graph = np.zeros((height + 2*margin, sim_count + 2*margin, 3))
inv_idx = np.where(graph == 0)
graph[inv_idx] = 255
cv2.line(graph, (margin, margin), (sim_count + margin, margin), (100, 100, 100), 1)
cv2.line(graph, (margin, margin), (margin, height + margin), (100, 100, 100), 1)
cv2.line(graph, (margin, height + margin), (sim_count + margin, height + margin), (100, 100, 100), 1)
cv2.line(graph, (sim_count + margin, margin), (sim_count + margin, height + margin), (100, 100, 100), 1)

for i in range(0, sim_count):
    start_x = margin + i*dx
    start_y = (height + margin) - 8*count0_vec[i]
    end_x = margin + (i + 1)*dx
    end_y = (height + margin) - 8*count0_vec[i+1]
    cv2.line(graph, (start_x, start_y), (end_x, end_y), (0, 0, 0), 2)

    start_x = margin + i*dx
    start_y = (height + margin) - 8*count1_vec[i]
    end_x = margin + (i + 1)*dx
    end_y = (height + margin) - 8*count1_vec[i+1]
    cv2.line(graph, (start_x, start_y), (end_x, end_y), (50, 98, 255), 2)

    start_x = margin + i*dx
    start_y = (height + margin) - 8*count2_vec[i]
    end_x = margin + (i + 1)*dx
    end_y = (height + margin) - 8*count2_vec[i+1]
    cv2.line(graph, (start_x, start_y), (end_x, end_y), (255, 0, 0), 2)


    file_name = "graph" + format(i, '0>5') + ".png"
    cv2.imwrite(file_name, graph)


scores = [0 for i in range(0, num_cars)]
random_move = [0 for i in range(0, num_cars)]
for i in range(0, num_cars):
    car = cars[i]
    if(car.move_total != 0):
        score = car.move_fee / car.move_total
        scores[i] = score
        random_move[i] = car.move_random
pdb.set_trace()
