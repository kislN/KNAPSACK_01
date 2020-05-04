import numpy as np
import copy
import random
from numpy.random import choice
import matplotlib.pyplot as plt
np.random.seed(42)


class Chromosome:
    def __init__(self, lenght):
        self.body = np.random.randint(low=0, high=2, size=lenght)
        self.fitness_value = 0
        self.capacity = np.inf

    def __str__(self):
        return str(self.body) + ' - ' + str(self.fitness_value)

    def __lt__(self, other):
        return self.fitness_value < other.fitness_value


class Population:
    def __init__(self, capacity, weights, costs, population_size=20, crossover_rate=0.2, mutation_rate=1/1000,
                 verbose=False, plot=False):
        self.epoch = 0
        self.capacity = capacity
        self.weights = weights
        self.costs = costs
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.population_size = population_size
        self.length = len(self.weights)
        self.population = [Chromosome(self.length) for _ in range(population_size)]
        self.history = []
        self.verbose = verbose
        self.plot = plot

    def get_fitness_value(self, chromosome):
        return (chromosome.body*self.costs).sum()

    def get_capacity(self, chromosome):
        return (chromosome.body*self.weights).sum()

    def update_capacity(self):
        for chr in self.population:
            chr.capacity = self.get_capacity(chr)

    def update_fitness(self):
        for chr in self.population:
            chr.fitness_value = self.get_fitness_value(chr)


    @staticmethod
    def choice_copy(chromosomes):
        for idx, chr in enumerate(chromosomes):
            chromosomes[idx] = copy.deepcopy(chromosomes[idx])
        return chromosomes

    def drop_redundant(self):
        for chromosome in self.population:
            while chromosome.capacity > self.capacity:
                indexes = np.where(chromosome.body == 1)[0]
                drop_index = choice(indexes)
                chromosome.body[drop_index] = 0
                chromosome.capacity -= self.weights[drop_index]
                chromosome.fitness_value -= self.costs[drop_index]

    def check_equ(self):
        fitness_values = []
        for chr in self.population:
            fitness_values.append(chr.fitness_value)

        values, counts = np.unique(fitness_values, return_counts=True)
        frequent_index = np.argmax(counts)
        self.history.append(values[frequent_index])
        percentage = counts.max()/counts.sum()
        return percentage

    def group_selection(self, chromosomes):
        chromosomes = sorted(chromosomes, reverse=True)
        num_chr = len(chromosomes)//4
        new_population = []
        for i in range(len(chromosomes)):
            group = choice(4, p=[0.5, 0.3, 0.15, 0.05])
            chr = choice(num_chr)
            chr = chromosomes[group*num_chr+chr]
            new_population.append(copy.deepcopy(chr))
        return new_population

    def roulette_wheel(self, chromosomes, num):

        fitness_values = []

        for chr in chromosomes:
            fitness_values.append(chr.fitness_value)

        fitness_values, indexes = np.unique(fitness_values, return_index=True)
        fitness_prob = fitness_values/fitness_values.sum()
        chromosomes = [chromosomes[i] for i in indexes]
        new_population = choice(chromosomes, size=num, p=fitness_prob)
        new_population = self.choice_copy(new_population)
        return new_population

    def crossover(self, chromosomes):
        for chr_1, chr_2 in zip(chromosomes[0::2], chromosomes[1::2]):
            if np.random.rand() < self.crossover_rate:
                crossover_point = np.random.randint(low=0, high=self.length)
                temp = copy.deepcopy(chr_1.body[crossover_point:])
                chr_1.body[crossover_point:] = copy.deepcopy(chr_2.body[crossover_point:])
                chr_2.body[crossover_point:] = temp
        return chromosomes

    def selection(self, best_ratio=1/2):
        self.population = sorted(self.population, reverse=True)
        take_best_num = int(len(self.population)*best_ratio)
        best = self.population[:take_best_num]
        roulette = self.roulette_wheel(self.population, self.population_size-take_best_num)
        return best, roulette

    def mutation(self, chromosomes):
        for i, chr in enumerate(chromosomes):
            for j, element in enumerate(chr.body):
                if np.random.rand() < self.mutation_rate:
                    if element==0:
                        chromosomes[i].body[j] = 1
                        chromosomes[i].capacity += self.weights[j]
                        chromosomes[i].fitness_value += self.costs[j]
                    else:
                        chromosomes[i].body[j] = 0
                        chromosomes[i].capacity -= self.weights[j]
                        chromosomes[i].fitness_value -= self.costs[j]

        return chromosomes

    def debug_info(self):
        fitness_values = []
        for chr in self.population:
            fitness_values.append(chr.fitness_value)

        values, indexes, counts = np.unique(fitness_values, return_counts=True, return_index=True)
        percentage = counts.max()/counts.sum()
        frequent_index = np.argmax(counts)
        frequent_value = values[frequent_index]
        chr = self.population[indexes[frequent_index]]
        print('Epoch: {} - frequent: {} - percentage: {}'.format(self.epoch, frequent_value, percentage))
        print(chr)

    def fit(self, epoches):
        self.update_capacity()
        self.update_fitness()
        self.drop_redundant()

        while self.check_equ() < 0.9:
            if self.epoch == epoches:
                break
            self.epoch += 1

            best, roulette = self.selection()
            np.random.shuffle(roulette)
            roulette = self.crossover(roulette)
            roulette = self.mutation(roulette)
            self.population = np.concatenate([best, roulette])

            self.update_capacity()
            self.update_fitness()
            self.drop_redundant()

            if self.verbose:
                self.debug_info()
        optim_weight = (self.population[0].body*self.weights).sum()
        optim_cost = (self.population[0].body*self.costs).sum()

        if self.plot:
            self.plot_fit()

        return (optim_cost, optim_weight, self.population[0].body)

    def plot_fit(self):
        x = np.arange(len(self.history))
        plt.plot(x, self.history)
        plt.xlabel('steps (log)')
        plt.ylabel('most frequent value')
        plt.xscale('log')
        plt.title('Genetic algorithm solution')
        plt.grid()
        plt.show()

def genetic_algorithm(capacity, weights, costs, population_size=20, crossover=0.75, mutation=0.001,
                      epoches=10000, verbose=False, plot=False):
    popul = Population(capacity=capacity, weights=weights, costs=costs,
                       population_size=population_size, crossover_rate=crossover,
                       mutation_rate=mutation, verbose=verbose, plot=plot)
    output = popul.fit(epoches)
    return output
