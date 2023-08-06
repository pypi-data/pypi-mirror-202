from abc import ABCMeta,abstractmethod
from gameuniterror import GameUnitError
from gameutils import *

class AbstractGameUnit(metaclass=ABCMeta):
    """An abstract obj to create virous game unit"""
    def __init__(self,name=''):
        self.max_hp = 0
        self.health_meter = 0
        self.name = name
        self.enemy = None
        self.unit_type = None

    @abstractmethod
    def info():
        """info on the unit.muse be overriden in subclass"""
        pass

    def attack(self,enemy):
        """main logic to determine the injured unit and amount of injury"""
        injured_unit = weighted_random_selection(self, enemy)
        injury = random.randint(10, 15)
        injured_unit.health_meter = max(injured_unit.health_meter - injury, 0)
        print("ATTACK! ", end='')
        self.show_health(end='  ')
        enemy.show_health(end='  ')

    def show_health(self, bold=False, end='\n'):
        """Show the remaining hit points of the player and the enemy"""
        # TODO: what if there is no enemy?
        msg = "Health: %s: %d" % (self.name, self.health_meter)

        if bold:
            print_bold(msg, end=end)
        else:
            print(msg, end=end)

    def heal(self, heal_by=2, full_healing=True):
        """Heal the unit replenishing all the hit points"""
        if self.health_meter == self.max_hp:
            return

        if full_healing:
            self.health_meter = self.max_hp
        else:
            # TODO: Do you see a bug here? it can exceed max hit points!
            self.health_meter += heal_by

        if self.health_meter > self.max_hp:
            raise GameUnitError("health_meter > max_hp!",101)


        print_bold("You are HEALED!", end=' ')
        self.show_health(bold=True)

    def reset_health_meter(self):
        """Reset the `health_meter` (assign default hit points)"""
        self.health_meter = self.max_hp
