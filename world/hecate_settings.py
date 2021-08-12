from evennia.utils.search import search_object_by_tag

DEFAULT_STARTING_LOCATION = search_object_by_tag(key="hecates_haven", category="rooms")[0]

DEFAULT_CHARACTER_BASE_HEALTH = 20
DEFAULT_CHARACTER_BASE_ENERGY = 20
