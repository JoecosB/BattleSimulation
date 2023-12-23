import pygame
import sys
from random import randint

#设置窗口大小、标题和底色
clock = pygame.time.Clock()
pygame.mixer.init()
pygame.init()
screen = pygame.display.set_mode((1440, 800))
screen.fill('white')
pygame.display.flip()
pygame.display.set_caption("BattleSimulation")
start = 0

#导入三位重量级选手的图片
lutalli_sprite = pygame.transform.scale(pygame.image.load("./imgs/lutalli.png"), (50, 50))
joecos_sprite = pygame.transform.scale(pygame.image.load("./imgs/joecos.png"), (50, 50))
sheldon_sprite = pygame.transform.scale(pygame.image.load("./imgs/sheldon.png"), (50, 50))

#初始化各位选手的数量，位置和加速度、速度
number = 15
lutalli_pos = [[randint(25, 1390), randint(25, 750)] for i in range(number)]   #[x, y]
joecos_pos = [[randint(25, 1390), randint(25, 750)] for i in range(number)]
sheldon_pos = [[randint(25, 1390), randint(25, 750)] for i in range(number)]
lutalli_vectors = [[[0, 0], [0, 0]] for i in range(number)]   #[acceleration, velocity]
joecos_vectors = [[[0, 0], [0, 0]] for i in range(number)]
sheldon_vectors = [[[0, 0], [0, 0]] for i in range(number)]

#设定函数，根据选手离目标、敌人的距离算出选手的加速度
def acceleration_calc(character_pos, enemy_pos, target_pos):
    character_accelerations = []

    for pos_1 in character_pos:
        acceleration_from_enemy = [0, 0]
        for pos_2 in enemy_pos:
            x = pos_2[0] - pos_1[0]
            y = pos_2[1] - pos_1[1]
            p = 3*10**(-((x**2 + y**2))**0.5/230)
            if x > 0:
                acceleration_from_enemy[0] -= 10*5**(-abs(x/150))*p
            elif x < 0:
                acceleration_from_enemy[0] += 10*5**(-abs(x/150))*p
            else:
                if pos_1[0] < 100:
                    acceleration_from_enemy[0] += 10*5**(-abs(x/150))*p
                else:
                    acceleration_from_enemy[0] -= 10*5**(-abs(x/150))*p
            if y > 0:
                acceleration_from_enemy[1] -= 10*5**(-abs(y/150))*p
            elif y < 0:
                acceleration_from_enemy[1] += 10*5**(-abs(y/150))*p
            else:
                if pos_1[1] < 100:
                    acceleration_from_enemy[1] += 10*5**(-abs(y/150))*p
                else:
                    acceleration_from_enemy[1] -= 10*5**(-abs(y/150))*p
   
        acceleration_to_target = [0, 0]
        if len(target_pos) != 0:
            nearest = 0
            min = 10000
            for i in range(len(target_pos)):
                distance = ((pos_1[0] - target_pos[i][0])**2 + (pos_1[1] - target_pos[i][1])**2)**(1/2)
                if min > distance:
                    nearest = i
                    min = distance
            x = target_pos[nearest][0] - pos_1[0]
            y = target_pos[nearest][1] - pos_1[1]
            if x >= 0:
                acceleration_to_target[0] += 10
            else:
                acceleration_to_target[0] -= 10
            if y >= 0:
                acceleration_to_target[1] += 10
            else:
                acceleration_to_target[1] -= 10

        acceleration = [acceleration_from_enemy[0]+acceleration_to_target[0], acceleration_from_enemy[1]+acceleration_to_target[1]]
        character_accelerations.append(acceleration)
    
    return character_accelerations

#设定函数，判断人物是否被击杀
def get_killed(character_pos, enemy_pos, mute):
    killed_list = []

    for i in range(len(character_pos)):
        for pos in enemy_pos:
            if ((character_pos[i][0] - pos[0])**2 + (character_pos[i][1] - pos[1])**2)**(1/2) <= 15:
                killed_list.append(i)
                if mute != 1:
                    death_effect = pygame.mixer.Sound("./audios/death_effect_" + str(randint(1, 6)) + ".wav")
                    death_effect.play()
                break

    killed_list.sort(reverse=True)
    return killed_list

#初始化选手显示，并在按下enter后开始模拟
start = 0
while True:
    for pos in lutalli_pos:
        screen.blit(lutalli_sprite, (pos[0]-25, pos[1]-25))
    for pos in joecos_pos:
        screen.blit(joecos_sprite, (pos[0]-25, pos[1]-25))
    for pos in sheldon_pos:
        screen.blit(sheldon_sprite, (pos[0]-25, pos[1]-25))
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == 13:  #enter
                start = 1
        
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if start == 1:
        break

#模拟过程主循环
m_pressed = 0
mute = -1
while True:
    clock.tick(40)

    lutalli_killed = get_killed(character_pos=lutalli_pos, enemy_pos=sheldon_pos, mute=mute)
    joecos_killed = get_killed(character_pos=joecos_pos, enemy_pos=lutalli_pos, mute=mute)
    sheldon_killed = get_killed(character_pos=sheldon_pos, enemy_pos=joecos_pos, mute=mute)
    for index in lutalli_killed:
        sheldon_pos.append(lutalli_pos[index])
        sheldon_vectors.append(lutalli_vectors[index])
    for index in joecos_killed:
        lutalli_pos.append(joecos_pos[index])
        lutalli_vectors.append(joecos_vectors[index])
    for index in sheldon_killed:
        joecos_pos.append(sheldon_pos[index])
        joecos_vectors.append(sheldon_vectors[index])
    for index in lutalli_killed:
        del lutalli_pos[index]
        del lutalli_vectors[index]
    for index in joecos_killed:
        del joecos_pos[index]
        del joecos_vectors[index]
    for index in sheldon_killed:
        del sheldon_pos[index]
        del sheldon_vectors[index]

    lutalli_a = acceleration_calc(character_pos=lutalli_pos, enemy_pos=sheldon_pos, target_pos=joecos_pos)
    joecos_a = acceleration_calc(character_pos=joecos_pos, enemy_pos=lutalli_pos, target_pos=sheldon_pos)
    sheldon_a = acceleration_calc(character_pos=sheldon_pos, enemy_pos=joecos_pos, target_pos=lutalli_pos)
    for i in range(len(lutalli_a)):
        lutalli_vectors[i][0] = lutalli_a[i]
        lutalli_vectors[i][1][0] += lutalli_a[i][0]/10
        lutalli_vectors[i][1][1] += lutalli_a[i][1]/10
        v = (lutalli_vectors[i][1][0]**2 + lutalli_vectors[i][1][1]**2)**(1/2)
        if v > 40:
            lutalli_vectors[i][1][0] /= ((v/20)**(1/2))
            lutalli_vectors[i][1][1] /= ((v/20)**(1/2))
    for i in range(len(joecos_a)):
        joecos_vectors[i][0] = joecos_a[i]
        joecos_vectors[i][1][0] += joecos_a[i][0]/10
        joecos_vectors[i][1][1] += joecos_a[i][1]/10
        v = (joecos_vectors[i][1][0]**2 + joecos_vectors[i][1][1]**2)**(1/2)
        if v > 40:
            joecos_vectors[i][1][0] /= ((v/20)**(1/2))
            joecos_vectors[i][1][1] /= ((v/20)**(1/2))
    for i in range(len(sheldon_a)):
        sheldon_vectors[i][0] = sheldon_a[i]
        sheldon_vectors[i][1][0] += sheldon_a[i][0]/10
        sheldon_vectors[i][1][1] += sheldon_a[i][1]/10
        v = (sheldon_vectors[i][1][0]**2 + sheldon_vectors[i][1][1]**2)**(1/2)
        if v > 40:
            sheldon_vectors[i][1][0] /= ((v/20)**(1/2))
            sheldon_vectors[i][1][1] /= ((v/20)**(1/2))

    for i in range(len(lutalli_pos)):
        lutalli_pos[i][0] += 1/2*lutalli_vectors[i][0][0]*0.1**2 + lutalli_vectors[i][1][0]*0.1
        lutalli_pos[i][1] += 1/2*lutalli_vectors[i][0][1]*0.1**2 + lutalli_vectors[i][1][1]*0.1
        if lutalli_pos[i][0] > 1420:
            lutalli_pos[i][0] = 1420
            lutalli_vectors[i][1][0] *= -1/2
        elif lutalli_pos[i][0] < 20:
            lutalli_pos[i][0] = 20
            lutalli_vectors[i][1][0] *= -1/2
        if lutalli_pos[i][1] > 780:
            lutalli_pos[i][1] = 780
            lutalli_vectors[i][1][1] *= -1/2
        elif lutalli_pos[i][1] < 20:
            lutalli_pos[i][1] = 20
            lutalli_vectors[i][1][1] *= -1/2
    for i in range(len(joecos_pos)):
        joecos_pos[i][0] += 1/2*joecos_vectors[i][0][0]*0.1**2 + joecos_vectors[i][1][0]*0.1
        joecos_pos[i][1] += 1/2*joecos_vectors[i][0][1]*0.1**2 + joecos_vectors[i][1][1]*0.1
        if joecos_pos[i][0] > 1420:
            joecos_pos[i][0] = 1420
            joecos_vectors[i][1][0] *= -1/2
        elif joecos_pos[i][0] < 20:
            joecos_pos[i][0] = 20
            joecos_vectors[i][1][0] *= -1/2
        if joecos_pos[i][1] > 780:
            joecos_pos[i][1] = 780
            joecos_vectors[i][1][1] *= -1/2
        elif joecos_pos[i][1] < 20:
            joecos_pos[i][1] = 20
            joecos_vectors[i][1][1] *= -1/2
    for i in range(len(sheldon_pos)):
        sheldon_pos[i][0] += 1/2*sheldon_vectors[i][0][0]*0.1**2 + sheldon_vectors[i][1][0]*0.1
        sheldon_pos[i][1] += 1/2*sheldon_vectors[i][0][1]*0.1**2 + sheldon_vectors[i][1][1]*0.1
        if sheldon_pos[i][0] > 1420:
            sheldon_pos[i][0] = 1420
            sheldon_vectors[i][1][0] *= -1
        elif sheldon_pos[i][0] < 20:
            sheldon_pos[i][0] = 20
            sheldon_vectors[i][1][0] *= -1
        if sheldon_pos[i][1] > 780:
            sheldon_pos[i][1] = 780
            sheldon_vectors[i][1][1] *= -1
        elif sheldon_pos[i][1] < 20:
            sheldon_pos[i][1] = 20
            sheldon_vectors[i][1][1] *= -1

    screen.fill('white')
    for pos in lutalli_pos:
        screen.blit(lutalli_sprite, (pos[0]-25, pos[1]-25))
    for pos in joecos_pos:
        screen.blit(joecos_sprite, (pos[0]-25, pos[1]-25))
    for pos in sheldon_pos:
        screen.blit(sheldon_sprite, (pos[0]-25, pos[1]-25))
    pygame.display.flip()


    #输入事件监听
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == 109 and m_pressed == 0:
                m_pressed = 1
                mute *= -1
        else:
            m_pressed = 0