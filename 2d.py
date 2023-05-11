import argparse
from enum import auto, Enum
import pyxel
import pprint
import random
import sys
import uuid

obj_info = {
    # obj
    "wall" : {"tile_x": 0, "tile_y": 6, "colkey": None, "col": 1},
    "water" : {"tile_x": 1, "tile_y": 6, "colkey": None, "col": 1},
    "aisle" : {"tile_x": 0, "tile_y": 5, "colkey": None, "col": 0},
    "grass" : {"tile_x": 1, "tile_y": 5, "colkey": None, "col": 0},
    "wood" : {"tile_x": 2, "tile_y": 5, "colkey": None, "col": 1},
    "status_corner" : {"tile_x": 3, "tile_y": 5, "colkey": 1, "col": 1},
    "status_edge" : {"tile_x": 4, "tile_y": 5, "colkey": 1, "col": 1},
    # charactor
    "hero" : {"tile_x": 1, "tile_y": 0, "colkey": 0, "col": 1},
    "reimu" : {"tile_x": 2, "tile_y": 0, "colkey": 1, "col": 1},
    "marisa" : {"tile_x": 3, "tile_y": 0, "colkey": 1, "col": 1},
    # enemy
    "enemy1" : {"tile_x": 0, "tile_y": 4, "colkey": 0, "col": 1},
    "enemy2" : {"tile_x": 1, "tile_y": 4, "colkey": 0, "col": 1},
    "enemy3" : {"tile_x": 2, "tile_y": 4, "colkey": 0, "col": 1},
    "enemy4" : {"tile_x": 3, "tile_y": 4, "colkey": 0, "col": 1},
    "boss" : {"tile_x": 4, "tile_y": 4, "colkey": 0, "col": 1},
    # item
    # wepon
    "wepon1" : {"tile_x": 0, "tile_y": 1, "colkey": 0, "col": 1},
    "wepon2" : {"tile_x": 1, "tile_y": 1, "colkey": 0, "col": 1},
    "wepon3" : {"tile_x": 2, "tile_y": 1, "colkey": 0, "col": 1},
    "wepon4" : {"tile_x": 3, "tile_y": 1, "colkey": 0, "col": 1},
    "wepon5" : {"tile_x": 4, "tile_y": 1, "colkey": 0, "col": 1},
    "armor1" : {"tile_x": 0, "tile_y": 2, "colkey": 0, "col": 1},
    "armor2" : {"tile_x": 1, "tile_y": 2, "colkey": 0, "col": 1},
    "armor3" : {"tile_x": 2, "tile_y": 2, "colkey": 0, "col": 1},
    "item1" : {"tile_x": 0, "tile_y": 3, "colkey": 0, "col": 1},
    "item2" : {"tile_x": 1, "tile_y": 3, "colkey": 0, "col": 1},
    "item3" : {"tile_x": 2, "tile_y": 3, "colkey": 0, "col": 1},
    "item4" : {"tile_x": 3, "tile_y": 3, "colkey": 0, "col": 1},
    "treasure" : {"tile_x": 4, "tile_y": 3, "colkey": 0, "col": 1},
}

class Obj:
    def __init__(self, name, tile_x=None, tile_y=None, x=None, y=None, colkey=None, col=False):
        self.id = str(uuid.uuid4())
        self.name = name
        self.attr = []
        self.x = x if None else x
        self.y = y if None else y
        self.tile_x = obj_info["tile_x"] if None else tile_x
        self.tile_y = obj_info["tile_y"] if None else tile_y
        self.colkey = obj_info["colkey"] if None else colkey
        self.col = obj_info["col"] if None else col
        self.hide = True
        # self.register()
        return self
    
    def register(self, params):
        if not "obj" in params:
            params["obj"] = {}
        params["obj"][self.id] = self

    def unregister(self, params):
        params["obj"].pop(self.id)

    def spawn(self, params, x=None, y=None):
        # game_map = args.
        if type(x) == type(y) == int:
            if x > 0 and y > 0 and is_collision(params, x, y):
                self.x = x
                self.y = y
                self.register(params)
                self.hide = False
        if x == y == None:
            x, y = get_random_position(params["map"], params["map_width"], params["map_height"])
            self.x = x
            self.y = y
            self.register(params)
            self.hide = False
        return self
    
    def kill(self, params):
        self.unregister(params)

class Character(Obj):
    def __init__(self, name, level=None, health=None, attack=None, defense=None, agility=None, gold=None, exp=None):
        super().__init__(name)
        self.level = obj_info["level"] if None else level
        self.health = obj_info["health"] if None else health
        self.attack = obj_info["attack"] if None else attack
        self.defense = obj_info["defense"] if None else defense
        self.agility = obj_info["agility"] if None else agility
        self.gold = obj_info["gold"] if None else gold
        self.exp = obj_info["exp"] if None else exp

class Enemy(Character):
    def __init__(self, name, health=None, attack=None, defense=None, agility=None, exp=None, gold=None):
        super().__init__(name, health, attack, defense, agility, exp, gold)

class Player(Character):
    def __init__(self, name, health=None, attack=None, defense=None, level=None, exp=None, gold=None):
        super().__init__(name, health, attack, defense, level, exp, gold)
        self.attr.append("player")

class Item(Obj):
    def __init__(self, name, desc=None):
        self.name = name
        self.desc = dbj_info["desc"] if None else desc

class Weapon(Item):
    def __init__(self, name, attack=None):
        super().__init__(name)
        self.attack = dbj_info["attack"] if None else attack

class Armor(Item):
    def __init__(self, name, defense=None):
        super().__init__(name)
        self.defense = dbj_info["defense"] if None else defense

def get_random_position(game_map, map_size_x, map_size_y):
    while True:
        x = random.randint(0, map_size_x - 1)
        y = random.randint(0, map_size_y - 1)
        if game_map[y][x]["col"] == 0:
            return x, y

def is_collision(params, x, y):
    if params["map"][y][x]["col"]:
        # print("map_col")
        return True
    for id, obj in params["obj"].items():
        if x == obj.x and y == obj.y:
            # print("sp_col")
            return True
    return False

class Game:
    def __init__(self, params):
        self.params = params
        self.tile_x = params["visible_tile_width"]
        self.tile_y = params["visible_tile_height"]
        self.bit_x = params["bit_width"]
        self.bit_y = params["bit_height"]
        self.width = self.tile_x*self.bit_x
        self.height = self.tile_y*self.bit_y
        self.status_hide = False
        pyxel.init(self.width, self.height, fps = args.fps)

        colors = pyxel.colors.to_list()
        print(colors)
        pyxel.load("assets.pyxres")

        self.map_size_x = params["map_width"]
        self.map_size_y = params["map_height"]
        self.map_init()
        # self.set_random_position()

        self.player = Player("reimu").spawn(self.params)
        self.x = self.player.x
        self.y = self.player.y

        pyxel.run(self.update, self.draw)

    def map_init(self):
        self.map = [[0 for _ in range(self.map_size_x)]
            for _ in range(self.map_size_y)]
        for i in range(self.map_size_x):
            for j in range(self.map_size_y):
                x, y = pyxel.tilemap(0).pget(i, j)
                for _, tile in obj_info.items():
                    if tile["tile_x"] == x and tile["tile_y"] == y:
                        self.map[j][i] = tile
        self.params["map"] = self.map

    def set_random_position(self):
        self.x, self.y = get_random_position(self.map,
                                            self.map_size_x,
                                            self.map_size_y)

    def draw_tile(self, x, y, tile, inv_x=False, inv_y=False):
        """
        x, y: 描画位置
        tile: image bank上の位置、透明色
        """
        tile_x = tile["tile_x"]
        tile_y = tile["tile_y"]
        colkey = tile["colkey"]
        # print(x, y, tile, tile_x, tile_y, pyxel.tilemap(0).pget(tile_x, tile_y))
        pyxel.blt(x*self.bit_x,
            y*self.bit_y,
            0,
            tile_x*self.bit_x,
            tile_y*self.bit_y,
            self.bit_x*(-1 if inv_x else 1),
            self.bit_y*(-1 if inv_y else 1),
            colkey)

    def update_direction(self):
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
            if mod and not is_collision(self.params, x, y):
                self.x = x
                self.y = y
            self.player.x = self.x
            self.player.y = self.y

    # 毎フレームオンメモリ情報を書き換える
    def update(self):
        self.update_direction()
        if pyxel.frame_count % 5 == 0:
            if pyxel.btn(pyxel.KEY_S):
                Enemy("enemy4").spawn(self.params)
                # print(self.params["obj"])
            if pyxel.btn(pyxel.KEY_K):
                obj_sample = random.choice(list(self.params["obj"].values()))
                if not "player" in obj_sample.attr:
                    obj_sample.kill(self.params)
                # print(self.params["obj"])
            if pyxel.btn(pyxel.KEY_D):
                for _, v in self.params["obj"].items():
                    pprint.pprint(vars(v))
                if self.status_hide:
                    self.status_hide = False
                else:
                    self.status_hide = True

    def draw_sprites(self):
        objects = self.params["obj"]
        
        for id, obj in objects.items():
            if obj.hide:
                continue
            # print(obj.x, obj.y, obj.name)
            self.draw_tile(obj.x, obj.y, obj_info[obj.name])
    
    def get_camera_corner(self):
        opt_x = max(self.x - self.tile_x//2, 0)
        opt_x = min(opt_x, self.map_size_x - self.tile_x)
        opt_y = max(self.y - self.tile_y//2, 0)
        opt_y = min(opt_y, self.map_size_y - self.tile_y)
        return opt_x, opt_y

    def draw_status(self, bar_len=0):
        if self.status_hide:
            return
        # カメラに追従させる
        opt_x, opt_y = self.get_camera_corner()
        self.draw_tile(opt_x, opt_y, obj_info["status_corner"])
        self.draw_tile(opt_x, opt_y + 1, obj_info["status_corner"], inv_y=True)
        for i in range(bar_len):
            self.draw_tile(opt_x+i+1, opt_y, obj_info["status_edge"])
            self.draw_tile(opt_x+i+1, opt_y + 1, obj_info["status_edge"], inv_y=True)
        self.draw_tile(opt_x + bar_len + 1, opt_y, obj_info["status_corner"], inv_x=True)
        self.draw_tile(opt_x + bar_len + 1, opt_y + 1, obj_info["status_corner"], inv_x=True, inv_y=True)

        pyxel.text(opt_x*self.bit_x + 5, opt_y*self.bit_y + 5, f"obj: {len(self.params['obj'])}", 7)

    # 毎フレーム実際描画する
    def draw(self):
        # 画面黒初期化
        pyxel.cls(0)
        pyxel.camera()
        
        # draw background
        opt_x, opt_y = self.get_camera_corner()
        pyxel.camera(opt_x*self.bit_x, opt_y*self.bit_y)
        
        for i in range(self.map_size_x):
            for j in range(self.map_size_y):
                # print(self.x, self.y, i, j, opt_x, opt_y)
                self.draw_tile(i, j, self.map[j][i])
        
        # draw sprites
        self.draw_sprites()
        self.draw_status(bar_len=5)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-bh", "--bit_height", type=int, default=8, help="")
    parser.add_argument("-bw", "--bit_width", type=int, default=8, help="")
    parser.add_argument("-mh", "--map_height", type=int, default=24, help="")
    parser.add_argument("-mw", "--map_width", type=int, default=24, help="")
    parser.add_argument("-th", "--visible_tile_height", type=int, default=16, help="")
    parser.add_argument("-tw", "--visible_tile_width", type=int, default=16, help="")
    parser.add_argument("-fps", "--fps", type=int, default=30, help="")
    parser.add_argument("-s", "--stop", action="store_true", help="")
    args = parser.parse_args()
    params = vars(args)

    pprint.pprint(params)

    Game(params)
