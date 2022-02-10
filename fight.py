from curses import KEY_UP
import pygame
from pygame.constants import (QUIT,K_SPACE, K_LEFT, K_RIGHT, K_DOWN, K_ESCAPE, KEYDOWN)
import os



class Settings(object):
    window = {'width': 300, 'height':200}
    fps = 60
    title = "fight"
    path = {}
    path['file'] = os.path.dirname(os.path.abspath(__file__))
    path['image'] = os.path.join(path['file'], "images")
    directions = {'stop':(0, 0), 'left':(-7, 0), 'right':(7, 0)}

    @staticmethod
    def dim():
        return (Settings.window['width'], Settings.window['height'])

    @staticmethod
    def filepath(name):
        return os.path.join(Settings.path['file'], name)

    @staticmethod
    def imagepath(name):
        return os.path.join(Settings.path['image'], name)


class Timer(object):
    def __init__(self, duration, with_start = True):
        self.duration = duration
        if with_start:
            self.next = pygame.time.get_ticks()
        else:
            self.next = pygame.time.get_ticks() + self.duration

    def is_next_stop_reached(self):
        if pygame.time.get_ticks() > self.next:
            self.next = pygame.time.get_ticks() + self.duration
            return True
        return False

    def change_duration(self, delta=10):
        self.duration += delta
        if self.duration < 0:
            self.duration = 0


class Animation(object):
    def __init__(self, namelist, endless, flip, animationtime, colorkey=None):
        self.images = []
        self.endless = endless
        self.timer = Timer(animationtime)
        self.flip = flip
        for filename in namelist:
            if colorkey == None:
                bitmap = pygame.image.load(Settings.imagepath(filename)).convert_alpha()
            else:
                bitmap = pygame.image.load(Settings.imagepath(filename)).convert()
                bitmap.set_colorkey(colorkey)
            if flip:
                bitmap = pygame.transform.flip(bitmap, True, False)
            self.images.append(bitmap)
        self.imageindex = -1

    def next(self):
        if self.timer.is_next_stop_reached():
            self.imageindex += 1
            if self.imageindex >= len(self.images):
                if self.endless:
                    self.imageindex = 0
                else:
                    self.imageindex = len(self.images) - 1
        return self.images[self.imageindex]

    def is_ended(self):
        if self.endless:
            return False
        elif self.imageindex >= len(self.images) - 1:
            return True
        else:
            return False

class Samurai(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image_id = ""
        self.image_flip_list = []
        for i in range(0, 12):
            if i >= 10:
                self.image_id = str(i)
            else:
                self.image_id = f"0{i}"
            self.image_flip_list.append(f"flip{self.image_id}.png")
        self.image_jumpspin_list = []
        for i in range(0, 8):
            self.image_jumpspin_list.append(f"jumpspin{i}.png")
        self.image_flash_list = []
        for i in range(0, 5):
            self.image_flash_list.append(f"flash{i}.png")
        self.animation_time = 100
        self.animation=Animation(self.image_flip_list, False, False, self.animation_time) # §\label{srcAnimation0102}§
        self.image = self.animation.next()
        self.rect = self.image.get_rect()
        self.rect.center = (Settings.window['width'] // 2, Settings.window['height'] // 2)
        self.direction = Settings.directions["stop"]
        self.timer = Timer(self.animation_time)
        self.animation_run = False

    def update(self):
        if self.animation_run:
            self.image = self.animation.next()

class SamuraiAnimation(object):
    def __init__(self) -> None:
        super().__init__()
        os.environ['SDL_VIDEO_WINDOW_POS'] = "10, 50"
        pygame.init()
        self.screen = pygame.display.set_mode(Settings.dim())
        pygame.display.set_caption(Settings.title)
        self.clock = pygame.time.Clock()
        self.samurai = pygame.sprite.GroupSingle(Samurai())
        self.running = False

    def run(self) -> None:
        self.running = True
        while self.running:
            self.clock.tick(Settings.fps)
            self.watch_for_events()
            self.update()
            self.draw()
        pygame.quit()

    def watch_for_events(self) -> None:
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.running = False
                elif event.key == K_LEFT:
                    if self.samurai.sprite.animation.is_ended() or self.samurai.sprite.animation_run == False:
                        self.samurai.sprite.animation = Animation(self.samurai.sprite.image_flash_list, False, True, self.samurai.sprite.animation_time)
                        self.samurai.sprite.animation_run = True
                elif event.key == K_RIGHT:
                    if self.samurai.sprite.animation.is_ended() or self.samurai.sprite.animation_run == False:
                        self.samurai.sprite.animation = Animation(self.samurai.sprite.image_flash_list, False, False, self.samurai.sprite.animation_time)
                        self.samurai.sprite.animation_run = True
                elif event.key == K_DOWN:
                    if self.samurai.sprite.animation.is_ended() or self.samurai.sprite.animation_run == False:
                        self.samurai.sprite.animation = Animation(self.samurai.sprite.image_flip_list, False, False, self.samurai.sprite.animation_time)
                        self.samurai.sprite.animation_run = True
                elif event.key == K_SPACE:
                    if self.samurai.sprite.animation.is_ended() or self.samurai.sprite.animation_run == False:
                        self.samurai.sprite.animation = Animation(self.samurai.sprite.image_jumpspin_list, False, False, self.samurai.sprite.animation_time)
                        self.samurai.sprite.animation_run = True


    def update(self) -> None:
        self.samurai.update()

    def draw(self) -> None:
        self.screen.fill((200, 200, 200))
        self.samurai.draw(self.screen)
        pygame.display.flip()



if __name__ == '__main__':
    anim = SamuraiAnimation()
    anim.run()

