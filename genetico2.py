import random
import mido
from mido import Message, MidiFile, MidiTrack
import pygame
import time

# Melodía de "Für Elise" de Beethoven (una lista de tuplas de nota y duración)
desired_melody = [('E', 500), ('D#', 500), ('E', 500), ('D#', 500),
                 ('E', 500), ('B', 500), ('D', 500), ('C', 500),
                 ('A', 500), ('A#', 500), ('B', 500), ('E', 500),
                 ('D', 500), ('C', 500), ('B', 500), ('E', 500),
                 ('D', 500), ('C', 500), ('B', 500), ('A', 500),
                 ('A#', 500), ('B', 500), ('E', 500), ('D', 500),
                 ('C', 500), ('B', 500), ('E', 500), ('D', 500),
                 ('C', 500), ('B', 500), ('A', 500)]
# Diccionario para mapear notas a sus valores MIDI
note_to_midi = {
    'C': 60,
    'C#': 61,
    'D': 62,
    'D#': 63,
    'E': 64,
    'F': 65,
    'F#': 66,
    'G': 67,
    'G#': 68,
    'A': 69,
    'A#': 70,
    'B': 71
}
# Función para convertir la nota a su valor MIDI
def note_to_midi_value(note):
    return note_to_midi.get(note, 60)  # 60 es el valor MIDI para 'C' si la nota no está en el diccionario
# Función para generar una secuencia de acordes
def generate_chords():
    # Ejemplo: Generación aleatoria de acordes para una canción de 4 compases
    chords = []
    possible_chords = ['C', 'D', 'E', 'F', 'G', 'A', 'B']

    for _ in range(16):  # 16 tiempos (4 compases de 4 tiempos cada uno)
        chord = random.choice(possible_chords)  # Seleccionar un acorde aleatorio
        chords.append(chord)

    return chords

# Función para generar una secuencia de melodía para un acorde
def generate_melody(chord):
    # Ejemplo: Generación de melodía básica para un acorde
    melody = []
    durations = [500, 1000, 1500, 2000]  # Ejemplo de duraciones posibles

    for _ in range(4):  # Generar 4 notas para el acorde
        note = random.choice(chord)  # Seleccionar una nota aleatoria del acorde
        duration = random.choice(durations)  # Seleccionar una duración aleatoria

        melody.append((note, duration))

    return melody

# Función para comparar la melodía generada con la melodía deseada
def compare_melodies(generated_melody):
    similarity_score = 0
    for desired_note, desired_duration in desired_melody:
        for generated_note, generated_duration in generated_melody:
            if desired_note == generated_note and desired_duration == generated_duration:
                similarity_score += 1
    return similarity_score

# Función de aptitud que utiliza la comparación de melodías
def fitness_function(chords):
    # Calculamos la puntuación de la secuencia de acordes basada en cuánto se ajusta a la melodía deseada
    melody = []
    for chord in chords:
        melody.extend(generate_melody(chord))

    # Retorna la puntuación de la aptitud basada en la comparación de melodías
    return compare_melodies(melody)

# Función para escribir la canción en un archivo MIDI
def write_midi_file(chords):
    midi_file = MidiFile()

    track = MidiTrack()
    midi_file.tracks.append(track)

    time = 0
    for chord in chords:
        for note in chord:
            midi_note = note_to_midi_value(note)
            track.append(Message('note_on', note=midi_note, velocity=64, time=time))
            track.append(Message('note_off', note=midi_note, velocity=64, time=500))  # Duración de nota (500 ms)
        time = 0  # Pausa entre acordes

    # Guardar el archivo MIDI
    midi_file.save('output.mid')

# Función para cargar el archivo MIDI en pygame y reproducir el audio
def play_audio():
    pygame.mixer.music.load("output.mid")
    pygame.mixer.music.play()

# Función para aumentar el volumen
def increase_volume():
    current_volume = pygame.mixer.music.get_volume()
    new_volume = min(current_volume + 0.1, 1.0)
    pygame.mixer.music.set_volume(new_volume)

# Función para disminuir el volumen
def decrease_volume():
    current_volume = pygame.mixer.music.get_volume()
    new_volume = max(current_volume - 0.1, 0.0)
    pygame.mixer.music.set_volume(new_volume)

# Función para crear una interfaz gráfica con pygame
def create_interface():
    pygame.init()
    screen = pygame.display.set_mode((400, 200))
    pygame.display.set_caption("Music Player")
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        screen.fill((255, 255, 255))

        # Botón para aumentar volumen
        pygame.draw.rect(screen, (0, 255, 0), (50, 50, 50, 50))
        pygame.draw.rect(screen, (255, 255, 255), (55, 55, 40, 40))
        pygame.draw.polygon(screen, (0, 0, 0), [(60, 65), (90, 75), (60, 85)])

        # Botón para disminuir volumen
        pygame.draw.rect(screen, (255, 0, 0), (150, 50, 50, 50))
        pygame.draw.rect(screen, (255, 255, 255), (155, 55, 40, 40))
        pygame.draw.rect(screen, (0, 0, 0), (160, 70, 30, 10))

        # Botón para reproducir audio
        pygame.draw.rect(screen, (0, 0, 255), (250, 50, 100, 50))
        pygame.draw.polygon(screen, (255, 255, 255), [(265, 55), (355, 75), (265, 95)])

        pygame.display.flip()

        # Control de eventos de clic en los botones
        mouse_pos = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if click[0]:
            if 50 < mouse_pos[0] < 100 and 50 < mouse_pos[1] < 100:
                increase_volume()
            elif 150 < mouse_pos[0] < 200 and 50 < mouse_pos[1] < 100:
                decrease_volume()
            elif 250 < mouse_pos[0] < 350 and 50 < mouse_pos[1] < 100:
                play_audio()

        pygame.time.Clock().tick(30)
def crossover(parent1, parent2):
    # Realiza el proceso de reproducción para crear un nuevo hijo (nueva secuencia de acordes)
    # Puedes implementar diferentes estrategias de cruzamiento aquí, como mezclar partes de los padres
    # o tomar la mitad de la secuencia de un padre y la otra mitad del otro padre, etc.
    # Aquí, por simplicidad, estamos tomando partes alternas de ambos padres para el hijo.
    
    child = []
    for i in range(len(parent1)):
        if i % 2 == 0:
            child.append(parent1[i])
        else:
            child.append(parent2[i])
    
    return child
def mutate(chords, mutation_rate):
    # Realiza cambios aleatorios en la secuencia de acordes con una tasa de mutación dada
    for i in range(len(chords)):
        if random.random() < mutation_rate:
            # Aquí puedes implementar diferentes tipos de mutaciones, como cambiar una nota aleatoria,
            # agregar o eliminar un acorde, cambiar la duración de una nota, etc.
            # Aquí, por simplicidad, cambiamos una nota aleatoria del acorde.
            chords[i] = generate_chords()

    return chords

# Algoritmo genético
def genetic_algorithm():
    # Parámetros del algoritmo genético
    population_size = 50
    generations = 50
    mutation_rate = 0.1

    # Generar una población inicial de secuencias de acordes
    population = [generate_chords() for _ in range(population_size)]

    for _ in range(generations):
        # Calcular la aptitud de cada secuencia de acordes en la población
        fitness_scores = [fitness_function(chords) for chords in population]

        # Seleccionar los mejores padres (mejores secuencias de acordes)
        num_parents = int(population_size * 0.2)  # Seleccionar el 20% mejores padres
        parents = [population[i] for i in sorted(range(len(fitness_scores)), key=lambda x: fitness_scores[x], reverse=True)[:num_parents]]

        # Reproducir y mutar para crear nueva generación
        num_children = population_size - num_parents
        children = []
        for _ in range(num_children):
            parent1, parent2 = random.sample(parents, 2)
            child = crossover(parent1, parent2)
            child = mutate(child, mutation_rate)
            children.append(child)

        # Crear nueva generación combinando padres e hijos
        population = parents + children

    # Seleccionar el mejor individuo (secuencia de acordes)
    best_chords = max(population, key=lambda x: fitness_function(x))

    return best_chords


# Función principal
if __name__ == "__main__":
    best_chords = genetic_algorithm()
    write_midi_file(best_chords)
    create_interface()
