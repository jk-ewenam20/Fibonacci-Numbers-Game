import pygame
from pygame.locals import *

pygame.init()

clock = pygame.time.Clock()
FPS = 60

screen_width = 1024
screen_height = 510

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Fibonacci Number Game')


#define game variables
tile_size = 106
main_menu = True

#load background image
BG = pygame.image.load('bg_grasslands.png')
BG2 = pygame.image.load('start_bg.png')
start_img = pygame.image.load('play_btn.png')

class Player:
    def __init__(self, x, y):
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0
        for num in range(1, 9):
            img_right = pygame.image.load(f'png\Run ({num}).png')
            img_right = pygame.transform.scale(img_right, (50, 50))
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)
        self.image = self.images_right[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_y = 0
        self.jumped = False
        self.direction = 0

    def update(self):
        #get key
        dx = 0
        dy = 0
        walk_cooldown = 15
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            dx -= 3
            self.counter += 5
            self.direction = -1
        if key[pygame.K_RIGHT]:
            dx += 3
            self.counter += 5
            self.direction = 1
        if key[pygame.K_UP] and self.jumped == False:
            self.vel_y = -5
            self.jumped = True
        if key[pygame.K_UP]:
            self.jumped = False

        if key[pygame.K_RIGHT] == False and key[pygame.K_LEFT] == False:
            self.counter = 0
            self.index = 0
            if self.direction == 1:
                self.image = self.images_right[self.index]

            if self.direction == -1:
                self.image = self.images_left[self.index]
        dy += self.vel_y

        #check collision
        

        #handle animation
        
        if self.counter > walk_cooldown:
            self.counter = 1
            self.index += 1
            if self.index >= len(self.images_right):
                self.index = 0
            if self.direction == 1:
                self.image = self.images_right[self.index]

            if self.direction == -1:
                self.image = self.images_left[self.index]

        #update player coordinates
        self.rect.x += dx
        self.rect.y += dy

        if self.rect.bottom > 429:
            self.rect.bottom = 429
            dy = 0

        
        #add gravity
        self.vel_y += 1
        if self.vel_y > 10:
            self.vel_y = 10
        


        #draw player to screen
        screen.blit(self.image, self.rect)
        

        


class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def draw(self):
        action = False
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True
                self.clicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        screen.blit(self.image, self.rect)
        return action


class World():
    def __init__(self, data):
        self.tile_list = []

        #load images
        dirt_img = pygame.image.load('Base pack\Tiles\dirt.png')
        grass_img = pygame.image.load('Base pack\Tiles\grass.png')
        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(dirt_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count *tile_size
                    img_rect.y = row_count *tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)

                if tile == 2:
                    img = pygame.transform.scale(grass_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count *tile_size
                    img_rect.y = row_count *tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                col_count += 1 
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])
            


world_data = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 2, 2, 2, 2, 1, 1, 1, 1]
]

player = Player(100, screen_height - 130)
world = World(world_data)
start_button = Button(screen_width // 2, screen_height // 2, start_img)


run = True
while run:
    clock.tick(FPS)
    screen.blit(BG, (0,0))
    if main_menu == True:
        screen.blit(BG2, (0,0))
        if start_button.draw():
            main_menu = False
    else:
        world.draw()
        player.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.update()

pygame.quit()