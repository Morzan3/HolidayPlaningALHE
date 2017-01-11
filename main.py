from enum import Enum
from faker import Factory
from random import randint, random

NUMBER_OF_CITIES = 20
NUMBER_OF_YEARS = 10
fakeFactory = Factory.create()


class Flight:
    def __init__(self, cityFrom, cityTo, price):
        self.cityFrom = cityFrom
        self.cityTo = cityTo
        self.price = price

def get_city_prices(self):
    city_price_list = {}

    for city in self.city_historic_days:
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
        year_flights = [None] * 365

        for day in range(0, 365):
            day_flights = {}
            for cityFrom in self.city_list:
                day_flights[cityFrom] = {}
                day_flights_dict = day_flights[cityFrom]
                for cityTo in self.city_list:
                    if cityFrom != cityTo:
                        day_flights_dict[cityTo] = randint(1, 600)

                day_flights[cityFrom] = day_flights_dict

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
        search_space = [[None for x in range(365)] for y in range(len(self.city_list))]
        for city in range(0, len(self.city_list)):
            for day in range(0, 365):
                




class Wheather(Enum):
    GOOD = 1
    NEUTRAL = 0
    BAD = -1



class Day():
    def __init__(self, origin_city_name, flight_city_dict):
        self.flight_city_dict = flight_city_dict
        self.city_name = origin_city_name
        self.predicted_city_wheather = {}
        flights = []




class UrlopPlaner():
    def __init__(self):
        pass



historicData = HistoricDataGenerator(NUMBER_OF_YEARS)
flightGenerator = CurrentFlightGenerator(historicData.get_city_list())
year_flights = flightGenerator.generate_flights()
dataPreprocesor = DataPreprocesor(historicData.city_historic_days, year_flights, historicData.get_city_list(),get_city_prices(),NUMBER_OF_YEARS)

