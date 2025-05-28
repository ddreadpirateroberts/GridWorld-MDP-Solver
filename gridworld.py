import pygame as pg
from enum import Enum, auto
from settings import *
import math
from random import randint


class DisplayMode(Enum): 
    UTILxDIR = auto()
    QVAL = auto()


class State(Enum):
    DIAMOND = auto()
    PIT = auto()
    WALKABLE = auto()
    WALL = auto()


class Triangle:
    def __init__(self, color, points) -> None:
        self.color = color
        self.points = points
        self.value = 0.00

    def get_center(self):
        p1, p2, p3 = self.points
        return ((p1[0]+p2[0]+p3[0])/3, (p1[1]+p2[1]+p3[1])/3)

    def update_value(self, value):
        self.value = value
        self._update_color()

    def _update_color(self):
        if 0 <= self.value:
            if self.value <= 1:
                self.color = pg.Color(*[math.ceil(x * self.value) for x in GREEN])
            else: self.color = GREEN
            
        elif self.value < 0:
            if self.value >= -1:
                self.color = pg.Color(*[math.ceil(x * (-self.value)) for x in RED])
            else: 
                self.color = RED

        self.color.a = 255


class Tile:
    def __init__(self, row, col, state=State.WALKABLE) -> None:
        self.row = row
        self.col = col
        self.state = state
        self.x = (col+.2) * TILESIZE
        self.y = (row+.2) * TILESIZE
        self.rect = pg.Rect(self.x, self.y, TILESIZE, TILESIZE)
        self.color = BLACK
        self._define_triangles()
        self.util = 0.00
        self.dir = 1 # U
        self.aval = {0: 0, 1: 0, 2: 0, 3: 0}

    def _define_triangles(self):
        center = (self.x + TILESIZE/2, self.y + TILESIZE/2)
        upper_tri = (self.x, self.y), (self.x+TILESIZE, self.y), center
        lower_tri = (self.x, self.y+TILESIZE), (self.x+TILESIZE, self.y+TILESIZE), center
        left_tri = (self.x, self.y), (self.x, self.y+TILESIZE), center
        right_tri = (self.x+TILESIZE, self.y), (self.x+TILESIZE, self.y+TILESIZE), center
        self.triangles = (Triangle(self.color, left_tri), Triangle(self.color, upper_tri), 
                          Triangle(self.color, right_tri), Triangle(self.color, lower_tri))

    def update_color(self, color):
        self.color = color
        for tri in self.triangles:
            tri.color = color

    def draw(self, screen, mode: DisplayMode):
        if mode == DisplayMode.QVAL: 
            for tri in self.triangles: 
                pg.draw.polygon(screen, tri.color, tri.points)
                
            if self.is_walkable():
                pg.draw.line(screen, WHITE, (self.x, self.y),
                            (self.x+TILESIZE, self.y+TILESIZE), 2)
                pg.draw.line(screen, WHITE, (self.x+TILESIZE, self.y),
                            (self.x, self.y+TILESIZE), 2)
                
        if mode == DisplayMode.UTILxDIR: 
            pg.draw.rect(screen, self.color, self.rect)
            
            # advised direction
            if self.is_walkable():
                rect = pg.Rect(0, 0, TILESIZE//10, TILESIZE//10)
                
                const = 2 * TILESIZE//20
                match self.dir: 
                    case 0: 
                        rect.center = self.rect.left + const, self.rect.center[1]
                    case 1:
                        rect.center = self.rect.center[0], self.rect.top + const
                    case 2:
                        rect.center = self.rect.right - const, self.rect.center[1]
                    case 3:
                        rect.center = self.rect.center[0], self.rect.bottom - const
                    case _: 
                        raise Exception("Unsupported Direction")
                        
                pg.draw.rect(screen, WHITE, rect)
        
        pg.draw.rect(screen, WHITE, self.rect, 2)

        if self.is_diamond() or self.is_pit():
            pg.draw.rect(screen, WHITE, (self.x+TILESIZE//15,
                        self.y+TILESIZE//15, TILESIZE-TILESIZE//8, TILESIZE-TILESIZE//8), 2)
            text = '%.2f' % self.util
            coor = (self.x+TILESIZE/2-TILESIZE//6,
                    self.y+TILESIZE/2-TILESIZE//12)
            draw_text(screen, text, TILESIZE//4, WHITE, *coor)
            
    def set_as_pit(self): 
        self.state = State.PIT 
        self.util = -1 
        self.update_color(RED)
        
    def set_as_diamond(self): 
        self.state = State.DIAMOND
        self.util = 1 
        self.update_color(GREEN)
        
    def set_as_wall(self): 
        self.state = State.WALL 
        self.update_color(LIGHTGREY)

    def set_as_walkable(self): 
        self.state = State.WALKABLE
        self.update_color(BLACK)
        
    def is_walkable(self):
        return self.state == State.WALKABLE

    def is_pit(self):
        return self.state == State.PIT

    def is_diamond(self):
        return self.state == State.DIAMOND

    def is_wall(self):
        return self.state == State.WALL

    def reset(self):
        self.util = 0
        self.aval = {0: 0, 1: 0, 2: 0, 3: 0}
        for tri in self.triangles:
            tri.update_value(value=0)
        self.dir = 1

    def set_aval(self, action, exp_u):
        left_tri, upper_tri, right_tri, lower_tri = self.triangles
        self.aval[action] = exp_u
        if action == 0:
           left_tri.update_value(exp_u)
        elif action == 1:
            upper_tri.update_value(exp_u)
        elif action == 2:
            right_tri.update_value(exp_u)
        elif action == 3:
            lower_tri.update_value(exp_u)

    def get_state_coor(self): 
        return self.row, self.col 
    
    
class Gridworld:
    def __init__(self, number_of_rows, number_of_cols, random=False, goal_ratio=10, wall_ratio=20):
        width, height = (number_of_cols+.4) * TILESIZE, (number_of_rows+.4) * TILESIZE
        self._create_screen(width, height, TITLE)
        self.rows = number_of_rows
        self.cols = number_of_cols
        self._set_up_grid(random, goal_ratio, wall_ratio)
        self.noise = 0.2
        self.discount = .9
        self.living_reward = 0
    
    def _create_screen(self, width, height, title):
        pg.init()
        self.screen = pg.display.set_mode((width, height))
        pg.display.set_caption(title)
        
    def _set_up_grid(self, random, goal_ratio, wall_ratio):
        self.grid = {(i, j): Tile(i, j)
                    for i in range(self.rows) for j in range(self.cols)}
        
        if not random:
            self.grid[(0, self.cols-1)].set_as_diamond()
            self.grid[(1, self.cols-1)].set_as_pit()
            self.grid[(1, 1)].set_as_wall()
            
        else:          
            self.spawn_terminals(goal_ratio)
            self.spawn_walls(wall_ratio)    
        
    def get_random_tile(self): 
        row, col = randint(0, self.rows-1), randint(0, self.cols-1)
        while not self.grid[(row, col)].is_walkable(): 
            row, col = randint(0, self.rows-1), randint(0, self.cols-1)
        return self.grid[(row, col)]
              
    def spawn_terminals(self, percent): 
        amount = int((self.rows * self.cols) * (percent / 100)) // 2
        desired_pairs = amount if amount != 0 else 1
        for _ in range(desired_pairs): 
            diamond = self.get_random_tile()
            diamond.set_as_diamond()
            pit = self.get_random_tile()
            pit.set_as_pit()
                                                   
    def add_wall_safely(self, tile: Tile):
        tile.set_as_wall()
        if not self.is_fully_connected():
            tile.set_as_walkable()
            return False
        return True
            
    def spawn_walls(self, percent):
        desired_walls = int((self.rows * self.cols) * (percent / 100))
        placed_walls = 0
        
        while True: 
            for tile in self.grid.values():
                if placed_walls >= desired_walls:
                    return
                if randint(1, 100) < percent and tile.is_walkable():
                    if self.add_wall_safely(tile):
                        placed_walls += 1
                            
    def is_fully_connected(self): 
        def neighbors(tile):
            row, col = tile
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
            for dr, dc in directions:
                nr, nc = row + dr, col + dc
                if (nr, nc) in self.grid and not self.grid[(nr, nc)].is_wall():
                    yield (nr, nc)

        walkable_tiles = [tile for tile in self.grid.values() if not tile.is_wall()]
        terminal_tiles = [tile for tile in walkable_tiles if tile.is_diamond() or tile.is_pit()]
        
        if not terminal_tiles:
            return False, [] 

        visited = set()
        stack = [terminal_tiles[0].get_state_coor()]
        while stack:
            current = stack.pop()
            if current in visited:
                continue
            visited.add(current)
            for neighbor in neighbors(current):
                stack.append(neighbor)

        all_connected = len(visited) == len(walkable_tiles)
        return all_connected 
                 
    def wipe(self):
        for tile in self.grid.values():
            if not (tile.is_diamond() or tile.is_pit() or tile.is_wall()):
                tile.reset()
                
    def draw_Q_values(self, tile: Tile):
        text_font = pg.font.SysFont("Arials", TILESIZE//5)
        for tri in tile.triangles:
            text = '%.2f' % tri.value
            img = text_font.render(text, True, WHITE)
            rect = img.get_rect()
            rect.center = tri.get_center()
            self.screen.blit(img, rect.topleft)

    def draw_V_values(self, tile: Tile):
        text_font = pg.font.SysFont("Arials", TILESIZE//4)
        text = '%.2f' % tile.util
        img = text_font.render(text, True, WHITE)
        rect = img.get_rect()
        rect.center = tile.rect.center
        self.screen.blit(img, rect.topleft)
        
    def display(self, mode: DisplayMode):
        self.screen.fill(BLACK)
        
        for tile in self.grid.values():
            tile.draw(self.screen, mode)
            if tile.is_walkable():
                if mode == DisplayMode.QVAL:
                    self.draw_Q_values(tile)
                elif mode == DisplayMode.UTILxDIR:
                    self.draw_V_values(tile)
                    
        pg.display.flip()
        
    def commit(self, state: Tile, action_index: int):
        actions = [(0, -1), (-1, 0), (0, 1), (1, 0)]  # L, U, R, D
        dr, dc = actions[action_index]
        newr, newc = state.row + dr, state.col + dc
        if newr < 0 or newc < 0 or newr >= self.rows or newc >= self.cols \
                or self.grid[(newr, newc)].is_wall():
            return state
        else:
            return self.grid[(newr, newc)]

    
def draw_text(screen, text, size, text_color, x, y):
    text_font = pg.font.SysFont("Arials", size)
    img = text_font.render(text, True, text_color)
    screen.blit(img, (x, y))


if __name__ == "__main__": 
    grid = Gridworld(6, 6, True, wall_ratio=25)
    print(grid.is_fully_connected())
    grid.display(DisplayMode.UTILxDIR)
    
    running = True
    while running: 
        for event in pg.event.get(): 
            if event.type == pg.QUIT: 
                running = False
            
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_n: 
                    grid = Gridworld(6, 6, True, wall_ratio=25)
                    grid.display(DisplayMode.UTILxDIR)
