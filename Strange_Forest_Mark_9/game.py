import os
import random
import math
import pygame
from os import listdir
from os.path import isfile, join
import sys
import subprocess

pygame.init()
pygame.mixer.init()

# 화면 설정
WIDTH, HEIGHT = 1280, 720
FPS = 120
PLAYER_VEL = 5
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Main Menu")

# 코인 설정
coin = 0

# 색 설정
black = (0, 0, 0)
white = (255, 255, 255)

clock = pygame.time.Clock()

# 사운드 설정
click_sound_volume = 50
BGM_sound_volume = 50

click_volume = pygame.mixer.Sound('sound/button_click.wav')
click_volume.set_volume(click_sound_volume / 100.0)

BGM_sound = pygame.mixer.Sound('sound/mainmenu_bgm.wav')
BGM_sound.set_volume(BGM_sound_volume / 100.0)
BGM_channel = pygame.mixer.Channel(0)

BGM_channel.play(BGM_sound)
BGM_channel.play(BGM_sound, loops=-1)

# 글씨 설정
font1_path = os.path.join(os.path.dirname(__file__), 'font/PixeloidSans.ttf')
font2_path = os.path.join(os.path.dirname(__file__), 'font/Sam3KRFont.ttf')
font1 = pygame.font.Font(font1_path, 36)
font2 = pygame.font.Font(font2_path, 36)
font3 = pygame.font.Font(font2_path, 36)

# 텍스트 설정
start_text = font1.render("START", True, black)
setting_text = font1.render("SETTING", True, black)
credit_text = font1.render("CREDIT", True, black)
quit_text = font1.render("QUIT", True, black)

BGM_volume_text = font1.render("BGM VOLUME", True, black)
click_volume_text = font1.render("Click VOLUME", True, black)
BGM_volume_up_text = font1.render(">", True, black)
BGM_volume_down_text = font1.render("<", True, black)
click_volume_up_text = font1.render(">", True, black)
click_volume_down_text = font1.render("<", True, black)

back_text = font1.render("BACK", True, black)

continue_text = font1.render("CONTINUE", True, black)
shop_text = font1.render("SHOP", True, black)

buy_text = font1.render("BUY", True, black)

# 글씨 위치 설정
start_rect = start_text.get_rect(center=(WIDTH // 2, 300))
setting_rect = setting_text.get_rect(center=(WIDTH // 2, 400))
credit_rect = credit_text.get_rect(center=(WIDTH // 2, 500))
quit_rect = quit_text.get_rect(center=(WIDTH // 2, 600))

BGM_volume_rect = BGM_volume_text.get_rect(center=(WIDTH // 2, 200))
click_volume_rect = click_volume_text.get_rect(center=(WIDTH // 2, 350))
BGM_volume_up_rect = BGM_volume_up_text.get_rect(center=(WIDTH // 2 + 50, 260))
BGM_volume_down_rect = BGM_volume_down_text.get_rect(center=(WIDTH // 2 - 50, 260))
click_volume_up_rect = click_volume_up_text.get_rect(center=(WIDTH // 2 + 50, 410))
click_volume_down_rect = click_volume_down_text.get_rect(center=(WIDTH // 2 - 50, 410))

back_rect = back_text.get_rect(center=(80, 50))

continue_rect = continue_text.get_rect(center=(WIDTH // 2, 200))
shop_rect = shop_text.get_rect(center=(WIDTH // 2, 300))
setting2_rect = setting_text.get_rect(center=(WIDTH // 2, 400))
back2_rect = back_text.get_rect(center=(WIDTH // 2, 500))

buy_rect = buy_text.get_rect(center=(WIDTH // 2, 400))

# CREDIT 내용 설정
credit_contents = """      제작자  202304032김영민 202004026김용범 202304126장선웅"""
credit_surface = font2.render(credit_contents, True, black)
credit_rect2 = credit_surface.get_rect(center=(WIDTH // 2, 30))

# 화면 설정 값
main_menu = True
setting_screen = False
menu_screen = False
credit_screen = False
shop_screen = False
stage_1_active = False
stage_2_active = False

previous_screen = None
previous_previous_screen = None

# 이전 장면 설정 함수(자체 제작)
def set_previous_screen():
    global previous_screen, previous_previous_screen
    previous_previous_screen = previous_screen
    previous_screen = None

# 이미지 좌우 전환 함수(Youtube 인용)
def flip(sprites):
    return [pygame.transform.flip(sprite, True, False) for sprite in sprites]

# 이미지 스프라이트 불러오는 함수(Youtube 인용)
def load_sprite_sheets(dir1, dir2, width, height, direction=False):
    path = join("image", dir1, dir2)
    images = [f for f in listdir(path) if isfile(join(path, f))]

    all_sprites = {}

    for image in images:
        sprite_sheet = pygame.image.load(join(path, image)).convert_alpha()

        sprites = []
        for i in range(sprite_sheet.get_width() // width):
            surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
            rect = pygame.Rect(i * width, 0, width, height)
            surface.blit(sprite_sheet, (0, 0), rect)
            sprites.append(pygame.transform.scale2x(surface))

        if direction:
            all_sprites[image.replace(".png", "") + "_right"] = sprites
            all_sprites[image.replace(".png", "") + "_left"] = flip(sprites)
        else:
            all_sprites[image.replace(".png", "")] = sprites

    return all_sprites

# 텍스트 그리는 함수(자체 제작)
def draw_text(surface, text, font2, color, rect, word_width):
    words = text.split(' ')
    y = rect.y

    for word in words:
        word_width, word_height = font2.size(word)
        text_surface = font2.render(word, True, color)
        text_rect = text_surface.get_rect(center=(rect.centerx, y))
        surface.blit(text_surface, text_rect)
        y += word_height

# 배경 가져오는 함수(Youtube 인용)
def get_background(name):
    image = pygame.image.load(join("image", "Background", name))
    width, height = image.get_rect().size
    tiles = []

    for i in range(WIDTH // width + 1):
        for j in range(HEIGHT // height + 1):
            pos = (i * width, j * height)
            tiles.append(pos)

    return tiles, image

#게임 메뉴 불러오기(자체 제작)
def show_game_menu(window):
    global stage_1_active, main_menu, click_sound_volume, BGM_sound_volume, stage_2_active, previous_screen, coin, game_clear, shop_screen
    game_menu = True
    shop_screen = False
    setting_screen = False

    previous_screen = None

    game_clear = False
    game_clear_text = font3.render("GAME CLEAR", True, black)
    game_clear_text_2 = font3.render("x 키를 누르면 종료됩니다", True, black)
    
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    pygame.quit()
                    sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                if game_menu:
                    if continue_rect.collidepoint(mouse_x, mouse_y):
                        game_menu = False
                        run = False
                        click_volume.play()
                        print("게임이 이어집니다")
                    elif shop_rect.collidepoint(mouse_x, mouse_y):
                        click_volume.play()
                        game_menu = False
                        shop_screen = True
                        print("상점이 열립니다.")
                    elif setting_rect.collidepoint(mouse_x, mouse_y):
                        game_menu = False
                        setting_screen = True
                        click_volume.play()
                        previous_screen = "game_menu"
                        print("SETTING 버튼이 클릭되었습니다.")
                    elif back2_rect.collidepoint(mouse_x, mouse_y):
                        game_menu = False
                        stage_1_active = False
                        stage_2_active = False
                        main_menu = True
                        run = False
                        click_volume.play()
                        print("나가기 버튼이 클릭되었습니다.")

                elif setting_screen:
                    if click_volume_up_rect.collidepoint(mouse_x, mouse_y):
                        click_sound_volume = min(100, click_sound_volume + 5)
                        click_volume.set_volume(click_sound_volume / 100.0)
                    elif click_volume_down_rect.collidepoint(mouse_x, mouse_y):
                        click_sound_volume = max(0, click_sound_volume - 5)
                        click_volume.set_volume(click_sound_volume / 100.0)
                    elif BGM_volume_up_rect.collidepoint(mouse_x, mouse_y):
                        BGM_sound_volume = min(100, BGM_sound_volume + 5)
                        BGM_sound.set_volume(BGM_sound_volume / 100.0)
                    elif BGM_volume_down_rect.collidepoint(mouse_x, mouse_y):
                        BGM_sound_volume = max(0, BGM_sound_volume - 5)
                        BGM_sound.set_volume(BGM_sound_volume / 100.0)
                    elif back_rect.collidepoint(mouse_x, mouse_y):
                        setting_screen = False
                        game_menu = True
                        click_volume.play()
                        print("Back 버튼이 클릭되었습니다.")
                
                elif shop_screen:
                    if buy_rect.collidepoint(mouse_x, mouse_y):
                        if coin >= 25:
                            click_volume.play()
                           
                            if stage_1_active:          # 스테이지 1인 경우
                                stage_1_active = False
                                stage_2_active = True
                                coin = 0
                                print("Stage 1 Clear")     
                            
                            elif stage_2_active:        # 스테이지 2인 경우
                                print("Stage 2 Clear")
                                game_clear = True
                            
                            if game_clear:      # 게임 클리어 여부에 따라 다른 동작 수행
                                print("Clear")
                            
                            print("Buy 버튼이 클릭되었습니다.")

                    elif back_rect.collidepoint(mouse_x, mouse_y):
                        shop_screen = False
                        game_menu = True
                        click_volume.play()
                        print("Back 버튼이 클릭되었습니다.")

        if game_menu:
            bg_tiles, bg_image = get_background('game_background_2.png')
            for tile in bg_tiles:
                window.blit(bg_image, tile)
            window.blit(bg_image, (0, 0))
            window.blit(continue_text, continue_rect)
            window.blit(shop_text, shop_rect)
            window.blit(setting_text, setting2_rect)
            window.blit(back_text, back2_rect)

        elif setting_screen:
            bg_tiles, bg_image = get_background('game_background_2.png')
            for tile in bg_tiles:
                window.blit(bg_image, tile)
            window.blit(bg_image, (0, 0))

            # 클릭 소리 볼륨 표시
            window.blit(click_volume_text, click_volume_rect)
            window.blit(click_volume_up_text, click_volume_up_rect)
            window.blit(click_volume_down_text, click_volume_down_rect)

            click_volume_value_text = font1.render(f"{click_sound_volume}", True, black)

            offset_x = 11 if click_sound_volume >= 100 else 0   # 볼륨 최대 100
            offset2_x = 11 if click_sound_volume < 10 else 0   # 볼륨 최저 0

            window.blit(click_volume_value_text, (WIDTH // 2 - 20 - offset_x + offset2_x, 390))

            # 배경 음악 볼륨 표시
            window.blit(BGM_volume_text, BGM_volume_rect)
            window.blit(BGM_volume_up_text, BGM_volume_up_rect)
            window.blit(BGM_volume_down_text, BGM_volume_down_rect)

            BGM_volume_value_text = font1.render(f"{BGM_sound_volume}", True, black)

            offset_x = 11 if BGM_sound_volume >= 100 else 0   # 볼륨 최대 100
            offset2_x = 11 if BGM_sound_volume < 10 else 0   # 볼륨 최저 0

            window.blit(BGM_volume_value_text,
                        (WIDTH // 2 - 20 - offset_x + offset2_x, 240))

            window.blit(back_text, back_rect)

        elif shop_screen:
            bg_tiles, bg_image = get_background('shop_background.png')
            for tile in bg_tiles:
                window.blit(bg_image, tile)
            window.blit(bg_image, (0, 0))
            window.blit(buy_text, buy_rect)
            window.blit(back_text, back_rect)
            if game_clear:
                window.fill(white)
                text_rect_1 = game_clear_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                text_rect_2 = game_clear_text_2.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))
                window.blit(game_clear_text, text_rect_1)
                window.blit(game_clear_text_2, text_rect_2)
                pygame.display.flip()
        
        pygame.display.flip()
        clock.tick(FPS)

# 메인 메뉴 불러오기(자체 제작)
def show_main_menu(window):
    global main_menu, credit_screen, setting_screen, stage_1_active, previous_screen, previous_previous_screen, click_sound_volume, BGM_sound_volume
    credit_screen = False
    setting_screen = False
    main_menu = True

    previous_screen = None
    previous_previous_screen = None

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                if main_menu:
                    if start_rect.collidepoint(mouse_x, mouse_y):
                        main_menu = False
                        stage_1_active = True
                        click_volume.play()
                        print("게임이 시작됩니다.")
                    elif credit_rect.collidepoint(mouse_x, mouse_y):
                        main_menu = False
                        credit_screen = True
                        click_volume.play()
                        print("CREDIT 버튼이 클릭되었습니다.")
                    elif setting_rect.collidepoint(mouse_x, mouse_y):
                        main_menu = False
                        setting_screen = True
                        click_volume.play()
                        print("SETTING 버튼이 클릭되었습니다.")
                    elif quit_rect.collidepoint(mouse_x, mouse_y):
                        click_volume.play()
                        pygame.quit()
                        quit()

                elif credit_screen:
                    if back_rect.collidepoint(mouse_x, mouse_y):
                        credit_screen = False
                        main_menu = True
                        click_volume.play()
                        print("Back 버튼이 클릭되었습니다.")

                elif setting_screen:
                    if click_volume_up_rect.collidepoint(mouse_x, mouse_y):
                        click_sound_volume = min(100, click_sound_volume + 5)
                        click_volume.set_volume(click_sound_volume / 100.0)
                    elif click_volume_down_rect.collidepoint(mouse_x, mouse_y):
                        click_sound_volume = max(0, click_sound_volume - 5)
                        click_volume.set_volume(click_sound_volume / 100.0)
                    elif BGM_volume_up_rect.collidepoint(mouse_x, mouse_y):
                        BGM_sound_volume = min(100, BGM_sound_volume + 5)
                        BGM_sound.set_volume(BGM_sound_volume / 100.0)
                    elif BGM_volume_down_rect.collidepoint(mouse_x, mouse_y):
                        BGM_sound_volume = max(0, BGM_sound_volume - 5)
                        BGM_sound.set_volume(BGM_sound_volume / 100.0)
                    elif back_rect.collidepoint(mouse_x, mouse_y):
                        setting_screen = False
                        main_menu = True
                        click_volume.play()
                        print("Back 버튼이 클릭되었습니다.")

        if main_menu:
            bg_tiles, bg_image = get_background('main_background.png')
            for tile in bg_tiles:
                window.blit(bg_image, tile)
            window.blit(start_text, start_rect)
            window.blit(setting_text, setting_rect)
            window.blit(credit_text, credit_rect)
            window.blit(quit_text, quit_rect)

        elif credit_screen:
            bg_tiles, bg_image = get_background('game_background_2.png')
            for tile in bg_tiles:
                window.blit(bg_image, tile)
            window.blit(bg_image, (0, 0))
            window.blit(back_text, back_rect)
            draw_text(window, credit_contents, font2, black, credit_rect2, 400)

        elif setting_screen:
            bg_tiles, bg_image = get_background('game_background_2.png')
            for tile in bg_tiles:
                window.blit(bg_image, tile)
            window.blit(bg_image, (0, 0))

            # 클릭 소리 볼륨 표시
            window.blit(click_volume_text, click_volume_rect)
            window.blit(click_volume_up_text, click_volume_up_rect)
            window.blit(click_volume_down_text, click_volume_down_rect)

            click_volume_value_text = font1.render(f"{click_sound_volume}", True, black)

            offset_x = 11 if click_sound_volume >= 100 else 0
            offset2_x = 11 if click_sound_volume < 10 else 0

            window.blit(click_volume_value_text, (WIDTH // 2 - 20 - offset_x + offset2_x, 390))

            # 배경 음악 볼륨 표시
            window.blit(BGM_volume_text, BGM_volume_rect)
            window.blit(BGM_volume_up_text, BGM_volume_up_rect)
            window.blit(BGM_volume_down_text, BGM_volume_down_rect)

            BGM_volume_value_text = font1.render(f"{BGM_sound_volume}", True, black)

            offset_x = 11 if BGM_sound_volume >= 100 else 0
            offset2_x = 11 if BGM_sound_volume < 10 else 0

            window.blit(BGM_volume_value_text,
                        (WIDTH // 2 - 20 - offset_x + offset2_x, 240))

            window.blit(back_text, back_rect)


        if stage_1_active:
            stage_1(window)
        
        if stage_2_active:
            stage_2(window)

        pygame.display.flip()
        clock.tick(FPS)

# 블록 이미지 불러오기(Youtube 인용)
def get_block_floor(size):
    path = join("image", "Terrain", "Terrain.png")
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
    rect = pygame.Rect(30, 0, image.get_width(), image.get_height())
    surface.blit(image, (0, 0), rect)
    return pygame.transform.scale2x(surface)

def get_block_obstacle_1(size):
    path = join("image", "Terrain", "Terrain.png")
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
    rect = pygame.Rect(0, 128, size, size)
    surface.blit(image, (0, 0), rect)
    return pygame.transform.scale2x(surface)

def get_block_obstacle_2(size):
    path = join("image", "Terrain", "Terrain.png")
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
    rect = pygame.Rect(48, 128, size, size)
    surface.blit(image, (0, 0), rect)
    return pygame.transform.scale2x(surface)

def get_block_obstacle_3(size):
    path = join("image", "Terrain", "Terrain.png")
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
    rect = pygame.Rect(128, 0, size, size)
    surface.blit(image, (0, 0), rect)
    return pygame.transform.scale2x(surface)

def get_block_obstacle_4(size):
    path = join("image", "Terrain", "Terrain.png")
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
    rect = pygame.Rect(128, 49, size, size)
    surface.blit(image, (0, 0), rect)
    return pygame.transform.scale2x(surface)


def get_block_obstacle_5(size):
    path = join("image", "Terrain", "Terrain.png")
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
    rect = pygame.Rect(128, 128, size, size)
    surface.blit(image, (0, 0), rect)
    return pygame.transform.scale2x(surface)

def get_block_obstacle_6(size):
    path = join("image", "Terrain", "Terrain.png")
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
    rect = pygame.Rect(480, 96, size, size)
    surface.blit(image, (0, 0), rect)
    return pygame.transform.scale2x(surface)

def get_block_obstacle_7(size):
    path = join("image", "Terrain", "Terrain.png")
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
    rect = pygame.Rect(528, 96, size, size)
    surface.blit(image, (0, 0), rect)
    return pygame.transform.scale2x(surface)

def get_block_obstacle_8(size):
    path = join("image", "Terrain", "Terrain.png")
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
    rect = pygame.Rect(480, 144, size, size)
    surface.blit(image, (0, 0), rect)
    return pygame.transform.scale2x(surface)

def get_block_obstacle_9(size):
    path = join("image", "Terrain", "Terrain.png")
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
    rect = pygame.Rect(528, 144, size, size)
    surface.blit(image, (0, 0), rect)
    return pygame.transform.scale2x(surface)

# 이미지 불러오는 함수(자체 제작)
def load_image(path):
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((image.get_width(), image.get_height()), pygame.SRCALPHA, 32)
    surface.blit(image, (0, 0))
    return surface

# 플레이어 클래스(Youtube 참고 + 활용 및 자체 제작)
class Player(pygame.sprite.Sprite):
    COLOR = (255, 255, 255)
    GRAVITY = 1
    SPRITES = load_sprite_sheets("Characters", "Blue", 56, 45, True)
    ANIMATION_DELAY = 3

    def __init__(self, x, y, width, height):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.x_vel = 0
        self.y_vel = 0
        self.mask = None
        self.direction = "left"
        self.animation_count = 0
        self.fall_count = 0
        self.jump_count = 0
        self.ATTACK_FRAMES = len(self.SPRITES["blue_attack_right"])
        self.is_attacking = False
        self.attack_count = 0
        self.attack_frame = 0
        self.attack_pressed = False

    def jump(self):
        self.y_vel = -self.GRAVITY * 8
        self.animation_count = 0
        self.jump_count += 1
        if self.jump_count == 1:
            self.fall_count = 0

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def make_attack(self):
        self.is_attacking = True

    def move_left(self, vel):
        self.x_vel = -vel
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0

    def move_right(self, vel):
        self.x_vel = vel
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0

    def loop(self, fps):
        global player_hp
        self.y_vel += min(1, (self.fall_count / fps) * self.GRAVITY)
        self.move(self.x_vel, self.y_vel)

        if self.is_attacking:
            self.ATTACK_FRAMES = 12

            if self.attack_frame >= self.ATTACK_FRAMES:
                self.is_attacking = False
            else:
                self.attack_frame += 1

        self.fall_count += 1
        self.update_sprite()

    def landed(self):
        self.fall_count = 0
        self.y_vel = 0
        self.jump_count = 0

    def attack(self):
        if not self.is_attacking and not self.attack_pressed:
            self.is_attacking = True
            self.attack_frame = 0
            self.animation_count = 0
            self.attack_pressed = True

    def attack_head(self):
        pass

    def update_sprite(self):
        sprite_sheet = "blue_idle"
        if self.is_attacking:
            sprite_sheet = "blue_attack"
        elif self.y_vel < 0:
            if self.jump_count == 1:
                sprite_sheet = "blue_jump"
        elif self.y_vel > self.GRAVITY * 2:
            sprite_sheet = "blue_fall"
        if self.x_vel != 0:
            sprite_sheet = "blue_run"

        sprite_sheet_name = sprite_sheet + "_" + self.direction
        sprites = self.SPRITES.get(sprite_sheet_name, [])
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.sprite = sprites[sprite_index]
        self.animation_count += 1
        self.update()


    def update(self):
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)

    def draw(self, win, offset_x):
        win.blit(self.sprite, (self.rect.x - offset_x, self.rect.y))

# 몬스터 클래스(자체 제작)
class Monster(pygame.sprite.Sprite):
    COLOR = (255, 255, 255)
    GRAVITY = 1
    SPRITES = load_sprite_sheets("Characters", "Slime", 32, 20, True)
    ANIMATION_DELAY = 6

    def __init__(self, x, y, width, height):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.alive = True 
        self.x_vel = 0
        self.y_vel = 0
        self.mask = None
        self.direction = "left"
        self.animation_count = 0
        self.fall_count = 0
        self.jump_count = 0
        self.is_attacking = False  # 추가
        self.attack_pressed = False

    def jump(self):
        self.y_vel = -self.GRAVITY * 8
        self.animation_count = 0
        self.jump_count += 1
        if self.jump_count == 1:
            self.fall_count = 0

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def move_left(self, vel):
        self.x_vel = -vel
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0

    def move_right(self, vel):
        self.x_vel = vel
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0

    def loop(self, fps):
        self.y_vel += min(1, (self.fall_count / fps) * self.GRAVITY)
        self.move(self.x_vel, self.y_vel)

        self.fall_count += 1
        self.update_sprite()

    def landed(self):
        self.fall_count = 0
        self.y_vel = 0
        self.jump_count = 0

    def attack(self):
        if not self.is_attacking and not self.attack_pressed:
            self.is_attacking = True
            self.attack_frame = 0
            self.animation_count = 0
            self.attack_pressed = True

    def attack_head(self):
        pass

    def update_sprite(self):
        sprite_sheet = "Slime_Medium_Green_idle"

        sprite_sheet_name = sprite_sheet + "_" + self.direction
        sprites = self.SPRITES[sprite_sheet_name]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % 3
        self.sprite = sprites[sprite_index]
        self.animation_count += 1
        self.update()


    def update(self):
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)

    def draw(self, win, offset_x):
        if self.alive: 
            win.blit(self.sprite, (self.rect.x - offset_x, self.rect.y))

# 오브젝트 클래스(Youtube 인용 + 활용 및 자체 제작)
class Object(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, name=None):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.width = width
        self.height = height
        self.name = name

    def draw(self, win, offset_x):
        win.blit(self.image, (self.rect.x - offset_x, self.rect.y))

# 바닥 클래스(Youtube 인용)
class Block_Floor(Object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        block_floor = get_block_floor(size)
        self.image.blit(block_floor, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)

# 장애물 클래스(Youtube 참고 및 자체 제작)
class Block_Obstacle_1(Object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        block_obstacle_1 = get_block_obstacle_1(size)
        self.image.blit(block_obstacle_1, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)

class Block_Obstacle_2(Object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        block_obstacle_2 = get_block_obstacle_2(size)
        self.image.blit(block_obstacle_2, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)

class Block_Obstacle_3(Object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        block_obstacle_3 = get_block_obstacle_3(size)
        self.image.blit(block_obstacle_3, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)

class Block_Obstacle_4(Object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        block_obstacle_4 = get_block_obstacle_4(size)
        self.image.blit(block_obstacle_4, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)

class Block_Obstacle_5(Object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        block_obstacle_5 = get_block_obstacle_5(size)
        self.image.blit(block_obstacle_5, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)

class Block_Obstacle_6(Object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        block_obstacle_6 = get_block_obstacle_6(size)
        self.image.blit(block_obstacle_6, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)

class Block_Obstacle_7(Object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        block_obstacle_7 = get_block_obstacle_7(size)
        self.image.blit(block_obstacle_7, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)

class Block_Obstacle_8(Object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        block_obstacle_8 = get_block_obstacle_8(size)
        self.image.blit(block_obstacle_8, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)

class Block_Obstacle_9(Object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        block_obstacle_9 = get_block_obstacle_9(size)
        self.image.blit(block_obstacle_9, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)

# 타일, 플레이어, 몬스터 관련 함수(GPT 참고)
def draw(window, background, bg_image, player, monsters, objects, offset_x):
    for tile in background:
        window.blit(bg_image, tile)

    for obj in objects:
        obj.draw(window, offset_x)

    player.draw(window, offset_x)
    
    for monster in monsters:  
        monster.draw(window, offset_x)

    pygame.display.update()

# 수직 충돌 함수(Youtube 참고 및 자체 제작)
def handle_vertical_collision(player, monster1, monster2, monster3, monster4, monster5, objects):
    collided_objects = []

    # 플레이어와 객체 간의 충돌 검사
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            if player.y_vel > 0:
                player.rect.bottom = obj.rect.top
                player.landed()
            elif player.y_vel < 0:
                player.rect.top = obj.rect.bottom
                player.attack_head()

            collided_objects.append(obj)

    # 몬스터와 객체 간의 충돌 검사
    for monster in [monster1, monster2, monster3, monster4, monster5]:
        for obj in objects:
            if pygame.sprite.collide_mask(monster, obj):
                if monster.y_vel > 0:
                    monster.rect.bottom = obj.rect.top
                    monster.landed()
                elif monster.y_vel < 0:
                    monster.rect.top = obj.rect.bottom
                    monster.attack_head()

                collided_objects.append(obj)

    return collided_objects

# 충돌 함수(Youtube 인용)
def collide(player, monster1, monster2, monster3, monster4, monster5, objects, dx):
    player.move(dx, 0)
    player.update()
    collided_object = None
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            collided_object = obj
            break

    for monster in [monster1, monster2, monster3, monster4, monster5]:
        if monster.alive and pygame.sprite.collide_mask(player, monster):
            collided_object = monster
            break

    player.move(-dx, 0)
    player.update()
    return collided_object

# 조종과 관련된 충돌 함수(Youtube 참고 및 자체 제작)
def handle_move(player, monster1, monster2, monster3, monster4, monster5, objects):
    keys = pygame.key.get_pressed()

    player.x_vel = 0
    collide_left = collide(player, monster1, monster2, monster3, monster4, monster5, objects, -PLAYER_VEL * 2)
    collide_right = collide(player, monster1, monster2, monster3, monster4, monster5, objects, PLAYER_VEL * 2)

    if keys[pygame.K_a] and not collide_left:
        player.move_left(PLAYER_VEL)
    if keys[pygame.K_d] and not collide_right:
        player.move_right(PLAYER_VEL)
    if keys[pygame.K_j]:
        player.attack()

    vertical_collide = handle_vertical_collision(player, monster1, monster2, monster3, monster4, monster5, objects)
    to_check = [collide_left, collide_right, *vertical_collide]

    for obj in to_check:
        if obj and isinstance(obj, Monster):  
            player.make_attack()

# 슬라임 충돌 확인 함수(자체 제작)
def check_slime_collision(player, monsters):
    global coin
    for monster in monsters:
        if monster.alive and pygame.sprite.collide_rect(player, monster):
            monster.alive = False
            coin += 5
            return True
    return False

# 스테이지 1 실행 함수(자체 제작)
def stage_1(window):
    clock = pygame.time.Clock()
    background, bg_image = get_background("game_background_1.png")

    block_size = 96

    global stage_1_active

    player = Player(170, 500, 50, 50)
    monster1 = Monster(500, 300, 50, 50)
    monster2 = Monster(800, 200, 50, 50)
    monster3 = Monster(1500, 200, 50, 50)
    monster4 = Monster(700, 500, 50, 50)
    monster5 = Monster(1650, 500, 50, 50)
    monsters = [monster1, monster2, monster3, monster4, monster5]
    floor = [Block_Floor(i * block_size, HEIGHT - block_size, block_size)
             for i in range(-WIDTH // block_size, (WIDTH * 2) // block_size)]
    objects = [Block_Obstacle_3(block_size * 3, HEIGHT - block_size * 3, block_size),
               Block_Obstacle_4(block_size * 3, HEIGHT - block_size * 2, block_size),
               Block_Obstacle_1(block_size * 5, HEIGHT - block_size * 4, block_size),
               Block_Obstacle_2(block_size * 6, HEIGHT - block_size * 4, block_size),
               Block_Obstacle_1(block_size * 8, HEIGHT - block_size * 5, block_size),
               Block_Obstacle_2(block_size * 9, HEIGHT - block_size * 5, block_size),
               Block_Obstacle_5(block_size * 11, HEIGHT - block_size * 5, block_size),
               Block_Obstacle_1(block_size * 15, HEIGHT - block_size * 5, block_size),
               Block_Obstacle_2(block_size * 16, HEIGHT - block_size * 5, block_size),
               Block_Obstacle_6(block_size * 19, HEIGHT - block_size * 5, block_size),
               Block_Obstacle_7(block_size * 20, HEIGHT - block_size * 5, block_size),
               Block_Obstacle_8(block_size * 19, HEIGHT - block_size * 4, block_size),
               Block_Obstacle_9(block_size * 20, HEIGHT - block_size * 4, block_size),
               Block_Obstacle_5(block_size * 2, HEIGHT - block_size * 2, block_size),
               Block_Obstacle_1(block_size * 7, HEIGHT - block_size * 2, block_size),
               Block_Obstacle_2(block_size * 8, HEIGHT - block_size * 2, block_size),
               Block_Obstacle_6(block_size * 12, HEIGHT - block_size * 3, block_size),
               Block_Obstacle_7(block_size * 13, HEIGHT - block_size * 3, block_size),
               Block_Obstacle_8(block_size * 12, HEIGHT - block_size * 2, block_size),
               Block_Obstacle_9(block_size * 13, HEIGHT - block_size * 2, block_size),
               Block_Obstacle_5(block_size * 10, HEIGHT - block_size * 2, block_size),
               Block_Obstacle_6(block_size * 17, HEIGHT - block_size * 2, block_size),
               Block_Obstacle_7(block_size * 18, HEIGHT - block_size * 2, block_size),
               Block_Obstacle_8(block_size * 17, HEIGHT - block_size * 1, block_size),
               Block_Obstacle_9(block_size * 18, HEIGHT - block_size * 1, block_size),
               Block_Obstacle_3(block_size * 14, HEIGHT - block_size * 4, block_size),
               Block_Obstacle_4(block_size * 14, HEIGHT - block_size * 3, block_size),
               Block_Obstacle_3(block_size * 22, HEIGHT - block_size * 4, block_size),
               Block_Obstacle_4(block_size * 22, HEIGHT - block_size * 3, block_size),
               Block_Obstacle_3(block_size * 23, HEIGHT - block_size * 3, block_size),
               Block_Obstacle_4(block_size * 23, HEIGHT - block_size * 2, block_size),
               Block_Obstacle_3(block_size * 24, HEIGHT - block_size * 2, block_size),
               Block_Obstacle_4(block_size * 24, HEIGHT - block_size * 1, block_size),
               Block_Obstacle_1(block_size * 25, HEIGHT - block_size * 1, block_size),
               Block_Obstacle_2(block_size * 26, HEIGHT - block_size * 1, block_size),
               Block_Obstacle_1(block_size * 27, HEIGHT - block_size * 1, block_size),
               Block_Obstacle_2(block_size * 28, HEIGHT - block_size * 1, block_size)]
    
    offset_x = 0
    scroll_area_width = 200

    game_over = False
    game_over_text = font3.render("GAME OVER", True, white)
    game_over_text_2 = font3.render("R키를 누르면 리스폰됩니다.", True, white)

    run = True
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if not game_over:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w and player.jump_count < 1:
                        player.jump()
                    elif event.key == pygame.K_j:
                        player.attack()
                        if check_slime_collision(player, monsters):
                            print("Slime killed!")
                    elif event.key == pygame.K_ESCAPE:
                        show_game_menu(window)
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_j:
                        player.attack_pressed = False

            elif game_over: 
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        game_over = False
                        player.rect.x = 170
                        player.rect.y = 500
                        offset_x = 0

        if not game_over:  
            clock.tick(FPS)  
            player.loop(FPS)  
            monsters = [monster for monster in monsters if monster.alive]
            for monster in monsters:
                monster.loop(FPS)
            
            handle_move(player, monster1, monster2, monster3, monster4, monster5, objects)
            draw(window, background, bg_image, player, monsters, objects, offset_x)

            if ((player.rect.right - offset_x >= WIDTH - scroll_area_width) and player.x_vel > 0) or (
                    (player.rect.left - offset_x <= scroll_area_width) and player.x_vel < 0):
                offset_x += player.x_vel

        if player.rect.y > 1500:
            game_over = True    
            window.fill(black) 
            text_rect_1 = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            text_rect_2 = game_over_text_2.get_rect(center= (WIDTH // 2, HEIGHT // 2 + 100))
            window.blit(game_over_text, text_rect_1)
            window.blit(game_over_text_2, text_rect_2)
            pygame.display.flip()

        if not stage_1_active:
            run = False

# 스테이지 2 실행 함수(자체 제작)
def stage_2(window):
    clock = pygame.time.Clock()
    background, bg_image = get_background("game_background_1.png")

    block_size = 96
    
    global stage_2_active, coin
    coin = 0

    player = Player(170, 500, 50, 50)
    monster1 = Monster(650, 500, 50, 50)
    monster2 = Monster(900, 600, 50, 50)
    monster3 = Monster(1300, 200, 50, 50)
    monster4 = Monster(1500, 500, 50, 50)
    monster5 = Monster(2000, 100, 50, 50)
    monsters = [monster1, monster2, monster3, monster4, monster5]
    floor = [Block_Floor(i * block_size, HEIGHT - block_size, block_size)
             for i in range(-WIDTH // block_size, (WIDTH * 2) // block_size)]
    objects = [Block_Obstacle_5(block_size * 2, HEIGHT - block_size * 2, block_size),
               Block_Obstacle_3(block_size * 3, HEIGHT - block_size * 3, block_size),
               Block_Obstacle_4(block_size * 3, HEIGHT - block_size * 2, block_size),
               Block_Obstacle_3(block_size * 5, HEIGHT - block_size * 3, block_size),
               Block_Obstacle_4(block_size * 5, HEIGHT - block_size * 2, block_size),
               Block_Obstacle_1(block_size * 6, HEIGHT - block_size * 2, block_size),
               Block_Obstacle_2(block_size * 7, HEIGHT - block_size * 2, block_size),
               Block_Obstacle_6(block_size * 9, HEIGHT - block_size * 6, block_size),
               Block_Obstacle_7(block_size * 10, HEIGHT - block_size * 6, block_size),
               Block_Obstacle_8(block_size * 9, HEIGHT - block_size * 5, block_size),
               Block_Obstacle_9(block_size * 10, HEIGHT - block_size * 5, block_size),
               Block_Obstacle_5(block_size * 7, HEIGHT - block_size * 5, block_size),
               Block_Obstacle_1(block_size * 9, HEIGHT - block_size * 1, block_size),
               Block_Obstacle_2(block_size * 10, HEIGHT - block_size * 1, block_size),
               Block_Obstacle_1(block_size * 13, HEIGHT - block_size * 5, block_size),
               Block_Obstacle_2(block_size * 14, HEIGHT - block_size * 5, block_size),
               Block_Obstacle_6(block_size * 12, HEIGHT - block_size * 1, block_size),
               Block_Obstacle_7(block_size * 13, HEIGHT - block_size * 1, block_size),
               Block_Obstacle_8(block_size * 12, HEIGHT - 0, block_size),
               Block_Obstacle_9(block_size * 13, HEIGHT - 0, block_size),
               Block_Obstacle_3(block_size * 14, HEIGHT - block_size * 2, block_size),
               Block_Obstacle_4(block_size * 14, HEIGHT - block_size * 1, block_size),
               Block_Obstacle_1(block_size * 15, HEIGHT - block_size * 2, block_size),
               Block_Obstacle_2(block_size * 16, HEIGHT - block_size * 2, block_size),
               Block_Obstacle_1(block_size * 20, HEIGHT - block_size * 6, block_size),
               Block_Obstacle_2(block_size * 21, HEIGHT - block_size * 6, block_size),
               Block_Obstacle_5(block_size * 19, HEIGHT - block_size * 2, block_size),
               Block_Obstacle_5(block_size * 23, HEIGHT - block_size * 2, block_size),
               Block_Obstacle_6(block_size * 25, HEIGHT - block_size * 3, block_size),
               Block_Obstacle_7(block_size * 26, HEIGHT - block_size * 3, block_size),
               Block_Obstacle_8(block_size * 25, HEIGHT - block_size * 2, block_size),
               Block_Obstacle_9(block_size * 26, HEIGHT - block_size * 2, block_size),
               Block_Obstacle_1(block_size * 27, HEIGHT - block_size * 3, block_size),
               Block_Obstacle_2(block_size * 28, HEIGHT - block_size * 3, block_size),
               Block_Obstacle_1(block_size * 29, HEIGHT - block_size * 3, block_size),
               Block_Obstacle_2(block_size * 30, HEIGHT - block_size * 3, block_size)]
               
    offset_x = 0
    scroll_area_width = 200

    game_over = False
    game_over_text = font3.render("GAME OVER", True, white)
    game_over_text_2 = font3.render("R키를 누르면 리스폰됩니다", True, white)

    run = True
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if not game_over:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w and player.jump_count < 1:
                        player.jump()
                    elif event.key == pygame.K_j:
                        player.attack()
                        if check_slime_collision(player, monsters):
                            print("Slime killed!")
                    elif event.key == pygame.K_ESCAPE:
                        show_game_menu(window)
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_j:
                        player.attack_pressed = False

            elif game_over: 
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        game_over = False
                        player.rect.x = 170
                        player.rect.y = 400
                        offset_x = 0

        if not game_over:  
            clock.tick(FPS)  
            player.loop(FPS)  
            monsters = [monster for monster in monsters if monster.alive]
            for monster in monsters:
                monster.loop(FPS)
            
            handle_move(player, monster1, monster2, monster3, monster4, monster5, objects)
            draw(window, background, bg_image, player, monsters, objects, offset_x)

            if ((player.rect.right - offset_x >= WIDTH - scroll_area_width) and player.x_vel > 0) or (
                    (player.rect.left - offset_x <= scroll_area_width) and player.x_vel < 0):
                offset_x += player.x_vel

        if player.rect.y > 1500:
            game_over = True    
            window.fill(black) 
            text_rect_1 = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            text_rect_2 = game_over_text_2.get_rect(center= (WIDTH // 2, HEIGHT // 2 + 100))
            window.blit(game_over_text, text_rect_1)
            window.blit(game_over_text_2, text_rect_2)
            pygame.display.flip()

        if not stage_2_active:
            run = False


if __name__ == "__main__":
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Main Menu")
    show_main_menu(window)