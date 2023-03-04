import pygame
pygame.init()
import os
from random import randint

os.environ["SDL_VIDEO_CENTERED"] = "1"
pygame.mouse.set_visible(False)

WIN_WIDTH = 900
WIN_HEIGHT = 600
FPS = 60
WHITE = (255,255,255)

def file_path(file_name):
    folder = os.path.abspath(__file__ + "/..")
    path = os.path.join(folder, file_name)
    return path

window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
clock = pygame.time.Clock()

pygame.mixer.music.load(file_path(r"sounds\sound_fon.mp3"))
pygame.mixer.music.set_volume(1)
pygame.mixer.music.play(-1)

music_shot = pygame.mixer.Sound(file_path(r"sounds\shot.ogg"))
music_shot_out = pygame.mixer.Sound(file_path(r"sounds\shot_out.ogg"))

fon = pygame.image.load(file_path(r"images\Stall\bg_green.png"))
fon = pygame.transform.scale(fon, (WIN_WIDTH, WIN_HEIGHT)).convert()

class Scope():
    def __init__(self):
        self.rect = pygame.Rect(0,0,40,40)
        self.image = pygame.image.load(file_path(r"images\HUD\crosshair_outline_large.png"))
        self.image = pygame.transform.scale(self.image,(40, 40)).convert_alpha()

    def show(self):
        self.rect.center = mouse_pos
        window.blit(self.image, (self.rect.x, self.rect.y))
        
scope = Scope()

class Target(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load(file_path(r"images\Objects\target_red1.png"))
        self.image = pygame.transform.scale(self.image,(120, 120)).convert_alpha()
        self.rect = self.image.get_rect(center=(x,y))



class Video_game():
    def __init__(self):
        self.level = 1
        self.font35  = pygame.font.SysFont("arial", 35)
        self.txt_username = self.font35.render("Введить имя:",True,WHITE)
        self.user_name = ""

        self.txt_btn_go = pygame.image.load(file_path(r"images\HUD\text_go.png"))
        self.rect_btn_go = self.txt_btn_go.get_rect(topleft = (370, 310))

        # level = 2

        self.txt_time = self.font35.render("Time", True, WHITE)
        self.txt_score = self.font35.render("Score", True, WHITE)
        
        self.target_group = pygame.sprite.Group()
        

    def to_level_2(self):
        self.txt_player_name = self.font35.render(self.user_name, True,WHITE)
        self.rect_player_name = self.txt_player_name.get_rect(midtop = (WIN_WIDTH//2, 30))

        self.score = 0
        self.time_show = 10

        self.target_group.empty()

        self.start_time = pygame.time.get_ticks()

        self.level = 2
    
    def time_go(self):
        self.time_new = pygame.time.get_ticks()
        if (self.time_new - self.start_time) / 1000 >= 1:
            self.time_show -= 1
            self.start_time = self.time_new

    def create_target(self):
        if len(self.target_group.sprites()) < 5:
            target = Target(randint(60, WIN_WIDTH - 60), randint(160, WIN_HEIGHT - 60))
            self.target_group.add(target)

    def update(self):
        if self.level == 1:
            window.blit(self.txt_username,(180,200))
            self.txt_name = self.font35.render(self.user_name, True, WHITE)
            window.blit(self.txt_name,(410,200))
            if len(self.user_name)>= 3:
                window.blit(self.txt_btn_go,(self.rect_btn_go.x, self.rect_btn_go.y))
        elif self.level == 2:
            window.blit(self.txt_player_name,(self.rect_player_name.x, self.rect_player_name.y))
            window.blit(self.txt_time, (700, 30))
            window.blit(self.txt_score, (80, 30))

            self.time_numder = self.font35.render(str(self.time_show), True, WHITE)
            window.blit(self.time_numder, (790, 30))

            self.score_numder = self.font35.render(str(self.score), True, WHITE)
            window.blit(self.score_numder,(190, 30))

            self.create_target()
            self.target_group.draw(window)

            self.time_go()

videogame = Video_game()

play = True
game = True

while game:
    mouse_pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        if videogame.level == 1:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    videogame.user_name = videogame.user_name[0:-1]
                elif event.key == pygame.K_RETURN:
                    if len(videogame.user_name) >= 3:
                        videogame.to_level_2()   
                else:
                    if len(videogame.user_name) <= 15:
                        videogame.user_name += event.unicode
            if event.type == pygame.MOUSEBUTTONDOWN:
                if videogame.rect_btn_go.collidepoint(mouse_pos):
                    if len(videogame.user_name)>= 3:
                        videogame.to_level_2()

        elif videogame.level == 2:
            if event.type == pygame.MOUSEBUTTONDOWN:
                for target in videogame.target_group.sprites()[::-1]:
                    if target.rect.collidepoint(mouse_pos):
                        target.kill()
                        videogame.score += 1
                        music_shot.play()
                        break

                
    
    if play:
        window.blit(fon,(0,0))

    videogame.update()
    
    scope.show()



    clock.tick(FPS)
    pygame.display.update() 