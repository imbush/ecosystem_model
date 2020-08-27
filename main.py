#First Trophic Level ecology simulator
#created by Inle Bush

import pygame, sys, random, time, numpy as np, math, matplotlib
from scipy.stats import norm
from pygame.locals import *
from sim_settings import *
from pygame_settings import *
from plots import ph_histogram, seed_by_time

def main():
    pygame.init()

    while True:
        #initializes game settings
        settings = Settings() 
        pg_sets = Pygame(settings.y_size, settings.x_size)
        plant_list = initiate_plants(settings.initial_num, settings.y_size, settings.x_size)
        year = 0
        run_mode = False
        sim_running = True
        
        #ph_histogram(plant_list, year)
        seed_productions = []
        years = []


        #Initializes Pygame
        mousex = 0
        mousey = 0 
        screen = pygame.display.set_mode((pg_sets.window_width, pg_sets.window_height))
        pygame.display.set_caption("Forest Niches")
        
        #creates text box objects with text class
        run_box = text("Run", pg_sets.font_size1, pg_sets.text_color, pg_sets.button_color, pg_sets.run_center, pg_sets.top_center, screen)
        step_box = text("Step", pg_sets.font_size1, pg_sets.text_color, pg_sets.button_color, pg_sets.step_center, pg_sets.top_center, screen)
        restart_box = text("Restart", pg_sets.font_size1, pg_sets.text_color, pg_sets.button_color, pg_sets.restart_center, pg_sets.top_center, screen)
        year_box = text("Year: 0", pg_sets.font_size2, pg_sets.white, pg_sets.black, pg_sets.year_center, pg_sets.bottom_center, screen)
        
        pg_sets.draw_board(plant_list, settings.floor_light, settings.understory_light, settings.ph_board, run_box, step_box, restart_box, year_box, screen)
        pygame.display.flip()

        #Main Loop
        while sim_running:
            mouse_clicked = False

            for event in pygame.event.get(): 
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    sim_running = False

                elif event.type == pygame.MOUSEBUTTONUP:
                    mousex, mousey = event.pos
                    mouse_clicked = True
            
            if mouse_clicked:
                if run_box.rectangle.collidepoint(mousex,mousey): #check validity
                    if run_mode:
                        run_mode = False
                        
                    else:
                        last_update = time.perf_counter() #gets time for tick time
                        run_mode = True

                elif step_box.rectangle.collidepoint(mousex, mousey):
                    if not run_mode:
                        year += 1
                        year_box.characters = "Year: " + str(year)
                        plant_list = settings.next_year(plant_list)

                        pg_sets.draw_board(plant_list, settings.floor_light, settings.understory_light, settings.ph_board, run_box, step_box, restart_box, year_box, screen)
                        pygame.display.flip() 
                        # for plant in plant_list:
                        #     seed_productions.append(plant.seed_production)
                        #     years.append(year)

                        # seed_by_time(seed_productions, years)
                        ph_histogram(plant_list, year)
                        print(year)

                elif restart_box.rectangle.collidepoint(mousex, mousey):
                    sim_running = False
                    break

            if run_mode:
                current_time = time.perf_counter()
                if (current_time - last_update) > settings.tick_time:
                    last_update = current_time
                    year += 1
                    year_box.characters = "Year: " + str(year)

                    plant_list = settings.next_year(plant_list)
                    pg_sets.draw_board(plant_list, settings.floor_light, settings.understory_light, settings.ph_board, run_box, step_box, restart_box, year_box, screen)                    
                    pygame.display.flip() 

if __name__ == "__main__":
    main()