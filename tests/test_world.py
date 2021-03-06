import pytest
from rogue.world import World
from rogue.tile import Tile
from rogue.entity import Entity
import rogue.room as room

@pytest.fixture
def world():
    return World(width=100, height=100)

@pytest.fixture
def entity():
    return Entity(0, 0, Tile.player)

def test_world_initialize(world):
    assert world.width == 100
    assert world.height == 100

def test_setting_then_getting_tile(world):
    world.set_tile(10, 10, Tile.up)
    assert world.get_tile(10, 10) == Tile.up

def test_checking_if_tile_is_wall(world):
    assert not world.is_wall(10, 10)
    world.set_tile(10, 10, Tile.wall)
    assert world.is_wall(10, 10)

def test_getting_out_of_range_tile(world):
    with pytest.raises(IndexError):
        world.get_tile(-10, -10)
        world.get_tile(1000, 1000)

def test_empty_tiles_correct_dimensions(world):
    tiles = world.Empty_Tiles(width=10, height=12, tile=Tile.floor)
    assert len(tiles) == 10 * 12
    assert tiles[(0, 0)] == Tile.floor

def test_random_floor_tile(world):
    world.set_tile(10, 12, Tile.floor)
    p = world.random_floor_tile()
    assert p.x == 10
    assert p.y == 12

def test_random_floor_tile_empty_world(world):
    with pytest.raises(ValueError):
        world.random_floor_tile()

def test_random_floor_tile_occupied_space(world, entity):
    entity.x = 10
    entity.y = 12
    world.add_entity(entity)
    world.set_tile(10, 12, Tile.floor)
    world.set_tile(11, 12, Tile.floor)

    # Should choose tile (11, 12), the only unoccupied option
    p = world.random_floor_tile()
    assert p.x == 11
    assert p.y == 12

    # Should raise exception if only occupied space available
    world.set_tile(11, 12, Tile.wall)
    with pytest.raises(ValueError):
        world.random_floor_tile()

def test_added_entity_becomes_added(world, entity):
    world.add_entity(entity)
    assert entity in world.entities

def test_getting_entity(world, entity):
    entity.x = 20
    entity.y = 24
    world.add_entity(entity)
    entity2 = Entity(x=20, y=24)
    world.add_entity(entity2)
    assert entity is world.get_entity_at(20, 24)

def test_getting_multiple_entities(world, entity):
    entity.x = 20
    entity.y = 24
    world.add_entity(entity)
    entity2 = Entity(x=20, y=24)
    world.add_entity(entity2)
    assert entity is world.get_entities_at(20, 24)[0]
    assert entity2 is world.get_entities_at(20, 24)[1]

def test_getting_entities_surrounding(world, entity):
    entity.x = 20
    entity.y = 24
    world.add_entity(entity)
    entity2 = Entity(x=20, y=25)
    world.add_entity(entity2)
    entity3 = Entity(x=21, y=25)
    world.add_entity(entity3)
    entity4 = Entity(x=50, y=50)
    world.add_entity(entity4)

    entities = world.get_entities_surrounding(21, 24)
    assert entity in entities
    assert entity2 in entities
    assert entity3 in entities
    assert entity4 not in entities

def test_get_tiles_surrounding(world):
    world.set_tile(0, 1, Tile.floor)
    world.set_tile(0, 2, Tile.floor)
    world.set_tile(1, 2, Tile.wall)
    res = world.get_tiles_surrounding(1, 1).values()
    assert Tile.wall in res
    assert Tile.floor in res

def test_adding_rectangular_room(world):
    world.add_room(10, 10, room.rect_room(width=10, height=12))
    assert world.get_tile(10, 10) == Tile.wall
    assert world.get_tile(11, 11) == Tile.floor

""" Removed test as it takes too long to generate dungeon world
def test_dungeon_world_has_floor_tiles(dungeon):
    dungeon.random_floor_tile()
"""
