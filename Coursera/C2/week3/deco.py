from abc import ABC, abstractmethod


class AbstractEffect(Hero, ABC):

    def __init__(self, base):
        self.base = base

    @abstractmethod
    def get_stats(self):
        pass

    def get_negative_effects(self):
        return self.base.get_negative_effects()

    def get_positive_effects(self):
        return self.base.get_positive_effects()


class AbstractPositive(AbstractEffect):
    @abstractmethod
    def get_stats(self):
        pass

    def get_positive_effects(self):
        positive_effects = self.base.get_positive_effects()
        positive_effects.append(self.__class__.__name__)
        return positive_effects

    def get_negative_effects(self):
        return self.base.get_negative_effects()

class AbstractNegative(AbstractEffect):
    @abstractmethod
    def get_stats(self):
        pass

    def get_negative_effects(self):
        negative_effects = self.base.get_negative_effects()
        negative_effects.append(self.__class__.__name__)
        return negative_effects

    def get_positive_effects(self):
        return self.base.get_positive_effects()        


class Berserk(AbstractPositive):
    def get_stats(self):
        stats = self.base.get_stats()
        stats["HP"] += 50
        stats["Strength"] += 7
        stats["Endurance"] += 7
        stats["Agility"] += 7
        stats["Luck"] += 7
        stats["Perception"] -= 3
        stats["Charisma"] -= 3
        stats["Intelligence"] -= 3
        return stats


class Blessing(AbstractPositive):
    def get_stats(self):
        stats = self.base.get_stats()
        stats["Strength"] += 2
        stats["Endurance"] += 2
        stats["Agility"] += 2
        stats["Luck"] += 2
        stats["Perception"] += 2
        stats["Charisma"] += 2
        stats["Intelligence"] += 2
        return stats


class Weakness(AbstractNegative):
    def get_stats(self):
        stats = self.base.get_stats()
        stats["Strength"] -= 4
        stats["Endurance"] -= 4
        stats["Agility"] -= 4
        return stats


class EvilEye(AbstractNegative):
    def get_stats(self):
        stats = self.base.get_stats()
        stats["Luck"] -= 10
        return stats


class Curse(AbstractNegative):
    def get_stats(self):
        stats = self.base.get_stats()
        stats["Strength"] -= 2
        stats["Endurance"] -= 2
        stats["Agility"] -= 2
        stats["Luck"] -= 2
        stats["Perception"] -= 2
        stats["Charisma"] -= 2
        stats["Intelligence"] -= 2
        return stats


# class Hero(AbstractEffect):
#     def __init__(self):
#         self.positive_effects = []
#         self.negative_effects = []
#         self.stats = {
#             "HP": 128,  # health points
#             "MP": 42,  # magic points, 
#             "SP": 100,  # skill points
#             "Strength": 15,  # сила
#             "Perception": 4,  # восприятие
#             "Endurance": 8,  # выносливость
#             "Charisma": 2,  # харизма
#             "Intelligence": 3,  # интеллект
#             "Agility": 8,  # ловкость 
#             "Luck": 1  # удача
#         }

#     def get_positive_effects(self):
#         return self.positive_effects.copy()

#     def get_negative_effects(self):
#         return self.negative_effects.copy()

#     def get_stats(self):
#         return self.stats.copy()


# hero = Hero()
# print(hero.get_stats())

# brs1 = Berserk(hero)
# print(brs1.get_stats())
# print(brs1.get_positive_effects())

# bls = Blessing(brs1)
# print(bls.get_stats())
# print(bls.get_positive_effects())
