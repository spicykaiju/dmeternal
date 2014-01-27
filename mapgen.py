import pygame
import random
import context
import animobs
import maps
import waypoints

class Plasma( object ):
    """Creates a plasma; cels have value from 0.0 to 1.0."""
    # Converted to Python from https://github.com/jseyster/plasmafractal/blob/master/Plasma.java
    def __init__( self, noise=5.0, width=129, height=129 ):
        self.noise = noise
        self.width = width
        self.height = height
        self.map = [[ float()
            for y in range(height) ]
                for x in range(width) ]
        self.divide_grid(0,0,width,height,random.random(),random.random(),random.random(),random.random())

    def displace( self, mag ):
        """Provide a random displacement of up to mag magnitude."""
        max_disp = mag * self.noise / ( self.width + self.height )
        return ( random.random() - 0.5 ) * max_disp

    def divide_grid( self,x,y,width,height,c1,c2,c3,c4 ):
        """Recursively divide up the plasma map."""
        # x,y,width,height describe the area currently being developed
        # c1,c2,c3,c4 are the four corner heights.

        nu_width = width/2
        nu_height = height/2

        if (width > 1) or (height > 1):
            middle = sum( (c1,c2,c3,c4) ) / 4 + self.displace( nu_width + nu_height )
            edge1 = sum((c1,c2))/2
            edge2 = sum((c2,c3))/2
            edge3 = sum((c3,c4))/2
            edge4 = sum((c4,c1))/2

            if middle < 0.0:
                middle = 0.0
            elif middle > 1.0:
                middle = 1.0

            self.divide_grid( x, y, nu_width, nu_height, c1, edge1, middle, edge4);
            self.divide_grid( x + nu_width, y, nu_width, nu_height, edge1, c2, edge2, middle);
            self.divide_grid( x + nu_width, y + nu_height, nu_width, nu_height, middle, edge2, c3, edge3);
            self.divide_grid( x, y + nu_height, nu_width, nu_height, edge4, middle, edge3, c4);

        else:
            # We are done! Just set the midpoint as average of 4 corners.
            self.map[int(x)][int(y)] = sum( (c1,c2,c3,c4) ) / 4

    def draw( self, screen ):
        for x in range( self.width ):
            for y in range( self.height ):
                pygame.draw.rect(screen,(255*self.map[x][y],255*self.map[x][y],127+128*self.map[x][y]),pygame.Rect(x*2,y*2,2,2) )

    def draw_layers( self, screen, w_el=0.3, l_el=0.5 ):
        for x in range( self.width ):
            for y in range( self.height ):
                if self.map[x][y] < w_el:
                    pygame.draw.rect(screen,(0,0,150),pygame.Rect(x*2,y*2,2,2) )
                elif self.map[x][y] < l_el:
                    pygame.draw.rect(screen,(150,200,0),pygame.Rect(x*2,y*2,2,2) )
                else:
                    pygame.draw.rect(screen,(50,250,100),pygame.Rect(x*2,y*2,2,2) )


#  *******************
#  ***   ANCHORS   ***
#  *******************
# Each anchor function takes two rect: a parent and a child.
# The child is arranged relative to the parent.

def northwest(par,chi):
    chi.topleft = par.topleft

def north( par,chi ):
    chi.midtop = par.midtop

def northeast(par,chi):
    chi.topright = par.topright

def west(par,chi):
    chi.midleft = par.midleft

def middle( par,chi):
    chi.center = par.center

def east(par,chi):
    chi.midright = par.midright

def southwest(par,chi):
    chi.bottomleft = par.bottomleft

def south( par,chi ):
    chi.midbottom = par.midbottom

def southeast(par,chi):
    chi.bottomright = par.bottomright

#  ********************
#  ***   MUTATORS   ***
#  ********************

class CellMutator( object ):
    """Uses cellular automata to mutate the maze."""
    def __init__( self, passes=5, do_carving=True, noise_throttle=25 ):
        self.passes = passes
        self.do_carving = do_carving
        self.noise_throttle = max( noise_throttle, 10 )

    DO_NOTHING, WALL_ON, WALL_OFF = range( 3 )

    def num_nearby_walls( self, gb, x0, y0 ):
        n = 0
        for x in range(x0-1,x0+2):
            for y in range(y0-1,y0+2):
                if gb.on_the_map(x,y):
                    if gb.map[x][y].wall:
                        n += 1
                else:
                    n += 1
        return n

    ANGDIR = ( (-1,-1), (0,-1), (1,-1), (1,0), (1,1), (0,1), (-1,1), (-1,0) )
    def wall_wont_block( self, gb, x, y ):
        """Return True if a wall placed here won't block movement."""
        if gb.map[x][y].blocks_walking():
            # This is a wall now. Changing it from a wall to a wall really won't
            # change anything, as should be self-evident.
            return True
        else:
            # Adding a wall will block a passage if there are two or more spaces
		    # in the eight surrounding tiles which are separated by walls.
            was_a_space = not gb.map[x-1][y].blocks_walking()
            n = 0
            for a in self.ANGDIR:
                is_a_space = not gb.map[x+a[0]][y+a[1]].blocks_walking()
                if is_a_space != was_a_space:
                    # We've gone from wall to space or vice versa.
                    was_a_space = is_a_space
                    n += 1
            return n <= 2

    def contains_a_space( self, gb, area ):
        for x in range( area.x, area.x + area.width ):
            for y in range( area.y, area.y + area.height ):
                if not gb.map[x][y].wall:
                    return True

    def carve_noise( self, gb, area ):
        myrect = pygame.Rect(0,0,5,5)
        for t in range( gb.width * gb.height // self.noise_throttle ):
            myrect.x = random.choice( range( area.x , area.x + area.width - myrect.width ) )
            myrect.y = random.choice( range( area.y , area.y + area.height - myrect.height ) )
            if self.contains_a_space( gb, myrect ):
                for x in range( myrect.x, myrect.x + myrect.width ):
                    for y in range( myrect.y, myrect.y + myrect.height ):
                        gb.map[x][y].wall = None

    def __call__( self, gb, area ):
        if self.do_carving:
            self.carve_noise( gb, area )
        temp = [[ int()
            for y in range(gb.height) ]
                for x in range(gb.width) ]
        # Perform the mutation several times in a row.
        for t in range( self.passes ):
            for x in range( area.x + 1, area.x + area.width - 1 ):
                for y in range( area.y + 1, area.y + area.height - 1 ):
                    if self.num_nearby_walls(gb,x,y) >= 5:
                        temp[x][y] = self.WALL_ON
                    else:
                        temp[x][y] = self.WALL_OFF
            for x in range( area.x + 1, area.x + area.width - 1 ):
                for y in range( area.y + 1, area.y + area.height - 1 ):
                    if temp[x][y] == self.WALL_OFF:
                        gb.map[x][y].wall = None
                    elif ( temp[x][y] == self.WALL_ON ) and self.wall_wont_block( gb, x, y ):
                        gb.map[x][y].wall = True


#  *****************
#  ***   ROOMS   ***
#  *****************

class Room( object ):
    """A Room is an area on the map. This room is nothing but an area."""
    def __init__( self, width=None, height=None, tags=(), anchor=None, parent=None ):
        self.width = width or random.randint(7,15)
        self.height = height or random.randint(7,15)
        self.tags = tags
        self.anchor = anchor
        self.area = None
        self.contents = list()
        # special_c lists contents that will be treated specially by the generator.
        self.special_c = dict()
        self.inventory = list()
        if parent:
            parent.contents.append( self )
    def step_two( self, gb ):
        self.arrange_contents( gb )
        # Prepare any child nodes in self.contents as needed.
        for r in self.contents:
            r.step_two( gb )
    def step_three( self, gb ):
        self.connect_contents( gb )
        # Prepare any child nodes in self.contents as needed.
        for r in self.contents:
            r.step_three( gb )
    def step_four( self, gb ):
        if self.mutate:
            self.mutate( gb, self.area )
        # Prepare any child nodes in self.contents as needed.
        for r in self.contents:
            r.step_four( gb )
    def step_five( self, gb ):
        self.render( gb )
        # Prepare any child nodes in self.contents as needed.
        for r in self.contents:
            r.step_five( gb )
    def step_six( self, gb ):
        self.deploy( gb )
        # Prepare any child nodes in self.contents as needed.
        for r in self.contents:
            r.step_six( gb )

    def arrange_contents( self, gb ):
        # Step Two: Arrange subcomponents within this area.
        closed_area = list()
        # Add already placed rooms to the closed_area list.
        for r in self.contents:
            if r.area:
                closed_area.append( r.area )
        # Add rooms with defined anchors next
        for r in self.contents:
            if r.anchor:
                myrect = pygame.Rect( 0, 0, r.width, r.height )
                r.anchor( self.area, myrect )
                if myrect.collidelist( closed_area ) == -1:
                    r.area = myrect
                    closed_area.append( myrect )
        # Assign areas for unplaced rooms.
        for r in self.contents:
            myrect = pygame.Rect( 0, 0, r.width, r.height )
            count = 0
            while ( count < 1000 ) and not r.area:
                myrect.x = random.choice( range( self.area.x , self.area.x + self.area.width - r.width ) )
                myrect.y = random.choice( range( self.area.y , self.area.y + self.area.height - r.height ) )
                if myrect.collidelist( closed_area ) == -1:
                    r.area = myrect
                    closed_area.append( myrect )
                count += 1

    def connect_contents( self, gb ):
        # Step Three: Connect all rooms in contents, making trails on map.
        # For this one, I'm just gonna straight line connect the contents in
        # a circle.
        if self.contents:
            prev = self.contents[-1]
            for r in self.contents:
                # Connect r to prev
                self.draw_L_connection( gb, r.area.centerx, r.area.centery, prev.area.centerx, prev.area.centery )
#                self.draw_direct_connection( gb, r.area.centerx, r.area.centery, prev.area.centerx, prev.area.centery )

                # r becomes the new prev
                prev = r

    mutate = None

    def render( self, gb ):
        # Step Five: Actually draw the room, taking into account terrain already on map.
        pass

    def deploy( self, gb ):
        # Step Six: Move items and monsters onto the map.
        # Find a list of good spots for stuff that goes in the open.
        good_spots = list()
        for x in range( self.area.x+1, self.area.x + self.area.width-1, 2 ):
            for y in range( self.area.y+1, self.area.y + self.area.height-1, 2 ):
                if not gb.map[x][y].blocks_walking():
                    good_spots.append( (x,y) )

        # Find a list of good walls for stuff that must be mounted on a wall.
        good_walls = list()
        for x in range( self.area.x + 1, self.area.x + self.area.width - 1 ):
            if gb.map[x][self.area.y].wall == maps.BASIC_WALL and gb.map[x-1][self.area.y].wall and gb.map[x+1][self.area.y].wall and not gb.map[x][self.area.y+1].blocks_walking():
                good_walls.append((x,self.area.y ))
        for y in range( self.area.y + 1, self.area.y + self.area.height - 1 ):
            if gb.map[self.area.x][y].wall == maps.BASIC_WALL and gb.map[self.area.x][y-1].wall and gb.map[self.area.x][y+1].wall and not gb.map[self.area.x+1][y].blocks_walking():
                good_walls.append((self.area.x,y ))

        for i in self.inventory:
            if hasattr( i, "ATTACH_TO_WALL" ) and i.ATTACH_TO_WALL and good_walls:
                p = random.choice( good_walls )
                good_walls.remove( p )
                if hasattr( i, "place" ):
                    i.place( gb, p )
                else:
                    i.pos = p
                    gb.contents.append( i )
            else:
                p = random.choice( good_spots )
                good_spots.remove( p )
                if hasattr( i, "place" ):
                    i.place( gb, p )
                else:
                    i.pos = p
                    gb.contents.append( i )


    def fill( self, gb, dest, floor=-1, wall=-1, decor=-1 ):
        # Fill the provided area with the provided terrain.
        for x in range( dest.x, dest.x + dest.width ):
            for y in range( dest.y, dest.y + dest.height ):
                if gb.on_the_map(x,y):
                    if floor != -1:
                        gb.map[x][y].floor = floor
                    if wall != -1:
                        gb.map[x][y].wall = wall
                    if decor != -1:
                        gb.map[x][y].decor = decor

    def draw_fuzzy_ground( self, gb, x, y ):
        # In general, just erase the wall to expose the floor underneath,
        # adding a floor if need be.
        if gb.on_the_map(x,y):
            gb.map[x][y].wall = None
            if gb.map[x][y].blocks_walking():
                gb.map[x][y].floor = maps.HIGROUND

    def probably_blocks_movement( self, gb, x, y ):
        if not gb.on_the_map(x,y):
            return True
        elif gb.map[x][y].wall is True:
            return True
        else:
            return gb.map[x][y].blocks_walking()

    def draw_direct_connection( self, gb, x1,y1,x2,y2 ):
        path = animobs.get_line( x1,y1,x2,y2 )
        for p in path:
            for x in range( p[0]-1, p[0]+2 ):
                for y in range( p[1]-1, p[1]+2 ):
                    self.draw_fuzzy_ground( gb, x, y )

    def draw_L_connection( self, gb, x1,y1,x2,y2 ):
        if random.randint(1,2) == 1:
            cx,cy = x1,y2
        else:
            cx,cy = x2,y1
        self.draw_direct_connection( gb, x1, y1, cx, cy )
        self.draw_direct_connection( gb, x2, y2, cx, cy )


class FuzzyRoom( Room ):
    """A room without hard walls, with default ground floors."""
    def render( self, gb ):
        # Step Five: Actually draw the room, taking into account terrain already on map.
        for x in range( self.area.x, self.area.x + self.area.width ):
            for y in range( self.area.y, self.area.y + self.area.height ):
                self.draw_fuzzy_ground( gb, x, y )

class SharpRoom( Room ):
    """A room with hard walls, with BASIC_FLOOR floors."""
    def deal_with_empties( self, gb, empties ):
        p2 = random.choice( empties )
        empties.remove( p2 )
        gb.map[p2[0]][p2[1]].wall = maps.OPEN_DOOR
        for pp in empties:
            gb.map[pp[0]][pp[1]].wall = maps.BASIC_WALL
        del empties[:]
    def probably_an_entrance( self, gb, p, vec ):
        return not self.probably_blocks_movement(gb,*p) and not self.probably_blocks_movement(gb,p[0]+vec[0],p[1]+vec[1])
    def draw_wall( self, gb, points, vec ):
        empties = list()
        for p in points:
            if self.probably_an_entrance(gb,p,vec):
                empties.append( p )
            else:
                gb.map[p[0]][p[1]].wall = maps.BASIC_WALL
                if empties:
                    self.deal_with_empties(gb, empties )
        if empties:
            self.deal_with_empties(gb, empties )

    def render( self, gb ):
        # Fill the floor with BASIC_FLOOR, and clear room interior
        self.fill( gb, self.area, floor=maps.BASIC_FLOOR )
        self.fill( gb, self.area.inflate(-2,-2), wall=None )
        # Set the four corners to basic walls
        gb.map[self.area.x][self.area.y].wall = maps.BASIC_WALL
        gb.map[self.area.x+self.area.width-1][self.area.y].wall = maps.BASIC_WALL
        gb.map[self.area.x][self.area.y+self.area.height-1].wall = maps.BASIC_WALL
        gb.map[self.area.x+self.area.width-1][self.area.y+self.area.height-1].wall = maps.BASIC_WALL

        # Draw each wall. Harder than it sounds.
        self.draw_wall( gb, animobs.get_line( self.area.x+1,self.area.y,self.area.x+self.area.width-2,self.area.y ), (0,-1) )
        self.draw_wall( gb, animobs.get_line( self.area.x,self.area.y+1,self.area.x,self.area.y+self.area.height-2 ), (-1,0) )
        self.draw_wall( gb, animobs.get_line( self.area.x+1,self.area.y+self.area.height-1,self.area.x+self.area.width-2,self.area.y+self.area.height-1 ), (0,1) )
        self.draw_wall( gb, animobs.get_line( self.area.x+self.area.width-1,self.area.y+1,self.area.x+self.area.width-1,self.area.y+self.area.height-2 ), (1,0) )

class BottleneckRoom( Room ):
    """A room that blocks passage, aside from one door."""
    def render( self, gb ):
        myrect = self.area.inflate(-2,-2)
        for x in range( myrect.x, myrect.x + myrect.width ):
            for y in range( myrect.y, myrect.y + myrect.height ):
                self.draw_fuzzy_ground( gb, x, y )
        # Determine whether the wall will be vertical or horizontal
        if self.probably_blocks_movement( gb, *self.area.midtop ) and self.probably_blocks_movement( gb, *self.area.midbottom ):
            # Obstacles above and below. Draw a vertical wall.
            x = myrect.centerx
            for y in range( myrect.y, myrect.y + myrect.height ):
                gb.map[x][y].wall = maps.BASIC_WALL
        else:
            y = myrect.centery
            for x in range( myrect.x, myrect.x + myrect.width ):
                gb.map[x][y].wall = maps.BASIC_WALL
        x,y = myrect.center
        gb.map[x][y].wall = maps.OPEN_DOOR
        door_wp = self.special_c.get( "door", None )
        if door_wp:
            door_wp.place( gb, (x,y) )

class RandomScene( Room ):
    """The blueprint for a scene."""
    def __init__( self, myscene ):
        super(RandomScene,self).__init__( myscene.width, myscene.height )
        self.gb = myscene
        self.area = pygame.Rect(0,0,myscene.width,myscene.height)

    def convert_true_walls( self ):
        for x in range( self.width ):
            for y in range( self.height ):
                if self.gb.map[x][y].wall == True:
                    self.gb.map[x][y].wall = maps.BASIC_WALL

    def make( self ):
        """Assemble this stuff into a real map."""
        # Conduct the five steps of building a level.
        self.prepare( self.gb ) # Only the scene generator gets to prepare
        self.step_two( self.gb ) # Arrange contents for self, then children
        self.step_three( self.gb ) # Connect contents for self, then children
        self.step_four( self.gb ) # Mutate for self, then children
        self.step_five( self.gb ) # Render for self, then children

        # Convert undefined walls to real walls.
        self.convert_true_walls()
        self.gb.validate_terrain()

        self.step_six( self.gb ) # Deploy for self, then children

        return self.gb

    def prepare( self, gb ):
        # Step one- we're going to use a plasma map to set water/lo/hi ground.
        # Fill all non-water tiles with True walls for now.
        myplasma = Plasma()
        for x in range( self.width ):
            for y in range( self.height ):
                if myplasma.map[x][y] < 0.3:
                    gb.map[x][y].floor = maps.WATER
                elif myplasma.map[x][y] < 0.5:
                    gb.map[x][y].floor = maps.LOGROUND
                    gb.map[x][y].wall = True
                else:
                    gb.map[x][y].floor = maps.HIGROUND
                    gb.map[x][y].wall = True


class DividedIslandScene( RandomScene ):
    """The rooms are divided into two groups by a single bridge."""
    # Special elements:
    #  bridge: The room in the middle of the river.
    #  before_bridge: The room before the bridge.
    #  after_bridge: The room after the bridge.
    # Tags of note:
    #  ENTRANCE: Rooms with this tag placed before the bridge
    #  GOAL: Rooms with this tag placed after the bridge
    def prepare( self, gb ):
        # Step one- we're going to use a plasma map to set water/lo/hi ground.
        # Fill all non-water tiles with True walls for now.
        myplasma = Plasma()
        for x in range( self.width ):
            for y in range( self.height ):
                if myplasma.map[x][y] < 0.25:
                    gb.map[x][y].floor = maps.WATER
                elif myplasma.map[x][y] < 0.5:
                    gb.map[x][y].floor = maps.LOGROUND
                    gb.map[x][y].wall = True
                else:
                    gb.map[x][y].floor = maps.HIGROUND
                    gb.map[x][y].wall = True

    def arrange_contents( self, gb ):
        # Divide the map into two segments.
        if random.randint(1,2) == 1:
            horizontal_river = True
            subzone_height = ( self.height - 10 ) // 2
            # Horizontal river
            z1 = Room()
            z1.area = pygame.Rect( 0,0,self.width,subzone_height )
            z1.special_c["bridge_anchor"] = south
            z2 = Room()
            z2.area = pygame.Rect( 0,0,self.width,subzone_height )
            z2.area.bottomleft = self.area.bottomleft
            z2.special_c["bridge_anchor"] = north
            river = pygame.Rect( 0,0,self.width,7 )
        else:
            horizontal_river = False
            subzone_width = ( self.width - 10 ) // 2
            # Vertical river
            z1 = Room()
            z1.area = pygame.Rect( 0,0,subzone_width,self.height )
            z1.special_c["bridge_anchor"] = east
            z2 = Room()
            z2.area = pygame.Rect( 0,0,subzone_width,self.height )
            z2.area.topright = self.area.topright
            z2.special_c["bridge_anchor"] = west
            river = pygame.Rect( 0,0,7,self.height )
        if random.randint(1,2) == 1:
            z1,z2 = z2,z1
        river.center = self.area.center
        self.fill( gb, river, floor=maps.WATER, wall=None )
        self.fill( gb, river.inflate(3,3), wall=None )

        # Locate the bridge, before_bridge, and after_bridge rooms, creating them
        # if none currently exist.
        bridge = self.special_c.get( "bridge" ) or self.special_c.setdefault( "bridge", FuzzyRoom(parent=self) )
        before_bridge = self.special_c.get( "before_bridge" ) or self.special_c.setdefault( "before_bridge", FuzzyRoom(parent=self) )
        after_bridge = self.special_c.get( "after_bridge" ) or self.special_c.setdefault( "after_bridge", FuzzyRoom(parent=self) )
        before_bridge.anchor = z1.special_c["bridge_anchor"]
        after_bridge.anchor = z2.special_c["bridge_anchor"]

        # Go through the remaining rooms, sorting each into either z1 or z2
        z1_turn = True
        for r in self.contents[:]:
            if r is bridge:
                r.area = pygame.Rect( 0, 0, r.width, r.height )
                r.area.center = self.area.center
            elif r is before_bridge:
                self.contents.remove( r )
                z1.contents.append( r )
            elif r is after_bridge:
                self.contents.remove( r )
                z2.contents.append( r )
            elif context.ENTRANCE in r.tags:
                self.contents.remove( r )
                z1.contents.append( r )
            elif context.GOAL in r.tags:
                self.contents.remove( r )
                z2.contents.append( r )
            elif z1_turn:
                self.contents.remove( r )
                z1.contents.append( r )
                z1_turn = False
            else:
                self.contents.remove( r )
                z2.contents.append( r )
                z1_turn = True

        self.contents += (z1,z2)

    def connect_contents( self, gb ):
        # This is pretty easy- just connect before_bridge to bridge to after_bridge.
        bridge = self.special_c[ "bridge" ]
        before_bridge = self.special_c[ "before_bridge" ]
        after_bridge = self.special_c[ "after_bridge" ]
        self.draw_direct_connection( gb, before_bridge.area.centerx, before_bridge.area.centery, bridge.area.centerx, bridge.area.centery )
        self.draw_direct_connection( gb, after_bridge.area.centerx, after_bridge.area.centery, bridge.area.centerx, bridge.area.centery )

    mutate = CellMutator(noise_throttle=100)

if __name__ == '__main__':
    pygame.init()

    # Set the screen size.
    screen = pygame.display.set_mode((800, 600))

    screen.fill((0,0,0))

    myplasma = Plasma()
#    myplasma.draw( screen )
    myplasma.draw_layers( screen )

#    p2 = Plasma()
#    p3 = Plasma()
#    for x in range( myplasma.width ):
#        for y in range( myplasma.height ):
#            pygame.draw.rect(screen,(255*myplasma.map[x][y],255*p2.map[x][y],255*p3.map[x][y]),pygame.Rect(x*2,y*2,2,2) )
#            pygame.draw.rect(screen,(255*myplasma.map[x][y],0,255*p2.map[x][y]),pygame.Rect(x*2,y*2,2,2) )


    pygame.display.flip()

    while True:
        ev = pygame.event.wait()
        if ( ev.type == pygame.MOUSEBUTTONDOWN ) or ( ev.type == pygame.QUIT ) or (ev.type == pygame.KEYDOWN):
            break


