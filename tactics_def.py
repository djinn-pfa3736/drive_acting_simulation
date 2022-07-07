import numpy as np
import random

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
