import pytest
from Smart_home_system import SmarthomeAPI

# Use coverage report to see how much of the code is covered

# Have to create fresh instance of class for each test 
@pytest.fixture
def smarthome():
    return SmarthomeAPI()

# Test set_house_name
def test_set_house_name_valid(smarthome):
    smarthome.set_house_name("My House")
    assert smarthome.house_name == "My House"

def test_set_house_name_invalid_symbols(smarthome):
    with pytest.raises(ValueError, match="House name cannot contain special characters."):
        smarthome.set_house_name("My@House")

# Test add_floor
def test_add_floor_valid(smarthome):
    smarthome.add_floor("floor1", "First Floor")
    assert smarthome.floors == {"floor1": "First Floor"}

def test_add_floor_empty_id(smarthome):
    with pytest.raises(ValueError, match="Floor ID cannot be empty."):
        smarthome.add_floor("", "First Floor")

def test_add_floor_duplicate_id(smarthome):
    smarthome.add_floor("floor1", "First Floor")
    with pytest.raises(ValueError, match="Floor floor1 already exists."):
        smarthome.add_floor("floor1", "Second Floor")

# Test add_room
def test_add_room_valid(smarthome):
    smarthome.add_floor("floor1", "First Floor")
    smarthome.add_room("room1", "Living Room", "floor1")
    assert smarthome.rooms == {
        "room1": {
            "name": "Living Room",
            "floor": "floor1",
            "devices": []
        }
    }

def test_add_room_empty_id(smarthome):
    with pytest.raises(ValueError, match="Room ID cannot be empty."):
        smarthome.add_room("", "Living Room", "floor1")

def test_add_room_duplicate_id(smarthome):
    smarthome.add_floor("floor1", "First Floor")
    smarthome.add_room("room1", "Living Room", "floor1")
    with pytest.raises(ValueError, match="Room room1 already exists."):
        smarthome.add_room("room1", "Bedroom", "floor1")

def test_add_room_invalid_floor(smarthome):
    with pytest.raises(ValueError, match="Floor floor1 does not exist."):
        smarthome.add_room("room1", "Living Room", "floor1")

# Test add_device
def test_add_device_valid(smarthome):
    smarthome.add_device("light1", "light")
    assert smarthome.devices == {
        "light1": {
            "type": "light",
            "status": "off",
            "room_id": None
        }
    }

def test_add_device_with_room(smarthome):
    smarthome.add_floor("floor1", "First Floor")
    smarthome.add_room("room1", "Living Room", "floor1")
    smarthome.add_device("light1", "light", room_id="room1")
    assert smarthome.devices == {
        "light1": {
            "type": "light",
            "status": "off",
            "room_id": "room1"
        }
    }
    assert smarthome.rooms["room1"]["devices"] == ["light1"]

def test_add_device_empty_id(smarthome):
    with pytest.raises(ValueError, match="Device ID cannot be empty."):
        smarthome.add_device("", "light")

def test_add_device_duplicate_id(smarthome):
    smarthome.add_device("light1", "light")
    with pytest.raises(ValueError, match="Device light1 already exists."):
        smarthome.add_device("light1", "thermostat")

def test_add_device_invalid_room(smarthome):
    with pytest.raises(ValueError, match="Room room1 does not exist."):
        smarthome.add_device("light1", "light", room_id="room1")

# Test toggle_device
def test_toggle_device_valid(smarthome):
    smarthome.add_device("light1", "light")
    smarthome.toggle_device("light1")
    assert smarthome.devices["light1"]["status"] == "on"
    smarthome.toggle_device("light1")
    assert smarthome.devices["light1"]["status"] == "off"

def test_toggle_device_empty_id(smarthome):
    with pytest.raises(ValueError, match="Device ID cannot be empty."):
        smarthome.toggle_device("")

def test_toggle_device_not_found(smarthome):
    with pytest.raises(ValueError, match="Device light1 not found."):
        smarthome.toggle_device("light1")

# Test get_status
def test_get_status(smarthome):
    smarthome.set_house_name("My House")
    smarthome.add_floor("floor1", "First Floor")
    smarthome.add_room("room1", "Living Room", "floor1")
    smarthome.add_device("light1", "light", room_id="room1")
    status = smarthome.get_status()
    assert status == {
        "house_name": "My House",
        "floors": {"floor1": "First Floor"},
        "rooms": {
            "room1": {
                "name": "Living Room",
                "floor": "floor1",
                "devices": ["light1"]
            }
        },
        "devices": {
            "light1": {
                "type": "light",
                "status": "off",
                "room_id": "room1"
            }
        }
    }
