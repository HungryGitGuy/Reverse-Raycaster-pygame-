import pygame, math

pygame.init()

win = pygame.display.set_mode((1300, 700))
win_width = win.get_width()
win_height = win.get_height()

class player:
    def __init__(self, x, y, direction=0, fov=90):
        """
        a class representing the player, the camera, ant the renderer
        :param x: position along the x axis
        :param y: position along the y axis
        :param direction: direction in degrees
        """
        self.p = pygame.Vector2(x, y)
        self.d = direction
        self.fov = fov

    def move_forward(self):
        self.p.x += (math.cos(math.radians(self.d)) * 5)
        self.p.y += (math.sin(math.radians(self.d)) * 5)
    def move_backward(self):
        self.p.x -= (math.cos(math.radians(self.d)) * 5)
        self.p.y -= (math.sin(math.radians(self.d)) * 5)

    def move_left(self):
        self.d -= 90
        self.move_forward()
        self.d += 90

    def move_right(self):
        self.d += 90
        self.move_forward()
        self.d -= 90


    def debug_draw(self):
        pygame.draw.rect(win, (0, 0, 255), (self.p.x - 5, self.p.y - 5, 10, 10))
        pygame.draw.line(win, (0, 0, 255), (self.p.x, self.p.y), (self.p.x + (math.cos(math.radians(self.d)) * 30), self.p.y + (math.sin(math.radians(self.d)) * 30)), 1)

    # renderer+camera functions below

    def angle_to_screenspace(self, theta):
        """

        :param theta:
        :return: -1 if out of the fov. otherwise a value between 0 and 1
        """
        L = round(self.d - (self.fov / 2))
        R = round(self.d + (self.fov / 2))
        pygame.draw.line(win, (255, 0, 255), (self.p.x, self.p.y), (self.p.x + (math.cos(math.radians(L)) * 300), self.p.y + (math.sin(math.radians(L)) * 300)), 1)
        pygame.draw.line(win, (255, 0, 255), (self.p.x, self.p.y), (self.p.x + (math.cos(math.radians(R)) * 300), self.p.y + (math.sin(math.radians(R)) * 300)), 1)
        # below is code for culling based on angle, not position on screen. may be worth revisiting for optimising complex scenes or polygon based wall drawing
        #if L < 0:
        #    print(f"L was too Large")
        #    L += 360
        #    theta += 360
        #if R < 0:
        #    print(f"R was too small")
        #    theta += 360
        #    R += 360
        #if theta > R: # was one statement but had issues
        #    if theta < L:
        #        print(f"culled, theta {theta} < L {L} or  theta {theta} > R{R}")
        #        return -1
        U = theta - L # prior to this line you would start at 0 degrees, turn theta degrees, and be pointing in the correct
                      # direction. to normalise the value, I had to make it so you start at L degrees ans turn theta degrees
                      # to look in the same direction
        U /= self.fov
        return U

    def draw_point(self, point):
        # calculating x
        angle = pygame.Vector2(0, 0).angle_to((self.p.x - point.p.x, self.p.y - point.p.y)) + 180
        pygame.draw.line(win, (0, 0, 255), (self.p.x, self.p.y), (self.p.x + (math.cos(math.radians(angle)) * 200), self.p.y + (math.sin(math.radians(angle)) * 200)), 1)
        #pygame.draw.line(win, (0, 100, 255), (0, 0), ((math.cos(math.radians(angle - self.d)) * 200), (math.sin(math.radians(angle - self.d)) * 200)), 1) # line from origin of the window
        #
        #angle = point.get_angle((self.p.x, self.p.y))
        pygame.draw.line(win, (0, 0, 0), (self.p.x, self.p.y), (self.p.x, self.p.y), 2)
        normalised_x = self.angle_to_screenspace(angle) # passes the angle from the point to the player
        draw_x = normalised_x * win_width

        distance = self.p.distance_to(point.p)

        # just know there's some unnecessary math here
        height = (35000 / distance) + 350
        y = round(-350 - height) + 1000
        height -= y

        pygame.draw.rect(win, (255, 255, 0), (draw_x, y, 10, height))
    def drawn_point(self, point):
        # calculating x
        angle = point.get_angle((self.p.x, self.p.y))
        normalised_x = self.angle_to_screenspace(angle)
        draw_x = normalised_x * win_width

        #calculating y and height (not sure what these are for)
        #width = self.p.x - point.p.x if self.p.x - point.p.x > 0 else self.p.x - point.p.y * -1
        #height = self.p.y - point.p.y if self.p.y - point.p.y > 0 else self.p.y - point.p.y * -1

        distance = self.p.distance_to(point.p)

        # I just know there's some unnecessary math here, but it's been a while since I wrote this and idk where the crap is
        height = (4000 / distance) + 350
        y = round(-350 - height) + 1000
        height -= y
        height *= 1.2

        return [draw_x, y, height]

    def draw_wall(self, w):
        left = w.p1
        right = w.p2

        left = self.drawn_point(left)
        right = self.drawn_point(right)

        if left[0] > right[0]:
            return
            #right = self.drawn_point(w.p1)
            #left = self.drawn_point(w.p2)

        Lheight = left[2]
        Rheight = right[2]


        # [draw_x, y, height]
        #x1 = left[0]
        #x2 = right[0] + 1
        #for x in range(x1, x2 + 1):
        #    a1 = (x - x1) / (x2 - x1) * (y2 - y1) + y1
        #    a2 = (a1 - y1) / (y2 - y1) * (x2 - x1) + x1
        #    pygame.draw.line(win, (200, 20, 50))
        #    foo(a1, a2)

        #print(top_left, top_right, bottom_right, bottom_left)

#        pygame.draw.polygon(win, (255, 255, 0), [top_left, top_right, bottom_left, bottom_right])
        pygame.draw.polygon(win, (255, 255, 0), [(left[0], left[1]), (left[0], right[2]), (right[0], left[2]), (right[0], right[1])]) # replace with lerp
#        pygame.display.update()


class Point:
    points = []
    def __init__(self, x, y, col):
        """
        A base class for anything that needs to be represented by a point in space.
        :param x: position along the x axis
        :param y: position along the y axis
        :param col: colour (r, g, b)
        :return:
        """
        self.p = pygame.Vector2(x, y)
        self.col = col
        self.lpos = len(Point.points) - 1

        Point.points.append(self)

    def begone(self):
        try:
            Point.points.pop(self.lpos)
        except Exception:
            Point.points = []

    def debug_draw(self, scale=3):
        pygame.draw.rect(win, self.col, (self.p.x - (scale * 0.5), self.p.y - (scale * 0.5), scale, scale))

    def get_angle(self, pos):
        pos = pygame.Vector2(pos)
        angle = self.p.angle_to(pos) + 180

        return angle


class Wall:
    walls = []
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        self.lpos = len(Wall.walls)

        Wall.walls.append(self)

    def begone(self):
        self.p1.begone()
        self.p2.begone()
        Wall.walls.pop(self.lpos)

    def debug_draw(self, size=1, points=True):
        pygame.draw.line(win, (255, 0, 0), (self.p1.p.x, self.p1.p.y), (self.p2.p.x, self.p2.p.y), size)
        if points:
            self.p1.debug_draw()
            self.p2.debug_draw()


# misc essential functions -------------------------------------------------------------------------#
pl = player(win_width / 2, win_height / 2)
follow = True
def redrawgamewindow(p1=0, p2=0):
    win.fill((255, 255, 255))
    for w in Wall.walls:
        w.debug_draw()
        pl.draw_wall(w)
    if walling and bool(p1 or p2):
        pygame.draw.line(win, (0, 255, 0), p1, p2)
    if len(Point.points) > 0:
        for p in Point.points:
            pl.draw_point(p)
    pl.debug_draw()
    pygame.display.update()


# mainloop -----------------------------------------------------------------------------------------#
run = True
walling = False
clock = pygame.time.Clock()

# default point, as of 7/16/2023, 292 lines, this is the only point that works properly and any changes to the points list will irreversibly break it until restart
bPoint = Point(0, 0, (255, 0, 0))

mouse_pos = pygame.mouse.get_pos()
mouse_x = mouse_pos[0]
mouse_y = mouse_pos[1]

del_cooldown = False

while run:
    #hpefully getting this working properly also fixes the camera issues
    if follow:
        pl.d = Point.points[-1].get_angle((pl.p.x, pl.p.y))

    clock.tick(60)

    redrawgamewindow()

    mouse_pos = pygame.mouse.get_pos()
    mouse_x = mouse_pos[0]
    mouse_y = mouse_pos[1]

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        # button down, beginning a line button up, ending a line
        if event.type == pygame.MOUSEBUTTONDOWN:
            walling = True
            bPoint = Point(mouse_x, mouse_y, (255, 0, 0))

        if event.type == pygame.MOUSEBUTTONUP:
            ePoint = Point(mouse_x, mouse_y, (255, 0, 0))

            Wall(bPoint, ePoint)
            walling = False

    keys = pygame.key.get_pressed()
#input ------------------------------------------------------------------------------------------#
    if keys[pygame.K_ESCAPE]:
        run = False

    if keys[pygame.K_DELETE] and del_cooldown and bool(len(Wall.walls)):
        Wall.walls[-1].begone()
        del_cooldown = False
    elif keys[pygame.K_DELETE]:
        del_cooldown = False
    else: del_cooldown = True

    if keys[pygame.K_w]:
        pl.move_forward()
    if keys[pygame.K_a]:
        pl.move_left()
    if keys[pygame.K_s]:
        pl.move_backward()
    if keys[pygame.K_d]:
        pl.move_right()

    if keys[pygame.K_LEFT]:
        pl.d -= 5
    if keys[pygame.K_RIGHT]:
        pl.d += 5
    if pl.d > 360:
        pl.d -= 360
    elif pl.d < 0:
        pl.d += 360

    if keys[pygame.K_SPACE]:
        follow = not follow
    if keys[pygame.K_q]:
        print(pl.d)

pygame.quit()

"""
TODO:
2: Fix drawing of points when pl.d ~= 360 or 0. if it starts >360, and a point goes past it to 0, add 360 to the angle, and vise-versa
3: fix walls. Preferably interpolate in between the plane edges to enable easy retro texture mapping, but if low-res 
openGL polygon texture mapping is an option it's probably better.
4: If openGL was learned: floor and roof textures. Else: sprites
"""

"""
DONE:
1: point class (~146), points only work properly if their position is 0, 0. try sub point's pos from point and player pos when calculating screenspace pos?
details: (7/19/2023), There was an issue with how the angle was computed so it took the angle of the vector to the origin and treated that like the angle from the vector. 
I found out about this by drawing a line from the origin towards any given point, and fixed it by altering the vectors that are given to the get_angle_to() function. 
"""
