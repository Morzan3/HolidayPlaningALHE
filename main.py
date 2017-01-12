from faker import Factory
from random import randint, random, gauss
import math

NUMBER_OF_CITIES = 40
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
        w, h = 365, year_number
        self.city_historic_days = {}
        self.years = year_number
        self.assing_cities(year_number)

    def assing_cities(self, year_number):
        unique_names = set()
        while len(unique_names) != NUMBER_OF_CITIES:
            unique_names.add(fakeFactory.city())
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
        # self.calculate_wheather_factor()
        # self.predict_city_wheather()
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
    def __init__(self, search_space, temperature, weather_importance, vacation_period):
        self.search_space = search_space
        self.temperature = temperature
        self.weather_importance = weather_importance
        self.vacation_period = vacation_period
        self.city_list = list(self.search_space.keys())

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

    def stopCondition(self, current_iteration):
        if current_iteration == 1000:
            return True
        return False

    def bad_pointy_acceptance_probability(self, current_temprature, qX, qY):
        return math.exp(-abs((qY - qX) / current_temprature))

    def q(self, coordinates):
        day_number, destination = coordinates
        all_days = self.search_space[destination][day_number: day_number + self.vacation_period]

        period_weather_factor = self.calculate_sum(all_days)

        objective_function = 1 / ((all_days[0].flight_price_to + all_days[-1].flight_price_from + (
        self.vacation_period * all_days[0].sleeping_price)) * (
                                  1 + ((self.weather_importance / self.vacation_period) * period_weather_factor)))
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

    def simulated_annealing(self):
        current_iteration = 1
        beginning_temp = self.temperature
        current_temperature = self.temperature
        random_day = randint(0, 365)
        random_city = self.city_list[randint(0, len(self.city_list) - 1)]

        current_point = (random_day, random_city)
        while not self.stopCondition(current_iteration):
            neighbour = self.select_neighbour(current_point, 10.0)
            if not neighbour:
                print("test")
            qX = self.q(current_point)
            qY = self.q(neighbour)
            if qX < qY:
                current_point = neighbour
            elif random() < self.bad_pointy_acceptance_probability(current_temperature, qX, qY):
                current_point = neighbour
            print(neighbour)
            current_iteration += 1
            current_temperature = beginning_temp / current_iteration


historicData = HistoricDataGenerator(NUMBER_OF_YEARS)
flightGenerator = CurrentFlightGenerator(historicData.get_city_list())
year_flights = flightGenerator.generate_flights()

dataPreprocesor = DataPreprocesor(historicData.city_historic_days, year_flights, historicData.get_city_list(),
                                  get_cities_prices(historicData.get_city_list()), NUMBER_OF_YEARS)

urlopPlanes = UrlopPlaner(dataPreprocesor.generate_search_space(), 100, 0.3, 6)
urlopPlanes.simulated_annealing()
