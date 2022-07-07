class Order:
    def __init__(self, shop_coord, dest_coord, generated_time, deadline_length):
        self.shop_coord = shop_coord
        self.dest_coord = dest_coord
        self.generated_time = generated_time
        self.deadline_length = deadline_length
        self.process_start_time = -1
        self.process_end_time = -1
