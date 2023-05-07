import pyxel
import random
import pprint

MAP_WIDTH = 30
MAP_HEIGHT = 20
TILE_SIZE = 16
class Game:
    def __init__(self):
        pyxel.init(MAP_WIDTH * 8, MAP_HEIGHT * 8, title="Rogue-like game")
        pyxel.load("assets.pyxres")
        self.player_x = 1
        self.player_y = 1
        self.player_health = 10
        self.player_damage = 1
        self.player_score = 0
        self.current_floor = 1
        self.enemy_types = [
            {"name": "Goblin", "health": 2, "damage": 1, "score": 1},
            {"name": "Orc", "health": 4, "damage": 2, "score": 2},
            {"name": "Troll", "health": 8, "damage": 4, "score": 3},
            {"name": "Dragon", "health": 16, "damage": 8, "score": 5},
        ]
        self.boss_types = [
            {"name": "Giant Spider", "health": 32, "damage": 8, "score": 10},
            {"name": "Minotaur", "health": 64, "damage": 16, "score": 20},
            {"name": "Demon Lord", "health": 128, "damage": 32, "score": 50},
        ]
        self.generate_map()
        self.spawn_objects()
        self.generate_enemy_pool()

    def generate_map(self):
        self.map = [[0 for y in range(MAP_HEIGHT)] for x in range(MAP_WIDTH)]
        for x in range(MAP_WIDTH):
            self.map[x][0] = 1
            self.map[x][MAP_HEIGHT - 1] = 1
        for y in range(MAP_HEIGHT):
            self.map[0][y] = 1
            self.map[MAP_WIDTH - 1][y] = 1
        for i in range(20):
            self.map[random.randint(1, MAP_WIDTH - 2)][random.randint(1, MAP_HEIGHT - 2)] = 1

    def is_walkable(self, x, y):
        return self.map[x][y] == 0

    def spawn_objects(self):
        self.items = []
        for i in range(10):
            item_x = random.randint(1, MAP_WIDTH - 2)
            item_y = random.randint(1, MAP_HEIGHT - 2)
            self.items.append({"x": item_x, "y": item_y, "type": "health"})
        for i in range(5):
            item_x = random.randint(1, MAP_WIDTH - 2)
            item_y = random.randint(1, MAP_HEIGHT - 2)
            self.items.append({"x": item_x, "y": item_y, "type": "damage"})
        self.enemies = []
        for i in range(20):
            enemy_x = random.randint(1, MAP_WIDTH - 2)
            enemy_y = random.randint(1, MAP_HEIGHT - 2)
            pprint.pp(vars(self))
            enemy_type = random.choice(self.enemy_types)
            self.enemies.append({"x": enemy_x, "y": enemy_y, "type": enemy_type})

    def generate_enemy_pool(self):
        self.enemy_pool = []
        for enemy_type in self.enemy_types:
            for i in range(5):
                self.enemy_pool.append(enemy_type)
        random.shuffle(self.enemy_pool)

    def get_random_enemy(self):
        if len(self.enemy_pool) == 0:
            self.generate_enemy_pool()
        enemy_type = self.enemy_pool.pop()
        enemy = {"health": enemy_type["health"], "damage": enemy_type["damage"], "score": enemy_type["score"]}
        return enemy

    def get_item_at(self, x, y):
        for item in self.items:
            if item["x"] == x and item["y"] == y:
                return item
        return None

    def get_enemy_at(self, x, y):
        for enemy in self.enemies:
            if enemy["x"] == x and enemy["y"] == y:
                return enemy
        return None

    def update(self):
        if pyxel.btn(pyxel.KEY_LEFT):
            if self.is_walkable(self.player_x - 1, self.player_y):
                self.player_x -= 1
        elif pyxel.btn(pyxel.KEY_RIGHT):
            if self.is_walkable(self.player_x + 1, self.player_y):
                self.player_x += 1
        elif pyxel.btn(pyxel.KEY_UP):
            if self.is_walkable(self.player_x, self.player_y - 1):
                self.player_y -= 1
        elif pyxel.btn(pyxel.KEY_DOWN):
            if self.is_walkable(self.player_x, self.player_y + 1):
                self.player_y += 1
        item = self.get_item_at(self.player_x, self.player_y)
        if item is not None:
            if item["type"] == "health":
                self.player_health += 2
                if self.player_health > 10:
                    self.player_health = 10
            elif item["type"] == "damage":
                self.player_damage += 1
            self.items.remove(item)
        enemy = self.get_enemy_at(self.player_x, self.player_y)
        if enemy is not None:
            enemy_health = enemy["health"]
            while enemy_health > 0 and self.player_health > 0:
                enemy_health -= self.player_damage
                if enemy_health <= 0:
                    self.player_score += enemy["score"]
                    self.enemies.remove(enemy)
                    pyxel.play(0, 0)
                    break
                self.player_health -= enemy["damage"]
                if self.player_health <= 0:
                    pyxel.play(0, 1)
                    break
        if len(self.enemies) == 0:
            if self.current_floor == 3:
                pyxel.quit()
            else:
                self.current_floor += 1
                self.generate_map()
                self.spawn_objects()
                pyxel.play(0, 2)

    def draw(self):
        pyxel.cls(0)
        for x in range(MAP_WIDTH):
            for y in range(MAP_HEIGHT):
                if self.map[x][y] == "#":
                    pyxel.rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE, 3)
                elif self.map[x][y] == ".":
                    pyxel.rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE, 1)
                elif self.map[x][y] == "P":
                    pyxel.rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE, 5)
                elif self.map[x][y] == "E":
                    pyxel.rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE, 8)
        for item in self.items:
            if item["type"] == "health":
                pyxel.rect(item["x"] * TILE_SIZE, item["y"] * TILE_SIZE, TILE_SIZE, TILE_SIZE, 10)
            elif item["type"] == "damage":
                pyxel.rect(item["x"] * TILE_SIZE, item["y"] * TILE_SIZE, TILE_SIZE, TILE_SIZE, 11)
        for enemy in self.enemies:
            pyxel.rect(enemy["x"] * TILE_SIZE, enemy["y"] * TILE_SIZE, TILE_SIZE, TILE_SIZE, 6)
        pyxel.text(5, 5, f"Floor: {self.current_floor}", 7)
        pyxel.text(5, 15, f"Health: {self.player_health}", 7)
        pyxel.text(5, 25, f"Damage: {self.player_damage}", 7)
        pyxel.text(5, 35, f"Score: {self.player_score}", 7)

if __name__ == "__main__":
    game = Game()
    # pyxel.init(MAP_WIDTH * TILE_SIZE, MAP_HEIGHT * TILE_SIZE, title="Roguelike Game")
    pyxel.run(game.update, game.draw)
