import sys
import random
import numpy as np

import matplotlib.pyplot as plt
import pdb

class Driver:

    state = 0
    move_total = 0
    move_fee = 0
    move_random = 0
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

    def random_walk(self):
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

    def move(self, grid_size):

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
                dist_x = int(random.randrange(0, grid_size))
                dist_y = int(random.randrange(0, grid_size))
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
radius = float(args[5])

cars = []
busy_num = 0

for i in range(0, num_cars):
    init_x = int(random.randrange(0, grid_size))
    init_y = int(random.randrange(0, grid_size))
    car = Driver(init_x, init_y)
    cars.append(car)

for i in range(0, sim_count):
    print("*** Simulating " + str(i) + "-th Step ***")
    busy_count = 0

    dest_x = random.randrange(0, grid_size)
    dest_y = random.randrange(0, grid_size)

    catch_flag = 0
    for j in range(0, num_cars):

        car = cars[j]
        if(car.calc_dist(dest_x, dest_y) < radius):
            if(car.state == 0):
                car.set_dest(dest_x, dest_y)
                car.state = 1
                catch_flag = 1
                # pdb.set_trace()
                break

        if(catch_flag == 0):
            while(True):
                car_idx = random.randrange(0, num_cars)
                car = cars[car_idx]
                if(car.state == 0):
                    car.set_dest(dest_x, dest_y)
                    car.state = 1
                    break

                if(busy_max < busy_count):
                    busy_num += 1
                    break
                busy_count += 1

    for j in range(0, num_cars):
        car = cars[j]
        if(car.state == 0):
            car.random_walk()
        else:
            car.move(grid_size)

scores = [0 for i in range(0, num_cars)]
random_move = [0 for i in range(0, num_cars)]
for i in range(0, num_cars):
    car = cars[i]
    if(car.move_total != 0):
        score = car.move_fee / car.move_total
        scores[i] = score
        random_move[i] = car.move_random

pdb.set_trace()
