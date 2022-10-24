from random import randint
from lair_rpg.equipment import Equipment

class Character():
    def __init__(self, base_health, base_attack) -> None:

        self.base_health = base_health
        self.base_attack = base_attack

        self.current_health = self.base_health

        self.equipment = {
            'head': None,
            'shouler': None,
            'chest': None,
            'hand': None,
            'waist': None,
            'legs': None,
            'feet': None,
            'weapon': None            
        }

    def take_damage(self, damage):
        self.current_health -= damage

    def get_is_dead(self):
        if self.current_health <= 0:
            return True
        else:
            return False

    def set_initial_equipment(self):
        if randint(1,100) > 50:
            self.equipment['head'] = Equipment('head')
        if randint(1,100) > 50:
            self.equipment['shoulder'] = Equipment('shoulder')
        if randint(1,100) > 50:
            self.equipment['chest'] = Equipment('chest')
        if randint(1,100) > 50:
            self.equipment['hand'] = Equipment('hand')
        if randint(1,100) > 50:
            self.equipment['waist'] = Equipment('waist')
        if randint(1,100) > 50:
            self.equipment['legs'] = Equipment('feet')
        if randint(1,100) > 50:
            self.equipment['feet'] = Equipment('feet')
        if randint(1,100) > 50:
            self.equipment['weapon'] = Equipment('weapon')
