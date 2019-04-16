import pygame
from constants import *
import random
from itertools import product

class Player(pygame.sprite.Sprite):
    def __init__(self, game, player_num = 0, color = PLAYER_SELECT, joystick_num = None):
        self._layer = 0
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        # Beim Multiplayer die Nummer und Farbe des Spielers
        self.player_num = player_num
        self.color = color
        # Beim Multiplayer mit nur einem Kontroller weichen Spielernummer und Kontrollernummer voneinander ab.
        if joystick_num != None:
            self.joystick_num = joystick_num
        else:
            self.joystick_num = self.player_num
        # Ohne Pause würde man auch bei kurzem drücken der Tasten gleich mehrere Felder verschieben. Daher merkt man sich die letzte verschieb Zeit um dann zu überprüfen, ob seit dem letzten verschieben schon gegnug Zeit vergangen ist
        self.last_move_time = pygame.time.get_ticks()
        # Rechteck
        self.rect_surf = pygame.Surface((self.game.rect_size+self.game.size_between_rects, self.game.rect_size+self.game.size_between_rects))#.convert_alpha()
        self.rect_surf.fill(color)
        #self.rect_surf.set_alpha(50)
        #self.backgournd_image = #ToDo
        self.image = self.rect_surf
        self.rect = self.image.get_rect()
        # Position der Spielers in Feldern
        self.pos = [0,0]
        # check wether this box is already filled
        pos_used = self.game.board.ordered_boxes[self.pos[0]][self.pos[1]].get_state()
        if self.game.with_falling:
            self.pos = [int(self.game.spielfeldbreite/2),0]
        else:
            # go through boxes until found an empty
            while pos_used != None:
                # go one box further in x direction
                self.pos[0] += 1
                # reached out at the end of x direction
                if not self.game.board.is_box_in_on_board(self.pos[0],self.pos[1]):
                    self.pos[0] = 0
                    # go one box further in y direction
                    self.pos[1] += 1
                    # reached end of y direction. No empty bocx found (should not happen when everything is working correctly)
                    if not self.game.board.is_box_in_on_board(self.pos[0],self.pos[1]):
                        self.pos[0] = 0
                        self.pos[1] = 0
                        # break to avoid a endless loop
                        break
                pos_used = self.game.board.ordered_boxes[self.pos[0]][self.pos[1]].get_state()

    def update(self):
        if self.last_move_time < pygame.time.get_ticks() -250:
            self.last_move_time = pygame.time.get_ticks()
            if self.game.check_key_pressed(RIGHT,self.joystick_num) and self.pos[0] < self.game.spielfeldbreite -1:
                self.pos[0] += 1
            if self.game.check_key_pressed(LEFT,self.joystick_num) and self.pos[0] > 0:
                self.pos[0] -= 1
            if not self.game.with_falling:
                if self.game.check_key_pressed(UP, self.joystick_num) and self.pos[1] > 0:
                    self.pos[1] -= 1
                if self.game.check_key_pressed(DOWN, self.joystick_num) and self.pos[1] < self.game.spielfeldhoehe -1:
                    self.pos[1] += 1
        self.rect.x = self.pos[0] * (self.game.rect_size + self.game.size_between_rects) + self.game.spielfeldx
        self.rect.y = self.pos[1] * (self.game.rect_size + self.game.size_between_rects) + self.game.spielfeldy
        if self.game.with_falling:
            self.rect.y -= 2 * (self.game.rect_size + self.game.size_between_rects)

    def get_pos(self):
        return self.pos

class Falling_icon(pygame.sprite.Sprite):
    def __init__(self, game, player_num, x, y):
        self._layer = 0
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        # Beim Multiplayer die Nummer und Farbe des Spielers
        self.player_num = player_num
        # Kreuz bzw. Kreis in das Image malen
        self.image = pygame.Surface((self.game.rect_size + self.game.size_between_rects, self.game.rect_size + self.game.size_between_rects))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.image.fill((0, 0, 0))
        if player_num == 0:
            pygame.draw.line(self.image, self.game.player_colors[0], (1 / 8 * self.game.rect_size, 1 / 8 * self.game.rect_size), (7 / 8 * self.game.rect_size, 7 / 8 * self.game.rect_size),self.game.icon_line_size)
            pygame.draw.line(self.image, self.game.player_colors[0], (1 / 8 * self.game.rect_size, 7 / 8 * self.game.rect_size), (7 / 8 * self.game.rect_size, 1 / 8 * self.game.rect_size),self.game.icon_line_size)
        else:
            radius = (self.game.rect_size / 2) - (self.game.rect_size / 8)
            pygame.draw.circle(self.image, self.game.player_colors[1], (int(self.image.get_width() / 2), int(self.image.get_height() / 2)), int(radius), int(self.game.icon_line_size))
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect.y += 11
        if (int(int(self.rect.y - self.game.spielfeldy) % self.game.rect_size) <= 5 or int(int(self.rect.y - self.game.spielfeldy) % self.game.rect_size) >= self.game.spielfeldhoehe - 5) and int(self.rect.y - self.game.spielfeldy) / int(self.game.rect_size) + 1 >= 0:
            found_place = False
            x_pos_in_feldern = int((self.rect.x - self.game.spielfeldx) / self.game.rect_size)
            y_pos_in_feldern = int(int(self.rect.y - self.game.spielfeldy) / int(self.game.rect_size) + 1)
            if y_pos_in_feldern == self.game.spielfeldhoehe:
                box = self.game.board.get_box(x_pos_in_feldern,y_pos_in_feldern -1)
                self.kill()
                if self.player_num == 0:
                    box.mark_x()
                else:
                    box.mark_o()
                found_place = True
            else:
                box = self.game.board.get_box(x_pos_in_feldern,y_pos_in_feldern)
                if box.get_state() != None:
                    box = self.game.board.get_box(x_pos_in_feldern, y_pos_in_feldern - 1)
                    self.kill()
                    if self.player_num == 0:
                        box.mark_x()
                    else:
                        box.mark_o()
                    found_place = True
            if found_place:
                if self.game.get_win_boxes(x_pos_in_feldern,y_pos_in_feldern-1, self.player_num) != False:
                    print("spieler", self.player_num, "hat gewonnen")
                    if self.player_num == 0:
                        self.game.player0_wins += 1
                    elif self.player_num == 1:
                        self.game.player1_wins += 1
                    self.game.player.kill()
                    self.game.current_player_box.kill()
                    self.game.game_status = END_GAME
                    for x in self.game.get_win_boxes(x_pos_in_feldern,y_pos_in_feldern-1, self.player_num):
                        x.mark_as_won()
                else:
                    if self.game.board.is_completely_full():
                        print("unendschieden")
                        self.game.unentschieden += 1
                        self.game.player.kill()
                        self.game.current_player_box.kill()
                        self.game.game_status = UNENDSCHIEDEN
                    else:
                        if self.game.multiplayer:
                            self.game.current_player = self.player_num + 1
                            if self.game.current_player > 1:
                                self.game.current_player= 0
                        if self.game.multi_on_one:
                            self.game.player = Player(self.game, player_num=self.game.current_player, joystick_num=0)
                        else:
                            self.game.player = Player(self.game, player_num=self.game.current_player)
                        self.game.all_sprites.add(self.game.player)

class Box(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = 1
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pygame.Surface((self.game.rect_size+self.game.size_between_rects, self.game.rect_size+self.game.size_between_rects))
        self.image.set_colorkey(BLACK)
        self.radius = (self.game.rect_size / 2) - (self.game.rect_size / 8)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.state = None

    def mark_x(self):
        self.state = 0
        self.image.fill((0,0,0))
        pygame.draw.line(self.image, self.game.player_colors[0], (1/8 * self.game.rect_size, 1/8 * self.game.rect_size), (7/8 * self.game.rect_size, 7/8 * self.game.rect_size), self.game.icon_line_size)
        pygame.draw.line(self.image, self.game.player_colors[0], (1/8 * self.game.rect_size, 7/8 * self.game.rect_size), (7/8 * self.game.rect_size, 1/8 * self.game.rect_size), self.game.icon_line_size)

    def mark_o(self):
        self.state = 1
        self.image.fill((0, 0, 0))
        pygame.draw.circle(self.image, self.game.player_colors[1], (int(self.image.get_width()/2),int(self.image.get_height()/2)), int(self.radius), int(self.game.icon_line_size))

    def mark_as_won(self):
        self.image.fill(WON_COLOR)
        if self.state == 1:
            pygame.draw.circle(self.image, self.game.player_colors[1], (int(self.image.get_width() / 2), int(self.image.get_height() / 2)), int(self.radius), int(self.game.icon_line_size))
        else:
            pygame.draw.line(self.image, self.game.player_colors[0], (1 / 8 * self.game.rect_size, 1 / 8 * self.game.rect_size), (7 / 8 * self.game.rect_size, 7 / 8 * self.game.rect_size),self.game.icon_line_size)
            pygame.draw.line(self.image, self.game.player_colors[0], (1 / 8 * self.game.rect_size, 7 / 8 * self.game.rect_size), (7 / 8 * self.game.rect_size, 1 / 8 * self.game.rect_size),self.game.icon_line_size)

    def update(self, *args):
        pass

    def get_state(self):
        return self.state

class Board(object):

    def __init__(self, game):
        self.game = game
        self.boxes = []
        self.ordered_boxes = []
        self.initialize_boxes()

    def initialize_boxes(self):
        for x_num in range(0, self.game.spielfeldbreite):
            self.ordered_boxes.append([])
            for y_num in range(self.game.spielfeldhoehe):
                box = Box(self.game, x_num*(self.game.rect_size + self.game.size_between_rects) + self.game.spielfeldx, y_num * (self.game.rect_size + self.game.size_between_rects) + self.game.spielfeldy)
                self.boxes.append(box)
                self.ordered_boxes[x_num].append(box)

    def set_box(self,x,y,player_num):
        box = self.get_box(x,y)
        if box is not None:
            if player_num == 0:
                if self.game.with_falling:
                    falling_box = Falling_icon(self.game,player_num, self.game.spielfeldx + (self.game.rect_size + self.game.size_between_rects) * x, self.game.spielfeldy - 2 * (self.game.rect_size + self.game.size_between_rects))
                    self.game.all_sprites.add(falling_box)
                else:
                    box.mark_x()
            else:
                if self.game.with_falling:
                    falling_box = Falling_icon(self.game,player_num, self.game.spielfeldx + (self.game.rect_size + self.game.size_between_rects) * x, self.game.spielfeldy - 2 * (self.game.rect_size + self.game.size_between_rects))
                    self.game.all_sprites.add(falling_box)
                else:
                    box.mark_o()

    def is_box_in_on_board(self,x,y):
        if x < self.game.spielfeldbreite and x >= 0 and y < self.game.spielfeldhoehe and y >= 0:
            return True
        return False

    def get_box(self,x,y):
        if self.is_box_in_on_board(x,y):
            return self.ordered_boxes[x][y]
        return False

    def draw_lines(self):
        for x in range(0,self.game.spielfeldbreite+1):
            wert = (self.game.rect_size + self.game.size_between_rects) * x + self.game.spielfeldx
            pygame.draw.line(screen, WHITE, (wert, self.game.spielfeldy), (wert, self.game.spielfeldy + self.game.total_spiefeldlhoehe), int(self.game.size_between_rects/2))
        for y in range(0,self.game.spielfeldhoehe + 1):
            wert = (self.game.rect_size + self.game.size_between_rects) * y + self.game.spielfeldy
            pygame.draw.line(screen, WHITE, (self.game.spielfeldx, wert), (self.game.spielfeldx + self.game.total_spiefeldlbreite, wert), int(self.game.size_between_rects/2))

    def is_completely_full(self):
        full = True
        for box in self.boxes:
            if box.get_state() == None:
                full = False
        return full