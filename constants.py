import pygame
from os import path, listdir

# Bildschrimgröße
WIDTH = 480*2
HEIGHT = 320 * 2
FPS = 60

# Pygame initialisieren und Fenster aufmachen
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic-Tac-Toe!")
clock = pygame.time.Clock()

# Konstanten für Art des Spielendes und die Tastenarten
END_GAME = "end game"
START_GAME = "start"
BEFORE_FIRST_GAME = "before first game"
NEXT_GAME = "next game"
UNENDSCHIEDEN = "unendschieden"
MAIN_SETTING = "main settings"
LEFT = "left"
RIGHT = "right"
UP = "up"
DOWN = "down"
PLACE = "place"
ESC = "escape"
ALL = "all"
START = "start"
XY = "xy"

# Standartfarben
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
TEXT_RED = (255, 65, 0)
TEXT_GREEN = (100,150,50)
TEXT_COLOR = (0,0,125)
PLAYER_SELECT = (80,105,190)
PLAYER_COLOR_RED = (255,50,0)
PLAYER_WON_COLOR_RED = (255,100,70)
PLAYER_COLOR_GREEN = (20,240,20)
PLAYER_WON_COLOR_GREEN = (70,200,70)

# finde passendste Schriftart zu arial.
font_name = pygame.font.match_font('arial')

# Lautstärke
game_sound_volume = 0.6


def load_graphics_from_file_array(file_array, dir, color_key=None, convert_aplha=False, as_dict=False):
    # Lädt alle Dateien des file_array's aus dem Pfad dir. Ein leeres file_array bedeutet alle Dateien des Pfades lesen.
    # Wenn color_key gesetzt ist wird dieser hinzugefügt.
    # Bei den Endgegner ist zudem eine alpha convert notwendig. Dazu convert_aplha auf True setzten.
    # Wenn as_dict True ist wird ein Dictionary mit Dateiname und dazu gehöriger Datei zurückgegeben.
    if file_array == []:
        file_array = [f for f in listdir(dir) if path.isfile(path.join(dir, f)) and f != '.DS_Store']

    if as_dict:
        return_images = {}
    else:
        return_images = []

    for img in file_array:
        if convert_aplha:
            loaded_img = pygame.image.load(path.join(dir, img)).convert_alpha()
        else:
            loaded_img = pygame.image.load(path.join(dir, img)).convert()

        if color_key != None:
            loaded_img.set_colorkey(color_key)
        if len(file_array) == 1:
            return loaded_img
        else:
            if as_dict:
                return_images[loaded_img] = img
            else:
                return_images.append(loaded_img)

    return return_images


# Dateipfade herausfinden
# Diese Pythondatei sollte im gleichen Ordner liegen wie der img Ornder mit den Grafiken und der snd Ordner mit den Tönen
img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'snd')

background = load_graphics_from_file_array(["startfield.png"], img_dir)
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
background_rect = background.get_rect()
