# -*- coding: utf-8 -*-
"""8Queen_EC.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ktPqfG86Ze_YukW-gO8aH6LLRD5YE9sb
"""

import numpy as np
import random
import heapq

n = 8
generation = 0
def RandomGene():
    x = []
    for i in range(8):
        x.append(random.randint(1, 8))
    return x

#--------------------------------------------------------------------------------------------

#---------------------------------Fitness Calculation---------------------------------------------
#calculating how many queens are in a same row
def Horizontal_Error(gene):
    error = 0
    for i in gene:
        error += (gene.count(i) - 1)
    return error/2
#calculating how many queens are in each left diagonal
def Left_Diagonals(gene):
    n = len(gene)
    left_diag = [0] * (2 * n)
    for i in range(n):
        left_diag[i + gene[i] - 1] += 1
    return left_diag
#calculating how many queens are in each right diagonal
def Right_Diagonals(gene):
    n = len(gene)
    right_diag = [0] * (2 * n)
    for i in range(n):
        right_diag[8 - i + gene[i] - 2] += 1
    return right_diag
#calculating how many diagonals have more than 1 queens in them 
def Diagonal_Error(gene):
    error = 0
    left_diag = Left_Diagonals(gene)
    right_diag = Right_Diagonals(gene)
    for i in range(16):
        if (left_diag[i] > 1):
            error += (left_diag[i])
        if (right_diag[i] > 1):
            error += (right_diag[i])
    return error / 2
#subtracting the number of errors from max fitness
def Fitness(gene):
    fitness = 20
    error = Diagonal_Error(gene) + Horizontal_Error(gene)
    return(fitness - error)

#-----------------------------Genetic Operators-------------------------------------------------
def Recombination(gene1, gene2):
    cut = random.randint(0 , 7)
    child1 = gene1[0 : cut] + gene2[cut : n]
    child2 = gene2[0 : cut] + gene1[cut : n]
    return child1 , child2 

#Mutation with a probability of 80%
def Mutation(gene):
    chance = random.randint(0, 100)
    if (chance < 80):
        bit = random.randint(0, 7)
        altered_bit = random.randint(1, 8)
        gene[bit] = altered_bit
    return gene

#Randomly Generating 100 genes 
def Initialize():
    
    population_size = 100 
    population = []
    for i in range(population_size):
        population.append(RandomGene())
    fitness_list = [Fitness(population[i]) for i in range(len(population))]
    return population, fitness_list

#Finding the two worst genes in population and removing them
def Cull(population, fitness_list):
    cull = []
    cull.append(heapq.nsmallest(2, fitness_list))

    index1 = fitness_list.index(cull[0][0])
    bad_gene1 = population[index1]
    fitness_list.remove(cull[0][0])
    population.remove(bad_gene1)


    index2 = fitness_list.index(cull[0][1])
    bad_gene2 = population[index2]
    fitness_list.remove(cull[0][1])
    population.remove(bad_gene2)
    
    return population, fitness_list

#randomly selecting 5 genes from population and select the best 2 out 5 to be parents
def Parent_Selection(population, fitness_list):
    randomgenes = random.choices(population, k=5)
    randomfitness = [Fitness(randomgenes[i]) for i in range(len(randomgenes))]
    parent1fit = max(randomfitness)
    parent1index = randomfitness.index(parent1fit)
    parent1 = randomgenes[parent1index]
    randomfitness.pop(parent1index)
    randomgenes.pop(parent1index)


    parent2fit = max(randomfitness)
    parent2index = randomfitness.index(parent2fit)
    parent2 = randomgenes[parent2index]
    return parent1 , parent2

#adding the generated children to the population
def ADD_Children(child1, child2, population, fitness_list):
    population.append(child1)
    fitness_list.append(Fitness(child1))
    population.append(child2)
    fitness_list.append(Fitness(child2))
    return population, fitness_list

#representing the best gene present in the population
def Best_Gene(population , fitness_list):
    max_fitness_in_pop = max(fitness_list)
    print(f"max fitness present in population: {max_fitness_in_pop}")
    index_best = fitness_list.index(max(fitness_list))
    print(population[index_best])

#selecting two parents, making 2 children out of them and replacing them with two of the worst genes in the population 
def Pass_Generation(population, fitness_list):
    parent1, parent2 = Parent_Selection(population, fitness_list)

    child1 , child2 = Recombination(parent1, parent2)

    child1 = Mutation(child1)
    child2 = Mutation(child2)

    population, fitness_list = ADD_Children(child1 , child2 , population, fitness_list)

    population, fitness_list = Cull(population, fitness_list)


    print(f"Generation {generation}")
    Best_Gene(population, fitness_list)

#Passing generations untill we reach a maximum fitness or 10000 generations have passed
population, fitness_list =Initialize()
while((not 20 in fitness_list) & (generation < 10000)):
    generation += 1
    Pass_Generation(population, fitness_list)