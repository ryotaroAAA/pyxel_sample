import pyxel
from enum import auto, Enum

class Game:
    tile_dic = {
        # background
        "wall" : (0, 6, None),
        "water" : (2, 6, None),
        "ailse" : (0, 5, None),
        "grass" : (2, 5, None),
        "wood" : (3, 5, None),
        # sprite
        # charactor
        "hero" : (0, 0, pyxel.colors[0]),
        "reimu" : (0, 1, pyxel.colors[1]),
        "marisa" : (0, 2, pyxel.colors[1]),
        # item
        "wepon1" : (0, 1, pyxel.colors[0]),
        "wepon2" : (1, 1, pyxel.colors[0]),
        "wepon3" : (2, 1, pyxel.colors[0]),
        "wepon4" : (3, 1, pyxel.colors[0]),
        "wepon5" : (4, 1, pyxel.colors[0]),
        "armor1" : (0, 2, pyxel.colors[0]),
        "armor2" : (1, 2, pyxel.colors[0]),
        "armor3" : (2, 2, pyxel.colors[0]),
        "item1" : (0, 3, pyxel.colors[0]),
        "item2" : (1, 3, pyxel.colors[0]),
        "item3" : (2, 3, pyxel.colors[0]),
        "item4" : (3, 3, pyxel.colors[0]),
        "treasure" : (4, 3, pyxel.colors[0]),
        # enemy
        "enemy1" : (0, 4, pyxel.colors[0]),   
        "enemy2" : (1, 4, pyxel.colors[0]),    
        "enemy3" : (2, 4, pyxel.colors[0]),   
        "enemy4" : (3, 4, pyxel.colors[0]),    
        "boss" : (4, 4, pyxel.colors[0])    
    }
    def __init__(self):
        self.tile_x = 8
        self.tile_y = 8
        self.bit_x = 8
        self.bit_y = 8
        self.size_x = self.tile_x*self.bit_x
        self.size_y = self.tile_y*self.bit_y
        pyxel.init(self.size_x, self.size_y, fps=30)

        # colors = pyxel.colors.to_list()
        # print(colors)
        pyxel.load("test.pyxres")

        # start position
        self.x = 2
        self.y = 2
        pyxel.run(self.update, self.draw)

    # 初期化
    # マップ、当たり判定、位置、
    # def map_init(self):

    # def is_passable(self):

    def draw_tile(self, x, y, tile):
        """
        x, y: 描画位置
        tile: image bank上の位置、透明色
        """
        tile_x = tile[0]
        tile_y = tile[1]
        colkey = tile[2]
        # print(tile, tile_x, tile_y, pyxel.tilemap(0).pget(tile_x, tile_y))
        if not colkey == None:
            pyxel.blt(x*self.bit_x,
                y*self.bit_y,
                0,
                tile_x*self.bit_x,
                tile_y*self.bit_y,
                self.bit_x,
                self.bit_y,
                colkey)
        else:
            pyxel.blt(x*self.bit_x,
                y*self.bit_y,
                0,
                tile_x*self.bit_x,
                tile_y*self.bit_y,
                self.bit_x,
                self.bit_y)

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
        # 画面黒初期化
        pyxel.cls(0)

        # draw background
        for i in range(0, self.tile_x):
            for j in range(0, self.tile_y):
                tile_x, tile_y = pyxel.tilemap(0).pget(
                    i + self.tile_x * (self.x//self.tile_x),
                    j + self.tile_y * (self.y//self.tile_y))
                for k, tile in self.tile_dic.items():
                    # if i == 7:
                    if k == "wall":
                        print(i, j, tile_x, tile_y, k, tile)
                    if tile[0] == tile_x and tile[1] == tile_y:
                        self.draw_tile(i, j, tile)
        
        # draw sprites
        self.draw_tile(self.x % self.tile_x,
                       self.y % self.tile_y,
                       self.tile_dic["hero"])

Game()
