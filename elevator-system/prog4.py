"""
-> Supports multiple elevators
-> Uses a direction aware dispatcher that can choose
   the best elevator to call on a hall call which is 
   either closest elevator in the same direction or 
   closest idle elevator or closest overall elevator
-> Has floor buttons inside each elevator, pressing
   whom calls the evelator.add_car_call(floor)
-> Has up and down buttons on each floor, pressing
   whom calls the dispatcher.find_best_elevator(hall_call)
   and then best_elevator.add_hall_call(hall_call)
-> Uses SCAN algo inside each elevator 
"""

import time
from enum import Enum
from typing import List, Optional

class Direction(Enum):
    UP = 1
    DOWN = -1
    IDLE = 0

class HallCall:
    """Represents a hall call (button press on a floor)"""
    def __init__(self, floor: int, direction: Direction):
        self.floor = floor
        self.direction = direction
        self.assigned_elevator_id: Optional[int] = None
    
    def __repr__(self):
        return f"HallCall(floor={self.floor}, direction={self.direction.name})"

class Elevator:
    """Individual elevator - manages only its own state and assigned requests"""
    def __init__(self, elevator_id: int, total_floors: int):
        self.id = elevator_id
        self.current_floor = 0
        self.direction = Direction.IDLE
        self.total_floors = total_floors
        self.car_calls = set()  # Destination floors from inside
        self.assigned_hall_calls = set()  # Hall calls assigned by dispatcher
    
    def add_car_call(self, floor: int):
        """Called when someone inside presses a floor button"""
        if floor < 0 or floor >= self.total_floors:
            print(f"[Elevator {self.id}] Error: Floor {floor} is out of bounds.")
            return
        
        if floor == self.current_floor:
            print(f"[Elevator {self.id}] Already at floor {floor}.")
            return
        
        self.car_calls.add(floor)
        print(f"[Elevator {self.id}] Car call added: Floor {floor}")
        
        # If IDLE, decide direction
        if self.direction == Direction.IDLE:
            self.direction = Direction.UP if floor > self.current_floor else Direction.DOWN
    
    def assign_hall_call(self, floor: int, direction: Direction):
        """Called by dispatcher to assign a hall call to this elevator"""
        self.assigned_hall_calls.add((floor, direction))
        print(f"[Elevator {self.id}] Assigned hall call: Floor {floor} [{direction.name}]")
        
        # If IDLE, decide direction
        if self.direction == Direction.IDLE:
            self.direction = Direction.UP if floor > self.current_floor else Direction.DOWN
    
    def has_requests(self) -> bool:
        """Check if elevator has any pending requests"""
        return bool(self.car_calls or self.assigned_hall_calls)
    
    def get_distance_to_floor(self, floor: int) -> int:
        """Calculate distance to a floor considering current direction"""
        if self.direction == Direction.IDLE:
            return abs(self.current_floor - floor)
        
        # If moving in the right direction towards the floor
        if self.direction == Direction.UP and floor >= self.current_floor:
            return floor - self.current_floor
        elif self.direction == Direction.DOWN and floor <= self.current_floor:
            return self.current_floor - floor
        
        # If need to reverse direction
        if self.direction == Direction.UP:
            # Go to top, then come down
            return (self.total_floors - 1 - self.current_floor) + (self.total_floors - 1 - floor)
        else:
            # Go to bottom, then come up
            return self.current_floor + floor
    
    def process_requests(self):
        """Process all assigned requests using SCAN algorithm"""
        while self.has_requests():
            if self.direction == Direction.UP:
                self._move_up()
            elif self.direction == Direction.DOWN:
                self._move_down()
            
            # Change direction if needed
            if self.direction == Direction.UP and not self._has_up_requests():
                self.direction = Direction.DOWN if self._has_down_requests() else Direction.IDLE

            elif self.direction == Direction.DOWN and not self._has_down_requests():
                self.direction = Direction.UP if self._has_up_requests() else Direction.IDLE
    
    def _has_up_requests(self) -> bool:
        """Check for requests above current floor"""
        has_car_calls = any(f > self.current_floor for f in self.car_calls)
        has_hall_calls = any(f > self.current_floor for f, _ in self.assigned_hall_calls)
        return has_car_calls or has_hall_calls
    
    def _has_down_requests(self) -> bool:
        """Check for requests below current floor"""
        has_car_calls = any(f < self.current_floor for f in self.car_calls)
        has_hall_calls = any(f < self.current_floor for f, _ in self.assigned_hall_calls)
        return has_car_calls or has_hall_calls
    
    def _move_up(self):
        print(f"[Elevator {self.id}] --- Moving UP from floor {self.current_floor} ---")
        
        # Find all stops going UP
        up_hall_calls = {f for f, d in self.assigned_hall_calls if f > self.current_floor and d == Direction.UP}
        car_calls_up = {f for f in self.car_calls if f > self.current_floor}
        all_stops = sorted(up_hall_calls | car_calls_up)
        
        if not all_stops:
            return
        
        for floor in range(self.current_floor + 1, max(all_stops) + 1):
            self.current_floor = floor
            time.sleep(0.5)
            
            should_stop = False
            reasons = []
            
            # Check for UP hall calls
            hall_call_to_remove = None
            for hc in self.assigned_hall_calls:
                if hc[0] == self.current_floor and hc[1] == Direction.UP:
                    should_stop = True
                    reasons.append("UP hall call")
                    hall_call_to_remove = hc
                    break
            
            if hall_call_to_remove:
                self.assigned_hall_calls.remove(hall_call_to_remove)
            
            # Check for car calls
            if self.current_floor in self.car_calls:
                should_stop = True
                reasons.append("car call")
                self.car_calls.remove(self.current_floor)
            
            if should_stop:
                self._stop_at_floor(reasons)
    
    def _move_down(self):
        print(f"[Elevator {self.id}] --- Moving DOWN from floor {self.current_floor} ---")
        
        # Find all stops going DOWN
        down_hall_calls = {f for f, d in self.assigned_hall_calls if f < self.current_floor and d == Direction.DOWN}
        car_calls_down = {f for f in self.car_calls if f < self.current_floor}
        all_stops = sorted(down_hall_calls | car_calls_down, reverse=True)
        
        if not all_stops:
            return
        
        for floor in range(self.current_floor - 1, min(all_stops) - 1, -1):
            self.current_floor = floor
            time.sleep(0.5)
            
            should_stop = False
            reasons = []
            
            # Check for DOWN hall calls
            hall_call_to_remove = None
            for hc in self.assigned_hall_calls:
                if hc[0] == self.current_floor and hc[1] == Direction.DOWN:
                    should_stop = True
                    reasons.append("DOWN hall call")
                    hall_call_to_remove = hc
                    break
            
            if hall_call_to_remove:
                self.assigned_hall_calls.remove(hall_call_to_remove)
            
            # Check for car calls
            if self.current_floor in self.car_calls:
                should_stop = True
                reasons.append("car call")
                self.car_calls.remove(self.current_floor)
            
            if should_stop:
                self._stop_at_floor(reasons)
    
    def _stop_at_floor(self, reasons: List[str]):
        reason_str = " & ".join(reasons)
        print(f"[Elevator {self.id}] [STOP] Floor {self.current_floor} - {reason_str}")
        time.sleep(1)
        print(f"[Elevator {self.id}] Doors closed")

class ElevatorDispatcher:
    """Central dispatcher that assigns hall calls to the best elevator"""
    def __init__(self, num_elevators: int, total_floors: int):
        self.elevators = [Elevator(i, total_floors) for i in range(num_elevators)]
        self.total_floors = total_floors
        self.pending_hall_calls = []
    
    def add_hall_call(self, floor: int, direction: Direction):
        """Someone pressed UP or DOWN button on a floor"""
        if floor < 0 or floor >= self.total_floors:
            print(f"[Dispatcher] Error: Floor {floor} is out of bounds.")
            return
        
        hall_call = HallCall(floor, direction)
        print(f"[Dispatcher] Hall call received: Floor {floor} [{direction.name}]")
        
        # Find best elevator for this call
        best_elevator = self._find_best_elevator(hall_call)
        
        if best_elevator:
            best_elevator.assign_hall_call(floor, direction)
            hall_call.assigned_elevator_id = best_elevator.id
        else:
            # No suitable elevator, add to pending
            self.pending_hall_calls.append(hall_call)
            print(f"[Dispatcher] No available elevator, call queued")
    
    def add_car_call(self, elevator_id: int, floor: int):
        """Someone inside elevator pressed a floor button"""
        if 0 <= elevator_id < len(self.elevators):
            self.elevators[elevator_id].add_car_call(floor)
        else:
            print(f"[Dispatcher] Error: Invalid elevator ID {elevator_id}")
    
    def _find_best_elevator(self, hall_call: HallCall) -> Optional[Elevator]:
        """
        Find the best elevator to serve this hall call.
        Strategy: Nearest elevator moving in the same direction, or nearest idle elevator
        """
        best_elevator = None
        min_distance = float('inf')
        
        for elevator in self.elevators:
            # Prefer elevators moving in the same direction towards the call
            if elevator.direction == hall_call.direction:
                if hall_call.direction == Direction.UP and elevator.current_floor <= hall_call.floor:
                    distance = elevator.get_distance_to_floor(hall_call.floor)
                    if distance < min_distance:
                        min_distance = distance
                        best_elevator = elevator
                elif hall_call.direction == Direction.DOWN and elevator.current_floor >= hall_call.floor:
                    distance = elevator.get_distance_to_floor(hall_call.floor)
                    if distance < min_distance:
                        min_distance = distance
                        best_elevator = elevator
            
            # Consider idle elevators
            elif elevator.direction == Direction.IDLE:
                distance = elevator.get_distance_to_floor(hall_call.floor)
                if distance < min_distance:
                    min_distance = distance
                    best_elevator = elevator
        
        # If no good match, assign to nearest elevator
        if best_elevator is None:
            for elevator in self.elevators:
                distance = elevator.get_distance_to_floor(hall_call.floor)
                if distance < min_distance:
                    min_distance = distance
                    best_elevator = elevator
        
        return best_elevator
    
    def process_all_requests(self):
        """Process all requests across all elevators"""
        print("\n[Dispatcher] Starting to process all requests...\n")
        
        # Simple simulation: process each elevator's requests
        for elevator in self.elevators:
            if elevator.has_requests():
                elevator.process_requests()
                print(f"[Elevator {elevator.id}] Now IDLE at floor {elevator.current_floor}\n")
        
        print("[Dispatcher] All requests processed.")

# --- Demo Execution ---
if __name__ == "__main__":
    print("="*70)
    print("=== Multi-Elevator System with Central Dispatcher ===")
    print("="*70 + "\n")
    
    # Create system with 3 elevators, 10 floors
    dispatcher = ElevatorDispatcher(num_elevators=3, total_floors=10)
    
    print("Initial state: All elevators at floor 0\n")
    
    # Scenario: Multiple people calling elevators
    print("--- Adding hall calls ---")
    dispatcher.add_hall_call(5, Direction.UP)    # Floor 5, going UP
    dispatcher.add_hall_call(3, Direction.DOWN)  # Floor 3, going DOWN
    dispatcher.add_hall_call(7, Direction.UP)    # Floor 7, going UP
    dispatcher.add_hall_call(2, Direction.UP)    # Floor 2, going UP
    
    print("\n--- Adding car calls (inside elevator buttons) ---")
    dispatcher.add_car_call(0, 8)  # Elevator 0: someone inside presses 8
    dispatcher.add_car_call(1, 6)  # Elevator 1: someone inside presses 6
    
    # Process all requests
    dispatcher.process_all_requests()
    
    print("\n" + "="*70)
    print("=== Scenario 2: Demonstrating intelligent assignment ===")
    print("="*70 + "\n")
    
    dispatcher2 = ElevatorDispatcher(num_elevators=2, total_floors=10)
    
    # Manually position elevators
    dispatcher2.elevators[0].current_floor = 5
    dispatcher2.elevators[0].direction = Direction.UP
    dispatcher2.elevators[1].current_floor = 8
    dispatcher2.elevators[1].direction = Direction.DOWN
    
    print(f"Elevator 0: at floor 5, moving UP")
    print(f"Elevator 1: at floor 8, moving DOWN\n")
    
    print("--- Hall call: Floor 7, UP ---")
    dispatcher2.add_hall_call(7, Direction.UP)
    print("Expected: Assigned to Elevator 0 (moving UP, closer)\n")
    
    print("--- Hall call: Floor 6, DOWN ---")
    dispatcher2.add_hall_call(6, Direction.DOWN)
    print("Expected: Assigned to Elevator 1 (moving DOWN, closer)\n")
    
    dispatcher2.process_all_requests()
    


