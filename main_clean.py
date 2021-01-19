import random
import math
import matplotlib

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

# cities 3
#x = [0, 3, 6, 7, 15, 10, 16, 5, 8, 1.5]
#y = [1, 2, 1, 4.5, -1, 2.5, 11, 6, 9, 12]

#cities 4:
x = [3, 2, 12, 7, 9, 3, 16, 11, 9, 2]
y = [1, 4, 2, 4.5, 9, 1.5, 11, 8, 10, 7]

list_cities = [None] * 10
n = 10  # number of cities and also number of ants
T_max = 500  # the maximum number of tours
alpha = 1 #1
beta = 5 #5
rho = 0.5
list_ants = 10 * [None]
list_possible_arcs = 45 * [None]
best_tour_distance = 1000
best_tour_list = [None]
best_i = 10000000000000

class City:
    def __init__(self, x, y):
        self.number = 0
        self.x = x
        self.y = y


class Ant:
    def __init__(self):
        self.initial_city = random.randint(0, 9)  # randomly choose the initial place for each ant
        self.unvisited_cities = [c for c in range(10) if c != self.initial_city]
        self.visited_cities = [self.initial_city]
        self.tour_distance = 0


for i in range(10):
    # list_cities[i] = [i, [x[i], y[i]]]  # list of number, x,y coord of each city
    list_cities[i] = City(x[i], y[i])

# all possible combinations - kind of a map
index = 0
for i in range(0, 10):
    for j in range(i + 1, 10):
        list_possible_arcs[index] = [[i, j], math.sqrt(
            pow(list_cities[i].x - list_cities[j].x, 2) + pow(list_cities[i].y - list_cities[j].y, 2)), 0.1]
        index = index + 1

# make a set of ants
for i in range(10):
    list_ants[i] = Ant()

# touring part - go through all cities
for i in range(T_max):
    for ant in list_ants:
        # ant goes on tour:
        for _ in range(10):  # all steps of 1 ant
            filtered_arcs = []  # really all possible choices for this step
            for arc in list_possible_arcs:
                [l, r] = arc[0] # {[A, B], dist, tau}
                if (ant.visited_cities[-1] == l) or (ant.visited_cities[-1] == r):
                    if len(set(ant.visited_cities[:-1]).intersection(arc[0])) == 0:  #:-1 = all but last elem
                        # arc is legal and not used before
                        filtered_arcs.append(arc + [
                            (pow(arc[2], alpha) * pow(1 / arc[1], beta))])  # numerator of aij is a last elem of arc
            a_denominator = 0
            for filtered_arc in filtered_arcs:
                print(filtered_arc[-1])
                a_denominator = a_denominator + filtered_arc[-1] # sum of all aij numerators is a denominator
            # roulette wheel:
            sum_p = 0
            sum_all = 0
            for filtered_arc in filtered_arcs: # [[A,B], dist, tau,
                sum_all = sum_all + filtered_arc[-1] / a_denominator
            # print(" sumall: ", sum_all)
            rand_val = random.uniform(0, sum_all)

            for filtered_arc in filtered_arcs:
                sum_p = sum_p + filtered_arc[-1] / a_denominator
                if sum_p >= rand_val:
                    next_city = set(filtered_arc[0])
                    next_city.discard(ant.visited_cities[-1])
                    next_city = list(next_city)[0]
                    print(ant.visited_cities, ant.unvisited_cities, filtered_arc[0])
                    ant.visited_cities.append(next_city)
                    ant.unvisited_cities.remove(next_city)
                    ant.tour_distance = ant.tour_distance + filtered_arc[1]
                    break

        for possible_arc in list_possible_arcs:
            if [ant.visited_cities[-1], ant.visited_cities[0]] in possible_arc:
                ant.tour_distance = ant.tour_distance + possible_arc[1]
                ant.visited_cities.append(ant.visited_cities[0])
            elif [ant.visited_cities[0], ant.visited_cities[-1]] in possible_arc:
                ant.tour_distance = ant.tour_distance + possible_arc[1]
                ant.visited_cities.append(ant.visited_cities[0])

        if ant.tour_distance <= best_tour_distance:
            best_tour_distance = ant.tour_distance
            best_tour_list = ant.visited_cities
            best_i = i

    # evaporation of pheromone:
    for possible_arc in list_possible_arcs:
        possible_arc[2] = (1 - rho) * possible_arc[2]

    for ant in list_ants:
        for j in range(n - 1):  # all pheromone trials
        #for j in range(len(ant.visited_cities) ):  # all pheromone trials
            # ant distributes pheromones
            for possible_arc in list_possible_arcs:
                #print("poss arc: ", possible_arc)
                if [ant.visited_cities[j], ant.visited_cities[j + 1]] in possible_arc:
                    # deposit:
                    possible_arc[2] = possible_arc[2] + 1 / ant.tour_distance
                elif [ant.visited_cities[j + 1], ant.visited_cities[j]] in possible_arc:
                    # deposit
                    possible_arc[2] = possible_arc[2] + 1 / ant.tour_distance

        if i == T_max - 1:
            break
        # delete all ant's knowledge about tour and start fresh
        ant.visited_cities = [ant.visited_cities[0]]
        ant.unvisited_cities = [c for c in range(10) if c != ant.initial_city]
        ant.tour_distance = 0

print("best distance: ", best_tour_distance, "tour: ", best_tour_list)

path_x = [x[i] for i in best_tour_list]
path_y = [y[i] for i in best_tour_list]
path_x.append(path_x[0])
path_y.append(path_y[0])

plt.scatter(x, y)
plt.plot(path_x, path_y)
plt.show()

print("best i in: ", best_i)
for ant in list_ants:
    print("ant init number: ", ant.initial_city, "visited: ", ant.visited_cities, "distance:", ant.tour_distance)
