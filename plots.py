from scipy.stats import norm
import time, numpy as np
import matplotlib.pyplot as plt

def moisture_histogram(plant_list, year):
    '''Creates a histogram of'''
    x = [plant.soil_moisture for plant in plant_list]
    n, bins, patches = plt.hist(x, bins = 50, range = (0,100), facecolor='g')
    plt.xlabel('Soil Moisture (Arbitrary Units)')
    plt.ylabel('Frequency (# Plants)')
    plt.title("Histogram of Plants Sorted by Ideal Soil Moisture: \nYear " + str(year))
    plt.xlim(0, 100)
    plt.grid(True)
    plt.show()


def plant_efficiency(moisture_at_plant):
    '''Plots one plants energy efficiency - soil moisture relationship'''
    #Draws normal distribution
    x = np.arange(0,100, 0.001)
    y = norm.pdf(x,30,10)/norm.pdf(30,30,10)
    plt.plot(x,y)
    
    #draws point of intersection
    plt.scatter(moisture_at_plant, norm.pdf(moisture_at_plant,30,10)/norm.pdf(30,30,10))
    
    #draws vertical line
    plt.axvline(moisture_at_plant, lw = 1, label="Soil moisture at plant's location = " + str(moisture_at_plant)) #draws verticle line
    
    plt.xlabel("Soil Moisture (Arbitrary Units)")
    plt.ylabel("Efficiency (percent of energy produced kept)")
    plt.title("Energy Efficiency of Plant at Varying Soil Moisture")
    plt.legend()
    plt.grid(True)
    plt.show()
if __name__ == "__main__":
    plant_efficiency(50)
