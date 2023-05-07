import pyxel
from enum import auto, Enum

class Game:
    HERO = (0, 0, pyxel.colors[0])
    REIMU = (0, 1, pyxel.colors[1])
    MARISA = (0, 2, pyxel.colors[1])
    WALL = (0, 6, None)
    AISLE = (0, 5, None)
    ENEMY = (0, 4, pyxel.colors[0])
    def __init__(self):
        self.tile_x = 24
        self.tile_y = 24
        self.bit_x = 8
        self.bit_y = 8
        self.size_x = self.tile_x*self.bit_x
        self.size_y = self.tile_y*self.bit_y
        pyxel.init(self.size_x, self.size_y, fps=30)

        colors = pyxel.colors.to_list()
        print(colors)
        # print(pyxel.colors)
        pyxel.load("test.pyxres")
        # pyxel.image(0).load(0, 0, "test.pyxres")
        # pyxel.blt(0, 0, 0, 0, 0, 8, 8)

        # start position
        self.x = 2
        self.y = 2
        pyxel.run(self.update, self.draw)

    # 初期化
    # マップ、当たり判定、位置、
    # def map_init(self):

    def draw_tile(self, tile_x, tile_y, tile):
        if tile[2] == None:
            pyxel.blt(tile_x*self.bit_x,
                    tile_y*self.bit_y,
                    0,
                    tile[0]*self.bit_x,
                    tile[1]*self.bit_y,
                    self.bit_x,
                    self.bit_y)
        else:
            pyxel.blt(tile_x*self.bit_x,
                    tile_y*self.bit_y,
                    0,
                    tile[0]*self.bit_x,
                    tile[1]*self.bit_y,
                    self.bit_x,
                    self.bit_y,
                    tile[2])

    # 毎フレームオンメモリ情報を書き換える
    def update(self):
        # self.x = (self.x + 1) % pyxel.width
        if pyxel.frame_count % 5 == 0:
            if pyxel.btn(pyxel.KEY_UP):
                self.y = self.y - 1
            if pyxel.btn(pyxel.KEY_DOWN):
                self.y = self.y + 1
            if pyxel.btn(pyxel.KEY_LEFT):
                self.x = self.x - 1
            if pyxel.btn(pyxel.KEY_RIGHT):
                self.x = self.x + 1
    
    # 毎フレーム実際描画する
    def draw(self):
        pyxel.cls(0)
        for i in range(0, self.tile_x):
            for j in range(0, self.tile_y):
                # def is_corner(i, j):
                #     return i in [0, self.size_x//8-1] or j in [0, self.size_y//8-1]
                # if is_corner(i, j):
                #     # pyxel.blt(i*8, j*8, 0, 0, 8*6, 8, 8)
                #     self.draw_tile(i, j, self.WALL)
                # else:
                #     # pyxel.blt(i*8, j*8, 0, 0, 8*5, 8, 8)
                #     self.draw_tile(i, j, self.AISLE)
                x, y = pyxel.tilemap(0).pget(
                    i + self.tile_x * (self.x//self.tile_x),
                    j + self.tile_y * (self.y//self.tile_y))
                self.draw_tile(i, j, (x, y, None))
                
        # pyxel.blt(self.x, self.y, 0, 0, 0, 8, 8, pyxel.colors[0])
        self.draw_tile(self.x % self.tile_x, self.y % self.tile_y, self.HERO)
        # pyxel.rect(self.x, 0, 8, 8, 9)

Game()
