import random
from .entity import Entity
from .tile   import Tile
from .queue  import queue

class Player(Entity):
    """ Player class controlled by the user. """

    def __init__(self, x=0, y=0):
        super().__init__(x, y, tile=Tile.player, solid=True,
                         tag='player', name='player', color_pair=10)
        self.regeneration = 5

    def attack_move(self, x, y, world):
        """ Moves as normal but also attacks enemy if enemy is in square
            being moved to.
        """
        # TODO: move this code to be entity generic
        # Deal damage if moving into enemy
        entities = world.get_entities_at(x, y)
        for entity in entities:
            if entity.tag == "enemy":
                # Player deals damage
                damage = self.calculate_damage(entity)
                entity.add_health(-damage)
                queue.append("hit {} with {} for {} hp!".format(entity.name,
                    self.get_slot("right hand").name, damage))

                # Entity dies
                if entity.health <= 0:
                    # Prevent entity from attacking on its last turn (i.e. while dead)
                    entity.die()

                    exp = random.randint(15, 250)
                    queue.append("gained {} exp".format(exp))

                    # Check if player has leveled up
                    old_level = self.level()
                    self.exp += exp

                    if self.level() > old_level:
                        self.max_health += 10
                        self.health = self.max_health
                        queue.append("ding! You are now level {}".format(self.level()))

                # New line between each message
                queue.append('\n')
                return

        self.move(x, y, world)

    def update(self, game):
        """ Update the game for the player.

        Movement is done in bindings.py
        """

        game.camera.center_on(self, game.world)

        super().update(game)
