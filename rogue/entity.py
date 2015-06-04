import random, math
from .tile import Tile
from . import item as _item

class Entity(object):
    """ Base entity class.

    Attributes:
    x -- x position in world space
    y -- y position in world space
    health -- hp left

    tile -- character representing the object
    solid -- whether entity is solid, i.e. whether this space can be moved
             into by other solid entities

    name -- name of the entity
    tag -- tag to use to identify types of entity (e.g. 'enemy' or 'player')

    level -- level of the entity
    attack -- attacking power of entity
    defense -- defensive power of entity

    items -- list of items held by entity
    equipment -- dictionary of equipped items {"slot": Item}
    """

    def __init__(self, x=0, y=0, health=100, tile=Tile.clear,
                 solid=False, tag='', name='entity'):
        self.x = x
        self.y = y
        self.health = health
        self.tile = tile
        self.solid = solid
        self.name = name
        self.tag = tag

        self.level = 10
        self.attack = 10
        self.defense = 6

        self.items = []
        self.equipment = {}

        # Equip fists
        self.equipment[_item.unarmed.slot] = _item.unarmed

    def move(self, x, y, world):
        """ Move to non-wall space x, y, in the world.

        Keyword arguments:
        x -- coordinate to move to along the x axis
        y -- same for the y axis
        world -- the current game World object

        Returns True if moved, False otherwise
        """

        # Non-solid entities can move anywhere!
        if not self.solid:
            self.x = x
            self.y = y
            return True

        if world.is_wall(x, y):
            return False

        # Don't allow movement into solid entity
        entity = world.get_entity_at(x, y)
        if entity is not None and entity.solid:
            return False

        self.x = x
        self.y = y
        return True

    def random_floor_tile(self, world):
        """ Place the entity on a random floor tile in the world. """
        p = world.random_floor_tile()
        self.x = p.x
        self.y = p.y

    def update(self, game, key):
        """ Update the entity.

        Keyword arguments:
        game -- current Game object representing game state
        key -- key pressed this frame
        """
        if self.health <= 0:
            game.world.remove_entity(self)

    def calculate_damage(self, entity):
        """ Calculate attack damage done to other entity, using
            FF's algorithm.
        """
        weapon_damage = self.get_slot("right hand").stats["attack"]
        attacker = self.attack / 2 + weapon_damage
        defender = entity.defense
        return math.floor(((random.random() + 1) * attacker) - defender)


    def add_item(self, item):
        """ Add item to the entity's inventory. """
        if item == _item.unarmed:
            raise ValueError("Cannot add fists to inventory")
        self.items.append(item)

    def remove_item(self, item):
        """ Remove item from the entity's inventory. """
        self.items.remove(item)

    def equip(self, item):
        """ Equip non-fist item into slot given by item.slot
        
        Also adds (not unarmed) item if not already in inventory.

        Raises ValueError if the item isn't an equipment, or
        if item == unarmed tries to be equipped
        """
        if item == _item.unarmed:
            raise ValueError("Cannot equip fists")
        if not item.equippable:
            raise ValueError("Item not equippable")
        if item not in self.items:
            self.add_item(item)

        self.equipment[item.slot] = item

    def unequip(self, item):
        """ Unequip given item. """
        if item == _item.unarmed:
            raise ValueError("Cannot unequip fists")

        if item.slot in self.equipment:
            del self.equipment[item.slot]

        # Rest to fists
        self.equipment[item.slot] = _item.unarmed

    def get_slot(self, slot):
        """ Get equipment from given slot.
        
        Returns None if nothing equipped in slot.
        """
        return self.equipment.get(slot, None)

    def get_loot(self):
        """ Get random sublist of entities items. """
        if len(self.items) == 1:
            num_loot = 1
        else:
            num_loot = random.randint(1, 2)

        return random.sample(self.items, num_loot)

    def __str__(self):
        return self.tile

