from scipy.stats import norm
import time, numpy as np
import statistics
import matplotlib.pyplot as plt

def ph_histogram(plant_list, year):
    '''Creates a histogram of plant pH values'''
    x = [plant.soil_ph for plant in plant_list]
    n, bins, patches = plt.hist(x, bins = 50, range = (0,100), facecolor='g')
    mean = sum(x)/len(x)
    standarddev = statistics.stdev(x)
    print("year: ", year)
    print("mean: ", mean)
    print("Standard Deviation: ", standarddev, "\n")
    plt.xlabel('Soil pH (Arbitrary Units)')
    plt.ylabel('Frequency (# Plants)')
    plt.title("Histogram of Plants Sorted by Ideal Soil pH: \nYear " + str(year))
    plt.xlim(0, 100)
    plt.grid(True)
    plt.show()


def plant_efficiency(ph_at_plant):
    '''Plots one plants energy efficiency - pH relationship'''
    #Draws normal distribution
    x = np.arange(0,100, 0.001)
    y = norm.pdf(x,30,10)/norm.pdf(30,30,10)
    plt.plot(x,y)
    
    #draws point of intersection
    plt.scatter(ph_at_plant, norm.pdf(ph_at_plant,30,10)/norm.pdf(30,30,10))
    
    #draws vertical line
    plt.axvline(ph_at_plant, lw = 1, label="pH at plant's location = " + str(ph_at_plant)) #draws verticle line
    
    plt.xlabel("pH (Arbitrary Units)")
    plt.ylabel("Efficiency (percent of energy produced kept)")
    plt.title("Energy Efficiency of Plant at Varying pH")
    plt.legend()
    plt.grid(True)
    plt.show()

def seed_by_time(seed_list, years):

    plt.scatter(years, seed_list, linewidths=1)

    plt.xlabel("Time(years)")
    plt.ylabel("Seed Production")
    plt.title("Energy Efficiency of Plant at Varying Soil ph")
    plt.legend()
    plt.grid(True)
    plt.show()



if __name__ == "__main__":
    plant_efficiency(50)
