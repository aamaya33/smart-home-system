class SmarthomeAPI:
    def __init__(self):
        self.house_name = ""
        self.floors = {}
        self.rooms = {}
        self.devices = {}
        self.temperature_devices = {}
        self.humidity_devices = {}

    def set_house_name(self, name: str):
        # TODO: Test invalid names
        symbols = "!@#$%^&*()_+{|}:<>?[]\;',./"
        for letter in name: 
            if letter in symbols: 
                raise ValueError("House name cannot contain special characters.")
        self.house_name = name

    def add_floor(self, floor_id: str, floor_name: str):

        if not floor_id:
            raise ValueError("Floor ID cannot be empty.")
        if floor_id in self.floors:
            raise ValueError(f"Floor {floor_id} already exists.")
        
        self.floors[floor_id] = floor_name

    def add_room(self, room_id: str, room_name: str, floor_id: str):
        
        # FIXME: Just add general error message for empty field after testing is done
        if not room_id: 
            raise ValueError("Room ID cannot be empty.")
        elif room_id in self.rooms:
            raise ValueError(f"Room {room_id} already exists.")
        elif not room_name: 
            raise ValueError("Room name cannot be empty.")
        elif not floor_id:
            raise ValueError("Floor ID cannot be empty.")
        
        if floor_id not in self.floors:
            raise ValueError(f"Floor {floor_id} does not exist.")
        self.rooms[room_id] = {
            "name": room_name,
            "floor": floor_id,
            "devices": []
        }

    def add_device(self, device_id: str, device_type: str, status: str = "off", room_id: str = None):

        if not device_id:
            raise ValueError("Device ID cannot be empty.")
        if device_id in self.devices:
            raise ValueError(f"Device {device_id} already exists.")
        
        self.devices[device_id] = {
            "type": device_type,
            "status": status,
            "room_id": room_id
        }
        if room_id:
            if room_id in self.rooms:
                self.rooms[room_id]["devices"].append(device_id)
            else:
                raise ValueError(f"Room {room_id} does not exist.")

    def toggle_device(self, device_id: str):
        if not device_id:
            raise ValueError("Device ID cannot be empty.")
        if device_id in self.devices:
            current_status = self.devices[device_id]["status"]
            new_status = "on" if current_status == "off" else "off"
            self.devices[device_id]["status"] = new_status
        else:
            raise ValueError(f"Device {device_id} not found.")

    def get_status(self):
        return {
            "house_name": self.house_name,
            "floors": self.floors,
            "rooms": self.rooms,
            "devices": self.devices
        }