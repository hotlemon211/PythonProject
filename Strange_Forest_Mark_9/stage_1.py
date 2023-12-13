import os
import random
import math
import pygame
from os import listdir
from os.path import isfile, join
pygame.init()

pygame.display.set_caption("Stage_1")

WIDTH, HEIGHT = 1000, 800
FPS = 60
PLAYER_VEL = 5
player_hp = 3

window = pygame.display.set_mode((WIDTH, HEIGHT))


def flip(sprites):
    return [pygame.transform.flip(sprite, True, False) for sprite in sprites]


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
    rect = pygame.Rect(128, 39, size, size)
    surface.blit(image, (0, 0), rect)
    return pygame.transform.scale2x(surface)

def get_block_obstacle_5(size):
    path = join("image", "Terrain", "Terrain.png")
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
    rect = pygame.Rect(128, 128, size, size)
    surface.blit(image, (0, 0), rect)
    return pygame.transform.scale2x(surface)

def load_image(path):
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((image.get_width(), image.get_height()), pygame.SRCALPHA, 32)
    surface.blit(image, (0, 0))
    return surface


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
        sprites = self.SPRITES[sprite_sheet_name]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % 6
        self.sprite = sprites[sprite_index]
        self.animation_count += 1
        self.update()


    def update(self):
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)

    def draw(self, win, offset_x):
        win.blit(self.sprite, (self.rect.x - offset_x, self.rect.y))

class Monster(pygame.sprite.Sprite):
    COLOR = (255, 255, 255)
    GRAVITY = 1
    SPRITES = load_sprite_sheets("Characters", "Slime", 32, 20, True)
    ANIMATION_DELAY = 6

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
        win.blit(self.sprite, (self.rect.x - offset_x, self.rect.y))


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


class Block_Floor(Object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        block_floor = get_block_floor(size)
        self.image.blit(block_floor, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)

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



def get_background(name):
    image = pygame.image.load(join("image", "background", name))
    _, _, width, height = image.get_rect()
    tiles = []

    for i in range(WIDTH // width + 1):
        for j in range(HEIGHT // height + 1):
            pos = (i * width, j * height)
            tiles.append(pos)

    return tiles, image


def draw(window, background, bg_image, player, monster, objects, offset_x):
    for tile in background:
        window.blit(bg_image, tile)

    for obj in objects:
        obj.draw(window, offset_x)

    player.draw(window, offset_x)
    monster.draw(window, offset_x)

    pygame.display.update()


def handle_vertical_collision(player, monster, objects):
    collided_objects = []
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            if player.y_vel > 0:
                player.rect.bottom = obj.rect.top
                player.landed()
            elif player.y_vel < 0:
                player.rect.top = obj.rect.bottom
                player.attack_head()

            collided_objects.append(obj)
        
        if pygame.sprite.collide_mask(monster, obj):
            if monster.y_vel > 0:
                monster.rect.bottom = obj.rect.top
                monster.landed()
            elif monster.y_vel < 0:
                monster.rect.top = obj.rect.bottom
                monster.attack_head()

            collided_objects.append(obj)

    return collided_objects


def collide(player, monster, objects, dx):
    player.move(dx, 0)
    player.update()
    collided_object = None
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            collided_object = obj
            break

    player.move(-dx, 0)
    player.update()
    return collided_object


def handle_move(player, monster, objects):
    keys = pygame.key.get_pressed()

    player.x_vel = 0
    collide_left = collide(player, monster, objects, -PLAYER_VEL * 2)
    collide_right = collide(player, monster, objects, PLAYER_VEL * 2)

    if keys[pygame.K_a] and not collide_left:
        player.move_left(PLAYER_VEL)
    if keys[pygame.K_d] and not collide_right:
        player.move_right(PLAYER_VEL)
    if keys[pygame.K_j]:
        player.attack()

    vertical_collide = handle_vertical_collision(player, monster, objects)
    to_check = [collide_left, collide_right, *vertical_collide]

    for obj in to_check:
        if obj and isinstance(obj, Monster):  # 수정
            player.make_attack()

def game_over_screen():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESC:
                    pygame.quit()
                    quit()

        window.fill((0, 0, 0))
        font = pygame.font.Font(None, 80)
        text = font.render("Game Over", True, (255, 0, 0))
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        window.blit(text, text_rect.topleft)
        pygame.display.flip()


def main(window):
    clock = pygame.time.Clock()
    background, bg_image = get_background("game_background_1.png")

    block_size = 96

    player = Player(100, 100, 50, 50)
    monster = Monster(400, 100, 50, 50)
    floor = [Block_Floor(i * block_size, HEIGHT - block_size, block_size)
             for i in range(-WIDTH // block_size, (WIDTH * 2) // block_size)]
    objects = [*floor, Block_Obstacle_3(0, HEIGHT - block_size * 2, block_size),
               Block_Obstacle_1(block_size * 3, HEIGHT - block_size * 3, block_size),
               Block_Obstacle_2(block_size * 4, HEIGHT - block_size * 3, block_size),
               Block_Obstacle_1(block_size * 6, HEIGHT - block_size * 4, block_size),
               Block_Obstacle_2(block_size * 7, HEIGHT - block_size * 4, block_size),
               Block_Obstacle_5(block_size * 9, HEIGHT - block_size * 4, block_size)]

    offset_x = 0
    scroll_area_width = 200

    run = True
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and player.jump_count < 1:
                    player.jump()
                elif event.key == pygame.K_j:
                    player.attack()
            
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_j:
                    player.attack_pressed = False

        player.loop(FPS)
        monster.loop(FPS)
        handle_move(player, monster, objects)
        draw(window, background, bg_image, player, monster, objects, offset_x)
        

        if ((player.rect.right - offset_x >= WIDTH - scroll_area_width) and player.x_vel > 0) or (
                (player.rect.left - offset_x <= scroll_area_width) and player.x_vel < 0):
            offset_x += player.x_vel

    pygame.quit()
    quit()


if __name__ == "__main__":
    main(window)