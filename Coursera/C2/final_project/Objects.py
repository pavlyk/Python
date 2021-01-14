from abc import ABC, abstractmethod
import pygame
import random
import os
import Service


def create_sprite(img, sprite_size):
    icon = pygame.image.load(img).convert_alpha()
    icon = pygame.transform.scale(icon, (sprite_size, sprite_size))
    sprite = pygame.Surface((sprite_size, sprite_size), pygame.HWSURFACE)
    sprite.blit(icon, (0, 0))
    return sprite

class AbstractObject(ABC):
    def __init__(self):
        self.sprite = None
        self.position = None
    
    def draw(self, display, mini = False):
        offset = display.screen_offset()
        cf = 20 if mini else 1
        sp = self.sprite.mini if mini else self.sprite
        display.blit(sp, ((self.position[0] - offset[0]) * display.game_engine.sprite_size/cf,
                                      (self.position[1] - offset[1]) * display.game_engine.sprite_size/cf))

class Interactive(ABC):

    @abstractmethod
    def interact(self, engine, hero):
        pass


# Союзник
class Ally(AbstractObject, Interactive):

    def __init__(self, icon, action, position):
        self.sprite = icon
        self.action = action
        self.position = position

    def interact(self, engine, hero):
        self.action(engine, hero)


# Человек
class Creature(AbstractObject):

    def __init__(self, icon, stats, position):
        self.sprite = icon
        self.stats = stats
        self.position = position
        self.calc_max_HP()
        self.hp = self.max_hp

    def calc_max_HP(self):
        self.max_hp = 5 + self.stats["endurance"] * 2
        
    def get_stats(self):
        return self.stats

class Enemy(Creature, Interactive):
    def __init__(self, icon, stats, xp, position):
        self.icon = icon
        self.stats = stats
        self.xp = xp
        self.position = position
        super().__init__(icon, stats, position)

    def interact(self, engine, hero):
        hero.hp -= self.stats['strength']
        engine.score += self.stats['intelligence']
        if hero.hp <= 0:
            engine.notify('YOU DIE!')
            engine.level -= 2
            hero.level -= 1
            Service.reload_game(engine, hero)
        hero.exp += self.stats['experience']
        hero.gold += self.stats['endurance'] * random.randint(1, self.stats['luck'])
        for i in hero.level_up():
            engine.notify('Level UP!')


class Hero(Creature):

    def __init__(self, stats, icon):
        pos = [1, 1]
        self.level = 1
        self.exp = 0
        self.gold = 0
        self.item_level = 0
        self.base_stats = stats        
        super().__init__(icon, stats, pos)

    def level_up(self):
        while self.exp >= 100 * (2 ** (self.level - 1)):
            yield "level up!"
            self.level += 1
            self.stats["strength"] += 2
            self.stats["endurance"] += 2
            self.calc_max_HP()
            self.hp = self.max_hp
            
    def get_stats(self):
        return {"strength": self.stats["strength"] * 2**self.item_level,
                "endurance": self.stats["endurance"] * 2**self.item_level,
                "intelligence": self.stats["intelligence"], 
                "luck": self.stats["luck"]}

class Effect(Hero):

    def __init__(self, base):
        self.base = base
        self.stats = self.base.stats.copy()
        self.apply_effect()
        
    @property
    def base_stats(self):
        return self.base.base_stats
        
    @property
    def item_level(self):
        return self.base.item_level

    @item_level.setter
    def item_level(self, value):
        if value < 4:
            self.base.item_level = value

    @property
    def position(self):
        return self.base.position

    @position.setter
    def position(self, value):
        self.base.position = value

    @property
    def level(self):
        return self.base.level

    @level.setter
    def level(self, value):
        self.base.level = value

    @property
    def gold(self):
        return self.base.gold

    @gold.setter
    def gold(self, value):
        self.base.gold = value

    @property
    def hp(self):
        return self.base.hp

    @hp.setter
    def hp(self, value):
        self.base.hp = value

    @property
    def max_hp(self):
        return self.base.max_hp

    @max_hp.setter
    def max_hp(self, value):
        self.base.max_hp = value

    @property
    def exp(self):
        return self.base.exp

    @exp.setter
    def exp(self, value):
        self.base.exp = value

    @property
    def sprite(self):
        return self.base.sprite

    @abstractmethod
    def apply_effect(self):
        pass

# add classes

class Berserk(Effect):
    def apply_effect(self):
        self.stats['strength'] += 50
        self.stats['endurance'] -= 20 if self.stats['endurance'] > 20 else self.stats['endurance']
        self.calc_max_HP()
        self.hp = self.max_hp
    
    
class Blessing(Effect):
    def apply_effect(self):
        self.stats['strength'] += 5
        self.stats['endurance'] += 5
        self.stats['luck'] += 5
        self.stats['intelligence'] += 5
        self.hp += 10
        if self.hp > self.max_hp:
            self.max_hp = self.hp


class Weakness(Effect):
    def apply_effect(self):
        self.stats['strength'] = 15


class Darkness(Effect):
    def apply_effect(self):
        self.stats['strength'] -= 5
        self.stats['endurance'] -= 5
        self.stats['luck'] -= 5
        self.stats['intelligence'] -= 5
        self.hp -= 10 if self.hp > 10 else self.hp - 1