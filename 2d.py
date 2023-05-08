import pyxel
import pprint
from enum import auto, Enum

class Obj:
    def __init__(self, name, tile_x, tile_y, colkey=None, col=False):
        self.name = name
        self.tile_x = tile_x
        self.tile_y = tile_y
        self.colkey = colkey
        self.col = col

class Character(Obj):
    def __init__(self, obj, name, health, attack, defense, agility):
        super().__init__(name)
        self.health = health
        self.attack = attack
        self.defense = defense
        self.agility = agility

class Enemy(Character):
    def __init__(self, name, health, attack, defense, gold, experience):
        super().__init__(name, health, attack, defense)
        self.gold = gold
        self.experience = experience

class Player(Character):
    def __init__(self, name, health, attack, defense, level, experience, gold):
        super().__init__(name, health, attack, defense)
        self.level = level
        self.experience = experience
        self.gold = gold

class Item(Obj):
    def __init__(self, name, description):
        self.name = name
        self.description = description

class Weapon(Item):
    def __init__(self, name, description, attack_bonus):
        super().__init__(name, description)
        self.attack_bonus = attack_bonus

class Armor(Item):
    def __init__(self, name, description, defense_bonus):
        super().__init__(name, description)
        self.defense_bonus = defense_bonus

class Game:
    tile_dic = {
        # background
        "wall" : (0, 6, None, 1),
        "water" : (2, 6, None, 1),
        "aisle" : (0, 5, None, 0),
        "grass" : (2, 5, None, 0),
        "wood" : (3, 5, None, 1),
        # sprite
        # charactor
        "hero" : (1, 0, 0, 1),
        "reimu" : (2, 0, 1, 1),
        "marisa" : (3, 0, 1, 1),
        # item
        "wepon1" : (0, 1, 0, 1),
        "wepon2" : (1, 1, 0, 1),
        "wepon3" : (2, 1, 0, 1),
        "wepon4" : (3, 1, 0, 1),
        "wepon5" : (4, 1, 0, 1),
        "armor1" : (0, 2, 0, 1),
        "armor2" : (1, 2, 0, 1),
        "armor3" : (2, 2, 0, 1),
        "item1" : (0, 3, 0, 1),
        "item2" : (1, 3, 0, 1),
        "item3" : (2, 3, 0, 1),
        "item4" : (3, 3, 0, 1),
        "treasure" : (4, 3, 0, 1),
        # enemy
        "enemy1" : (0, 4, 0, 1),
        "enemy2" : (1, 4, 0, 1),
        "enemy3" : (2, 4, 0, 1),
        "enemy4" : (3, 4, 0, 1),
        "boss" : (4, 4, 0, 1)
    }
    def __init__(self):
        self.tile_x = 8
        self.tile_y = 8
        self.bit_x = 8
        self.bit_y = 8
        self.size_x = self.tile_x*self.bit_x
        self.size_y = self.tile_y*self.bit_y
        pyxel.init(self.size_x, self.size_y, fps = 30)

        colors = pyxel.colors.to_list()
        print(colors)
        pyxel.load("assets.pyxres")

        # start position
        self.x = 2
        self.y = 2

        self.map_size_x = 24
        self.map_size_y = 24
        self.map_init()
        pyxel.run(self.update, self.draw)

    # 初期化
    # マップ、当たり判定、位置、
    def map_init(self):
        self.map = [[0 for _ in range(self.map_size_x)]
            for _ in range(self.map_size_y)]
        for i in range(self.map_size_x):
            for j in range(self.map_size_y):
                x, y = pyxel.tilemap(0).pget(i, j)
                for _, tile in self.tile_dic.items():
                    if tile[0] == x and tile[1] == y:
                        self.map[j][i] = tile

    def is_collision(self, x, y):
        return self.map[y][x][3]

    def draw_tile(self, x, y, tile):
        """
        x, y: 描画位置
        tile: image bank上の位置、透明色
        """
        tile_x = tile[0]
        tile_y = tile[1]
        colkey = tile[2]
        # print(x, y, tile, tile_x, tile_y, pyxel.tilemap(0).pget(tile_x, tile_y))
        pyxel.blt(x*self.bit_x,
            y*self.bit_y,
            0,
            tile_x*self.bit_x,
            tile_y*self.bit_y,
            self.bit_x,
            self.bit_y,
            colkey)

    # 毎フレームオンメモリ情報を書き換える
    def update(self):
        # self.x = (self.x + 1) % pyxel.width
        if pyxel.frame_count % 5 == 0:
            x = self.x
            y = self.y
            mod = False
            if pyxel.btn(pyxel.KEY_UP):
                y = y - 1
                mod = True
            if pyxel.btn(pyxel.KEY_DOWN):
                y = y + 1
                mod = True
            if pyxel.btn(pyxel.KEY_LEFT):
                x = x - 1
                mod = True
            if pyxel.btn(pyxel.KEY_RIGHT):
                x = x + 1
                mod = True
            if mod and not self.is_collision(x, y):
                self.x = x
                self.y = y
    
    # 毎フレーム実際描画する
    def draw(self):
        # 画面黒初期化
        pyxel.cls(0)
        pyxel.camera()
        
        # draw background
        opt_x = max(self.x - self.tile_x//2, 0)
        opt_x = min(opt_x, self.map_size_x - self.tile_x)
        opt_y = max(self.y - self.tile_y//2, 0)
        opt_y = min(opt_y, self.map_size_y - self.tile_y)
        pyxel.camera(opt_x*self.bit_x, opt_y*self.bit_y)
        
        for i in range(self.map_size_x):
            for j in range(self.map_size_y):
                # print(self.x, self.y, i, j, opt_x, opt_y)
                self.draw_tile(i, j, self.map[j][i])
        
        # draw sprites
        self.draw_tile(self.x, self.y, self.tile_dic["reimu"])

Game()
