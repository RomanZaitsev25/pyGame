import pygame
import random
from os import path


'''Определяем месторасположение папки img, snd'''
img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'snd')


WIDTH = 480
HEIGHT = 600
FPS = 60
"""
Используя раздел рендеринга, мы определям цветовую гамму, используя таблицу
цветов RGB
"""
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
''' Перен началом мы должны запустить игру, использую библиотеку pygame и метод 
init. Метод mixer и метод init отвечают за звук в игре.Set_caption- на дисплее 
образует значок на экране, с надписью.  Screen — окно программы, которое 
создается, когда мы задаем его размер в настройках.Использую set_mode, в 
основном в кортеже указывают размер окна.Clock- игра, будет играть с 
определённой частотой кадров. Pygame.time.Clock - объект, который поможет 
отслеживать время'''
pygame.init() # запускает игру
pygame.mixer.init()  # отвечает за звук
screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Let's go!")
clock = pygame.time.Clock()

font_name = pygame.font.match_font('arial')


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def newmob():
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)


def draw_shield_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)


''' Пишем класс Player, который является потомком класса Sprite.Pygame.sprite -
модуль библиотеки pygame с базовыми классами игровых объектов. Далее пишем метод
init. Далее запускаем инициализатор, встроенных родительского класса Sprite.
Surface-модуль библиотеки pygame, который случит для предоставления изображения.
Image- модуль, для сохранения изображения и графического предоставления Sprite.
Rect - показывает положение и размер спрайта. Get_rect- возвращает ссылку на
размер этой области, в ввиде экземпляра класса Rect. Transform.scale()- мы
уменьшим изображение вдвое — до размера 50х30 пикселей, т.к. наша картинка
была больше, чем требуется. Set_colorkey- мы сделали прозрачный фон картинки
(на самом деле покрасили в черный, как цвет фона), чтобы не было черного 
прямоугольника вокруг корабля. Self-radius- превращает наше изображение в
круги, с определныым радиусом'''


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (50, 38))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        # self.radius = 20
        # pygame.draw.circle(self.image, GREEN, self.rect.center, self.radius)
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.shield = 100
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()

    '''Данный метод будет перемещать будет перемещать спрайт с разной ск-тью
    Поэтому обязательно указываем скорость кораблика равное 0, потому что при
    каждом кадре, заново изменяется. Pygame.key - модуль pygame для работы с
    клавиатурой. Pygame.key.get_pressed- возвращает словарь со всеми клавишами 
    клавиатуры и значениями True или False, которые указывают на то, нажата ли 
    какая-то из них. Если одна из кнопок нажимается, скорость меняется 
    соответственно. Сохранение, место положения кораблика'''

    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -8
        if keystate[pygame.K_RIGHT]:
            self.speedx = 8
        if keystate[pygame.K_SPACE]:
            self.shoot()
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        now = pygame.time.get_ticks()

        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)
            shoot_sound.play()


'''Пишем класс Mob, который является потомком класса Sprite.Pygame.sprite -
модуль библиотеки pygame с базовыми классами игровых объектов. Далее пишем метод
init. Далее запускаем инициализатор, встроенных родительского класса Sprite.
Surface-модуль библиотеки pygame, который случит для предоставления изображения.
Image- модуль, для сохранения изображения и графического предоставления Sprite.
Rect - показывает положение и размер спрайта. Get_rect- возвращает ссылку на
размер этой области, в ввиде экземпляра класса Rect. Rot- свойство rot 
(сокращенно от «rotation» (вращение)) будет измерять, на сколько градусов 
должен вращаться астероид. rot_speed- скорость вражения стероида. 
Time.get_ticks - можно будет узнать сколько прошло милисекунд, что бы можно
 было менять изображение спрайта.'''


class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # self.image = pygame.Surface((30, 40)) # атрибуты класса
        # self.image.fill(RED)
        self.image_orig = random.choice(meteor_images)
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .80/2)
        # pygame.draw.circle(self.image, GREEN, self.rect.center, self.radius)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()


    def rotate(self):
        '''
        Затем в методе rotate нужно обновить значение rot и применить
        вращение к исходному изображению
        '''

        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image_orig.get_rect()
            self.rect.center = old_center


    '''Дальше нам нужно задать движение спрайта и что будет с ним, когда он
    достигнет низа. он должен перенеститься случацно в другое место экрана
    (вверх).Top- проверяем по высоте. Rotate - вращение moba.'''
    def update(self):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or \
                self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        # self.image = pygame.Surface((10, 20))
        # self.image.fill(YELLOW)
        self.image = bullet_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50
    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center
'''Pygame.image.load() – загрузка изображения из файла.Get_rect- установи, 
картинку как фон.'''

background = pygame.image.load(path.join(img_dir, "background.jpg")).convert()
background_rect = background.get_rect()
player_img = pygame.image.load(path.join(img_dir, "ship.png")).convert()
# meteor_img = pygame.image.load(path.join(img_dir, "meteor.png")).convert()
bullet_img = pygame.image.load(path.join(img_dir, "fire.png")).convert()
shoot_sound = pygame.mixer.Sound(path.join(snd_dir, 'pew.wav'))
pygame.mixer.music.load(path.join(snd_dir, 'tgfcoder-FrozenJam-SeamlessLoop.ogg'))
pygame.mixer.music.set_volume(0.4)
meteor_images = []
meteor_lst = ['meteorBrown_big1.png', 'meteorBrown_Med.png',
              'meteorBrown_med1.png', 'meteorBrown_med3.png',
              'meteorBrown_tiny2.png', 'meteorBrown_tiny1.png',
              'meteorBrown_small2.png', 'meteorBrown_small2.png',
              'meteorBrown_med3.png' ]

for img in meteor_lst:
    meteor_images.append(pygame.image.load(path.join(img_dir, img)).convert())


explosion_anim = {}
explosion_anim['lg'] = []
explosion_anim['sm'] = []
for i in range(9):
    filename = 'regularExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    img_lg = pygame.transform.scale(img, (75, 75))
    explosion_anim['lg'].append(img_lg)
    img_sm = pygame.transform.scale(img, (32, 32))
    explosion_anim['sm'].append(img_sm)

expl_sounds = []
for snd in ['expl3.wav', 'expl6.wav']:
    expl_sounds.append(pygame.mixer.Sound(path.join(snd_dir, snd)))
'''Теперь нужно показать спрайт, убедиться, что он отображается на экране.
Создаём объект класса Player. Добавляем его в all_sprites, для его обновления
'''
all_sprites = pygame.sprite.Group()
player = Player()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
all_sprites.add(player)

''' Вызвать определённое количество мобов и добавить в группу '''
for i in range(8):
    newmob()
    # m = Mob()
    # all_sprites.add(m)
    # mobs.add(m)
score = 0
pygame.mixer.music.play(loops=-1)



"""Цикл игры создаём.Clock.tick(FPS) - держим цикл на правильной скорости.
Event-модуль для взаимодействия с событиями. Pygame.QUIT -проверка на зкарытие
окна."""
running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # elif event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_SPACE:
        #         player.shoot()

    '''Функция groupcollide() похожа на spritecollide() за исключением того,
    что нужно указывать две группы для сравнения, а возвращать функция будет
    список задетых мобов'''
    all_sprites.update()
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        score += 50 - hit.radius
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        # m = Mob()
        # all_sprites.add(m)
        # mobs.add(m)
        newmob()

    '''Обновление всех спрайтов. Spritecollide() принимает 3 аргумента: 
    название спрайта, который нужно проверять, название группы для сравнения и
    значения True или False. Последний параметр позволяет указать, должен ли 
    объект удаляться при столкновении. pygame.sprite.collide_circle-изменение 
    типа столкновений'''
    hits = pygame.sprite.spritecollide(player, mobs, True,
                                       pygame.sprite.collide_circle)
    for hit in hits:
        player.shield -= hit.radius * 2
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
        newmob()
        if player.shield <= 0:
            running = False
    # if hits:
    #     running = False

    '''Нам нужно отрисовать игру(Рендеринг).Fill- заполняем экран черным.
    Draw- рисует фигуры. Но это не всё нам нжно использовать двойную буфериза-
    цию.Пример- дан 2-х двухсторонний лист, одна сторона для клиента, вторая 
    для компа. С обратной стороны происходит отрисовка, за один кадр. В 
    пайгейм происходит автом.,  когда отрисовка закончится при мопощи метода
    Flip- происходит переворот доски и отрисовка видна пользователю.Blit-
    прорисовка фона на экране'''
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, str(score), 18, WIDTH/2, 10)
    draw_shield_bar(screen,5,5,player.shield)
    pygame.display.flip()

pygame.quit()






