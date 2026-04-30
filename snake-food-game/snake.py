from collections import deque

class Snake:
    def __init__(self, init_pos):
        self.body = deque([init_pos])   # head at end
        self.body_set = set([init_pos]) # for O(1) collision check

    def get_head(self):
        return self.body[-1]

    def move(self, new_head, grow=False):
        # add new head
        self.body.append(new_head)
        self.body_set.add(new_head)

        if not grow:
            tail = self.body.popleft()
            self.body_set.remove(tail)

    def will_collide(self, new_head, grow):
        tail = self.body[0]
        if grow:
            return new_head in self.body_set
        else:
            return new_head in self.body_set and new_head != tail


