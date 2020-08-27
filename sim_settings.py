import numpy as np, random, math, time
from scipy.stats import norm
import matplotlib

class Settings():
    def __init__(self):
        self.min_dist = 100
        self.initial_num = 150
        self.tick_time = 0 #time between updates during run mode
        
        #Max initial energy is 723
        self.efficiency_stdev = 10 #50 is less selective, 10 is very selective, 20 is less shocking
        self.area_energy_cost = 30
        self.height_growth_cost = 300
        self.area_growth_cost = 20
        self.seed_cost = 100

        #mutation_rate out of 1
        self.mutation_rate = 0.3

        self.max_age = 20
        self.leaf_obscurity = 0.8

        self.x_size = 300
        self.y_size = 300

        #initial light grids
        self.understory_light = np.full((self.x_size,self.y_size), 100)
        self.floor_light = np.full((self.x_size, self.y_size), 100)

        #initial 
        # self.ph_board = np.full((self.x_size, self.y_size),50) 
        ph_row = [np.concatenate([np.full((int(self.x_size / 2), 1),25), np.full((int(self.x_size / 2), 1), 75)])]
        self.ph_board = ph_row
        for _ in range(self.y_size-1):
            self.ph_board = np.append(self.ph_board, ph_row, axis = 0)

    def update_light_boards(self, plant_list):
        '''updates light boards on the floor and understory.
        At the same time, calculates plants energy'''
        new_understory_light = np.full((self.x_size,self.y_size), 100)
        new_floor_light = np.full((self.x_size, self.y_size), 100)

        for plant in plant_list:
            new_energy = 100 * np.pi * (plant.radius_canopy)

            #Checks through squares on all levels to see if it the squares lie within its radius adds to the energy the brightness of the light at that level
            largest_radius = max(plant.radius_understory, plant.radius_floor, plant.radius_canopy) 
            for boxx in range(plant.x_pos-largest_radius, plant.x_pos + largest_radius):
                for boxy in range(plant.y_pos -largest_radius, plant.y_pos + largest_radius):
                    if boxx >= 0 and boxy >=0 and boxy < self.y_size and boxx < self.x_size:
                        distance = (plant.x_pos - boxx)**2 + (plant.y_pos - boxy)**2

                        if distance <= plant.radius_canopy ** 2 and plant.radius_canopy != 0:
                            new_understory_light[boxy, boxx] = new_understory_light[boxy, boxx] * (1-self.leaf_obscurity)
                            new_floor_light[boxy, boxx] = new_floor_light[boxy, boxx] * (1-self.leaf_obscurity)

                        if distance <= plant.radius_understory ** 2 and plant.radius_understory != 0:
                            new_floor_light[boxy, boxx] = new_floor_light[boxy, boxx] * (1-self.leaf_obscurity)
                            new_energy += self.understory_light[boxy, boxx]

                        if distance <= plant.radius_floor ** 2 and plant.radius_floor != 0:
                            new_energy += self.floor_light[boxy, boxx]

            required_sustenance = np.pi * (plant.radius_floor**2 + plant.radius_understory**2 + plant.radius_canopy**2) * self.area_energy_cost
            
            #Calculates plant energy with pdf centered at the 
            plant.energy = new_energy * (norm.pdf(self.ph_board[plant.y_pos, plant.x_pos], plant.soil_ph, self.efficiency_stdev)/norm.pdf(plant.soil_ph, plant.soil_ph, self.efficiency_stdev)) - required_sustenance

        self.understory_light = new_understory_light
        self.floor_light = new_floor_light


    def next_year(self, plant_list):
        '''Runs the simulation for one year. Updates boards etc'''
        
        self.update_light_boards(plant_list)
        male_list = []
        female_list = []

        #Loop through all plants
        for plant in plant_list:
            if plant.age == self.max_age or plant.energy < 0 : #kill all plants which do not reach a minimum energy input
                plant_list.remove(plant) #kill all plants above max_age
            else: 
                plant.age += 1 #age all plants

                #Grows height and radius if not maximized
                if plant.height <= plant.growth_height and plant.energy > self.height_growth_cost:
                    
                    plant.height += 1
                    plant.energy -= self.height_growth_cost
                    
                #test interaction by looping through all distances
                can_grow_floor, can_grow_understory, can_grow_canopy = plant.check_can_grow(plant_list) #
                #grow all plants which have the energy to do so, have not reached their growth limit and do not interact with other trees
                if plant.height == 3 and plant.radius_canopy < plant.max_rad_can and can_grow_canopy and plant.energy > np.pi * (2 * plant.radius_canopy + 1) * self.area_growth_cost:
                    plant.radius_canopy += 1
                    plant.energy -= np.pi * (2 * plant.radius_canopy + 1) * self.area_growth_cost #area_growth_cost times the change in area of the canopy

                if plant.height >= 2 and plant.radius_understory < plant.max_rad_und and can_grow_understory and plant.energy > np.pi * (2 * plant.radius_understory + 1) * self.area_growth_cost:
                    plant.radius_understory += 1
                    plant.energy -= np.pi * (2 * plant.radius_understory + 1) * self.area_growth_cost

                if plant.radius_floor < plant.max_rad_flo and can_grow_floor and plant.energy > np.pi * (2 * plant.radius_understory + 1) * self.area_growth_cost:
                    plant.radius_floor += 1
                    plant.energy -= np.pi * (2 * plant.radius_floor + 1) * self.area_growth_cost
        
                if plant.gender:#adds to male or female plant lists
                    for _ in range(int(min(plant.seed_production, plant.energy//self.seed_cost))):
                        male_list.append(plant)
                else:
                    female_list.append(plant)
        
        random.shuffle(male_list)

        for seed in male_list:           
            if len(plant_list) < self.y_size * self.x_size:
                random.shuffle(female_list)
                for female in female_list:
                    if seed.check_viable_mate(self.min_dist, female):
                        not_chosen = True
                        #generates random x,y variable which is not yet taken up
                        while not_chosen:
                            new_x = random.randint(0, self.x_size -1)
                            new_y = random.randint(0, self.y_size -1)
                            if (new_y,new_x) not in plant_list:
                                not_chosen = False
                        plant_list.append(create_seed(seed, female, new_x, new_y, self.mutation_rate))
                        break
            else:
                break
        return(plant_list)

class Plant:
    def __init__(self, soil_ph, seed_production, growth_height, max_rad_flo, max_rad_und, max_rad_can, gender:bool, x_pos = None , y_pos = None):
        
        #Genetic Information
        self.soil_ph = soil_ph
        self.seed_production = seed_production  
        self.growth_height = growth_height
        self.max_rad_flo = max_rad_flo
        self.max_rad_und = max_rad_und
        self.max_rad_can = max_rad_can
        self.gender = gender # True is Male, False is Female

        #Plant information
        self.height = 1
        self.radius_canopy = 0 
        self.radius_understory = 0
        self.radius_floor = 2
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.age = 0
        self.display_color = (0, min(255, math.floor(255/100 * self.soil_ph)), 0)
        self.energy = None

    def __eq__(self, coords):
        '''returns true if tuple is equal to x,y coordinates'''

        if isinstance(coords, tuple):
            if coords[0] == self.y_pos and coords[1] == self.x_pos:
                return True
            return False
        if coords.y_pos == self.y_pos and coords.x_pos == self.x_pos:
            return True
        return False

    def check_viable_mate(self, min_dist, mate):
        '''Returns whether two plants can mate(are of the same species)'''
        dist_to_mate = (self.soil_ph - mate.soil_ph)**2 + ((self.growth_height - mate.growth_height)*100/3)**2 + (self.seed_production - mate.seed_production)**2
        if dist_to_mate <= min_dist:
            return True
        return False

    def check_can_grow(self, plant_list):
        '''Outputs a tuple of booleans determining whether the plant has space to grow'''
        can_grow_floor = True
        can_grow_understory = True
        can_grow_canopy = True 

        for p in plant_list:
            if not self.__eq__(p):
                distance = ((p.x_pos - self.x_pos)**2 + (p.y_pos - self.y_pos)**2)**0.5

                if can_grow_floor:
                    can_grow_floor = (distance - p.radius_floor) > (self.radius_floor + 1) or distance < self.radius_floor

                if can_grow_understory and self.height >= 2 and p.height >= 2:
                    can_grow_understory = (distance - p.radius_understory) > (self.radius_understory + 1) or distance < self.radius_understory

                if can_grow_canopy == True and self.height == 3 and p.height == 3:
                    can_grow_canopy = (distance - p.radius_canopy) > (self.radius_canopy + 1) or distance < self.radius_canopy
        
        return(can_grow_floor, can_grow_understory, can_grow_canopy)

def create_seed(parent1, parent2, x, y, mutation_rate):
    '''Creates a new seed in the plant class.
    All of the seeds variables are selected using a normal distribution where the average of the 
    parents variables is the mean and the mutation_rate is the standard deviation
    '''

    seed_soil_ph = np.random.normal((parent1.soil_ph + parent2.soil_ph)/2, mutation_rate * 20)
    if seed_soil_ph < 0:
        seed_soil_ph = 0

    seed_seed_production = math.ceil(np.random.normal((parent1.seed_production + parent2.seed_production)/2, mutation_rate * 10))
    if seed_seed_production < 0:
        seed_seed_production = 0
    
    seed_growth_height = random.choice([random.choice([parent1.growth_height, parent2.growth_height]),random.randint(1,3)]) # 4/9 times 
    
    seed_rad_flo = math.ceil(np.random.normal((parent1.max_rad_flo + parent2.max_rad_flo)/2, mutation_rate * 10))
    if seed_rad_flo <1:
        seed_rad_flo = 1

    seed_rad_und = math.ceil(np.random.normal((parent1.max_rad_und + parent2.max_rad_und)/2, mutation_rate * 10))
    if seed_rad_und <1:
        seed_rad_und = 1

    seed_rad_can = math.ceil(np.random.normal((parent1.max_rad_can + parent2.max_rad_can)/2, mutation_rate * 10))
    if seed_rad_can <1:
        seed_rad_can = 1

    seed = Plant(seed_soil_ph, seed_seed_production, seed_growth_height, seed_rad_flo, seed_rad_und, seed_rad_can, bool(random.getrandbits(1)), x, y) 
    return seed 



def initiate_plants(num_plants: int, y_size: int, x_size):
    x_list = np.random.choice(range(x_size), num_plants, replace= False).tolist()
    y_list = np.random.choice(range(y_size), num_plants, replace= False).tolist()
    plant_list = []
    
    for _ in range(num_plants):
        
        soil_ph = random.uniform(1,100)
        growth_height = random.randint(1,3)
        seed_production = random.randint(1, 5)

        #need to finish
        rad_flo = random.randint(1, 30)
        rad_und = random.randint(1, 30)
        rad_can = random.randint(1, 30)
        x = x_list.pop()
        y = y_list.pop()

        plant_list.append(Plant(soil_ph, seed_production, growth_height, rad_flo, rad_und, rad_can, bool(random.getrandbits(1)),x, y))
        
    return plant_list
        