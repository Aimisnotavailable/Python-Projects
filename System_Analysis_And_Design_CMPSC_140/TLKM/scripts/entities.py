import pygame
import random
import math
from scripts.particles import Particles
from abc import ABC, abstractmethod
# from scripts.projectiles import Projectiles

class PhysicsEntities:
    
    def __init__(self, game, e_type, max_speed=0, pos=(0,0), size=(16,16)):
        self.game = game
        self.type = e_type
        self.pos = list(pos)
        self.size = size
        self.velocity = [0, 0]
        self.collisions = {'up' : False, 'down' : False, 'right' : False, 'left' : False}

        self.max_speed = max_speed
        self.action = ''
        self.last_action = ''
        self.anim_offset = [0, 0]
        self.flip = False
        self.jump = False
        self.air_time = 0

        self.last_movement = [0, 0]

        self.objects = []
        self.attacking = 0
        self.drag = 1
        self.track = 0
        self.combo = 0

        self.atk_type = ''
        self.attacked = 0

    def mask(self):
        return pygame.mask.from_surface(pygame.transform.flip(self.animation.img(), self.flip, False)).to_surface(setcolor=(185 ,11 ,11), unsetcolor=(0, 0, 0, 0))
    
    def sprite(self):
        return pygame.sprite.Group()
    
    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
    
    # def mask(self):
    #     return pygame.mask.from_surface(self.animation.img())
    
    def render(self, surf, offset=(0,0)):
        img = pygame.transform.flip(self.animation.img(), self.flip, False)
        self.anim_offset = [(img.get_width() - self.size[0]) * 1 if self.flip else 1, img.get_height() - self.size[1]]
        #print(self.anim_offset)
        #surf.blit(pygame.transform.flip(self.mask().to_surface(setcolor=(0, 255, 255), unsetcolor=(0, 0, 0)), self.flip, False), (self.pos[0] - offset[0] + self.anim_offset[0], self.pos[1] - offset[1] + self.anim_offset[1]))
        surf.blit(img if not self.attacked or (self.attacked % 2) == 0 else self.mask(), (self.pos[0] - offset[0] - self.anim_offset[0], self.pos[1] - offset[1] - self.anim_offset[1]))

    def update(self, tilemap, surf, movement=(0,0), offset=(0,0)):
        self.movement = movement
        self.collisions = {'up' : False, 'down' : False, 'right' : False, 'left' : False}
        self.frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1] )

        self.pos[0] += self.frame_movement[0] * self.drag
        entity_rect = self.rect()
        tile_data = tilemap.tiles_rect_around(self.rect())

        for i in range(len(tile_data['rects'])):
            rect = tile_data['rects'][i]
            color = tile_data['color'][i]
            if entity_rect.colliderect(rect):
                if self.frame_movement[0] > 0:
                    entity_rect.right = rect.left
                    self.collisions['right'] = True
                
                if self.frame_movement[0] < 0:
                    entity_rect.left = rect.right
                    self.collisions['left'] = True

                self.pos[0] = entity_rect.x

        self.pos[1] += self.frame_movement[1] * self.drag   
        entity_rect = self.rect()
        
        tile_data = tilemap.tiles_rect_around(self.rect())
        
        for i in range(len(tile_data['rects'])):
            rect = tile_data['rects'][i]
            color = tile_data['color'][i]

            # pygame.draw.rect(surf, (255,255,255), (self.pos[0] - offset[0], self.pos[1] - offset[1], self.size[0], self.size[1]))

            # pygame.draw.rect(surf, (255, 255, 255), (rect[0] - offset[0], rect[1] - offset[1], rect[2], rect[3]))
            if entity_rect.colliderect(rect):
                if int(self.drag):
                    spawn_particles = random.random() + int(abs(self.velocity[1]))
                else:
                    spawn_particles = False

                if self.frame_movement[1] > 0:
                    entity_rect.bottom = rect.top
                    self.collisions['down'] = True

                if self.frame_movement[1] < 0:
                    entity_rect.top = rect.bottom
                    self.collisions['up'] = True

                self.pos[1] = entity_rect.y

                # if self.type == 'player' or self.type == 'enemy':
                #     if spawn_particles > 0.6 and (self.collisions['down'] or self.collisions['up']):
                #         if self.action != 'idle':
                #             x = self.pos[0]
                #             if self.collisions['down']:
                #                 y = rect.top
                #                 angle = ((random.random() * math.pi) + math.pi)
                #             elif self.collisions['up']:
                #                 y = rect.bottom
                #                 angle = ((random.random()) * math.pi)

                #             speed = random.random() * random.random()
                #             self.game.particles.append(Particles(self.game, 'dust', angle, speed, (x, y), color_key=color))
                    
        water_loc_int = [int((self.pos[0] //tilemap.tile_size)), int((self.pos[1]//tilemap.tile_size))]
        water_loc = str(water_loc_int[0]) + ";" + str(water_loc_int[1])

        if water_loc in tilemap.water_map:
            self.drag = 0.6
            tilemap.propogate_wave(water_loc, water_loc_int, velocity=self.velocity, offset=offset, entity_rect=entity_rect)
        else:
            self.drag = min(1, self.drag + 0.01)
        
        if movement[0] > 0:
            self.flip = False
        elif movement[0] < 0:
            self.flip = True
        
        self.velocity[1] = min(5 * self.drag, self.velocity[1] + 0.1)

        if self.collisions['down']:
            self.jump = False
            self.air_time = 0
        else:
            self.air_time += 1

        if self.collisions['up'] or self.collisions['down']:
            self.velocity[1] = 0

        if self.running > 0:
            self.flip = False
            self.velocity[0] = min(self.max_speed, self.velocity[0] + 1)
        elif self.running < 0:
            self.flip = True
            self.velocity[0] = max(-self.max_speed, self.velocity[0] - 1)

        if self.velocity[0] > 0:
            self.velocity[0] = max(self.velocity[0] - 0.4, 0)
        elif self.velocity[0] < 0:
            self.velocity[0] = min(self.velocity[0] + 0.4, 0)
        self.animation.update()

        self.track = max(0, self.track - 1)

        self.attacked = max(0, self.attacked -1)

class NonobjEntities(PhysicsEntities):
    
    def set_action(self, action):
        if action != self.action:
            self.action = action
            if action != 'attack':
                self.animation = self.game.assets[self.type][self.action]['all'].copy()

    def attack(self, atk_type, combo):
        if atk_type != self.atk_type:
            self.atk_type = atk_type
            combo = 0

        anim = self.game.assets[self.type][self.action][atk_type]
        if combo < len(anim):
            self.animation = anim[combo].copy()

    # def perform_attack(self, atk_type, current_weapon):
    #     #if(self.air_time < 4):
    #     self.cooldown_time = current_weapon.attack_cooldowns[atk_type]
    #     self.attacking = self.cooldown_time
    #     self.current_weapon = current_weapon
    #     # self.initialize_weapon(atk_type, current_weapon)
    #     #self.set_action('attack')
    #     #else:
    #        # self.set_action('jump')

    # def load_atk_type(self, atk_type, current_weapon):
    #     pass 

    # def initialize_weapon(self, atk_type, current_weapon):
    #     if atk_type == "normal_attack" or atk_type == "charged_attack":
    #         self.objects.append({'img': current_weapon.particle_animation()[atk_type].copy(), 'pos' : self.pos, 'type' : 'attack_radius'})
    #         self.objects.append({'img' : current_weapon.weapon_animation()[atk_type].copy(), 'pos' : self.pos, 'type' : 'weapon'})
    #     elif atk_type == "throw_meele_attack":
    #         return
    #     elif atk_type == "shoot_attack":
    #         self.objects.append({'img' : current_weapon.weapon_animation().copy(), 'pos' : (self.rect().centerx + (-7 if self.flip else -3), self.rect().centery), 'type' : 'weapon'})
    #         self.game.projectiles.append(Projectiles(current_weapon.particle_animation()[atk_type].copy().img(), speed=(-5 if self.flip else 5), life=1000, pos=self.rect().center))

# class Enemy(NonobjEntities):
#     def __init__(self, game, pos, size=(16,15)):
#         super().__init__(game, 'enemy', pos, size)
#         self.set_action('idle')
#         self.walking = 0
#         self.current_hp = 5
#         self.max_hp = 5
#         self.attacked =0

#         self.hat = self.game.assets['enemy/hat'].copy()

#     def damage(self):
#         self.current_hp -=1
#         self.attacked = 30
#         self.velocity[1] = -2
#         self.flip = not self.flip

#     def update(self, tilemap, movement=(0,0), offset=(0, 0)):
#         if self.walking and self.action != 'damaged':
#             if tilemap.solid_check((self.rect().centerx + (-7 if self.flip else 7), self.pos[1] + 23)):
#                 if(self.collisions['right'] or self.collisions['left']):
#                     self.flip = not self.flip
#                 movement = (movement[0] + (-0.5 if self.flip else 0.5), movement[1])
#             else:
#                 self.flip = not self.flip
#                 self.velocity[0] = 0
#             self.walking = max(0, self.walking - 1)
#         elif random.random() < 0.01:
#             self.walking = random.randint(30, 120)
        
#         self.attacked -= 1

#         if self.attacked <= 0:
#             self.attacked = 0

#         if self.attacked > 0:
#             self.set_action('damaged')
#             movement = (movement[0] + (-0.3 if self.flip else 0.3), movement[1])
#         elif movement[0] != 0:
#             self.set_action('run')
#         else:
#             self.set_action('idle')
        
#         super().update(tilemap, movement)
    
#     def render(self, surf, offset=(0,0)):
#         super().render(surf, offset)
#         # pygame.draw.rect(surf, (255, 0, 0), pygame.Rect(self.pos[0] - offset[0], self.pos[1] - offset[1], 5 * (self.max_hp), 5))
#         # pygame.draw.rect(surf, (0, 255, 0), pygame.Rect(self.pos[0] - offset[0], self.pos[1] - offset[1], (5 * self.current_hp) + self.attacked//3, 5))
#         surf.blit(self.hat.img(), (self.pos[0] - offset[0], self.pos[1] - offset[1] - 4))
#         self.hat.update()

# class Player(NonobjEntities):

#     def __init__(self, game, pos, size=(8, 16)):
#         super().__init__(game,'player', pos, size)
#         self.set_action('idle')

#         self.attack_type = 0
#         self.atk_type = ''

#         self.is_initialized = False
#         self.charge_duration = 30

#         self.dashing = 0
#         self.dash_duration = 10
#         self.dash_multiplier = 1

#         self.atk_type_count_meele = 2
#         self.shooting = False
#         self.jumps = 1

#         self.teleporting = 0

#     def start_charge(self, is_initialized=False):
#         self.is_initialized = is_initialized
    
#     def dash(self):
#         if self.dashing >= 1:
#             self.velocity[0] = self.dash_velocity[0]
#             self.velocity[1] = self.dash_velocity[1]
#             if self.dashing == 1 or self.dashing == int((self.dash_duration * self.dash_multiplier)):
#                 for i in range(30):
#                     angle = (random.random() + 0.5) * math.pi * 2
#                     speed = (random.random() + 0.5) * 2
#                     self.game.sparks.append(Sparks(angle, speed, self.rect().center, self.current_weapon.color))
                
#             else:
#                 for i in range(4):
#                     angle = (random.random() - 0.5) * math.pi * 0.5 + (math.pi if not self.flip else 0)
#                     speed = (random.random() + 0.5) * 2
#                     self.game.sparks.append(Sparks(angle, speed, self.rect().center, self.current_weapon.color))

#             self.dashing -= 1
#         return self.dashing

    
#     def perform_attack(self, atk_type, current_weapon):
#         super().perform_attack(atk_type, current_weapon)

#         self.atk_type = atk_type
        

#         a_r = self.game.angle * (-1 if self.game.rotation.flip_x else 1)
#         angle = math.radians(a_r)
#         animation = self.current_weapon.particle_animation()[atk_type].copy()
#         img_rotation_angle = -a_r
#         if atk_type == "normal_attack":
#             self.game.projectiles.append(Projectiles(animation, img_rotation_angle, speed=2, angle=angle, life=15, pos=self.rect().center))
#             self.current_weapon.play_sound(variant=0, vol=0.5)
#         elif self.atk_type == "charged_attack":
#             self.dash_velocity = (math.cos(math.radians(a_r)) * 8, math.sin(math.radians(a_r)) * 5)
#             self.current_weapon.play_sound(variant=1, vol=1.0)
#         elif self.atk_type == "throw_meele_attack":
#             # self.track = self.cooldown_time
#             self.game.projectiles.append(Projectiles(animation, img_rotation_angle, speed=10, angle=angle, life=self.cooldown_time // 2, pos=self.rect().center, spawn=self.current_weapon))
#             self.current_weapon.play_sound(variant=2, vol=1.0)
#             self.game.zooming = self.cooldown_time // 2

#         elif self.atk_type == "shoot_attack":
#             for i in range(4):
#                 s_angle = random.random() - 0.5 + angle
#                 speed = random.random() + 2
#                 self.game.sparks.append(Sparks(angle=s_angle, speed=speed, pos=(math.cos(angle) * 15 + self.rect().center[0], math.sin(angle) * 15 + self.rect().center[1]), color=(255, 165, 30)))
#             self.recoil(2, 0.5)
#             self.game.projectiles.append(Projectiles(animation, img_rotation_angle, speed=10, angle=angle, life=100, pos=(math.cos(angle) * 10 + self.rect().center[0], math.sin(angle) * 10 + self.rect().center[1])))
#             self.current_weapon.play_sound(variant=0, vol=0.3)
#         elif self.atk_type == "splash_attack":
#             a_r -= 10
#             speed = random.random() + 10
#             for i in range(3):
#                 img_rotation_angle = -a_r
#                 a = math.radians(a_r)
                
#                 self.game.projectiles.append(Projectiles(animation, img_rotation_angle, speed, a, 100, pos=(math.cos(angle) * 10 + self.rect().center[0], math.sin(angle) * 10 + self.rect().center[1])))
#                 a_r += 10
#             for i in range(12):
#                 s_angle = random.random() - 0.5 + angle
#                 speed = random.random() + 2
#                 self.game.sparks.append(Sparks(angle=s_angle, speed=speed, pos=(math.cos(angle) * 15 + self.rect().center[0], math.sin(angle) * 15 + self.rect().center[1]), color=(255, 165, 30)))
#             self.current_weapon.play_sound(variant=1, vol=0.3)
#             self.recoil(5, 4)
                

#     def recoil(self, x_recoil, y_recoil):
#         self.velocity[0] = - math.cos(math.radians(self.game.angle)) * x_recoil
#         y_vel = math.sin(math.radians(self.game.angle * (1 if self.game.rotation.flip_x else -1))) * y_recoil
#         self.velocity[1] += y_vel 

#     def teleport(self, end_pos=[0, 0]):
#         self.teleporting = 21
#         self.set_action('fade')
#         self.pos = end_pos 

#     def cooldown(self, surf, offset=(0, 0)):
#         pos = self.rect().topleft
#         pygame.draw.rect(surf, (255, 255, 255), (pos[0] - offset[0], pos[1] - offset[1] - 10, (self.attacking/self.cooldown_time) * 20 , 5))

#     def update(self, tilemap, movement=(0,0), offset=(0, 0)):
#         super().update(tilemap, movement)

#         for pos in self.game.background.pos:
#             pos[0] += self.frame_movement[0] * 0.4
#             pos[1] += self.frame_movement[1] * 0.4

#         if self.collisions['down']:
#             self.jumps = 1
            
#         self.air_time += 1
#         self.attack_type = min(self.attack_type + 1, self.charge_duration * self.atk_type_count_meele - 1)
#         self.attacking = max(0, self.attacking - 1)
        
#         if not self.is_initialized:
#             self.attack_type = 0
#         if self.collisions['down']:
#             self.air_time = 0

#         if self.attacking > 0:
            
#             if self.attacking == 1:
#                 self.start_charge(is_initialized=False)
#                 self.set_action('idle')

#             if self.atk_type == "charged_attack":
#                 if self.attacking == 29:
#                     self.dashing = int(self.dash_duration * (1 + ((self.attack_type - self.charge_duration) / self.charge_duration) * 0.5))
#                     self.attack_type = 0
#                 if self.dashing:
#                     self.dash()
#                 else:
#                     self.velocity[0] = 0
#                     self.velocity[1] = 0

#         if not self.teleporting:

#             if (self.collisions['left'] or self.collisions['right']) and self.movement[0] != 0 and self.frame_movement[0] != 0:
#                 self.set_action('wall_slide')
#                 self.flip = not self.flip
#                 self.drag = 0.5
#                 self.jumps = 1
#             elif self.air_time > 4 + (4 * 1 - self.drag):
#                 self.set_action('jump')
#             elif self.movement[0] != 0:
#                 self.set_action('run')
#             else:
#                 self.set_action('idle')

#         self.teleporting = max(0, self.teleporting - 1)
        
#     def render(self, surf, offset=(0,0)):
        
#         if self.attacking:
#             self.cooldown(surf, offset)

#         # Charge tooltip
#         if self.is_initialized and self.attacking == 0:
#             pygame.draw.rect(surf, (255, 255, 255), (self.pos[0] - offset[0], self.pos[1] - offset[1] - 10, self.attack_type // 5, 3), 0, 2)
#             pygame.draw.rect(surf, (255, 0, 0) if self.attack_type < self.charge_duration else (0, 255, 0) if self.attack_type < self.charge_duration * self.atk_type_count_meele - 1 else (0, 0, 255), pygame.Rect(self.pos[0] - offset[0] - (self.charge_duration * self.atk_type_count_meele - 1 - self.attack_type) //5, self.pos[1] - offset[1] - 10, self.attack_type //5, 3))

#         # if(self.attacking != 0):
#         #     for object in self.objects:
#         #         if self.dashing <= 0:
#         #             surf.blit(pygame.transform.flip(object['img'].img(), self.flip, False), (object['pos'][0] - offset[0] + (-10 if self.flip else 10), object['pos'][1] - offset[1] - 5))
#         #         if (object['type'] == 'attack_radius'):
#         #             self.game.attack_rect = pygame.Rect(object['pos'][0] + (-10 if self.flip else 10), object['pos'][1], 16, 16)
#         #         object['img'].update()
#         #         if object['img'].done:
#         #             self.objects.remove(object)

#         if not self.dashing:
#             super().render(surf, offset)