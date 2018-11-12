import random
import math
import pygame
import time

DISPLAY_SIZE = 600

MAX_ROOM_SIZE = 15
MIN_ROOM_SIZE = 5

DISPLAY_SCALE = 3
RADIUS_BUFFER = 5


class Dungeon:

    def __init__(self):
        self.rooms = []

    def scatter(self):
        self.display()
        # print("Scattering rooms")
        for room in self.rooms:
            push_x = random.choice([random.randint(-12, -8), random.randint(8, 12)])
            push_y = random.choice([random.randint(-12, -8), random.randint(8, 12)])
            room.center[0] += push_x
            room.center[1] += push_y
            # print(f"Pushed room with id {room.id} by (x: {push_x}, y:{push_y})")

    @staticmethod
    def distance(a, b):
        x_dist = abs(a[0]-b[0])
        y_dist = abs(a[1]-b[1])
        dist = math.floor(math.sqrt(x_dist**2 + y_dist**2))
        # print(f"Calculated distance between A({a[0]},{[1]}) and B({b[0]},b[1]): {dist}")
        return dist

    def spread(self):
        self.scatter()
        self.display()
        # print("Performing room spread...")
        spread = False
        count = 1
        while spread is not True:
            spread = True
            # print(f"Performing spread iteration {count}")
            count += 1
            for room in self.rooms:
                # print(f"Processing room with id {room.id} with postition ({room.center[0]},{room.center[1]})")
                for far_room in self.rooms:
                    if room.id == far_room.id:
                        continue
                    # print(f"Comparing to room with id {far_room.id}")
                    distance = Dungeon.distance(room.center, far_room.center)
                    if distance < room.radius + far_room.radius:
                        # print(f"Rooms {room.id} and {far_room.id} are too close, adjusting")
                        spread = False
                        if room.center[0] < far_room.center[0]:
                            room.center[0] -= 1
                            far_room.center[0] += 1
                        else:
                            room.center[0] += 1
                            far_room.center[0] -= 1
                        if room.center[1] < far_room.center[1]:
                            room.center[1] -= 1
                            far_room.center[1] += 1
                        else:
                            room.center[1] += 1
                            far_room.center[1] -= 1
                    else:
                        # print(f"Rooms {room.id} and {far_room.id} are a sufficient distance apart")
                        pass
                self.display()

    def display(self):
        # time.sleep(0.1)
        screen.fill(bg)
        x_range = [0, 0]
        y_range = [0, 0]
        for room in self.rooms:

            if room.center[0] > 0:
                x_extend = room.center[0] + room.extend_x
            else:
                x_extend = room.center[0] - room.extend_x
            if room.center[1] > 0:
                y_extend = room.center[1] + room.extend_y
            else:
                y_extend = room.center[1] - room.extend_y

            if x_extend < x_range[0]:
                x_range[0] = x_extend
            elif x_extend > x_range[1]:
                x_range[1] = x_extend

            if y_extend < y_range[0]:
                y_range[0] = y_extend
            elif y_extend > y_range[1]:
                y_range[1] = y_extend

        for room in self.rooms:
            top_left_x = room.center[0] - room.extend_x
            top_left_y = room.center[1] + room.extend_y
            bottom_right_x = room.center[0] + room.extend_x
            bottom_right_y = room.center[1] - room.extend_y
            pygame.draw.rect(screen, (0, 0, 0), ((DISPLAY_SIZE/2) + top_left_x, (DISPLAY_SIZE/2) + top_left_y, (room.extend_x * 2) + 1, (room.extend_y * 2) + 1))
        pygame.display.flip()


    @staticmethod
    def center_to_zz(zz, center):
        loc = [None, None]
        if center[0] > zz[0]:
            loc[0] = zz[0] + center[0]
        else:
            loc[0] = zz[0] - center[0]
        if center[1] > zz[1]:
            loc[1] = zz[1] + center[1]
        else:
            loc[1] = zz[1] - center[1]
        return loc


class Room:

    def __init__(self, room_id):
        self.id = room_id
        self.center = [0, 0]
        self.extend_x = random.randint(MIN_ROOM_SIZE, MAX_ROOM_SIZE)
        self.extend_y = random.randint(MIN_ROOM_SIZE, MAX_ROOM_SIZE)
        self.radius = math.ceil(math.sqrt(self.extend_x**2 + self.extend_y**2) + RADIUS_BUFFER)


def start():
    print("Generating Dungeon")
    dungeon = Dungeon()
    for id in range(50):
        dungeon.rooms.append(Room(id))
    dungeon.spread()
    input()


if __name__ == "__main__":
    bg = (255, 255, 255)
    running = True
    width, height = DISPLAY_SIZE, DISPLAY_SIZE
    screen = pygame.display.set_mode((width, height))
    screen.fill(bg)
    pygame.display.flip()
    time.sleep(1)
    start()
    pygame.quit()
