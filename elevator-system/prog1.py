"""
-> Has only 1 elevator
-> Has floor buttons inside elevator, pressing
   whom calls the evelator.add_request(floor)
-> Has only call elevator button on each floor
   (not up and down), pressing whom calls the
   elevator.add_request(floor)
-> Uses FCFS algo
"""

import time
from enum import Enum

class Direction(Enum):
    UP = 1
    DOWN = -1
    IDLE = 0

class Elevator:
    def __init__(self, total_floors):
        self.current_floor = 0
        self.direction = Direction.IDLE
        self.total_floors = total_floors
        # Using list to maintain order of requests (FCFS)
        self.request_queue = []

    def add_request(self, floor):
        if floor < 0 or floor >= self.total_floors:
            print(f"Error: Floor {floor} is out of bounds.")
            return

        if floor == self.current_floor:
            print(f"Already at floor {floor}.")
            return
        
        # Avoid duplicate requests
        if floor not in self.request_queue:
            self.request_queue.append(floor)
            print(f"Request added: Floor {floor}")

    def process_requests(self):
        while self.request_queue:
            # FCFS: Process the first request in the queue
            target_floor = self.request_queue[0]
            
            # Determine direction to target floor
            if target_floor > self.current_floor:
                self.direction = Direction.UP
                self._move_to_floor(target_floor)

            elif target_floor < self.current_floor:
                self.direction = Direction.DOWN
                self._move_to_floor(target_floor)
            
            # Remove the serviced request
            self.request_queue.pop(0)
        
        self.direction = Direction.IDLE
        print("All requests serviced. Elevator is now IDLE.")

    def _move_to_floor(self, target_floor):
        direction_str = "UP" if self.direction == Direction.UP else "DOWN"
        print(f"--- Moving {direction_str} from {self.current_floor} to {target_floor} ---")
        
        # Move floor by floor
        step = 1 if target_floor > self.current_floor else -1
        
        for floor in range(self.current_floor, target_floor + step, step):
            self.current_floor = floor
            time.sleep(0.5)  # Simulating travel time
        
        # Stop at target floor
        self._stop_at_floor(target_floor)

    def _stop_at_floor(self, floor):
        print(f"[STOP] Reached Floor {floor}. Opening Doors...")
        time.sleep(1)  # Simulating passengers getting in/out
        print(f"[STOP] Closing Doors.")

# --- Demo Execution ---
if __name__ == "__main__":
    my_elevator = Elevator(total_floors=10)

    # Simulating users pressing buttons 
    print("Requests received: Floor 3, Floor 8, Floor 1")
    my_elevator.add_request(3)
    my_elevator.add_request(8)
    my_elevator.add_request(1)

    print("\n=== Processing with FCFS Algorithm ===\n")
    my_elevator.process_requests()

