import pygame
import time
from joystickpins import JoystickPins, KeyboardStick
from constants import *
from computer_player import *
from sprites import *

class Game():
    def __init__(self):
        self.game_status = START_GAME
        self.running = True
        screen.blit(background, background_rect)

        # Anzahl der Felder in x und y Richtung
        self.spielfeldbreite = 3
        self.spielfeldhoehe = 3
        self.needed_lenght_to_win = 3
        self.with_falling = False

        # Größen von Feldern, Linien und Lücken
        self.rect_size = 0
        self.spielfeldy = 0
        self.spielfeldx = 0
        self.size_between_rects = 6
        self.icon_line_size = 10
        self.set_spielfeldwerte()

        # Kontroller und Multiplayer
        self.multiplayer = False
        self.multi_on_one = False
        self.all_joysticks = []
        self.find_josticks()

        # Spieler, der gerade am Zug ist
        self.current_player = 0
        self.player_colors = [PLAYER_COLOR_RED,PLAYER_COLOR_GREEN]
        self.player_won_colors = [PLAYER_WON_COLOR_RED,PLAYER_WON_COLOR_GREEN]
        self.last_placing = pygame.time.get_ticks()

        # Spielwerte (Gewonnene/verlorerene Spiele, wie vielte Spielrunde, ...)
        self.player0_wins = 0
        self.player1_wins = 0
        self.unentschieden = 0
        self.runde = 1

        # Für Computergegner
        self.go_on_automatically = False
        self.weg = None
        self.r2 = None

    def set_spielfeldwerte(self):
        if self.with_falling:
            self.spielfeldhoehe += 2
        self.rect_size = HEIGHT / self.spielfeldhoehe - self.size_between_rects
        querkant = False
        if (self.rect_size + self.size_between_rects) * self.spielfeldbreite > WIDTH * 5/7:
            querkant = True
            self.rect_size = (WIDTH * 5/7) / self.spielfeldbreite - self.size_between_rects
        if querkant:
            self.spielfeldx = 0
            self.spielfeldy = int((HEIGHT - (self.rect_size * self.spielfeldhoehe)) / 2)
        else:
            self.spielfeldx = int((WIDTH * 5/7 - (self.rect_size * self.spielfeldbreite)) / 2)
            self.spielfeldy = 0
        self.total_spiefeldlbreite = (self.rect_size + self.size_between_rects) * self.spielfeldbreite
        self.total_spiefeldlhoehe = (self.rect_size + self.size_between_rects) * self.spielfeldhoehe
        if self.with_falling:
            self.spielfeldhoehe -= 2
            self.spielfeldy += 2 * (self.rect_size + self.size_between_rects)

    def find_josticks(self):
        # Knöpfe und Kontroller finden und Initialisieren
        self.all_joysticks = [JoystickPins(KeyboardStick())]
        for joy in range(pygame.joystick.get_count()):
            pygame_joystick = pygame.joystick.Joystick(joy)
            pygame_joystick.init()
            my_joystick = JoystickPins(pygame_joystick)
            self.all_joysticks.append(my_joystick)
            print("found_joystick: " + my_joystick.get_name())

    def draw_text(self, surf, text, size, x, y, color=TEXT_COLOR, rect_place="oben_mitte"):
        # Zeichnet den text in der color auf die surf.
        # x und y sind die Koordinaten des Punktes rect_place. rect_place kann "oben_mitte", "oben_links" oder "oben_rechts" sein.
        font = pygame.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if rect_place == "oben_mitte":
            text_rect.midtop = (x, y)
        elif rect_place == "oben_links":
            text_rect.x = x
            text_rect.y = y
        elif rect_place == "oben_rechts":
            text_rect.topright = (x, y)
        elif rect_place == "mitte":
            text_rect.center = (x, y)
        surf.blit(text_surface, text_rect)

    def check_key_pressed(self, check_for=ALL, joystick_num="both"):
        # Überprüft ob die Taste(n) check_for gedrückt ist und achtet dabei auch auf Multi und Singleplayer.
        # Bei Multiplayer kann mit joystick_num zusätzlich mitgegeben werden welcher Kontroller gemeint ist.
        if self.multiplayer:
            if joystick_num == "both":
                for joystick in self.all_joysticks:
                    if check_for == LEFT:
                        if joystick.get_axis_left() or joystick.get_shoulder_left():
                            return True
                    if check_for == RIGHT:
                        if joystick.get_axis_right() or joystick.get_shoulder_right():
                            return True
                    if check_for == UP:
                        if joystick.get_axis_up():
                            return True
                    if check_for == DOWN:
                        if joystick.get_axis_down():
                            return True
                    if check_for == PLACE:
                        if joystick.get_A() or joystick.get_B():
                            return True
                    if check_for == XY:
                        if joystick.get_X() or joystick.get_Y():
                            return True
                    if check_for == X:
                        if joystick.get_X():
                            return True
                    if check_for == ESC:
                        if joystick.get_select() and joystick.get_start():
                            return True
                    if check_for == START:
                        if joystick.get_start():
                            return True
                    if check_for == ALL:
                        if joystick.get_A() or joystick.get_B() or joystick.get_X() or joystick.get_Y() or joystick.get_start() or joystick.get_shoulder_left() or joystick.get_shoulder_right() or joystick.get_axis_left() or joystick.get_axis_right() or joystick.get_axis_up() or joystick.get_axis_down():
                            return True
            else:
                if check_for == LEFT:
                    if self.all_joysticks[joystick_num].get_axis_left() or self.all_joysticks[joystick_num].get_shoulder_left():
                        return True
                if check_for == RIGHT:
                    if self.all_joysticks[joystick_num].get_axis_right() or self.all_joysticks[joystick_num].get_shoulder_right():
                        return True
                if check_for == UP:
                    if self.all_joysticks[joystick_num].get_axis_up():
                        return True
                if check_for == DOWN:
                    if self.all_joysticks[joystick_num].get_axis_down():
                        return True
                if check_for == PLACE:
                    if self.all_joysticks[joystick_num].get_A() or self.all_joysticks[joystick_num].get_B():
                        return True
                if check_for == XY:
                    if self.all_joysticks[joystick_num].get_X() or self.all_joysticks[joystick_num].get_Y():
                        return True
                if check_for == X:
                    if self.all_joysticks[joystick_num].get_X():
                        return True
                if check_for == ESC:
                    if self.all_joysticks[joystick_num].get_select() and self.all_joysticks[joystick_num].get_start():
                        return True
                if check_for == START:
                    if self.all_joysticks[joystick_num].get_start():
                        return True
                if check_for == ALL:
                    if self.all_joysticks[joystick_num].get_A() or self.all_joysticks[joystick_num].get_B() or self.all_joysticks[joystick_num].get_X() or self.all_joysticks[joystick_num].get_Y()\
                        or self.all_joysticks[joystick_num].get_start() or self.all_joysticks[joystick_num].get_shoulder_left() or self.all_joysticks[joystick_num].get_shoulder_right() \
                        or self.all_joysticks[joystick_num].get_axis_left() or self.all_joysticks[joystick_num].get_axis_right() or self.all_joysticks[joystick_num].get_axis_up() \
                        or self.all_joysticks[joystick_num].get_axis_down():
                        return True
        else:
            for joystick in self.all_joysticks:
                if check_for == LEFT:
                    if joystick.get_axis_left() or joystick.get_shoulder_left():
                        return True
                if check_for == RIGHT:
                    if joystick.get_axis_right() or joystick.get_shoulder_right():
                        return True
                if check_for == UP:
                    if joystick.get_axis_up():
                        return True
                if check_for == DOWN:
                    if joystick.get_axis_down():
                        return True
                if check_for == PLACE:
                    if joystick.get_A() or joystick.get_B():
                        return True
                if check_for == XY:
                    if joystick.get_X() or joystick.get_Y():
                        return True
                if check_for == X:
                    if joystick.get_X():
                        return True
                if check_for == ESC:
                    if joystick.get_select() and joystick.get_start():
                        return True
                if check_for == START:
                    if joystick.get_start():
                        return True
                if check_for == ALL:
                    if joystick.get_A() or joystick.get_B() or joystick.get_X() or joystick.get_Y() or joystick.get_start() or joystick.get_shoulder_left() or joystick.get_shoulder_right() or joystick.get_axis_left() or joystick.get_axis_right() or joystick.get_axis_up() or joystick.get_axis_down():
                        return True
        return False

    def wait_for_single_multiplayer_selection(self):
        # Am Anfang, vor dem Spiel, wird zwischen Single und Multiplayer ausgewählt.
        # Links und Rechts wird zum Auswahl ändern benutzt, A oder B zum auswählen. Esc zum Spiel beenden
        self.find_josticks()
        selected = 0
        waiting = True
        last_switch = pygame.time.get_ticks()
        while waiting:
            clock.tick(FPS)
            self.show_on_screen(screen, self.game_status, selected)
            pygame.display.flip()
            # Quit-events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            if self.check_key_pressed(ESC):
                pygame.quit()
            # Auswahl ändern durch hochzählen von selected
            if self.check_key_pressed(LEFT) or self.check_key_pressed(UP):
                if last_switch + 300 < pygame.time.get_ticks():
                    last_switch = pygame.time.get_ticks()
                    selected -= 1
                    if selected < 0:
                        selected = 0
            if self.check_key_pressed(RIGHT) or self.check_key_pressed(DOWN):
                if last_switch + 300 < pygame.time.get_ticks():
                    last_switch = pygame.time.get_ticks()
                    selected += 1
                    if selected > 2:
                        selected = 2
            # Auswahl getroffen
            if self.check_key_pressed(PLACE):
                # Single-palyer
                if selected == 0:
                    # Auswählen welche Kontroller genommen werden soll. Weitere Schritte wie beim Single-player
                    if self.wait_for_joystick_confirm(screen, 1):
                        waiting = False
                        self.end_game = None
                        self.multiplayer = False
                        self.multi_on_one = False
                # Multi-palyer
                elif selected == 1:
                    # Auswählen welcher Kontroller genommen werden soll, wenn Auswahl gepasst hat Spiel starten, sonst nochmals nach Kontrollern suchen und wieder zwischen Multi- und Singelplayer wählen lassen
                    if self.wait_for_joystick_confirm(screen, 2):
                        waiting = False
                        self.end_game = None
                        self.multiplayer = True
                        self.multi_on_one = False
                # Multi-palyer auf einem Kontroller
                elif selected == 2:
                    # Auswählen welche Kontroller genommen werden soll. Weitere Schritte wie beim Single-player
                    if self.wait_for_joystick_confirm(screen, 1):
                        waiting = False
                        self.end_game = None
                        self.multiplayer = True
                        self.multi_on_one = True

    def wait_for_joystick_confirm(self, surf, num_joysticks):
        # Diese Funktion zeigt den Bilschirm an, auf dem die zu benutzenden Kontroller gewählt werden.
        # num_joysticks ist die Anzahl der zu wählenden Joysticks
        # Links und Rechts zum Auswahl ändern. A oder B zum Auswählen
        # X oder Y um zurück zur Multi- / Singleplayer auswahl zu kommen

        # Angeschlossene Kontroller finden
        self.find_josticks()

        # Auswahlbilschrimanzeigen
        self.show_on_screen(surf, None)
        self.draw_text(surf, "Wähle deine Kontroller", 32, WIDTH / 2, HEIGHT / 2.2)
        for controller in self.all_joysticks:
            self.draw_text(surf, controller.get_name(), 28, WIDTH / 2 - 10, HEIGHT / 1.9 + 35 * self.all_joysticks.index(controller), rect_place="oben_rechts")
        pygame.display.flip()
        # warten, um zu verhindern, dass noch versehetlich Tasten auf einem falschem Kontroller gedrückt sind.
        time.sleep(0.5)

        # Auswahl starten
        selected_controllers = []
        selected_controller_num = 0
        last_switch = pygame.time.get_ticks()
        while len(selected_controllers) < num_joysticks:
            clock.tick(FPS)
            # Bildschrimzeichnen
            self.show_on_screen(surf, None)
            self.draw_text(surf, "Wähle deine Kontroller", 32, WIDTH / 2, HEIGHT / 2.2)
            # Jeden gefundenen Kontroller zut Auswahl stellen
            for controller in self.all_joysticks:
                if self.all_joysticks.index(controller) == selected_controller_num:
                    self.draw_text(surf, controller.get_name(), 30, WIDTH / 2 - 10, HEIGHT / 1.9 + 35 * self.all_joysticks.index(controller), rect_place="oben_rechts", color=TEXT_RED)
                else:
                    self.draw_text(surf, controller.get_name(), 28, WIDTH / 2 - 10, HEIGHT / 1.9 + 35 * self.all_joysticks.index(controller), rect_place="oben_rechts")
                if controller in selected_controllers:
                    self.draw_text(surf, "bestätigt", 18, WIDTH / 2 + 10, HEIGHT / 1.9 + 8 + 35 * self.all_joysticks.index(controller), color=TEXT_GREEN, rect_place="oben_links")
                else:
                    self.draw_text(surf, "nicht bestätigt", 18, WIDTH / 2 + 10, HEIGHT / 1.9 + 8 + 35 * self.all_joysticks.index(controller), rect_place="oben_links")
            pygame.display.flip()
            # Quit-events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            if self.check_key_pressed(ESC):
                pygame.quit()
            # Auswahl ändern
            if (self.check_key_pressed(LEFT) or self.check_key_pressed(UP)) and last_switch + 300 < pygame.time.get_ticks():
                last_switch = pygame.time.get_ticks()
                selected_controller_num -= 1
                if selected_controller_num < 0:
                    selected_controller_num = 0
            if (self.check_key_pressed(RIGHT) or self.check_key_pressed(DOWN)) and last_switch + 300 < pygame.time.get_ticks():
                last_switch = pygame.time.get_ticks()
                selected_controller_num += 1
                if selected_controller_num >= len(self.all_joysticks):
                    selected_controller_num = len(self.all_joysticks) - 1
            # Auswahl getroffen
            if self.check_key_pressed(PLACE):
                if self.all_joysticks[selected_controller_num] not in selected_controllers:
                    selected_controllers.append(self.all_joysticks[selected_controller_num])
            # Zurück zur Multi- / Singleplayer auswahl
            if self.check_key_pressed(XY):
                return False
        # Wenn genug Kontroller gewählt wurden stimmt die Auswahl. Es wrid True zurückgegeben
        if len(selected_controllers) == num_joysticks:
            self.all_joysticks = selected_controllers
            return True
        # Wenn die Auswahl nicht stimmt wird False zurückgegeben
        else:
            return False

    def settings(self,surf):
        # Mithilfe dieser Funktion kann der Spieler die Einstellungen, sprich Spielfeldgröße und benötigte Länge zum gewinnen

        # Auswahlbilschrimanzeigen
        self.show_on_screen(surf, MAIN_SETTING)
        pygame.display.flip()
        # warten, um zu verhindern, dass noch versehetlich Tasten auf einem falschem Kontroller gedrückt sind.
        time.sleep(0.5)

        # Auswahl starten
        selected = 0
        last_switch = pygame.time.get_ticks()
        while True:
            clock.tick(FPS)
            # Bildschrimzeichnen
            self.show_on_screen(surf, MAIN_SETTING, selected)
            pygame.display.flip()
            # Quit-events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            if self.check_key_pressed(ESC):
                pygame.quit()
            # Auswahl ändern
            if self.check_key_pressed(UP) and last_switch + 300 < pygame.time.get_ticks():
                last_switch = pygame.time.get_ticks()
                selected -= 1
                if selected < 0:
                    selected = 0
            if self.check_key_pressed(DOWN)and last_switch + 300 < pygame.time.get_ticks():
                last_switch = pygame.time.get_ticks()
                selected += 1
                if self.multiplayer == False and selected > 1:
                    selected = 1
                elif self.multiplayer == True and selected > 5:
                    selected = 5
            # Standart tic -tac-toe mit A/B bzw. Pfeiltaste auswählen
            if self.check_key_pressed(PLACE) and last_switch + 300 < pygame.time.get_ticks():
                last_switch = pygame.time.get_ticks()
                if selected == 0:
                    self.spielfeldbreite = 3
                    self.spielfeldhoehe = 3
                    self.needed_lenght_to_win = 3
                    self.with_falling = False
                elif selected == 1:
                    self.spielfeldbreite = 9
                    self.spielfeldhoehe = 6
                    self.needed_lenght_to_win = 4
                    self.with_falling = True
                elif selected == 5:
                    if self.with_falling:
                        self.with_falling = False
                    else:
                        self.with_falling = True
                self.set_spielfeldwerte()
            if self.check_key_pressed(LEFT) and last_switch + 300 < pygame.time.get_ticks():
                last_switch = pygame.time.get_ticks()
                if selected == 2 and self.spielfeldbreite > 3:
                    self.spielfeldbreite -= 1
                    if self.needed_lenght_to_win > self.spielfeldbreite:
                        self.needed_lenght_to_win = self.spielfeldbreite
                if selected == 3 and self.spielfeldbreite > 3:
                    self.spielfeldhoehe -= 1
                    if self.needed_lenght_to_win > self.spielfeldhoehe:
                        self.needed_lenght_to_win = self.spielfeldhoehe
                if selected == 4 and self.needed_lenght_to_win > 3:
                    self.needed_lenght_to_win -= 1
                if selected == 5:
                    if self.with_falling:
                        self.with_falling = False
                    else:
                        self.with_falling = True
                self.set_spielfeldwerte()
            if self.check_key_pressed(RIGHT) and last_switch + 300 < pygame.time.get_ticks():
                last_switch = pygame.time.get_ticks()
                if selected == 2 and self.spielfeldbreite < 12:
                    self.spielfeldbreite += 1
                if selected == 3 and self.spielfeldhoehe < 12:
                    self.spielfeldhoehe += 1
                if selected == 4 and self.needed_lenght_to_win < 12:
                    self.needed_lenght_to_win += 1
                    if self.spielfeldhoehe < self.needed_lenght_to_win:
                        self.spielfeldhoehe = self.needed_lenght_to_win
                    if self.spielfeldbreite < self.needed_lenght_to_win:
                        self.spielfeldbreite = self.needed_lenght_to_win
                if selected == 5:
                    if self.with_falling:
                        self.with_falling = False
                    else:
                        self.with_falling = True
                self.set_spielfeldwerte()
            if self.check_key_pressed(START):
                return

    def show_on_screen(self, surf, calling_reason, selected=None):
        screen.blit(background, background_rect)

        # Je nach dem ob es um die Kontrollerauswahl oder die Einstellungen geht ein anderen Text zeigen
        texte = []
        if calling_reason == START_GAME:
            texte.append("Single player")
            texte.append("Multi player")
            texte.append("Multiplayer auf einen Kontroller")
        elif calling_reason == MAIN_SETTING:
            texte.append("Standart Tic-tac-toe")
            texte.append("Standart 4 Gewinnt")
            texte.append("Spielfeldbreite: "+str(self.spielfeldbreite))
            texte.append("Spielfeldhöhe: " + str(self.spielfeldhoehe))
            texte.append("Länge zum Gewinnen: "+str(self.needed_lenght_to_win))
            texte.append("Runterfallend: "+{True:"Ja",False:"Nein"}[self.with_falling])

        if calling_reason != MAIN_SETTING:
            höhe = HEIGHT/2
            self.draw_text(surf, "Tic-tac-toe and more!", 32, WIDTH / 2, HEIGHT / 2.8)
        else:
            # Die Einstellungen brauchen mehr Platz, daher kein "Tic-tac-toe and more!" text und dafür weiter oben anfangen
            höhe = HEIGHT/3
        for text_num in range(0,len(texte)):
            if text_num == selected:
                self.draw_text(surf, texte[text_num], 34, WIDTH / 2, höhe + (40*text_num), color=TEXT_RED, rect_place="mitte")
            else:
                if calling_reason == MAIN_SETTING and not self.multiplayer and text_num > 1:
                    self.draw_text(surf, texte[text_num], 20, WIDTH / 2, höhe + (40 * text_num), rect_place="mitte", color=TEXT_GREY)
                else:
                    self.draw_text(surf, texte[text_num], 25, WIDTH / 2, höhe + (40*text_num), rect_place="mitte")

        # Standart Texte
        self.draw_text(surf, "TAM!", 64, WIDTH / 2, HEIGHT / 6.5)
        self.draw_text(surf, "Drücke Start oder Leertaste zum Starten", 18, WIDTH / 2, HEIGHT * 4 / 5)
        self.draw_text(surf, "Drücke Start und Select oder Leertaste und Enter zum Beenden", 18, WIDTH / 2, HEIGHT * 4 / 5 + 23)

        if calling_reason == START_GAME:
            self.draw_text(surf, "A/D oder Joystick zum Auswahl ändern, Pfeiltaste oder A/B zum Auswählen", 20, WIDTH / 2, HEIGHT * 3 / 4)
        if calling_reason == MAIN_SETTING:
            self.draw_text(surf, "W/S oder Joystick zum Auswahl ändern", 20, WIDTH / 2, HEIGHT * 3 / 4 - 25)
            if selected == 0 or selected == 1:
                self.draw_text(surf, "Pfeiltasten oder A/B zum Auswählen", 20, WIDTH / 2, HEIGHT * 3 / 4)
            else:
                self.draw_text(surf, "A/D oder Joystick zum erhöhen oder verringern", 20, WIDTH / 2, HEIGHT * 3 / 4)

    def show_game_info(self, surf, center_x, y):
        self.draw_text(surf,"Spieler {}".format(self.current_player),50,center_x,y,self.player_colors[self.current_player])
        center_y = HEIGHT/2
        self.draw_text(surf,"Runde: {}".format(self.runde),25,center_x,center_y-30)
        self.draw_text(surf, "Spieler1", 30, center_x, center_y +20)
        self.draw_text(surf, "Unendschieden", 30, center_x, center_y + 100)
        self.draw_text(surf, "Spieler2", 30, center_x, center_y + 180)
        self.draw_text(surf, str(self.player0_wins), 30, center_x, center_y + 60)
        self.draw_text(surf, str(self.unentschieden),30, center_x, center_y + 140)
        self.draw_text(surf, str(self.player1_wins), 30, center_x, center_y + 220)

    def show_end_game_info(self, surf, center_x, y):
        if self.game_status == END_GAME:
            self.draw_text(surf, "Spieler "+str(self.current_player), 50, center_x, y, self.player_colors[self.current_player])
            self.draw_text(surf, "gewinnt", 50, center_x, y+50, self.player_colors[self.current_player])
        elif self.game_status == UNENDSCHIEDEN:
            self.draw_text(surf, "Unend-", 50, center_x, y)
            self.draw_text(surf, "schieden", 50, center_x, y+50)
        if not self.game_status == BEFORE_FIRST_GAME:
            self.draw_text(surf, "Start zum Nochmalspielen", 20, center_x, y + 185)
            self.draw_text(surf, "X/Y für Einstellungen", 20, center_x, y + 215)
        else:
            self.draw_text(surf, "Start zum Tic-Tac-Toe spielen", 50, center_x, y + 120)
            self.draw_text(surf, "X/Y oder Pfeiltasten für Einstellungen", 50, center_x, y + 200)
        center_y = HEIGHT / 2
        self.draw_text(surf, "Spieler1", 30, center_x, center_y +20)
        self.draw_text(surf, "Unendschieden", 30, center_x, center_y + 100)
        self.draw_text(surf, "Spieler2", 30, center_x, center_y + 180)
        self.draw_text(surf, str(self.player0_wins), 30, center_x, center_y + 60)
        self.draw_text(surf, str(self.unentschieden), 30, center_x, center_y + 140)
        self.draw_text(surf, str(self.player1_wins), 30, center_x, center_y + 220)

        pygame.display.flip()
        time.sleep(1)

        waiting = True
        while waiting:
            clock.tick(FPS)
            # Quit-events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            # mit Start geht's weiter
            if self.check_key_pressed(START):
                waiting = False
            if self.check_key_pressed(XY):
                self.settings(screen)

        self.game_status = NEXT_GAME

    def get_win_boxes(self,x,y,player_num):
        boxes_in_x_direction = self.get_boxes_in_direction(x, y, 1, 0, player_num) + self.get_boxes_in_direction(x, y, -1, 0, player_num)
        boxes_in_x_direction.append(self.board.get_box(x,y))
        if len(boxes_in_x_direction) >= self.needed_lenght_to_win:
            return boxes_in_x_direction

        boxes_in_y_direction = self.get_boxes_in_direction(x, y, 0, 1, player_num) + self.get_boxes_in_direction(x, y, 0, -1, player_num)
        boxes_in_y_direction.append(self.board.get_box(x, y))
        if len(boxes_in_y_direction) >= self.needed_lenght_to_win:
            return boxes_in_y_direction

        boxes_in_xy_direction = self.get_boxes_in_direction(x, y, 1, 1, player_num) + self.get_boxes_in_direction(x, y, -1, -1, player_num)
        boxes_in_xy_direction.append(self.board.get_box(x, y))
        if len(boxes_in_xy_direction) >= self.needed_lenght_to_win:
            return boxes_in_xy_direction

        boxes_in_yx_direction = self.get_boxes_in_direction(x, y, -1, 1, player_num) + self.get_boxes_in_direction(x, y, 1, -1, player_num)
        boxes_in_yx_direction.append(self.board.get_box(x, y))
        if len(boxes_in_yx_direction) >= self.needed_lenght_to_win:
            return boxes_in_yx_direction

        return False

    def get_boxes_in_direction(self,x,y,x_dazu,y_dazu,player_num):
        return_boxes = []
        if self.board.is_box_in_on_board(x + x_dazu, y + y_dazu):
            box = self.board.get_box(x + x_dazu, y + y_dazu)
            state = box.get_state()
            if state == player_num:
                return_boxes.append(box)
                durchgang_num = 1
                while state == player_num:
                    durchgang_num += 1
                    if self.board.is_box_in_on_board(x + (x_dazu*durchgang_num), y + (y_dazu*durchgang_num)):
                        box = self.board.get_box(x + (x_dazu*durchgang_num), y + (y_dazu*durchgang_num))
                        state = box.get_state()
                        if state == player_num:
                            return_boxes.append(box)
                    else:
                        break
                return return_boxes
            else:
                return []
        else:
            return []

    def make_computer_move(self):
        if self.spielfeldhoehe == 3 and self.spielfeldbreite == 3 and self.needed_lenght_to_win == 3 and self.with_falling == False:
            zu_setzten = make_tic_tac_toe_move(self, self.runde)
            if zu_setzten != False or zu_setzten == 0:
                x = int((zu_setzten-(zu_setzten%self.spielfeldbreite))/self.spielfeldbreite)
                y = int(zu_setzten%self.spielfeldbreite)
                self.board.get_box(x,y).mark_o()
                self.runde += 1
                if self.get_win_boxes(x,y, 1) != False:
                    print("Computer hat gewonnen")
                    self.player1_wins += 1
                    self.current_player_box.kill()
                    self.game_status = END_GAME
                    for x in self.get_win_boxes(x,y, 1):
                        x.mark_as_won()
                else:
                    if self.board.is_completely_full():
                        print("unendschieden")
                        self.unentschieden += 1
                        self.current_player_box.kill()
                        self.game_status = UNENDSCHIEDEN
                    else:
                        self.player = Player(self, player_num=self.current_player)
                        self.all_sprites.add(self.player)
        elif self.spielfeldbreite == 9 and self.spielfeldbreite == 6 and self.needed_lenght_to_win == 4 and self.with_falling == True:
            pass
            # ToDo: 4 gewinnt Computer

    ########## Hier startet das eigentliche Spiel ##########
    def start_game(self):
        # Multiplayerauswahl
        self.wait_for_single_multiplayer_selection()
        self.game_status = BEFORE_FIRST_GAME
        screen.fill(BLACK)
        screen.blit(background, background_rect)
        self.show_end_game_info(screen, WIDTH / 2, 20)
        self.game_status = START_GAME

        # Dauerschleife des Spiels
        while self.running:
            # Ist das Spiel aus irgendeinem Grund zu Ende, ist also game_over nicht None, werden alle Spieler, Gegner und Meteoriten erstellt und das Spiel gestartet
            if self.game_status == NEXT_GAME or self.game_status == START_GAME:
                self.new()

            # Bilschirm leeren
            screen.fill(BLACK)
            screen.blit(background, background_rect)

            # Auf Bildschirmgeschwindigkeit achten
            clock.tick(FPS)

            # Eingaben zum Verlassen des Spiels checken
            if self.check_key_pressed(ESC):
                self.running = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # Alle Spieler, Gegner, Meteoriten, ... updaten. (Ruft die Funktion 'update()' von allen Sprites, die in der Gruppe all_sprites liegen auf)
            self.all_sprites.update()

            self.handle_selection()

            # Mit X Spiel abbrechen
            if self.check_key_pressed(X):
                self.current_player_box.kill()
                self.game_status = UNENDSCHIEDEN

            # Skalen und Texte auf den Bildschirm malen
            self.all_sprites.draw(screen)
            self.draw_display()

            # Nachdem alles gezeichnet ist anzeigen
            pygame.display.flip()

    def new(self):
        self.all_sprites = pygame.sprite.LayeredUpdates()

        self.board = Board(self)
        for box in self.board.boxes:
            self.all_sprites.add(box)

        self.current_player_box = Box(self,  WIDTH - ((WIDTH - (WIDTH*3/4)) / 2) - self.rect_size/2, 80)
        self.all_sprites.add(self.current_player_box)

        if self.multi_on_one:
            self.player = Player(self, player_num=self.current_player, joystick_num=0)
        else:
            self.player = Player(self, player_num=self.current_player)
        self.all_sprites.add(self.player)

        self.game_status = None
        self.running = True

        self.last_placing = pygame.time.get_ticks()

        self.runde = 0

        self.go_on_automatically = False
        self.weg = None
        self.r2 = None

    def handle_selection(self):
        if self.multiplayer and self.last_placing + 800 < pygame.time.get_ticks():
            if self.multi_on_one == False:
                if self.check_key_pressed(PLACE, self.current_player) and self.board.get_box(*self.player.get_pos()).get_state() == None:
                    self.runde += 1
                    placing_sound.play()
                    self.last_placing = pygame.time.get_ticks()
                    self.board.set_box(*self.player.get_pos(), self.current_player)
                    if not self.with_falling:
                        if self.get_win_boxes(*self.player.get_pos(), self.current_player) != False:
                            print("spieler", self.current_player, "hat gewonnen")
                            if self.current_player == 0:
                                self.player0_wins += 1
                            elif self.current_player == 1:
                                self.player1_wins += 1
                            self.player.kill()
                            self.current_player_box.kill()
                            self.game_status = END_GAME
                            for x in self.get_win_boxes(*self.player.get_pos(), self.current_player):
                                x.mark_as_won()
                        else:
                            if self.board.is_completely_full():
                                print("unendschieden")
                                self.unentschieden += 1
                                self.player.kill()
                                self.current_player_box.kill()
                                self.game_status = UNENDSCHIEDEN
                            else:
                                self.current_player += 1
                                if self.current_player > 1:
                                    self.current_player = 0
                                self.player.kill()
                                self.player = Player(self, player_num=self.current_player)
                                self.all_sprites.add(self.player)
                    else:
                        self.player.kill()
            else:
                if self.check_key_pressed(PLACE, 0) and self.board.get_box(*self.player.get_pos()).get_state() == None:
                    self.runde += 1
                    placing_sound.play()
                    self.last_placing = pygame.time.get_ticks()
                    self.board.set_box(*self.player.get_pos(), self.current_player)
                    if not self.with_falling:
                        if self.get_win_boxes(*self.player.get_pos(), self.current_player) != False:
                            print("spieler", self.current_player, "hat gewonnen")
                            if self.current_player == 0:
                                self.player0_wins += 1
                            elif self.current_player == 1:
                                self.player1_wins += 1
                            self.player.kill()
                            self.current_player_box.kill()
                            self.game_status = END_GAME
                            for x in self.get_win_boxes(*self.player.get_pos(), self.current_player):
                                x.mark_as_won()
                        else:
                            if self.board.is_completely_full():
                                print("unendschieden")
                                self.unentschieden += 1
                                self.player.kill()
                                self.current_player_box.kill()
                                self.game_status = UNENDSCHIEDEN
                            else:
                                self.current_player += 1
                                if self.current_player > 1:
                                    self.current_player = 0
                                self.player.kill()
                                self.player = Player(self, player_num=self.current_player, joystick_num=0)
                                self.all_sprites.add(self.player)
                    else:
                        self.player.kill()
        elif self.multiplayer == False and self.last_placing + 800 < pygame.time.get_ticks():
            if self.check_key_pressed(PLACE) and self.board.get_box(*self.player.get_pos()).get_state() == None:
                self.last_placing = pygame.time.get_ticks()
                self.runde += 1
                placing_sound.play()
                self.board.set_box(*self.player.get_pos(), self.current_player)
                if not self.with_falling:
                    if self.get_win_boxes(*self.player.get_pos(), self.current_player) != False:
                        print("spieler", self.current_player, "hat gewonnen")
                        if self.current_player == 0:
                            self.player0_wins += 1
                        elif self.current_player == 1:
                            self.player1_wins += 1
                        self.player.kill()
                        self.current_player_box.kill()
                        self.game_status = END_GAME
                        for x in self.get_win_boxes(*self.player.get_pos(), self.current_player):
                            x.mark_as_won()
                    else:
                        if self.board.is_completely_full():
                            print("unendschieden")
                            self.unentschieden += 1
                            self.player.kill()
                            self.current_player_box.kill()
                            self.game_status = UNENDSCHIEDEN
                        else:
                            self.player.kill()
                            self.make_computer_move()
                else:
                    self.player.kill()

    def draw_display(self):
        # Bildschrim zeichnen

        # Linien zwischen den Feldern zeichnen
        self.board.draw_lines()

        # Rechts Infos zu piel und aktellem Zug
        if self.game_status == END_GAME or self.game_status == UNENDSCHIEDEN:
            self.show_end_game_info(screen, WIDTH - ((WIDTH - (WIDTH*5/7)) / 2), 20)
        else:
            self.show_game_info(screen, WIDTH - ((WIDTH - (WIDTH*5/7)) / 2), 20)

        if self.current_player == 0:
            self.current_player_box.mark_x()
        else:
            self.current_player_box.mark_o()

game = Game()
game.start_game()

pygame.quit()