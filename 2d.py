import argparse
from enum import auto, Enum
import pyxel
import pprint
import random
import sys
import uuid
import maze

obj_info = {
    # obj
    "black" : {"tile_x": 0, "tile_y": 0, "colkey": None, "col": 0, "attr": "obst"},
    "wall" : {"tile_x": 0, "tile_y": 6, "colkey": None, "col": 1, "attr": "obst"},
    "water" : {"tile_x": 1, "tile_y": 6, "colkey": None, "col": 1, "attr": "obst"},
    "aisle" : {"tile_x": 0, "tile_y": 5, "colkey": None, "col": 0, "attr": "obst"},
    "grass" : {"tile_x": 1, "tile_y": 5, "colkey": None, "col": 0, "attr": "obst"},
    "tree" : {"tile_x": 2, "tile_y": 5, "colkey": None, "col": 1, "attr": "obst"},
    "status_corner" : {"tile_x": 3, "tile_y": 5, "colkey": 1, "col": 1, "attr": "obst"},
    "status_ver_edge" : {"tile_x": 3, "tile_y": 6, "colkey": 1, "col": 1, "attr": "obst"},
    "status_hori_edge" : {"tile_x": 4, "tile_y": 5, "colkey": 1, "col": 1, "attr": "obst"},
    # charactor
    "hero" : {"tile_x": 1, "tile_y": 0, "colkey": 0, "col": 1, "attr": "chara"},
    "reimu" : {"tile_x": 2, "tile_y": 0, "colkey": 1, "col": 1, "attr": "chara"},
    "marisa" : {"tile_x": 3, "tile_y": 0, "colkey": 1, "col": 1, "attr": "chara"},
    # enemy
    "enemy1" : {"tile_x": 0, "tile_y": 4, "colkey": 0, "col": 1, "attr": "enemy", "attack": 1, "defence":1, "agility":1, "exp":1, "gold":1},
    "enemy2" : {"tile_x": 1, "tile_y": 4, "colkey": 0, "col": 1, "attr": "enemy", "attack": 2, "defence":2, "agility":2, "exp":3, "gold":5},
    "enemy3" : {"tile_x": 2, "tile_y": 4, "colkey": 0, "col": 1, "attr": "enemy", "attack": 5, "defence":5, "agility":5, "exp":5, "gold":20},
    "enemy4" : {"tile_x": 3, "tile_y": 4, "colkey": 0, "col": 1, "attr": "enemy", "attack": 10, "defence":10, "agility":10, "exp":7, "gold":50},
    "boss" : {"tile_x": 4, "tile_y": 4, "colkey": 0, "col": 1, "attr": "enemy", "attack": 100, "defence":50, "agility":30, "exp":30, "gold":500},
    # item
    # wepon
    "wepon1" : {"tile_x": 0, "tile_y": 1, "colkey": 0, "col": 1, "attr": "wepon", "attack": 1},
    "wepon2" : {"tile_x": 1, "tile_y": 1, "colkey": 0, "col": 1, "attr": "wepon", "attack": 2},
    "wepon3" : {"tile_x": 2, "tile_y": 1, "colkey": 0, "col": 1, "attr": "wepon", "attack": 3},
    "wepon4" : {"tile_x": 3, "tile_y": 1, "colkey": 0, "col": 1, "attr": "wepon", "attack": 5},
    "wepon5" : {"tile_x": 4, "tile_y": 1, "colkey": 0, "col": 1, "attr": "wepon", "attack": 10},
    "armor1" : {"tile_x": 0, "tile_y": 2, "colkey": 0, "col": 1, "attr": "wepon", "defence": 1},
    "armor2" : {"tile_x": 1, "tile_y": 2, "colkey": 0, "col": 1, "attr": "wepon", "defence": 3},
    "armor3" : {"tile_x": 2, "tile_y": 2, "colkey": 0, "col": 1, "attr": "wepon", "defence": 5},
    "item1" : {"tile_x": 0, "tile_y": 3, "colkey": 0, "col": 1, "attr": "item", "heal": 1},
    "item2" : {"tile_x": 1, "tile_y": 3, "colkey": 0, "col": 1, "attr": "item", "heal": 2},
    "item3" : {"tile_x": 2, "tile_y": 3, "colkey": 0, "col": 1, "attr": "item", "heal": 5},
    "item4" : {"tile_x": 3, "tile_y": 3, "colkey": 0, "col": 1, "attr": "item", "heal": 10},
    "treasure" : {"tile_x": 4, "tile_y": 3, "colkey": 0, "col": 1, "attr": "item", "heal": 99},
}

params = {}
obsts = {}
charas = {}
enemys = {}
items = {}
wepons = {}

class Obj:
    def __init__(self, name, tile_x=None, tile_y=None, x=None, y=None, colkey=None, col=False):
        self.id = str(uuid.uuid4())
        self.name = name
        self.attr = []
        self.x = obj_info.get("x", x)
        self.y = obj_info.get("y", y)
        self.to_x = obj_info.get("x", x)
        self.to_y = obj_info.get("y", y)
        self.move_bit = 0
        self.tile_x = obj_info.get("tile_x", tile_x)
        self.tile_y = obj_info.get("tile_y", tile_y)
        self.colkey = obj_info.get("colkey", colkey)
        self.col = obj_info.get("col", col)
        self.hide = True
        # self.register()
        print(name)
        return self
    
    def register(self):
        if not "obj" in params:
            params["obj"] = {}
        params["obj"][self.id] = self

    def unregister(self):
        # pprint.pprint(params["obj"])
        params["obj"].pop(self.id)

    def spawn(self, x=None, y=None):
        # game_map = args.
        if type(x) == type(y) == int:
            if x > 0 and y > 0 and is_collision(x, y):
                self.x = self.to_x = x
                self.y = self.to_y = y
                self.register()
                self.hide = False
        if x == y == None:
            x, y = get_random_position()
            self.x = self.to_x = x
            self.y = self.to_y = y
            self.register()
            self.hide = False
        return self
    
    def kill(self):
        self.unregister()

class Character(Obj):
    def __init__(self, name, level, hp, mp, attack, defence, agility, gold, exp):
        super().__init__(name)
        obj = obj_info[name]
        self.level = obj.get("level", level)
        self.hp = obj.get("hp", hp)
        self.max_hp = obj.get("hp", hp)
        self.mp = obj.get("mp", mp)
        self.max_mp = obj.get("mp", mp)
        self.attack = obj.get("attack", attack)
        self.defence = obj.get("defence", defence)
        self.agility = obj.get("agility", agility)
        self.gold = obj.get("gold", gold)
        self.exp = obj.get("exp", exp)
class Enemy(Character):
    def __init__(self, name, level=1, hp=5, mp=10, attack=1, defence=1, agility=1, gold=1, exp=1):
        super().__init__(name, level, hp, mp, attack, defence, agility, gold, exp)
        self.attr.append("enemy")

class Player(Character):
    def __init__(self, name, level=1, hp=10, mp=10, attack=1, defence=1, agility=1, gold=1, exp=1):
        super().__init__(name, level, hp, mp, attack, defence, agility, gold, exp)
        self.attr.append("player")
        self.beat_enemy = 0
        self.next_level_exp = 10
    
    def level_up(self):
        self.level += 1
        self.max_hp += random.randint(0,5)
        self.max_mp += random.randint(0,5)
        self.attack += random.randint(0,2)
        self.defence += random.randint(0,2)
        self.agility += random.randint(0,2)
        self.hp = self.max_hp
        self.mp = self.max_mp

class Item(Obj):
    def __init__(self, name, heal=1, desc=None):
        super().__init__(name)
        obj = obj_info[name]
        self.desc = obj.get("desc", desc)
        self.heal = obj.get("heal", heal)
        self.attr.append("item")

class Weapon(Item):
    def __init__(self, name, attack=0, defence=0):
        super().__init__(name)
        obj = obj_info[name]
        self.attack = obj.get("attack", attack)
        self.defence = obj.get("defence", defence)
        self.attr.append("weapon")

def get_random_position():
    game_map = params["map"]
    map_size_x = params["map_width"]
    map_size_y = params["map_height"]
    while True:
        x = random.randint(0, map_size_x - 1)
        y = random.randint(0, map_size_y - 1)
        if game_map[y][x]["col"] == 0:
            return x, y

def is_collision(x, y):
    if params["map"][y][x]["col"]:
        # print("map_col")
        return True
    for id, obj in params["obj"].items():
        if x == obj.x and y == obj.y:
            # print("sp_col")
            return True
    return False

def collision_obj(x, y):
    if params["map"][y][x]["col"]:
        # print("map_col")
        return True
    for id, obj in params["obj"].items():
        if x == obj.x and y == obj.y:
            # print("sp_col")
            return True
    return False

class Game:
    def __init__(self):
        self.tile_x = params["visible_tile_width"]
        self.tile_y = params["visible_tile_height"]
        self.bit_x = params["bit_width"]
        self.bit_y = params["bit_height"]
        self.width = self.tile_x*self.bit_x
        self.height = self.tile_y*self.bit_y
        self.status_hide = False
        self.is_game_over = False
        pyxel.init(self.width, self.height, fps = args.fps)

        colors = pyxel.colors.to_list()
        # print(colors)
        pyxel.load("assets.pyxres")

        self.map_size_x = params["map_width"]
        self.map_size_y = params["map_height"]
        self.map_init()
        # self.set_random_position()

        self.player = Player("reimu").spawn()
        self.x = self.player.x*self.bit_x
        self.y = self.player.y*self.bit_x
        
        for k, tile in obj_info.items():
            if tile["attr"] == "obst":
                obsts[k] = tile
            elif tile["attr"] == "chara":
                charas[k] = tile
            elif tile["attr"] == "enemy":
                enemys[k] = tile
            elif tile["attr"] == "wepon":
                wepons[k] = tile
            elif tile["attr"] == "item":
                items[k] = tile
                
        pyxel.run(self.update, self.draw)

    def map_init(self):
        self.map = [[0 for _ in range(self.map_size_x)]
            for _ in range(self.map_size_y)]
        for i in range(self.map_size_x):
            for j in range(self.map_size_y):
                x, y = pyxel.tilemap(0).pget(i, j)
                not_found = True
                for _, tile in obj_info.items():
                    if tile["tile_x"] == x and tile["tile_y"] == y:
                        self.map[j][i] = tile
                        not_found = False
                        break
                if not_found:
                    print(f"tile not found, {i} {j}")
                    raise RuntimeError
        params["map"] = self.map
        return

        self.maze_map = maze.get_maze("bar_down", self.map_size_x, self.map_size_y)
        print(len(self.maze_map), len(self.maze_map[0]))
        # maze_map = [[0 for i in range(self.map_size_x)] for j in range(self.map_size_y)]
        for i in range(self.map_size_x):
            for j in range(self.map_size_y):
                # print(i, j, self.maze_map[j][i])
                obj_attr = self.maze_map[j][i]
                if obj_attr == maze.ObjAttr.AISLE:
                    self.maze_map[j][i] = obj_info["aisle"]
                elif obj_attr == maze.ObjAttr.WALL:
                    self.maze_map[j][i] = obj_info["wall"]
                elif obj_attr == maze.ObjAttr.GOAL:
                    self.maze_map[j][i] = obj_info["wall"]
                else:
                    print(f"invalid attr, {i} {j}")
                    raise RuntimeError
        params["maze_map"] = self.maze_map
        params["map"] = self.maze_map
        # params["map"] = self.map

    def set_random_position(self):
        x, y = get_random_position()
        self.x, self.y = x*self.bit_x, y*self.bit_y

    def draw_tile(self, x, y, tile, inv_x=False, inv_y=False):
        """
        x, y: 描画位置
        tile: image bank上の位置、透明色
        """
        tile_x = tile["tile_x"]
        tile_y = tile["tile_y"]
        colkey = tile["colkey"]
        # print(x, y, tile, tile_x, tile_y, pyxel.tilemap(0).pget(tile_x, tile_y))
        pyxel.blt(x,
            y,
            0,
            tile_x*self.bit_x,
            tile_y*self.bit_y,
            self.bit_x*(-1 if inv_x else 1),
            self.bit_y*(-1 if inv_y else 1),
            colkey)
    
    def move_tile(self, obj, tile,
                    inv_x=False, inv_y=False):
        """
        x, y: 描画位置
        tile: image bank上の位置、透明色
        """
        tile_x = tile["tile_x"]
        tile_y = tile["tile_y"]
        colkey = tile["colkey"]
        to_x = obj.to_x
        to_y = obj.to_y
        x = obj.x
        y = obj.y
        
        if to_x - x and to_y - y:
            self.player.x = self.player.to_x
            self.player.y = self.player.to_y
            return
        if obj.move_bit < 8:
            pyxel.blt(x*self.bit_x + (to_x - x)*obj.move_bit,
                y*self.bit_y + (to_y - y)*obj.move_bit,
                0,
                tile_x*self.bit_x,
                tile_y*self.bit_y,
                self.bit_x*(-1 if inv_x else 1),
                self.bit_y*(-1 if inv_y else 1),
                colkey)
            obj.move_bit += 1
            if "player" in obj.attr:
                self.x = obj.x*self.bit_x + (to_x - x)*obj.move_bit
                self.y = obj.y*self.bit_y + (to_y - y)*obj.move_bit
        else:
            obj.x = obj.to_x
            obj.y = obj.to_y
            obj.move_bit = 0
            if "player" in obj.attr:
                self.player.x = obj.x
                self.player.y = obj.y
                self.x = obj.x*self.bit_x
                self.y = obj.y*self.bit_y
            pyxel.blt(self.x,
                self.y,
                0,
                tile_x*self.bit_x,
                tile_y*self.bit_y,
                self.bit_x*(-1 if inv_x else 1),
                self.bit_y*(-1 if inv_y else 1),
                colkey)

    def game_over(self):
        self.is_game_over = True

    def add_exp(self, exp):
        player = self.player
        while True:
            if player.next_level_exp - exp > 0:
                player.next_level_exp -= exp
                break
            else:
                exp -= player.next_level_exp
                player.next_level_exp = 10
                player.level_up()
        
    def battle(self, enemy):
        player = self.player
        first, second = (player, enemy) if player.agility > enemy.agility else (enemy, player)
        turn = 0
        while(True):
            def one_turn(atk_side, def_side):
                battle_end = False
                def_side.hp -= max((atk_side.attack - def_side.defence), 1)
                if def_side.hp <= 0:
                    if def_side == player:
                        self.game_over()
                    else:
                        player.exp += enemy.exp
                        player.gold += enemy.gold
                        self.add_exp(enemy.exp)
                        def_side.kill()
                    battle_end = True
                return battle_end
            battle_end = one_turn(first, second)
            if battle_end:
                break
            battle_end = one_turn(second, first)
            if battle_end:
                break
            if ((turn := turn + 1) > 100):
                print("too many turn")
                raise RuntimeError

    def update_direction(self):
        if pyxel.frame_count % 5 == 0:
            if self.player.move_bit > 0:
                return
            x = self.x//self.bit_x
            y = self.y//self.bit_x
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
            if not mod:
                return
            
            # enemy/item なら消す
            col_obj = None
            for id, obj in params["obj"].items():
                if x == obj.x and y == obj.y:
                    # print(vars(obj))
                    col_obj = obj
                    break
            if not col_obj == None: 
                if "enemy" in col_obj.attr:
                    self.battle(col_obj)
                elif "weapon" in col_obj.attr:
                    # pprint.pprint(vars(col_obj))
                    self.player.attack += col_obj.attack
                    self.player.defence += col_obj.defence
                    col_obj.kill()
                elif "item" in col_obj.attr:
                    if col_obj.name == "treasure":
                        self.add_exp(random.randint(1, 114514))
                    else:
                        self.player.hp = min(self.player.hp + col_obj.heal, self.player.max_hp)
                    col_obj.kill()
            if mod and not is_collision(x, y):
                self.player.to_x = x
                self.player.to_y = y

    # 毎フレームオンメモリ情報を書き換える
    def update(self):
        if self.is_game_over:
            if pyxel.frame_count % 5 == 0:
                if pyxel.btn(pyxel.KEY_R):
                    self.set_random_position()
                    self.player.hp = self.player.max_hp
                    self.player.mp = self.player.max_mp
                    self.is_game_over = False
            return
        self.update_direction()
        if pyxel.frame_count % 5 == 0:
            if pyxel.btn(pyxel.KEY_S):
                sample = random.choice(list(enemys.keys()))
                Enemy(sample).spawn()
            if pyxel.btn(pyxel.KEY_W):
                sample = random.choice(list(wepons.keys()))
                Weapon(sample).spawn()
            if pyxel.btn(pyxel.KEY_I):
                sample = random.choice(list(items.keys()))
                Item(sample).spawn()
            if pyxel.btn(pyxel.KEY_K):
                obj_sample = random.choice(list(params["obj"].values()))
                if not "player" in obj_sample.attr:
                    obj_sample.kill(params)
                # print(self.params["obj"])
            if pyxel.btn(pyxel.KEY_D):
                # for _, v in params["obj"].items():
                if self.status_hide:
                    self.status_hide = False
                else:
                    self.status_hide = True

    def draw_sprites(self):
        objects = params["obj"]
        
        for id, obj in objects.items():
            if obj.hide:
                continue
            # print(obj.x, obj.y, obj.name)
            if obj.to_x == obj.x and obj.to_y == obj.y:
                self.draw_tile(obj.x*self.bit_x, obj.y*self.bit_x, obj_info[obj.name])
            else:
                self.move_tile(obj, obj_info[obj.name])
    
    def get_camera_corner(self):
        opt_x = max(self.x - self.tile_x*self.bit_x//2, 0)
        opt_x = min(opt_x, self.map_size_x*self.bit_x - self.tile_x*self.bit_x)
        opt_y = max(self.y - self.tile_y*self.bit_y//2, 0)
        opt_y = min(opt_y, self.map_size_y*self.bit_y - self.tile_y*self.bit_y)
        return opt_x, opt_y

    def draw_status(self, opt_x, opt_y, bar_x=0, bar_y=0):
        if self.status_hide:
            return

        for i in range(bar_x):
            for j in range(bar_y):
                if i in [0, bar_x - 1] or j in [0, bar_y - 1]:
                    inv_x = (i == bar_x - 1)
                    inv_y = (j == bar_y - 1)
                    tile_type = obj_info["status_hori_edge"]
                    if i == 0 or i == bar_x - 1:
                        tile_type = obj_info["status_ver_edge"]
                    if i in [0, bar_x - 1] and j in [0, bar_y - 1]:
                        tile_type = obj_info["status_corner"]
                    # print(opt_x + i*self.bit_x, opt_y + j*self.bit_y)
                    
                    self.draw_tile(opt_x + i*self.bit_x,
                                opt_y + j*self.bit_y,
                                tile_type,
                                inv_x=inv_x,
                                inv_y=inv_y)
                else:
                    self.draw_tile(opt_x + i*self.bit_x,
                        opt_y + j*self.bit_y,
                        obj_info["black"])

        def draw_text(line, text):
            pyxel.text(opt_x + 5,
                        opt_y + 5 + 6*line, 
                        text,
                        7)
        if self.is_game_over:
            draw_text(0, "geme_over")
        else:
            # text = f"{len(params['obj'])} {self.player.hp} {self.player.gold} {self.player.exp} "
            # pyxel.text(opt_x*self.bit_x + 5,
            #             opt_y*self.bit_y + 5, 
            #             text,
            #             7)
            me = self.player
            text_list = []
            text_list.append(f"LV:{me.level}")
            text_list.append(f"HP:{me.hp}/{me.max_hp}")
            text_list.append(f"MP:{me.mp}/{me.max_mp}")
            text_list.append(f"ATK:{me.attack}")
            text_list.append(f"DEF:{me.defence}")
            text_list.append(f"AGI:{me.agility}")
            text_list.append(f"GOLD:{me.gold}")
            text_list.append(f"EXP:{me.exp}")
            for i, text in enumerate(text_list):
                draw_text(i, text)

    # 毎フレーム実際描画する
    def draw(self):
        # 画面黒初期化
        pyxel.cls(0)
        pyxel.camera()
        
        # draw background
        opt_x, opt_y = self.get_camera_corner()
        pyxel.camera(opt_x, opt_y)
        
        for i in range(self.map_size_x):
            for j in range(self.map_size_y):
                self.draw_tile(i*self.bit_x, j*self.bit_y, params["map"][j][i])
        
        # draw sprites
        self.draw_sprites()
        self.draw_status(opt_x, opt_y, bar_x=6, bar_y=7)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-bh", "--bit_height", type=int, default=8, help="")
    parser.add_argument("-bw", "--bit_width", type=int, default=8, help="")
    parser.add_argument("-mh", "--map_height", type=int, default=40, help="")
    parser.add_argument("-mw", "--map_width", type=int, default=40, help="")
    parser.add_argument("-th", "--visible_tile_height", type=int, default=16, help="")
    parser.add_argument("-tw", "--visible_tile_width", type=int, default=16, help="")
    parser.add_argument("-fps", "--fps", type=int, default=60, help="")
    parser.add_argument("-s", "--stop", action="store_true", help="")
    args = parser.parse_args()
    params = vars(args)

    pprint.pprint(params)
    Game()

    # maze_map = maze.get_maze("wall_extend", args.map_width, args.map_height)
    # print("get_maze")
    # for j in range(args.map_height):
    #     print([1 if s == maze.ObjAttr.WALL else 0 for s in maze_map[j]])
