import copy
from telnetlib import NOP
# from tkinter import LEFT
import cython
from dataclasses import *
import logging
import logging.config
import numpy as np
from pathlib import Path
import sys
import time
import traceback
from typing import *

from hexdump import hexdump
from pprint import *
from print_color import print
from tabulate import tabulate
import yaml
from enum import auto, Enum
import random

import argparse
import pygame

class ObjAttr(Enum):
    WALL = auto() 
    AISLE = auto()
    GOAL = auto()

class DIRE(Enum):
    L = auto() 
    R = auto() 
    U = auto()
    D = auto()

BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255,255,255)
BROWN = (115, 66, 41)
ORANGE = (233,168, 38)

ME_COLOR = RED
AISLE_COLOR = WHITE
WALL_COLOR = BLACK
GOAL_COLOR = ORANGE

scale = 5
TILE_SIZE = (30, 30)
screen_size = (TILE_SIZE[0]*scale, TILE_SIZE[0]*scale)
TILE = (screen_size[0]//TILE_SIZE[0], screen_size[1]//TILE_SIZE[1])
maze = []

def init_scale(scale_):
    global scale, screen_size, TILE_SIZE, TILE
    scale = scale_
    screen_size = (TILE_SIZE[0]*scale, TILE_SIZE[0]*scale)
    TILE = (screen_size[0]//TILE_SIZE[0], screen_size[1]//TILE_SIZE[1])

x = TILE_SIZE[0]
y = TILE_SIZE[1]

class Pos:
    def __init__(self, pos, maze):
        self.x = pos[0]
        self.y = pos[1]
        self.movable_init()
        self.maze = maze
        self.stack = []
        self.stack.append(pos)

    def movable_init(self):
        self.movable = [
            DIRE.L, DIRE.R, DIRE.U, DIRE.D
        ]

    def is_collision(self, x, y):
        if 0 <= x < TILE[0] and 0 <= y < TILE[1]:
            if maze[y][x] in [ObjAttr.WALL]:
                return True
            else:
                return False
        return True

    def detect_obj(self, x, y):
        if 0 <= x < TILE[0] and 0 <= y < TILE[1]:
            return maze[y][x]
        else:
            return False

    def get_move_pos(self, dire, move=1):
        if dire == DIRE.L:
            x, y = self.get_left(move)
        elif dire == DIRE.R:
            x, y = self.get_right(move)
        elif dire == DIRE.U:
            x, y = self.get_up(move)
        elif dire == DIRE.D:
            x, y = self.get_down(move)
        else:
            raise Exception
        return x, y

    def move(self, dire, move=2):
        for _ in range(move):
            self.x, self.y = self.get_move_pos(dire)
            self.stack.append((self.x, self.y))

    def chack_2step_forward(self, dire):
        x, y = self.get_move_pos(dire, 2)
        if (x in range(TILE[0]) and y in range(TILE[0]) and
                not (x, y) in self.stack):
            return self.maze[y][x]
        else:
            return False

    def get_left(self, move=1):
        return self.x - move, self.y

    def get_right(self, move=1):
        return self.x + move, self.y

    def get_up(self, move=1):
        return self.x, self.y - move

    def get_down(self, move=1):
        return self.x, self.y + move

    def enable_wall(self):
        for w in self.stack:
            self.maze[w[1]][w[0]] = ObjAttr.WALL
    
    def disable_wall(self):
        for w in self.stack:
            self.maze[w[1]][w[0]] = ObjAttr.AISLE

    def get_random_direct(self):
        index =  random.randint(0, len(self.movable)-1)
        dire = self.movable[index]
        return index, dire

    def wall_extend(self):
        while len(self.movable)>0:
            # random choise one direction
            index, one_dire = self.get_random_direct()
            
            if attr := self.chack_2step_forward(one_dire):
                if attr == ObjAttr.AISLE:
                    self.movable_init()
                    self.move(one_dire)
                elif attr == ObjAttr.WALL:
                    self.move(one_dire)
                    self.enable_wall()
                    return True
                else:
                    raise Exception

            self.movable.pop(index)
            if len(self.movable) == 0:
                print("no movable, retry")
                self.movable_init()
                break
        
        return False

    def bar_down(self):
        a, b = self.x, self.y
        self.movable_init()
        if not self.y == 2:
            self.movable.remove(DIRE.U)
        while len(self.movable) > 0:
            dire = random.choice(self.movable)
            x, y = self.get_move_pos(dire)
            if maze[y][x] != ObjAttr.WALL:
                maze[y][x] = ObjAttr.WALL
                # print(f"({a}, {b}) : {dire}")
                break
            else:
                self.movable.remove(dire)

def is_eq_objattr(maze, pos, attr):
    return maze[pos[1]][pos[0]] == attr

def wall_extend():
    global maze
    maze = []
    for j in range(TILE[1]):
        row = []
        for i in range(TILE[0]):
            # outer wall
            if (i == 0 or j == 0 or
                    i == TILE[0]-1 or j == TILE[1]-1):
                row.append(ObjAttr.WALL)
            else:
                row.append(ObjAttr.AISLE)
                
        # print([1 if s == ObjAttr.WALL else 0 for s in row])
        maze.append(row)

    print("[wall_extend]")
    
    for j in range(TILE[1]):
        print([1 if s == ObjAttr.WALL else 0 for s in maze[j]])
    
    is_wall_cand = (lambda i, j: 
                    i in range(1, TILE[0]-1) and
                    j in range(1, TILE[1]-1) and
                    i%2 == 0 and j%2 == 0)
    cand = [(i, j) for i in range(TILE[0])
        for j in range(TILE[1]) if is_wall_cand(i, j)]
    while len(cand) > 0:
        # decide start position
        index_cand = random.randint(0, len(cand) - 1)
        rand_cand = cand[index_cand]
        if is_eq_objattr(maze, rand_cand, ObjAttr.WALL):
            cand.pop(index_cand)
            continue
        # decide where to extend wall
        pos = Pos(rand_cand, maze)
        pos.wall_extend()

    for j in range(TILE[1]):
        print([1 if s in [ObjAttr.WALL]  else 0 for s in maze[j]])

def bar_down():
    global maze
    maze = []
    for j in range(TILE[1]):
        row = []
        for i in range(TILE[0]):
            # outer wall
            if (i == 0 or j == 0 or
                    i == TILE[0]-1 or j == TILE[1]-1):
                row.append(ObjAttr.WALL)
            elif (i%2 == 0 and j%2 == 0):
                row.append(ObjAttr.WALL)
            else:
                row.append(ObjAttr.AISLE)
                
        # print([1 if s == ObjAttr.WALL else 0 for s in row])
        maze.append(row)

    print("[bar_down]")
    for j in range(TILE[1]):
        for i in range(TILE[0]):
            if (i == 0 or j == 0 or
                    i == TILE[0]-1 or j == TILE[1]-1):
                # nothing to do
                pass
            elif (i%2 == 0 and j%2 == 0):
                pos = Pos((i, j), maze)
                pos.bar_down()
            else:
                continue
    
    for j in range(TILE[1]):
        print([1 if s == ObjAttr.WALL else 0 for s in maze[j]])

def aisle_extend():
    return

def make_maze():
    global x, y, maze
    
    # bar_down()
    wall_extend()

    while True:
        i = random.randint(0, TILE[0]-1)
        j = random.randint(0, TILE[1]-1)
        if (maze[j][i] == ObjAttr.AISLE and
                not i == x//TILE_SIZE[0] and not j == y//TILE_SIZE[1]):
            maze[j][i] = ObjAttr.GOAL
            # print(f"goal:({i}, {j}), cur:({x//TILE_SIZE[0]}, {y//TILE_SIZE[1]})")
            break

def is_not_collision(x, y):
    global maze
    t_x = x // TILE_SIZE[0]
    t_y = y // TILE_SIZE[1]
    if 0 <= t_x < TILE[0] and 0 <= t_y < TILE[1]:
        if maze[t_y][t_x] == ObjAttr.AISLE:
            return True
        elif maze[t_y][t_x] == ObjAttr.GOAL:
            make_maze()
            return True
    return False

def run():
    global maze, x, y, scale
    # assert((x % 10 == 0) and (y % 10 == 0), "screen size error")

    print(scale)
    print(screen_size)
    pygame.init()
    clock = pygame.time.Clock()
    pygame.key.set_repeat(100, 50)
    make_maze()
    
    count = 0

    screen = pygame.display.set_mode(screen_size)
    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                break

        press = pygame.key.get_pressed()
        if (press[pygame.K_ESCAPE]):
            break

        if (press[pygame.K_u]):
            print(scale)
            if (t := scale+2) in range(5, 100):
                init_scale(t)
                screen = pygame.display.set_mode(screen_size)
                make_maze()
    
        if (press[pygame.K_d]):
            print(scale)
            if (t := scale-2) in range(5, 100):
                init_scale(t)
                screen = pygame.display.set_mode(screen_size)
                make_maze()

        if (press[pygame.K_m]):
            make_maze()

        if (press[pygame.K_LEFT] and is_not_collision(x - TILE_SIZE[0], y)):
            x -= TILE_SIZE[0]

        if (press[pygame.K_RIGHT] and is_not_collision(x + TILE_SIZE[1], y)):
            x += TILE_SIZE[0]
        
        if (press[pygame.K_UP] and is_not_collision(x, y - TILE_SIZE[1])):
            y -= TILE_SIZE[1]

        if (press[pygame.K_DOWN] and is_not_collision(x, y + TILE_SIZE[1])):
            y += TILE_SIZE[1]

        # print(f"[FPS] {}")
        # wall
        for j in range(TILE[1]):
            for i in range(TILE[0]):
                if maze[j][i] == ObjAttr.WALL:
                    wall = pygame.Rect(i * TILE_SIZE[0], j * TILE_SIZE[1],
                        TILE_SIZE[0], TILE_SIZE[1])
                    pygame.draw.rect(screen, WALL_COLOR, wall)
                elif maze[j][i] == ObjAttr.AISLE:
                    aisle = pygame.Rect(i * TILE_SIZE[0], j * TILE_SIZE[1],
                        TILE_SIZE[0], TILE_SIZE[1])
                    pygame.draw.rect(screen, AISLE_COLOR, aisle)
                elif maze[j][i] == ObjAttr.GOAL:
                    goal = pygame.Rect(i * TILE_SIZE[0], j * TILE_SIZE[1],
                        TILE_SIZE[0], TILE_SIZE[1])
                    pygame.draw.rect(screen, GOAL_COLOR, goal)

        me = pygame.Rect(x, y, TILE_SIZE[0], TILE_SIZE[1])
        pygame.draw.rect(screen, ME_COLOR, me)
        pygame.display.flip()
        clock.tick(16)
        # if (count % 100 == 0):
        #     print(f"[FPS] {clock.get_fps():.2f}")
        # if (count % 100 == 0):
        #     make_maze()
        count += 1

    pygame.quit()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--loop", type=int, default=-1, help="loop")
    parser.add_argument("-r", "--rom", default="", help="rom")
    args = parser.parse_args()
    print(vars(args), tag="args", tag_color="green", color="white")

    run()