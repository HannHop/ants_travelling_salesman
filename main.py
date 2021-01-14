import random
# cities 3
x = [0, 3, 6, 7, 15, 10, 16, 5, 8, 1.5]
y = [1, 2, 1, 4.5, -1, 2.5, 11, 6, 9, 12]
list_cities = [None] * 10

for i in range(10):
    list_cities[i] = [x[i], y[i]]
n = 10  # number of cities and also number of ants
T_max = 200  # the maximum number of tours
alpha = 1
beta = 5
rho = 0.5


list_ants = 10 * [None]

class Ant:
    def __init__(self):
        self.initial_city = random.randint(0, 9)  # randomly choose the initial place for each ant
        self.unvisited_cities = [c for c in range(10) if c != self.initial_city]
        self.visited_cities = [self.initial_city]


ant = Ant()
for i in range(10):
    list_ants[i] = Ant()
# touring part - go through all cities and

for i in range(T_max):
    break
    #

print(list_cities)
# print(ant.initial_city, ant.unvisited_cities, ant.visited_cities)

for ant in list_ants:
    print(ant.initial_city, ant.unvisited_cities, ant.visited_cities)