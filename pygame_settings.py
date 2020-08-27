import pygame, math

class Pygame:
    def __init__(self, board_tile_height: int, board_tile_width: int):#initialize settings
        '''board_tile_length is the number of tiles wide the board is'''
        #Window settings
        self.top_margin_height = 50
        self.bottom_margin_height = 25
        self.margin_width = 20 
        self.gap_size = 5

        #dimensions of board array
        self.board_tile_height = board_tile_height 
        self.board_tile_width = board_tile_width

        #pixel size of each tile
        self.tile_size = 1

        #Pixel sizes of each board
        self.board_height = self.board_tile_height * self.tile_size 
        self.board_width = self.board_tile_width * self.tile_size

        self.window_width = 2*self.gap_size + 3*self.board_width + 2 * self.margin_width
        self.window_height = self.gap_size + 2*self.board_height + self.bottom_margin_height + self.top_margin_height
        
        self.font_size1 = 30
        self.font_size2 = 15

        '''may need to change'''
        #colors used
        self.white = (255, 255, 255) 
        self.gray = (199, 199, 199) 
        self.blue = (135, 206, 235)
        self.red = (240, 79, 69)
        self.dark_blue = (20, 54, 86)
        self.black = (0,0,0)
        self.brown = (78, 72, 36)

        #game colors
        self.bg_color = self.black
        self.floor_bg = self.brown
        self.sky_bg = self.blue
        self.text_color = self.black
        self.shadow_color = self.gray
        self.shadow_color2 = self.black
        self.light_hue = 216
        self.trunk_color = self.black
        self.button_color = self.white

        #Text box coordinates
        self.top_center = math.ceil(self.top_margin_height/2)
        self.bottom_center = self.top_margin_height + self.gap_size + 2*self.board_height + math.ceil(self.bottom_margin_height/2)
        self.step_center = self.margin_width + math.ceil(self.board_width/2)
        self.run_center = self.step_center + self.gap_size + self.board_width
        self.restart_center = self.run_center + self.gap_size + self.board_width
        self.year_center = self.step_center 

    def draw_board(self, plant_list, floor_light, understory_light, soil_ph, run_box, step_box, restart_box, year_box, screen): 
        '''resets screen with new boards'''
        screen.fill(self.bg_color)

        for boxx in range (self.board_tile_width):
            for boxy in range (self.board_tile_height):
                left = boxx * self.tile_size
                top = boxy * self.tile_size + self.top_margin_height +self.board_height + self.gap_size

                #bottom left (floor light )
                pygame.draw.rect(screen, (math.floor(self.light_hue * floor_light[boxy, boxx]/100), math.floor(self.light_hue * floor_light[boxy, boxx]/100) , 0), (left + self.margin_width, top, self.tile_size, self.tile_size))

                #bottom middle (understory light)
                pygame.draw.rect(screen, (math.floor(self.light_hue * understory_light[boxy, boxx]/100), math.floor(self.light_hue * understory_light[boxy, boxx]/100), 0),(left + self.margin_width + self.gap_size + self.board_width, top, self.tile_size, self.tile_size))
                
                #bottom right (soil ph)
                pygame.draw.rect(screen, (0,0, math.floor(255/100 * soil_ph[boxy, boxx])) ,(left + self.margin_width + 2*self.gap_size + 2*self.board_width, top, self.tile_size, self.tile_size))

        #Top left background
        pygame.draw.rect(screen, self.floor_bg, (self.margin_width, self.top_margin_height,self.board_width, self.board_height))


        #Top middle background
        pygame.draw.rect(screen, self.sky_bg, (self.margin_width + self.gap_size + self.board_width, self.top_margin_height, self.board_width, self.board_height))

        #Top right background
        pygame.draw.rect(screen, self.sky_bg, (self.margin_width + 2*self.gap_size + 2*self.board_width, self.top_margin_height, self.board_width, self.board_height))
        
        #draw circles for each plant based in each rectangle
        for plant in plant_list:
            #Floor circles
            pygame.draw.circle(screen, plant.display_color, (plant.x_pos * self.tile_size + self.margin_width , plant.y_pos * self.tile_size + self.top_margin_height), plant.radius_floor * self.tile_size)
            pygame.draw.circle(screen, self.trunk_color, (plant.x_pos * self.tile_size + self.margin_width , plant.y_pos * self.tile_size + self.top_margin_height), self.tile_size, )

            #understory circles
            if plant.height >= 2:
                pygame.draw.circle(screen, plant.display_color, (plant.x_pos * self.tile_size + self.margin_width + self.board_width + self.gap_size, plant.y_pos * self.tile_size + self.top_margin_height), plant.radius_understory * self.tile_size)
                pygame.draw.circle(screen, self.trunk_color, (plant.x_pos * self.tile_size + self.margin_width + self.board_width + self.gap_size, plant.y_pos * self.tile_size + self.top_margin_height), self.tile_size,)

            #canopy circles
            if plant.height == 3:
                pygame.draw.circle(screen, plant.display_color, (plant.x_pos * self.tile_size + self.margin_width + 2*self.board_width + 2*self.gap_size, plant.y_pos * self.tile_size + self.top_margin_height), plant.radius_canopy * self.tile_size)
                pygame.draw.circle(screen, self.trunk_color, (plant.x_pos * self.tile_size + self.margin_width + 2*self.board_width + 2*self.gap_size, plant.y_pos * self.tile_size + self.top_margin_height), self.tile_size)

        run_box.display_rectangle()
        step_box.display_rectangle()
        restart_box.display_rectangle()
        year_box.display_rectangle()


class text: #used for all text boxes
    def __init__(self, characters:str, text_size: int, text_color: tuple, color: tuple, x_cent: int, y_cent: int, screen, font = "freesansbold.ttf"):
        '''initializes object in text class'''
        self.characters = characters
        self.text_size = round(text_size)
        self.text_color = text_color
        self.color = color
        self.screen = screen
        self.font = font
        self.x_cent = x_cent
        self.y_cent = y_cent


        font = pygame.font.Font(self.font, self.text_size) #creates a font object
        
        text_object = font.render(self.characters, True, self.color) #creates a text surface object

        self.rectangle = text_object.get_rect()

        self.rectangle.center = (self.x_cent, self.y_cent)


    def display_rectangle(self):
        '''creates and displays text and rectangle on screen'''
        
        font = pygame.font.Font(self.font, self.text_size) #creates a font object
        
        text_object = font.render(self.characters, True, self.text_color) #creates a text surface object

        self.rectangle = text_object.get_rect()

        #sets coordinates of rectangle based off of left side and height center
        self.rectangle.center = (self.x_cent, self.y_cent)

        self.screen.fill(self.color, self.rectangle)
        self.screen.blit(text_object, self.rectangle)

    # def update_characters(self, characters):
    #     '''Changes characters and the text rectangles'''
    #     font = pygame.font.Font(self.font, self.text_size) #creates a font object
        
    #     text_object = font.render(self.characters, True, self.text_color) #creates a text surface object

    #     self.rectangle = text_object.get_rect()
    #     self.rectangle.center = (self.x_cent, self.y_cent)