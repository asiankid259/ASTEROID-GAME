import pygame
import time
import random
import os
#####################################무조선 필요#################################
#기본 초기화 (반드시 해야 하는 것들)
pygame.init() # 초기화 (반드시 필요)

#화면 크기 생성 및 설정
WIDTH = 1000 # 가로 크기
HEIGHT = 700 #세로 크기
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT), ) # creates new window with above dimensions

#화면 타이틀 설정
pygame.display.set_caption("asteroid game") #게임 이름
##################################무조건 필요########################################
# 1. 사용자 게임 초기화 (배경 화변, 게임 이미지, 좌표 폰츠 등)
WHITE = 255,255,255
BLACK = 0,0,0
BLUE = 0,0,255
GREEN = 0,255,0
RED = 255,0,0

SHOOTER = pygame.image.load( "shooter.png")
SHOOTER = pygame.transform.scale(SHOOTER, (50, 50))
shooter_mask = pygame.mask.from_surface(SHOOTER)

ASTEROID = pygame.image.load("asteroid.png")
BACKGROUND = pygame.image.load("background.png")

########### classes ##################
class Asteroid():# ateroid class
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.mask = pygame.mask.from_surface(ASTEROID)

    def move(self):
        pass

    def draw(self, obj,  window): # gets object(IMAGE) and window and draws object on previously defined location
        window.blit(obj, (self.x,self.y))

    def move(self, direction, vel): # gets direction, and speed of asteroid(1 asteroid)
        if direction == "x": # if given direction x 
            self.x += vel # add given speed to x coordinate of asteroid
        if direction == "y": # if given direction is y
            self.y += vel # add given speed to y coordinate fo asteroid
            
class Shooter(): # shooter class
    def __init__(self, health): # gets health of shooter
        self.health = health

############## classes ##################
def collide(obj1, obj2):
    mouse_x, mouse_y = pygame.mouse.get_pos() # get mouse positon
    offset_x = mouse_x - obj1.x - 70
    offset_y = mouse_y - obj1.y - 70
    return obj1.mask.overlap(obj2, (offset_x, offset_y)) != None
############### main ####################
def main():
    global mouse_x, mouse_y 
    mouse_x, mouse_y = pygame.mouse.get_pos() # get mouse positon
    shooter_width = SHOOTER.get_width() # gets weidth of shooter
    shooter_height = SHOOTER.get_height() # gets height o shooter
    shooter_x_pos = WIDTH/2 - shooter_width/2 # x position is center of screen
    shooter_y_pos = HEIGHT/2 - shooter_height/2# y position is center of screen 
    shooter_health = 100
    clock = pygame.time.Clock() # tick
    running = True

    asteroids = [] # asteroids that come from the top
    asteroids_bot = [] # asteroid that comes from the btotom
    asteroids_left = [] # asteroid thats comes from the left
    asteroids_right = [] # asetroids that come from the right
    asteroid_speed = 4 # speed of every single asteroid
    asteroid_num = 1 # number of asteorids per side
    
    lost = False # if shooter dies

    main_font = pygame.font.SysFont("comicsans", 50)
    # creates asteroids, assigns x y value, and adds to asteroids list

    def create_shooter():
        shooter = Shooter(100)
    # draws everything
    def draw():
        mouse_x, mouse_y = pygame.mouse.get_pos() # get mouse positon
        WINDOW.blit(BACKGROUND, (0,0)) # blits background at 0,0
        WINDOW.blit(SHOOTER, (mouse_x - 70, mouse_y -70)) # blits shooter at mosue position minus offset
        
        for asteroid in asteroids: # for every ateroid in top asteroid list
            asteroid.draw(ASTEROID, WINDOW) # draws obecjt(image) at window on previously defined location 
            asteroid.move("y", asteroid_speed) # move at speed of asteroid_speed 8
           

        for asteroid_bot in asteroids_bot: # fore every asteroid in bottom asteroid list
            asteroid_bot.draw(ASTEROID, WINDOW) # draws an asteroid using the set of coordinates already defined in each variable in list
            asteroid_bot.move("y", -asteroid_speed)# move at speed 8 vertically but negative speed so it goes up not down
            

        for asteroid_left in asteroids_left:
            asteroid_left.draw(ASTEROID, WINDOW)
            asteroid_left.move("x", asteroid_speed) # move at speed 8 horizontally moves left
            

        for asteroid_right in asteroids_right:
            asteroid_right.draw(ASTEROID, WINDOW)
            asteroid_right.move("x", -asteroid_speed) # move at negative speed 9 horizontally moves right
        
        health_label = main_font.render(f"Lives: {shooter_health}",1, (255,255,255))
        WINDOW.blit(health_label, (10,10))

        
         

        pygame.display.update()


        
    while running: # 
        pygame.mouse.set_visible(False)
        dt = clock.tick(60) # 60 frames
        draw()

        # quiting loop
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:# if x presed escape window
                quit()
        if shooter_health <= 0:
            lost = True
        
        for i in range(asteroid_num): # gets asteroid number per side
            asteroid = Asteroid(random.randrange(0, WIDTH-200), random.randrange(-4000, -100)) # spawn asteroids above the screen and random x value
            asteroids.append(asteroid) # add to top asteroid list
        for i in range(asteroid_num):
            asteroid_bot = Asteroid(random.randrange(0, WIDTH-200), random.randrange(1100, 5100)) # adds value to asteroid function, spawn below screen and random x value
            asteroids_bot.append(asteroid_bot) # add to bottom asteroid list
        for i in range(asteroid_num):
            asteroid_left = Asteroid(random.randrange(-4000, -100), random.randrange(0, 600)) # spawn left of screen
            asteroids_left.append(asteroid_left) # add to left asteorid list
        for i in range(asteroid_num):
            asteroid_right = Asteroid(random.randrange(1100, 5100), random.randrange(0, 600)) # spawn right of screen
            asteroids_right.append(asteroid_right) # add to right asteroid list


        for asteroid in asteroids: # for every ateroid in top asteroid lisT
            if collide(asteroid, shooter_mask):
                print("top asteroid and shooter collided")
                asteroids.remove(asteroid)
                shooter_health -= 10

        for asteroid_bot in asteroids_bot: # fore every asteroid in bottom asteroid lis
            if collide(asteroid_bot, shooter_mask):
                print("bottom asteroid and shooter collided")
                asteroids_bot.remove(asteroid_bot)
                shooter_health -= 10

        for asteroid_left in asteroids_left:
            if collide(asteroid_left, shooter_mask):
                print("left asteroid and shooter collided")
                asteroids_left.remove(asteroid_left)
                shooter_health -= 10

        for asteroid_right in asteroids_right:
            if collide(asteroid_right, shooter_mask):
                print("right asteroid and shooter collided")
                asteroids_right.remove(asteroid_right)
                shooter_health -= 10
        if lost:
            lost_label = main_font.render("You Lost!!", 1, (255,255,255))
            WINDOW.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, 350))
            
            pygame.display.update()
            pygame.time.delay(3000)
            

def main_menu():
    title_font = pygame.font.SysFont("comicsans",70)
    running = True 
    while running:
        WINDOW.blit(BACKGROUND, (0,0)) # blits background at 0,0
        title_label = title_font.render("Press the mouse to begin...", 1,(255,255,255))
        WINDOW.blit(title_label, (WIDTH/2 - title_label.get_width()/2, 250))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()
    pygame.quit()


main_menu()



