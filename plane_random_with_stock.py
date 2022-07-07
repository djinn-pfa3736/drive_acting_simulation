import sys
import random
import numpy as np
import cv2

import matplotlib.pyplot as plt
import pdb

class Operator:

    def __init__(self, max_stock):
        self.max_stock = max_stock
        self.cars = []
        self.stock = []

    def set_cars(self, cars):
        self.cars = cars

    def add_dest(self, dest):
        self.stock.append(dest)
        # pdb.set_trace()

    def get_dest(self):
        stock = self.stock.pop()

        return stock

    def check_empty_car(self):
        empty_idx = -1
        for i in range(0, len(self.cars)):
            car = self.cars[i]
            if(car.state == 0):
                empty_idx = i
                break

        return empty_idx

class Driver:

    def __init__(self, init_x, init_y):
        self.x = init_x
        self.y = init_y
        self.state = 0
        self.move_total = 0
        self.move_fee = 0
        self.move_random = 0
        self.dest_x = 0
        self.dest_y = 0

    def set_dest(self, dest_x, dest_y):
        self.dest_x = dest_x
        self.dest_y = dest_y

    def move(self, grid_size, operator):

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

        else:
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
                    if(len(operator.stock) != 0):
                        self.state = 1
                        dest = operator.get_dest()
                        self.set_dest(dest[0], dest[1])
                    else:
                        self.state = 0

args = sys.argv
num_cars_per_op = int(args[1])
num_operators = int(args[2])
grid_size = int(args[3])
sim_count = int(args[4])
busy_max = int(args[5])
stock_max = int(args[6])
supply_const = int(args[7])
plot_flag = int(args[8])

operators = []
busy_num = 0
for i in range(0, num_operators):
    cars = []
    for j in range(0, num_cars_per_op):
        init_x = int(random.randrange(0, grid_size))
        init_y = int(random.randrange(0, grid_size))
        car = Driver(init_x, init_y)
        cars.append(car)
    operator = Operator(stock_max)
    operator.set_cars(cars)
    operators.append(operator)

order_supply = supply_const*num_cars_per_op*num_operators
order_prob = order_supply/sim_count

count0_vec = [num_operators*num_cars_per_op]
count1_vec = [0]
count2_vec = [0]


for i in range(0, sim_count):
    print("*** Simulating " + str(i) + "-th Step ***")
    busy_count = 0

    prob = random.uniform(0.0, 1.0)
    if(prob < order_prob):
        dest_x = random.randrange(0, grid_size)
        dest_y = random.randrange(0, grid_size)

        while(True):
            operator_idx = random.randrange(0, num_operators)
            operator = operators[operator_idx]
            car_idx = operator.check_empty_car()

            if(car_idx == -1):
                if(len(operator.stock) == stock_max):
                    busy_count += 1
                else:
                    operator.add_dest([dest_x, dest_y])
                    break
            else:
                operator.cars[car_idx].state = 1
                operator.cars[car_idx].set_dest(dest_x, dest_y)
                break

            if(busy_max < busy_count):
                busy_num += 1
                break

    if(plot_flag == 1):
        unit_size = 15
        image = np.zeros((unit_size*grid_size, unit_size*grid_size, 3))
        inv_idx = np.where(image == 0)
        image[inv_idx] = 255

    for j in range(0, num_operators):
        for k in range(0, num_cars_per_op):

            operator = operators[j]
            car = operator.cars[k]
            car.move(grid_size, operator)
            if(plot_flag == 1):
                if(car.state == 0):
                    cv2.rectangle(image, (int(car.x)*unit_size, int(car.y)*unit_size), ((int(car.x) + 2)*unit_size, (int(car.y) + 2)*unit_size), (0, 0, 0), -1)
                elif(car.state == 1):
                    cv2.rectangle(image, (int(car.x)*unit_size, int(car.y)*unit_size), ((int(car.x) + 2)*unit_size, (int(car.y) + 2)*unit_size), (50, 98, 255), -1)
                elif(car.state == 2):
                    cv2.rectangle(image, (int(car.x)*unit_size, int(car.y)*unit_size), ((int(car.x) + 2)*unit_size, (int(car.y) + 2)*unit_size), (255, 0, 0), -1)

    states = np.asarray([operators[i].cars[j].state for i in range(0, num_operators) for j in range(0, num_cars_per_op)])
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
height = scale_y*num_operators*num_cars_per_op

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

scores = []
random_move = []
for i in range(0, num_operators):
    operator = operators[i]
    for j in range(0, num_cars_per_op):
        car = operator.cars[j]
        if(car.move_total != 0):
            score = car.move_fee / car.move_total
            scores.append(score)
            random_move.append(car.move_random)
            
pdb.set_trace()
