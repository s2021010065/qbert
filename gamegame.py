import sys
import pygame
import random
import math
from pygame import mixer

mixer.init()
pygame.init()

mixer.music.load('background.wav')
#фоновая музыка
mixer.music.play(-1)

screen = pygame.display.set_mode((600, 700))
pygame.display.set_caption('Q`bert and bugs')
username = None
is_name = False

background = pygame.image.load('fon_igra_2.png')

playerimg = pygame.image.load('strelok_kopia.png')
bugimg = pygame.image.load('zhuki.png')

bugX = []
bugs = []
bugY = []
bugspeedX = []
bugspeedY = []


def intro():
    #функция заставки в начале игры
    fon = pygame.image.load('fon.jpg')
    fontt = pygame.font.SysFont('stxingkai', 70)
    text_welcome = fontt.render('Welcome!', True, 'white')
    name = 'Введите своё Имя'
    is_name = False
    while not is_name:
    #проверка на наличие никнейма
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)

            elif event.type == pygame.KEYDOWN:
                if event.unicode.isalpha():
                    name += event.unicode
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif event.key == pygame.K_RETURN:
                    if len(name) > 3:
                        global username
                        username = name
                        is_name = True
                        break

        screen.fill('black')
        text_name = fontt.render(name, True, 'white')
        screen.blit(pygame.transform.scale(fon, (600, 700)), (0, 0))
        screen.blit(text_welcome, (175, 35))
        screen.blit(text_name, (125, 100))
        pygame.display.update()


intro()
#вызов функции заставки игры


count_of_bugs = 6
#количество жуков на поле

for i in range(count_of_bugs):
#цикл расположения жуков
    bugs.append(bugimg)
    bugX.append(random.randint(0, 550))
    bugY.append(random.randint(30, 150))
    bugspeedX.append(-7)
    bugspeedY.append(40)

score = 0

bulletimg = pygame.image.load('pulya.png')
check = False
bulletX = 386
bulletY = 490

playerX = 370
playerY = 480
changeX = 0
running = True

font = pygame.font.SysFont('Arial', 32, 'bold')

def score_text():
    #функция счёта
    img = font.render(f'Score:{score}', True, 'white')
    screen.blit(img, (10, 10))

font_gameover = pygame.font.SysFont('Arial', 64, 'bold')

def gameover():
    #функция проигрыша
    img_gameover = font_gameover.render('GAME OVER', True, 'white')
    screen.blit(img_gameover, (200, 250))


while running:
    #главная часть игры
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                changeX = -5
            if event.key == pygame.K_RIGHT:
                changeX = 5
            if event.key == pygame.K_SPACE:
                if check is False:
                    bulletSound = mixer.Sound('laser.wav')
                    bulletSound.play()
                    check = True
                    bulletX = playerX + 16

        if event.type == pygame.KEYUP:
            changeX = 0
    playerX += changeX  # spaceshipX=spaceshipX-changeX
    if playerX <= 0:
        playerX = 0
    elif playerX >= 550:
        playerX = 550

    for i in range(count_of_bugs):
        if bugY[i] > 420:
            for j in range(count_of_bugs):
                bugY[j] = 2000
            gameover()
            break
        bugX[i] += bugspeedX[i]
        if bugX[i] <= 0:
            bugspeedX[i] = 1
            bugY[i] += bugspeedY[i]
        if bugX[i] >= 550:
            bugspeedX[i] = -1
            bugY[i] += bugspeedY[i]

        distance = math.sqrt(math.pow(bulletX - bugX[i], 2) + math.pow(bulletY - bugY[i], 2))
        if distance < 27:
            #условие попадания снаряда во врага
            explosion = mixer.Sound('explosion.wav')
            explosion.play()
            bulletY = 480
            check = False
            bugX[i] = random.randint(0, 436)
            bugY[i] = random.randint(30, 150)
            score += 1
        screen.blit(bugs[i], (bugX[i], bugY[i]))

    if bulletY <= 0:
        bulletY = 490
        check = False
    if check:
        screen.blit(bulletimg, (bulletX, bulletY))
        bulletY -= 5



    screen.blit(playerimg, (playerX, playerY))
    score_text()
    pygame.display.update()