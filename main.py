import numpy as np

notas_disponiveis = ['A', 'A#', 'B', 'B#', 'C', 'C#', 'D', 'D#', 'E', 'E#', 'F', 'F#', 'G', 'G#']

def check_stop_condition():
    return
def generate_population(population_size, chromossome_size):
    return np.random.choice(notas_disponiveis, (population_size, chromossome_size))
def population_selection():
    return
def mutate_swap():
    return
def mutate_generate():
    return
def mutate_degenerate():
    return
def crossover():
    return

population_size = 100
entrada = [['C', 'E', 'G'], ['C', 'E', 'G'], ['E', 'G#', 'B'], ['E', 'G#', 'B'], ['G', 'B', 'D'], ['G', 'B', 'D'], ['C', 'E', 'G'], ['E', 'G#', 'B'], ['G', 'B', 'D'], ['G', 'B', 'D']]

saida = ('C', ['C', 'C', 'E', 'E', 'G', 'G', 'C', 'E', 'G', 'G'])

print(generate_population(population_size, np.shape(entrada)[1] + 1))