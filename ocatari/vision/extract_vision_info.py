import sys
from termcolor import colored
from .utils import find_objects, match_objects, match_blinking_objects, find_objects_external_detector
from .skiing import Player, Flag, Tree, Mogul, Score, Clock
# hier alle anderen Gameobjects aus allen anderen files importieren


blinking_categories_per_game = {
        "Amidar": ["Chicken", "Warrior", "Pig", "Shadow"],
        "Bankheist": ["Bank", "Police", "Dynamite"],
        "Frogger": ["Car", "Log", "Alligator", "Turtle", "LadyFrog", "AlligatorHead", "Fly", "HappyFrog", "Snake"],
        "Kangaroo": ["Fruit", "Enenmy"],
        "Spaceinvaders": ["Bullet"],
        "Stargunner": ["FlyingEnemy"]}

# TODO: detector wieder entfernen
def detect_objects_vision(objects, obs, game_name, hud):

    p_module = __name__.split('.')[:-1] + [game_name.lower()]
    game_module = '.'.join(p_module)
    for obj in objects:  # saving the previsous positions
        if obj:
            obj._save_prev()
    try:
        mod = sys.modules[game_module]
        mod._detect_objects
    except KeyError:
        raise NotImplementedError(
            colored(f"Game module does not exist: {game_module}", "red"))
    except AttributeError:
        raise NotImplementedError(
            colored(f"_detect_objects not implemented for game: {game_name}", "red"))

    return mod._detect_objects(objects, obs, hud)
    

# max_objects_per_category format: {'Player': 1, 'Tree': 4, 'Mogul': 3, 'Flag': 4}
def detect_objects_vision_detector(objects, obs, game_name, hud, detector, max_objects_per_category):
    p_module = __name__.split('.')[:-1] + [game_name.lower()]
    game_module = '.'.join(p_module)
    for obj in objects:  # saving the previsous positions
        if obj:
            obj._save_prev()
    try:
        mod = sys.modules[game_module]
        mod._detect_objects
    except KeyError:
        raise NotImplementedError(
            colored(f"Game module does not exist: {game_module}", "red"))
    except AttributeError:
        raise NotImplementedError(
            colored(f"_detect_objects not implemented for game: {game_name}", "red"))
    
    
    # hier beginnen

    # max Anzahl an Objekten pro Klasse holen, für hud true und false
    # self.max_objects_per_cat = get_max_objects(self.game_name, self.hud)
    # core.py Zeile 119 den Call Stack runter übergeben

    # Alle Klassen (GameObjects) aus dem jeweiligen Spiel importieren
    # herausfinden, ob match_blinking_objects oder match_objects
    # dict erstellen und selbst zusammensuchen
    # Objekte, die blinking nutzen, sortiert nach Spielen:
    # - Amidar: Chicken, Warrior, Pig, Shadow
    # - Bankheist: Bank, Police, Dynamite
    # - Frogger: Car, Log, Alligator, Turtle, LadyFrog, AlligatorHead, Fly, HappyFrog, Snake
    # - Kangaroo: Fruit, Enenmy
    # - Spaceinvaders: Bullet
    # - Stargunner: FlyingEnemy

    # print("++++++++++++++++", max_objects_per_category)
    # exit()

    detected_objects = find_objects_external_detector(obs, detector, hud)
    index = 0 # TODO: Reihenfolge herausfinden -> @Philipp: notieren

    for category in max_objects_per_category:

        matching_function = match_blinking_objects if game_name in blinking_categories_per_game and category in blinking_categories_per_game[game_name] else match_objects

        max_objects = max_objects_per_category[category]
        matching_function(
            objects, detected_objects[category][:max_objects], index, max_objects, get_game_object_class(category))

        index += max_objects

    return mod._detect_objects(objects, obs, hud, detector)

def get_game_object_class(category):
    return globals().get(category)

