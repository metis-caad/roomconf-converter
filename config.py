# constants for room type
PARKING = 'PARKING'
BUILDINGSERVICES = 'BUILDINGSERVICES'
EXTERIOR = 'EXTERIOR'
STORAGE = 'STORAGE'
CHILDREN = 'CHILDREN'
TOILET = 'TOILET'
BATH = 'BATH'
CORRIDOR = 'CORRIDOR'
KITCHEN = 'KITCHEN'
WORKING = 'WORKING'
SLEEPING = 'SLEEPING'
LIVING = 'LIVING'
ROOM = 'ROOM'

# constants for edge type
WINDOW = 'WINDOW'
STAIRS = 'STAIRS'
SLAB = 'SLAB'
ENTRANCE = 'ENTRANCE'
WALL = 'WALL'
PASSAGE = 'PASSAGE'
DOOR = 'DOOR'
EDGE = 'EDGE'

# constants for zones
ZONE_SERVICE = 'ZONE_SERVICE'
ZONE_HABITATION = 'ZONE_HABITATION'
ZONE_SLEEPING = 'ZONE_SLEEPING'
ZONE_LIVING = 'ZONE_LIVING'
ZONE_DRY = 'ZONE_DRY'
ZONE_WET = 'ZONE_WET'

room_type_codes = {
    ROOM: 'r',
    LIVING: 'l',
    SLEEPING: 's',
    WORKING: 'w',
    KITCHEN: 'k',
    CORRIDOR: 'c',
    BATH: 'b',
    TOILET: 't',
    CHILDREN: 'h',
    STORAGE: 'g',
    EXTERIOR: 'e',
    BUILDINGSERVICES: 'v',
    PARKING: 'p'
}

room_types = {
    'l': '11',  # living
    's': '12',  # sleeping
    'w': '13',  # working
    'k': '14',  # kitchen
    'c': '15',  # corridor
    'b': '16',  # bath
    't': '17',  # toilet
    'h': '18',  # children
    'g': '19',  # storage
    'r': '21',  # room
    'e': '22',  # exterior
    'v': '23',  # buildingservices
    'p': '24'  # parking
}

room_code_numbers = {
    '11': LIVING,
    '12': SLEEPING,
    '13': WORKING,
    '14': KITCHEN,
    '15': CORRIDOR,
    '16': BATH,
    '17': TOILET,
    '18': CHILDREN,
    '19': STORAGE,
    '22': EXTERIOR,
    '21': ROOM,
    '23': BUILDINGSERVICES,
    '24': PARKING
}

edge_type_codes = {
    EDGE: 'e',
    DOOR: 'd',
    PASSAGE: 'p',
    WALL: 'w',
    ENTRANCE: 'r',
    SLAB: 'b',
    STAIRS: 's',
    WINDOW: 'n'
}

edge_types = {
    'd': '11',  # door
    'p': '12',  # passage
    'w': '13',  # wall
    'r': '14',  # entrance
    'b': '15',  # slab
    's': '16',  # stairs
    'n': '17',  # window
    'e': '21'  # edge
}

edge_code_numbers = {
    '11': DOOR,
    '12': PASSAGE,
    '13': WALL,
    '14': ENTRANCE,
    '15': SLAB,
    '16': STAIRS,
    '17': WINDOW,
    '21': EDGE
}

all_zones = {
    ZONE_WET: [KITCHEN, TOILET, BATH],
    ZONE_DRY: [LIVING, SLEEPING, WORKING, CORRIDOR, CHILDREN],
    ZONE_LIVING: [KITCHEN, LIVING],
    ZONE_SLEEPING: [SLEEPING],
    ZONE_HABITATION: [KITCHEN, LIVING, SLEEPING, EXTERIOR, CHILDREN],
    ZONE_SERVICE: [CORRIDOR, TOILET, BATH, STORAGE, BUILDINGSERVICES, PARKING]
}

all_zones_colors_priority = {
    ZONE_WET: ['0', 4],
    ZONE_DRY: ['1', 3],
    ZONE_LIVING: ['3', 5],
    ZONE_SLEEPING: ['5', 6],
    ZONE_HABITATION: ['7', 1],
    ZONE_SERVICE: ['9', 2]
}
