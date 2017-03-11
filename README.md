# Holiday Planning using simulated annealing algorithm

Program written for "Heuristic Algorithms" subject which task is to plan the best holidays of specified length based on various factors. Things which are evaluated by algorithm:
1. Ticket price for both directions.
2. Price of hotel located in the destination place
3. Weather

Weather is predicted with specific probability based on the data from 10 previous years about conditions each day.

Search space is 2 dimensional table of specific city and specific day of the year. Each cell contains data about flight prices (from this city and to this city), historical weather data, price of the hotel.

To find the global maximum of this search space a simulated annealing with changeable temperature was implemented.

In order to determine best temperature change function and variables like weather importance factor the following tests were carried out:
A) Different, constant values of temperature.
B) Different functions defining temperature change.
    i) Square function
    ii) Sin function
    iii) One divided by iteration number
C) Different values of weather importance factor.
D) Optimization time depending on length of the holiday.
E) Quality of optimization depending on length of the holiday.

## Getting Started

```
$ git clone https://github.com/Morzan3/HolidayPlaningALHE/blob/master/main.py
$ cd HolidayPlaningALHE
```

### Prerequisites

In order to run the script you have to install used libraries (Faker, matplotlib etc.)

```
$ pip3 install faker
```


## Running the tests

Test are already implemented in the script

## Running the script

```
python(3) main.py
```

## Authors

* **Ignacy Ślusarczyk** - [Morzan3](https://github.com/Morzan3)
* **Piotr Ganicz** - [PGanicz](https://github.com/PGanicz)
