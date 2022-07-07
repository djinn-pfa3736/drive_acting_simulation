import numpy as np

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
                distances = [np.sum(np.abs(np.array(appli_queue[i].shop_coord) - np.array(self.dest_coord))) for i in range(len(appli_queue))]
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
