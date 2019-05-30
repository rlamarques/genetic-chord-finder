import numpy as np
import sys
import random

from relations import harmonic_fields
from chords import available_chords

np.set_printoptions(threshold=sys.maxsize)

notas_disponiveis = ['A', 'A#', 'B', 'B#', 'C', 'C#', 'D', 'D#', 'E', 'E#', 'F', 'F#', 'G', 'G#']
tons_disponiveis = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']

acordes_disponiveis = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']
acordes_disponiveis += [s + 'm' for s in acordes_disponiveis]

def arrived_at_stop_condition(gen, max_gen, chromosome,):
    if gen >= max_gen:
        return True
    if fitness(chromosome) == 1.0:
        return True
    return False

def generate_population(population_size, chromossome_size):
    population = []
    while population_size > 0:
        random_key = np.random.choice(tons_disponiveis, 1)
        random_chords = np.random.choice(acordes_disponiveis, chromossome_size)

        population.append(list(np.concatenate((random_key, random_chords))))
        population_size -= 1

    return population

def pre_selection(population, elite_ratio):
    fitness_sort = np.argsort([fitness(x) for x in population])
    sorted_population = np.array(population)[fitness_sort[::-1]]
    elite_index = np.shape(population)[0] / elite_ratio

    elite_index = int(elite_index)

    return sorted_population[:elite_index]

def post_selection(population, initial_size):
    fitness_sort = np.argsort([fitness(x) for x in population])
    sorted_population = np.array(population)[fitness_sort[::-1]]
    return sorted_population[:initial_size]

def mutate_gene(offspring):
    original_offspring = np.copy(offspring)
    offspring_size = len(offspring)
    available_chords_count = len(acordes_disponiveis) - 1
    available_keys_count = len(tons_disponiveis) - 1
    chromosome_size = len(offspring[0]) - 1

    random_chords = np.random.randint(0, available_chords_count, offspring_size)
    random_keys   = np.random.randint(0, available_keys_count, offspring_size)
    random_indexes = np.random.randint(1, chromosome_size, offspring_size)
    for i, individual in enumerate(offspring):
        individual[random_indexes[i]] = acordes_disponiveis[random_chords[i]]
        individual[0] = tons_disponiveis[random_keys[i]]
    return offspring

def crossover(elite):
    offspring = []
    elite_size = len(elite[0])-1
    rnd = random.randint(1, elite_size)
    for index in enumerate(elite[:-1]):
        i = index[0]
        head = elite[i][:rnd]
        tail = elite[i+1][rnd:]
        child = np.concatenate((head, tail))
        offspring.append(child)
    head = elite
    return offspring

# Calculate an index of correct notes from a chord
def calculate_chord_match(notes, chord):
    chord_fitness = 0
    chord_notes = available_chords[chord][1]
    for note in notes:
        if note in chord_notes:
            chord_fitness += 1
        else:
            chord_fitness -= 1

    return chord_fitness / len(notes) #normalize for range 0-1

# Calculate an index of the harmony of a gene given a key
def calculate_key_match(gene):
    allowed_chords = harmonic_fields[gene[0]][1] #### check if the allowed chords are a tuple or an array
    key_fitness = 0
    for chord in gene[1:]:
        if chord in allowed_chords:
            key_fitness += 1
        else:
            key_fitness -= 1
    return key_fitness / len(gene[1:]) #normalize for range 0-1

# Calculate the overall fitness of a chromosome
def fitness(chromossome):
    chromossome_size = np.shape(chromossome)[0]
    chords_fitness = 0
    for index, chord in enumerate(chromossome[1:]):
        notes = entrada[index]
        chords_fitness += calculate_chord_match(notes, chord)

    key_fitness = calculate_key_match(chromossome)

    chords_fitness = chords_fitness / (chromossome_size - 1)
    # returns the current fitness divided by the maximum fitness
    return (chord_weight * chords_fitness + key_weight * key_fitness) / (chord_weight + key_weight)


# Main ---------------------------------------------------------------------------------------------



entrada = [['C', 'E', 'G'], ['C', 'E', 'G'], ['E', 'G', 'B'], ['E', 'G', 'B'], ['G', 'B', 'D'], ['G', 'B', 'D'], ['C', 'E', 'G'], ['E', 'G', 'B'], ['G', 'B', 'D'], ['G', 'B', 'D'], ['D', 'F', 'A']]

# Parameters
population_size = 450
max_gen = 1000
elite_ratio = 20
chord_weight = len(entrada)
key_weight = 1
print(len(entrada))


saida = ['C', 'C', 'C', 'Em', 'Em', 'G', 'G', 'C', 'Em', 'G', 'G', 'Dm']
print('Fitness ideal: ', fitness(saida))

print('Generated initial population.')

print('Population fitness evolution:')
should_stop = False
population = initial_population
gen_count = 0
while(not should_stop):
    elite = pre_selection(population, elite_ratio)

    offspring = crossover(elite)
    mutated_offspring = mutate_gene(offspring)

    family = np.concatenate((population, mutated_offspring))

    population = post_selection(family, len(population))

    should_stop = arrived_at_stop_condition(gen_count, max_gen, population[0])

    gen_count += 1

print('Gerações produzidas ' + str(gen_count - 1))
print('Ultima solução encontrada: ', population[0])
print('Fitness da solução:', fitness(population[0]))
