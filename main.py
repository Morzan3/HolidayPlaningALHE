from enum import Enum
from faker import Factory
from random import randint, random
import math

NUMBER_OF_CITIES = 20
NUMBER_OF_YEARS = 10

fakeFactory = Factory.create()


class Flight:
    def __init__(self, cityFrom, cityTo, price):
        self.cityFrom = cityFrom
        self.cityTo = cityTo
        self.price = price




class Day():
    def __init__(self, destination, flight_price, sleeping_price, historic_weather):
        self.destination = destination
        self.flight_price_to, self.flight_price_from = flight_price
        self.historic_weather_day_city_data = historic_weather
        self.sleeping_price = sleeping_price



def get_city_prices(city_list):
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
        for i in range(0, NUMBER_OF_CITIES):
            self.city_historic_days[fakeFactory.city()] = self.populate_days_with_random_data(year_number)

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
        flights = self.generate_flights()
        print(flights)


    def generate_flights(self):
        # year_flights = [None] * 365
        #
        # for day in range(0, 365):
        #     day_flights = {}
        #     for cityFrom in self.city_list:
        #         day_flights[cityFrom] = {}
        #         day_flights_dict = day_flights[cityFrom]
        #         for cityTo in self.city_list:
        #             if cityFrom != cityTo:
        #                 day_flights_dict[cityTo] = randint(1, 600)
        #
        #         day_flights[cityFrom] = day_flights_dict
        #
        #     year_flights[day] = day_flights
        #
        # return year_flights


        year_flights = [None] * 365

        for day in range(0, 365):
            day_flights = {}
            for cityTo in self.city_list:
                day_flights[cityTo] = (randint(1, 600), randint(1, 600))

            year_flights[day] = day_flights

        return year_flights


class DataPreprocesor():
    def __init__(self, city_historic_days, year_flights, city_list,city_price_list, years):
        self.city_historic_days = city_historic_days
        self.years = years
        self.city_list = city_list
        self.city_price_list = city_price_list
        self.year_flights = year_flights
        self.calculate_wheather_factor()
        self.predict_city_wheather()
        self.generate_search_space()

    def calculate_wheather_factor(self):
        self.city_day_wheather_probability = {}
        for city in self.city_historic_days:
            current_city = self.city_historic_days[city]
            all_days_city_wheather = []
            for day in range(0,365):
                good_days = 0
                neutral_days = 0
                for year in range(0, self.years):
                    if current_city[year][day] == 1:
                        good_days += 1
                    elif current_city[year][day] == 0:
                        neutral_days += 1
                    elif current_city[year][day] == -1:
                        pass
                    else:
                        raise Exception("That should not happen")

                good_probability = good_days/self.years
                neutral_probability = neutral_days/self.years
                all_days_city_wheather.append((good_probability, neutral_probability + good_probability, 1))
            self.city_day_wheather_probability[city] = all_days_city_wheather

    def predict_city_wheather(self):
        self.predicted_city_days_wheather = {}
        for city in self.city_day_wheather_probability:
            current_city_probabilities = self.city_day_wheather_probability[city]
            all_days_predicted_wheather = [None] * 365

            for day in range(0, 365):
                probability_tuple = current_city_probabilities[day]
                random_factor = random()
                for index, value in enumerate(probability_tuple):
                    if random_factor > value:
                        pass
                    else:
                        if index == 0:
                            all_days_predicted_wheather[day] = 1
                        elif index == 1:
                            all_days_predicted_wheather[day] = 0
                        elif index == 2:
                            all_days_predicted_wheather[day] = -1

            self.predicted_city_days_wheather[city] = all_days_predicted_wheather


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


    def calculate_sum(self, all_days):
        days_values = []
        for day in all_days:
            good_days = 0
            neutral_days = 0
            for year in day.historic_weather_day_city_data:
                if year == 1:
                    good_days += 1
                elif year == 0:
                    neutral_days += 1
                elif year == -1:
                    pass
                else:
                    raise Exception("That should not happen")
            days_values.append((good_days/NUMBER_OF_YEARS, (neutral_days + good_days)/NUMBER_OF_YEARS))

        all_days_predicted_wheather = [-1] * len(days_values)
        for tuple_index,tuple in enumerate(days_values):
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

    def stop(self, current_iteration):
        if current_iteration == 1000000000:
            return True
        return False

    def bad_pointy_acceptance_probability(self,current_temprature, qX, qY):
        return math.exp(-abs((qY-qX)/current_temprature))

    def q(self, coordinates):
        day_number, destination = coordinates
        all_days = self.search_space[destination][day_number: day_number+self.vacation_period]

        period_weather_factor = self.calculate_sum(all_days)

        try:
            objective_function = 1/((all_days[0].flight_price_to + all_days[-1].flight_price_from + (self.vacation_period * all_days[0].sleeping_price)) * (1 + ((self.weather_importance/self.vacation_period) * period_weather_factor)))
        except Exception as e:
            print("siema")
        return objective_function


    def select_neighbour(self, current_point):
        day, city = current_point

        random_factor = random()
        city_index = self.city_list.index(city)


        if 0 <= random_factor < 0.25:
            return (abs(day + 1) % 365, city)
        elif 0.25 <= random_factor < 0.5:
            return (abs(day - 1) % 365, city)
        elif 0.5 <= random_factor < 0.75:
            print((city_index + 1) % NUMBER_OF_CITIES)
            new_city = self.city_list[(city_index + 1) % NUMBER_OF_CITIES]
            return (day, new_city)
        elif 0.75 <= random_factor <= 1:
            new_city = self.city_list[abs(city_index - 1) % NUMBER_OF_CITIES]
            return (day, new_city)

    def simulated_annealing(self):
        current_iteration = 1
        begining_temp = self.temperature
        current_temprature = self.temperature
        self.city_list = list(self.search_space.keys())
        random_day = randint(0, 365)
        random_city = self.city_list[randint(0,len(self.city_list)-1)]

        visited_points_set = set((random_day,random_city))
        current_point = (random_day, random_city)
        while not self.stop(current_iteration):
            neighbour = self.select_neighbour(current_point)
            qX = self.q(current_point)
            qY = self.q(neighbour)
            if qX < qY:
                current_point = neighbour
                visited_points_set.add(current_point)
            elif random() < self.bad_pointy_acceptance_probability(current_temprature, qX, qY):
                current_point = neighbour
                visited_points_set.add(current_point)
            print(neighbour)
            current_iteration += 1
            current_temprature = begining_temp/current_iteration





historicData = HistoricDataGenerator(NUMBER_OF_YEARS)
flightGenerator = CurrentFlightGenerator(historicData.get_city_list())
year_flights = flightGenerator.generate_flights()

dataPreprocesor = DataPreprocesor(historicData.city_historic_days, year_flights, historicData.get_city_list(), get_city_prices(historicData.get_city_list()),NUMBER_OF_YEARS)

urlopPlanes = UrlopPlaner(dataPreprocesor.generate_search_space(), 100, 0.3, 6)
urlopPlanes.simulated_annealing()