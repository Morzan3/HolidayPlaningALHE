from faker import Factory
from random import randint, random, gauss
import math
import time
import matplotlib.pyplot as plt

import numpy as np
import scipy.misc as smp


NUMBER_OF_CITIES = 365
NUMBER_OF_YEARS = 10




fakeFactory = Factory.create()


class Day():
    def __init__(self, destination, flight_prices, sleeping_price, destination_weather_historic_data):
        self.destination = destination
        self.flight_price_to, self.flight_price_from = flight_prices
        self.destination_weather_historic_data = destination_weather_historic_data
        self.sleeping_price = sleeping_price


def get_cities_prices(city_list):
    city_price_list = {}
    for city in city_list:
        city_price_list[city] = randint(1, 250)

    return city_price_list


class HistoricDataGenerator:
    def __init__(self, year_number):
        self.city_historic_days = {}
        self.years = year_number
        self.assing_cities(year_number)

    def assing_cities(self, year_number):
        unique_names = set()
        while len(unique_names) != NUMBER_OF_CITIES:
            unique_names.add(fakeFactory.city() + str(randint(1, 100)))
        for name in unique_names:
            self.city_historic_days[name] = self.populate_days_with_random_data(year_number)

    def populate_days_with_random_data(self, year_number):
        historic_date = [[None for x in range(365)] for y in range(year_number)]
        for column in range(0, len(historic_date)):
            for row in range(0, len(historic_date[column])):
                historic_date[column][row] = randint(-1, 1)
        return historic_date

    def get_city_list(self):
        city_name_list = []

        for city in self.city_historic_days:
            city_name_list.append(city)

        return city_name_list


class CurrentFlightGenerator:
    def __init__(self, city_list):
        self.city_list = city_list

    def generate_flights(self):
        year_flights = [None] * 365

        for day in range(0, 365):
            day_flights = {}
            for cityTo in self.city_list:
                day_flights[cityTo] = (randint(1, 600), randint(1, 600))

            year_flights[day] = day_flights

        return year_flights


class DataPreprocesor():
    def __init__(self, city_historic_days, year_flights, city_list, city_price_list, years):
        self.city_historic_days = city_historic_days
        self.years = years
        self.city_list = city_list
        self.city_price_list = city_price_list
        self.year_flights = year_flights
        self.generate_search_space()

    def generate_search_space(self):
        search_space = {}
        for city in self.city_list:
            destination_city_days = []
            for day in range(0, 365):
                historic_day_weather = []
                city_weather = self.city_historic_days[city]
                for year in range(0, NUMBER_OF_YEARS):
                    historic_day_weather.append(city_weather[year][day])
                day_flights = self.year_flights[day]
                city_day = Day(city, day_flights[city], self.city_price_list[city], historic_day_weather)
                destination_city_days.append(city_day)

            search_space[city] = destination_city_days

        return search_space


class UrlopPlaner():
    def __init__(self, search_space, vacation_period):
        self.search_space = search_space
        self.vacation_period = vacation_period
        self.city_list = list(self.search_space.keys())
        self.history = []

    def calculate_sum(self, all_days):
        days_values = []
        for day in all_days:
            good_days = 0
            neutral_days = 0
            for year in day.destination_weather_historic_data:
                if year == 1:
                    good_days += 1
                elif year == 0:
                    neutral_days += 1
                elif year == -1:
                    pass
                else:
                    raise Exception("That should not happen")
            days_values.append((good_days / NUMBER_OF_YEARS, (neutral_days + good_days) / NUMBER_OF_YEARS))

        all_days_predicted_wheather = [-1] * len(days_values)
        for tuple_index, tuple in enumerate(days_values):
            random_factor = random()
            for index, value in enumerate(tuple):
                if random_factor > value:
                    pass
                else:
                    if index == 0:
                        all_days_predicted_wheather[tuple_index] = 1
                        break
                    elif index == 1:
                        all_days_predicted_wheather[tuple_index] = 0
                        break

        wheather_value = 0
        for day_wheather in all_days_predicted_wheather:
            wheather_value += day_wheather

        return wheather_value

    def bad_pointy_acceptance_probability(self, current_temprature, qX, qY):
        return math.exp(-abs((qY - qX) / current_temprature))

    def q(self, coordinates, wi):
        day_number, destination = coordinates
        all_days = self.search_space[destination][day_number: day_number + self.vacation_period]
        if day_number + self.vacation_period > 364:
            all_days = self.search_space[destination][day_number:]
            all_days += self.search_space[destination][0:(day_number + self.vacation_period) % 364]

        period_weather_factor = self.calculate_sum(all_days)
        weather_part  = (wi / self.vacation_period) * period_weather_factor
        if weather_part == -1:
            weather_part = -0.999999

        objective_function = 1 / ((all_days[0].flight_price_to + all_days[-1].flight_price_from + (
        self.vacation_period * all_days[0].sleeping_price)) * (
                                  1 + (weather_part)))
        return objective_function

    def select_neighbour(self, current_point, sigma):
        day, city = current_point
        city_index = self.city_list.index(city)

        new_day = math.floor(gauss(day, sigma))
        new_city_idx = math.floor(gauss(city_index, sigma))
        while ((0 <= new_day < 365) is False) or ((0 <= new_city_idx < len(self.city_list)) is False):
            new_day = math.floor(gauss(day, sigma))
            new_city_idx = math.floor(gauss(city_index, sigma))

        return new_day, self.city_list[new_city_idx]

    def simulated_annealing(self, temp_generator, stop_condition, weather_importance, sigma):
        wi = weather_importance
        history = []
        current_iteration = 1
        beginning_temp = temp_generator(0)
        current_temperature = beginning_temp
        random_day = randint(0, 365)
        random_city = self.city_list[randint(0, len(self.city_list) - 1)]

        current_point = (random_day, random_city)
        while not stop_condition(current_iteration):
            self.history.append((current_point, current_iteration))
            neighbour = self.select_neighbour(current_point, sigma)
            qX = self.q(current_point, wi)
            qY = self.q(neighbour, wi)
            if qX < qY:
                current_point = neighbour
            elif random() < self.bad_pointy_acceptance_probability(current_temperature, qX, qY):
                current_point = neighbour
            current_iteration += 1
            current_temperature = temp_generator(current_iteration)

        return self.q(current_point, wi)


"""Data initialization"""
historicData = HistoricDataGenerator(NUMBER_OF_YEARS)
flightGenerator = CurrentFlightGenerator(historicData.get_city_list())
year_flights = flightGenerator.generate_flights()

dataPreprocesor = DataPreprocesor(historicData.city_historic_days, year_flights, historicData.get_city_list(),
                                  get_cities_prices(historicData.get_city_list()), NUMBER_OF_YEARS)
search_space = dataPreprocesor.generate_search_space()

urlopPlanes = UrlopPlaner(search_space, 6)

"""Helpers"""


def const_temp_gen(const):
    def const_temp(inter):
        return const
    return const_temp


def iter_stop_condition_gen(max):
    def fun(iter):
        if iter == max:
            return True
        return False
    return fun


def timed_stop_condition_gen(seconds):
    start = time.clock()

    def fun(iter):
        if time.clock() > seconds + start:
            return True
        return False
    return fun


def A():
    """ A) Różne stałe wartości parametru temperatury. """
    axisX = []
    axisY = []
    for temp_gen in range(1, 100, 10):
        qmax = 0
        for x in range(1, 20):
            qmax += urlopPlanes.simulated_annealing(const_temp_gen(temp_gen), iter_stop_condition_gen(100000), 0.3, 10.0)
        qmax /= 100.0
        axisX.append(temp_gen)
        axisY.append(qmax)
    plt.plot(axisX, axisY, 'ro')
    plt.ylabel('q')
    plt.xlabel('temperature')
    plt.show()

def B():
    """ B) Różne funkcje definiujące wartości temperatury zmiennej w czasie. """
    def square_function(iter):
        value = -0.03 * (iter*iter) + iter * 0.3 + 1
        if value != 0:
            return value
        return 0.000001

    def sin_func(iter):
        value = math.sin((iter+1)/100)
        if value != 0:
            return value
        return 0.000001

    def one_divided_by_iter(iter):
        value = 1/(iter+1)
        if value != 0:
            return value
        return 0.000001


    temp_functions = [square_function, sin_func, one_divided_by_iter]
    axisX = []
    axisY = []
    xticks = []
    for temp_function in temp_functions:
        qmax = 0
        iter = 10
        for x in range(1, iter):
            qmax += urlopPlanes.simulated_annealing(temp_function, iter_stop_condition_gen(1000), 0.3, 10.0)
        axisX.append(qmax/iter)
        axisY.append(qmax)
        xticks.append(temp_function.__name__)
    plt.xticks(axisX, xticks)
    plt.plot(axisX, axisY)
    plt.xlabel('function')
    plt.ylabel('q')
    plt.show()

B()

def C():
    """ C) Różne wartości współczynnika udziału pogody. """
    axisX = []
    axisY = []
    for wi in range(1, 10):
        iter = 10
        qmax = 0
        for x in range(1, iter):
            qmax += urlopPlanes.simulated_annealing(const_temp_gen(1000), iter_stop_condition_gen(1000), wi, 10.0)
        axisY.append(qmax/iter)
        axisX.append(wi)
    plt.plot(axisX, axisY, 'ro')

    plt.xlabel('wi')
    plt.ylabel('q')
    plt.show()


def D():
    """ D) Czas optymalizacji w zależności od długości planowanego urlopu. """
    axisX = []
    axisY = []
    for test in range(1, 100, 10):
        urlopPlanes = UrlopPlaner(search_space, test)
        iter = 10
        total = 0
        for x in range(1, iter):
            start = time.clock()
            qmax = urlopPlanes.simulated_annealing(const_temp_gen(10), iter_stop_condition_gen(100), 0.3, 10.0)
            total += time.clock() - start
        axisX.append(test)
        axisY.append(total/iter)
    plt.plot(axisX, axisY, 'ro')
    plt.xlabel('vacation period')
    plt.ylabel('time')
    plt.show()


def E():
    """E) Jakość optymalizacji w zależności od długości planowanego urlopu."""
    axisX = []
    axisY = []
    for test in range(1, 100, 10):
        urlopPlanes = UrlopPlaner(search_space, test)
        intr = 10
        qmax = 0
        for x in range(1, 10):
            qmax += urlopPlanes.simulated_annealing(const_temp_gen(10), iter_stop_condition_gen(100), 0.3, 10.0)
        axisX.append(test)
        axisY.append(qmax/iter)
    plt.plot(axisX, axisY, 'ro')
    plt.plot(axisX, axisY, 'ro')
    plt.xlabel('vacation period')
    plt.ylabel('qmax')
    plt.show()

E()
def draw_search_space():
    # Create a 1024x1024x3 array of 8 bit unsigned integers
    data = np.zeros( (NUMBER_OF_CITIES, 365, 3), dtype=np.uint8)
    data.fill(255)
    iterations = 100000.0;
    urlopPlanes.simulated_annealing(const_temp_gen(10), iter_stop_condition_gen(iterations), 0.3, 1000.0)
    history = urlopPlanes.history
    for point, iteration in history:
        day, city = point
        city_idx = urlopPlanes.city_list.index(city)
        data[day, city_idx] = [255.0*(iteration/iterations), 0, 255 * (1-iteration/iterations)]
    img = smp.toimage( data )       # Create a PIL image
    img.save('out.bmp')
    img.show()

draw_search_space()
