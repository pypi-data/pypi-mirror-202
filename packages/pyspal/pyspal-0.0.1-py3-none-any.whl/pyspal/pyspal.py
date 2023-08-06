import pygame
import playsound
import time
import os
import ast




class Pyspal:
    def __init__(self, resolution = (800, 600), bg = True, fps = 60, vsync = True, title = 'Pyspal Game Window', bgc = (0, 0, 0)):
        pygame.display.init()
        pygame.display.quit()

        # Initialize Pygame
        pygame.init()
        self.res = resolution
        self.display = pygame.display.set_mode(self.res, pygame.NOFRAME, vsync = vsync)
        pygame.display.set_caption(title)
        self.cwd = os.getcwd()
        os.chdir('pyspal/')
        self.quit_image = pygame.image.load("quit_button.png")
        self.quit_image = pygame.transform.scale(self.quit_image, (50, 24))
        os.chdir(self.cwd)
        # Get image dimensions
        self.qimage_x, self.qimage_y = self.quit_image.get_size()
        # Define image position
        self.qimage_x = self.res[0] - self.qimage_x
        self.qimage_y = 0
        self.quit_rect = pygame.Rect((self.qimage_x, self.qimage_y), (50, 24))
        self.objects = {}
        self.ids = []
        self.bg = bg
        import time

        self.prev_time = time.time()
        self.FPS = fps
        self.STEP_TIME = 1./self.FPS
        self.running = True
        self.count = 0
        self.accum = 0
        self.mouseleftdown = False
        self.mouserightdown = False
        self.colors = {
            'WHITE': (255, 255, 255),
            'BLACK': (0, 0, 0),
            'RED': (255, 0, 0),
            'GREEN': (0, 255, 0),
            'BLUE': (0, 0, 255),
            'YELLOW': (255, 255, 0),
            'MAGENTA': (255, 0, 255),
            'CYAN': (0, 255, 255),
            'ORANGE': (255, 165, 0),
            'GRAY': (128, 128, 128)
        }
        self.img_objects = {}
        self.img_ids = []
        self.mods = {}
        self.gravity = 6.32
        self.animations = {}
        self.anim_ids = []
        self.font = pygame.font.SysFont('Arial', 24)
        self.holding = ''
        self.holding_img = ''
        self.bgc = bgc
        self.gravity = 3.84
        self.FRICTION = 0.01
        self.texts = {}
        self.keyboard = {
            "escape": False,
            "f1": False,
            "f2": False,
            "f3": False,
            "f4": False,
            "f5": False,
            "f6": False,
            "f7": False,
            "f8": False,
            "f9": False,
            "f10": False,
            "f11": False,
            "f12": False,
            "backspace": False,
            "tab": False,
            "return": False,
            "space": False,
            "delete": False,
            "shift": False,
            "ctrl": False,
            "alt": False,
            "left": False,
            "right": False,
            "up": False,
            "down": False,
            "0": False,
            "1": False,
            "2": False,
            "3": False,
            "4": False,
            "5": False,
            "6": False,
            "7": False,
            "8": False,
            "9": False,
            "a": False,
            "b": False,
            "c": False,
            "d": False,
            "e": False,
            "f": False,
            "g": False,
            "h": False,
            "i": False,
            "j": False,
            "k": False,
            "l": False,
            "m": False,
            "n": False,
            "o": False,
            "p": False,
            "q": False,
            "r": False,
            "s": False,
            "t": False,
            "u": False,
            "v": False,
            "w": False,
            "x": False,
            "y": False,
            "z": False
        }
        self.grounded = []
        self.background_surface = pygame.Surface(self.res)
        self.mousedown = Trigger()
        self.mouseup = Trigger()
        self.holdings = []
        self.drupa = False
        self.holdingx = []
        

    def update(self):
        # fps reduction and vsync
        self.current_time = time.time()
        self.dt = self.current_time - self.prev_time
        self.accum += self.dt
        self.count += 1
        if self.accum >= 1.0:
            self.accum -= 1.0
            print(self.count)
            self.count = 0

        self.prev_time = self.current_time
        self.sleep_time = self.STEP_TIME - self.dt
        if self.sleep_time > 0:
            time.sleep(self.sleep_time)


        #updating the background
        if self.bg:
            self.display.fill(self.bgc)
        #region updating the objects
        
        for a in self.img_ids:
            tmp = pygame.transform.scale(self.img_objects[a][1], self.img_objects[a][6])
            self.display.blit(tmp, (self.img_objects[a][3], self.img_objects[a][4]))
        #endregion

        # drawing the important images & buttons
        self.display.blit(self.quit_image, (self.qimage_x, self.qimage_y))

        # events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.mousedown.t()
            if event.type == pygame.MOUSEBUTTONUP:
                self.mouseup.t()
            self.drupa = event.type == pygame.MOUSEBUTTONDOWN

            #region keyboard keys
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.keyboard["escape"] = True
                elif event.key == pygame.K_F1:
                    self.keyboard["f1"] = True
                elif event.key == pygame.K_F2:
                    self.keyboard["f2"] = True
                elif event.key == pygame.K_F3:
                    self.keyboard["f3"] = True
                elif event.key == pygame.K_F4:
                    self.keyboard["f4"] = True
                elif event.key == pygame.K_F5:
                    self.keyboard["f5"] = True
                elif event.key == pygame.K_F6:
                    self.keyboard["f6"] = True
                elif event.key == pygame.K_F7:
                    self.keyboard["f7"] = True
                elif event.key == pygame.K_F8:
                    self.keyboard["f8"] = True
                elif event.key == pygame.K_F9:
                    self.keyboard["f9"] = True
                elif event.key == pygame.K_F10:
                    self.keyboard["f10"] = True
                elif event.key == pygame.K_F11:
                    self.keyboard["f11"] = True
                elif event.key == pygame.K_F12:
                    self.keyboard["f12"] = True
                elif event.key == pygame.K_BACKSPACE:
                    self.keyboard["backspace"] = True
                elif event.key == pygame.K_TAB:
                    self.keyboard["tab"] = True
                elif event.key == pygame.K_RETURN:
                    self.keyboard["return"] = True
                elif event.key == pygame.K_SPACE:
                    self.keyboard["space"] = True
                elif event.key == pygame.K_DELETE:
                    self.keyboard["delete"] = True
                elif event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                    self.keyboard["shift"] = True
                elif event.key == pygame.K_LCTRL or event.key == pygame.K_RCTRL:
                    self.keyboard["ctrl"] = True
                elif event.key == pygame.K_LALT or event.key == pygame.K_RALT:
                    self.keyboard["alt"] = True
                elif event.key == pygame.K_LEFT:
                    self.keyboard["left"] = True
                elif event.key == pygame.K_RIGHT:
                    self.keyboard["right"] = True
                elif event.key == pygame.K_UP:
                    self.keyboard["up"] = True
                elif event.key == pygame.K_DOWN:
                    self.keyboard["down"] = True
                elif event.key >= pygame.K_0 and event.key <= pygame.K_9:
                    num = event.key - pygame.K_0
                    self.keyboard[str(num)] = True
                elif event.key >= pygame.K_a and event.key <= pygame.K_z:
                    char = chr(event.key)
                    self.keyboard[char] = True
            # Check for key releases
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    self.keyboard["escape"] = False
                elif event.key == pygame.K_F1:
                    self.keyboard["f1"] = False
                elif event.key == pygame.K_F2:
                    self.keyboard["f2"] = False
                elif event.key == pygame.K_F3:
                    self.keyboard["f3"] = False
                elif event.key == pygame.K_F4:
                    self.keyboard["f4"] = False
                elif event.key == pygame.K_F5:
                    self.keyboard["f5"] = False
                elif event.key == pygame.K_F6:
                    self.keyboard["f6"] = False
                elif event.key == pygame.K_F7:
                    self.keyboard["f7"]
                elif event.key == pygame.K_F8:
                    self.keyboard["f8"] = False
                elif event.key == pygame.K_F9:
                    self.keyboard["f9"] = False
                elif event.key == pygame.K_F10:
                    self.keyboard["f10"] = False
                elif event.key == pygame.K_F11:
                    self.keyboard["f11"] = False
                elif event.key == pygame.K_F12:
                    self.keyboard["f12"] = False
                elif event.key == pygame.K_BACKSPACE:
                    self.keyboard["backspace"] = False
                elif event.key == pygame.K_TAB:
                    self.keyboard["tab"] = False
                elif event.key == pygame.K_RETURN:
                    self.keyboard["return"] = False
                elif event.key == pygame.K_SPACE:
                    self.keyboard["space"] = False
                elif event.key == pygame.K_DELETE:
                    self.keyboard["delete"] = False
                elif event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                    self.keyboard["shift"] = False
                elif event.key == pygame.K_LCTRL or event.key == pygame.K_RCTRL:
                    self.keyboard["ctrl"] = False
                elif event.key == pygame.K_LALT or event.key == pygame.K_RALT:
                    self.keyboard["alt"] = False
                elif event.key >= pygame.K_0 and event.key <= pygame.K_9:
                    num = event.key - pygame.K_0
                    self.keyboard[str(num)] = False
                elif event.key >= pygame.K_a and event.key <= pygame.K_z:
                    char = chr(event.key)
                    self.keyboard[char] = False
            #endregion
        for i in self.ids:
            if self.objects[i][3] == 'enabled':
                self.objects[i][2] = (self.objects[i][0].x, self.objects[i][0].y)
                self.objects[i][9]['bottomcenter'] = (self.objects[i][0].center[0], self.objects[i][0].bottom - 2)
                if self.objects[i][10] > 0.0:
                    self.objects[i][10] -= 0.1
                if self.objects[i][10] < 0.0:
                    self.objects[i][10] += 0.1
                if self.objects[i][11] > 0.0:
                    self.objects[i][11] -= self.objects[i][12]
                if self.objects[i][11] < 0.0:
                    self.objects[i][11] += self.objects[i][12]
                pygame.draw.rect(self.display, self.objects[i][1], pygame.Rect(self.objects[i][2], (self.objects[i][0].w, self.objects[i][0].h)))
                
            if self.objects[i][3] == 'disabled':
                pygame.draw.rect(self.display, self.objects[i][1], pygame.Rect((6000, 6000), (self.objects[i][0].w, self.objects[i][0].h)))
            if 'phys' in self.mods[i]:
                dragging = False
                if 'dynamic' in self.mods[i]:
                    self.phys(i)
                if 'holdableffffffff' in self.mods[i]:
                    if self.drupa and self.objects[i][0].collidepoint(pygame.mouse.get_pos()):
                        if not i in self.holdingx:
                            self.holdingx.append(i)
                        if self.mouseleftdown and i in self.holdingx:
                            if not i in self.holdings:
                                self.holdings.append(i)
                                self.reset_force(i)
                                self.reset_vel(i)
                                if not i in self.holdings:
                                    self.holdings.append(i)
                                    self.reset_force(i)
                                    self.reset_vel(i)
                                rel = self.get_relative_mouse_pos()
                                self.set_x(i, self.get_mouse_pos()[0] - 25)
                                self.set_y(i, self.get_mouse_pos()[1] - 25)
                                if rel[0] < 0:
                                    self.add_force(i, [rel[0] + self.get_mass(i), rel[1] - 10])
                                if rel[0] > 0:
                                    self.add_force(i, [rel[0] - self.get_mass(i), rel[1] - 10])
                                if not self.mouseleftdown and i in self.holdings:
                                    self.holdings.pop(self.holdings.index(i))
                            rel = self.get_relative_mouse_pos()
                            self.set_x(i, self.get_mouse_pos()[0] - 25)
                            self.set_y(i, self.get_mouse_pos()[1] - 25)
                            if rel[0] < 0:
                                self.add_force(i, [rel[0] + self.get_mass(i), rel[1] - 10])
                            if rel[0] > 0:
                                self.add_force(i, [rel[0] - self.get_mass(i), rel[1] - 10])
                        if not self.mouseleftdown and i in self.holdings:
                            self.holdings.pop(self.holdings.index(i))
                        if not self.mouseleftdown and i in self.holdingx:
                            self.holdingx.pop(self.holdingx.index(i))
            print(self.holdings)
        # custom events
        if self.mouseleftdown:
            if self.quit_rect.collidepoint(pygame.mouse.get_pos()):
                try:
                    pygame.quit()
                except:
                    print('Quitting!')
        
        for v in self.ids:
            if self.objects[v][0].collidepoint(self.get_mouse_pos()):
                self.holding = v
            else:
                self.holding = ''
        for z in self.img_ids:
            if pygame.Rect((self.img_objects[z][3], self.img_objects[z][4]), self.img_objects[z][1].get_size()).collidepoint(self.get_mouse_pos()):
                self.img_holding = z
            else:
                self.img_holding = ''

        # user events
        try:
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.mouseleftdown = True
            else:
                self.mouseleftdown = False
            if pygame.mouse.get_pressed(num_buttons=3)[2]:
                self.mouserightdown = True
            else:
                self.mouserightdown = False
        except:
            print()

        # update the screen
        try:
            pygame.display.update()
        except:
            print()

    # functions
    def draw_rect(self, id, position, scale, color, mods = [], mass = 1):
        self.objects[id] = [pygame.draw.rect(self.display, color, pygame.Rect(position, scale)), color, position, 'enabled', 4, 5, 'rect', scale, [0.0, 0.0], {}, 0.0, 0.0, mass]
        self.ids.append(id)
        self.mods[id] = mods
    def draw_img(self, id, position, path, scale = (100, 100)):
        temp_img = pygame.image.load(path)
        self.img_objects[id] = [self.display.blit(temp_img, position), temp_img, position, position[0], position[1], 'img', scale]
        self.img_ids.append(id)

    def set_x(self, id, xval):
        self.objects[id][0].x = xval
    
    def set_y(self, id, yval):
        self.objects[id][0].y = yval

    def get_x(self, id):
        return self.objects[id][0].x
    
    def get_y(self, id):
        return self.objects[id][0].y
    
    def get_mouse_pos(self):
        return pygame.mouse.get_pos()
    
    def get_color(self):
        
        return self.colors
    
    def set_x_img(self, id, xval):
        self.img_objects[id][3] = xval
    def set_y_img(self, id, yval):
        self.img_objects[id][4] = yval

    def get_x_img(self, id):
        return self.img_objects[id][3]
    def get_y_img(self, id):
        return self.img_objects[id][4]
    
    def collide(self, id1, id2):
        rect1 = self.objects[id1][0]
        rect2 = self.objects[id2][0]
        if rect1.colliderect(rect2):
            return True
        else:
            return False
    def collides(self, id1):
        idx = [False, []]
        colis = []
        trus = []
        rect1 = self.objects[id1][0]
        
        for u in self.ids:
            if not u == id1 and not 'nocollider' in self.mods[u]:
                if rect1.colliderect(pygame.Rect((self.objects[u][2][0], self.objects[u][2][1]), (self.objects[u][7][0], self.objects[u][7][1]))):
                    if idx[0] == False:
                        idx[0] = True
                        idx[1].append(u)

                    if rect1.colliderect(pygame.Rect((self.objects[u][2][0], self.objects[u][2][1]), (self.objects[u][7][0], self.objects[u][7][1]))):
                        # Determine the direction of the collision
                        
                        if rect1.left < pygame.Rect((self.objects[u][2][0], self.objects[u][2][1]), (self.objects[u][7][0], self.objects[u][7][1])).right and rect1.right < pygame.Rect((self.objects[u][2][0], self.objects[u][2][1]), (self.objects[u][7][0], self.objects[u][7][1])).right:
                            colis.append('right')
                        if rect1.bottom > pygame.Rect((self.objects[u][2][0], self.objects[u][2][1]), (self.objects[u][7][0], self.objects[u][7][1])).top and rect1.top > pygame.Rect((self.objects[u][2][0], self.objects[u][2][1]), (self.objects[u][7][0], self.objects[u][7][1])).top:
                            colis.append('top')
                        if rect1.top < pygame.Rect((self.objects[u][2][0], self.objects[u][2][1]), (self.objects[u][7][0], self.objects[u][7][1])).bottom and rect1.bottom < pygame.Rect((self.objects[u][2][0], self.objects[u][2][1]), (self.objects[u][7][0], self.objects[u][7][1])).bottom:
                            colis.append('bottom')
                        if pygame.Rect((self.objects[u][2][0], self.objects[u][2][1]), (self.objects[u][7][0], self.objects[u][7][1])).collidepoint(rect1.center):
                            colis.append('center')
                        if pygame.Rect((self.objects[u][2][0], self.objects[u][2][1]), (self.objects[u][7][0], self.objects[u][7][1])).collidepoint(self.objects[id1][9]['bottomcenter']):
                            colis.append('bc')
        return [idx[0], colis, idx[1]]
            
                
        
    def apply_force(self, force_direction, force_scale=0.01, force_limit=10):
        # calculate the force to apply
        force_magnitude = min(force_direction.length() * force_scale, force_limit)
        self.force = force_direction.normalize() * force_magnitude

    def clicked(self, id):
            if self.mousedown:
                if self.objects[id][0].collidepoint(self.get_mouse_pos()):
                    return True
            
            
    def img_clicked(self, id):
        if self.mouseleftdown:
            # check if the mouse is over the object
            if pygame.Rect((self.img_objects[id][3], self.img_objects[id][4]), self.img_objects[id][6]).collidepoint(self.get_mouse_pos()):
                return True
            
    def create_animation(self, id, moves):
        #moves = ['self.set_y(^, blah blah)'] ^ = object id blah blah blah blah
        animation = [moves, id]
        self.animations[id] = animation
        self.anim_ids.append(id)

    def animation(self, anim_id, obj_id):
        for j in self.animations[anim_id][0]:
            exec(j.replace('^', obj_id))

    def draw_text(self, id, position, textx, color = (255, 255, 255), scale = 10):
        #scales = (len(textx) * 15 + scale, 27 + scale)
        self.font = pygame.font.SysFont('Arial', scale)
        text = self.font.render(textx, True, color)
        # Draw text on screen
        self.img_objects[id] = [self.display.blit(text, position), text, position, position[0], position[1], 'img', text.get_size()]
        self.img_ids.append(id)

    def enabled(self, id, yn):
        if yn:
            self.objects[id][3] = 'enabled'
        elif yn == False:
            self.objects[id][3] = 'disabled'
        else:
            self.objects[id][3] = 'enabled'

    def change_img(self, id, path):
        self.objects[id][2] = pygame.image.load(path)
    def get_center(self, id):
        return self.objects[id][0].center
    def phys(self, id):
        if not self.collides(id)[0]:
            #self.set_y(id, self.get_y(id) + self.gravity)
            self.add_vel(id, (0, self.gravity))
        else:
            for h in self.collides(id)[2]:
                if 'phys' in self.mods[h] and 'dynamic' in self.mods[h] and not 'bottom' in self.collides(id)[2]:
                    print('adf')
                    self.add_force(h, [self.objects[id][10], self.objects[id][11]])
            if 'bottom' in self.collides(id)[1]:
                self.reset_vel(id)

            
                
            else:
                #self.set_y(id, self.get_y(id) + self.gravity)
                self.add_vel(id, (0, self.gravity))
            if 'bottom' in self.collides(id)[1] and 'bc' in self.collides(id)[1]:
                self.set_y(id, -1 + self.get_y(id))
            
        self.set_y(id, self.objects[id][8][1] + self.get_y(id))
        self.set_x(id, self.objects[id][8][0] + self.get_x(id))
        print(self.objects[id][10], self.objects[id][11])
        self.set_y(id, self.objects[id][11] + self.get_y(id))
        self.set_x(id, self.objects[id][10] + self.get_x(id))

    def add_vel(self, id, velocity):
        self.objects[id][8] = velocity

    def reset_vel(self, id):
        self.objects[id][8] = (0.0, 0.0)
    def add_force(self, id, force):
        self.objects[id][10] = force[0]
        self.objects[id][11] = force[1]

    def reset_force(self, id):
        self.objects[id][10] = 0.0
        self.objects[id][11] = 0.0
        self.objects[id][8] = [0.0, 0.0]

    def get_relative_mouse_pos(self):
        return pygame.mouse.get_rel()
    
    def get_mass(self, id):
        return self.objects[id][12]

class Trigger:
    def __init__(self):
        self.triggered = False
        self.used = False

    def t(self):
        self.triggered = True
    
    def untrigger(self):
        if self.used:
            self.used = False
            self.triggered = False

    def __bool__(self):
        self.used = True
        if self.triggered:
            self.untrigger()
            return True
        else:
            self.untrigger()
            return False
            
    
