import math
import queue
import random


def generate(width, height, spacing, terrain_icon_coords, point_size):
    """Driver function that creates all the data for a world's terrain"""

    terrain = perlin_noise(width, height, spacing)
    terrain = allocate_biomes(width*spacing, height*spacing, terrain, 10)
    terrain = colourise(terrain)
    terrain = generate_objects(terrain, terrain_icon_coords, point_size)

    return terrain


def perlin_noise(width, height, spacing):
    """Implementation of 2D Perlin noise, returning a nested list of noise values between -1 and 1"""

    def fade(point):
        """Fades a noise value depending on how far away it is from a vector's lattice position"""

        return 6 * point ** 5 - 15 * point ** 4 + 10 * point ** 3

    # Create lattice of gradients
    lattice = []
    for row in range(height + 1):
        to_append = []
        for point in range(width + 1):
            # Assign a random 2D vector to each x_point in the lattice
            vector = (random.random() * 2 - 1, random.random() * 2 - 1)
            to_append.append(vector)
        lattice.append(to_append)

    # Filling in points between lattice points
    noise_map = []
    for y_point in range(height * spacing):
        to_append = []

        for x_point in range(width * spacing):
            # Finds the corresponding closest lattice point to the top-left of the new noise point
            lattice_x = x_point // spacing
            lattice_y = y_point // spacing
            # These values can be used to find the other three surrounding points: top-right, bottom-left, bottom-right
            surrounding_vectors = [(lattice_x, lattice_y), (lattice_x+1, lattice_y), (lattice_x, lattice_y+1),
                                   (lattice_x+1, lattice_y+1)]

            noise = 0
            for vector in surrounding_vectors:
                # Calculates the distance between each surrounding vector and the new noise point
                difference_vector = (x_point/spacing - vector[0], y_point/spacing - vector[1])
                vector_value = lattice[vector[1]][vector[0]]
                dot_product = difference_vector[0]*vector_value[0] + difference_vector[1]*vector_value[1]
                multiplier = fade(1 - abs(difference_vector[0])) * fade(1 - abs(difference_vector[1]))
                noise += multiplier * dot_product

            to_append.append(noise)
        noise_map.append(to_append)

    return noise_map


def allocate_biomes(width, height, noise_map, total_points):
    """Splits a noise map up into biomes, allocating a biome to each point, using Voronoi diagrams and the JFA"""

    biomes = ["plains", "desert", "forest", "caves"]

    def generate_voronoi():
        """Uses Voronoi diagrams to allocate biomes centres to the noise map"""

        # Initialise framework for JFA
        seeds_queue = queue.Queue()
        step = math.ceil(max(height, width) / 2)

        # Initialise an empty grid to populate with some Voronoi points
        voronoi_points = []
        for i in range(height):
            voronoi_points.append([(None, float("inf"))] * width)

        for point_index in range(total_points):
            # Generate a random point, assign a random biome, store in queue
            new_point = (random.randint(0, width-1), random.randint(0, height-1))
            new_biome = biomes[random.randint(0, 3)]
            voronoi_points[new_point[1]][new_point[0]] = (new_biome, 0.0)
            seeds_queue.put((new_point, new_point, new_biome, step))

        return seeds_queue, voronoi_points

    def JFA(seeds_queue, voronoi_points):
        """Implementation of the Jump Flooding Algorithm to allocate each point in the noise map to the biome of its
         closest Voronoi point"""

        while seeds_queue.qsize() > 0:
            origin, position, biome, step = seeds_queue.get()
            sx, sy = position

            # Generate a list of all possible directions to jump by
            directions = [(-step, -step), (-step, 0), (-step, step), (0, -step), (0, step), (step, -step), (step, 0),
                          (step, step)]

            for dx, dy in directions:
                # Calculate the new (x, y) of the coords to jump to
                nx = sx + dx
                ny = sy + dy
                multiplier = 1
                in_bounds = True

                # Ensure the new (x, y) coords are in the bounds of the noise map, if not, half the jumping distance
                # iteratively until it is or give up if the distance is less than 1
                if not (0 <= nx < width and 0 <= ny < height):
                    in_bounds = False
                    while (not (0 <= nx < width and 0 <= ny < height)) and \
                            (abs(dx * multiplier) >= 1 or abs(dy * multiplier) >= 1):
                        nx = round(sx + dx * multiplier)
                        ny = round(sy + dy * multiplier)
                        if 0 <= nx < width and 0 <= ny < height:
                            in_bounds = True
                        multiplier /= 2

                if in_bounds:
                    to_change = True

                    # Calculate the distance between the new point and the Voronoi point using Pythagoras
                    new_distance = round((nx - origin[0]) ** 2 + (ny - origin[1]) ** 2, 1)

                    # If a point has already been allocated a biome, check whether it is the closer one
                    if voronoi_points[ny][nx][0] is not None:
                        if voronoi_points[ny][nx][1] < new_distance:
                            to_change = False

                    if to_change:
                        voronoi_points[ny][nx] = (biome, new_distance)
                        # If a point's biome has changed, add it as a seed to the queue, with a halved step
                        if step > 1:
                            seeds_queue.put((origin, (nx, ny), biome, step//2))

        for row_index, row in enumerate(voronoi_points):
            for col, value in enumerate(row):
                # Combines a point's noise value with its biome
                noise_map[row_index][col] = (noise_map[row_index][col], voronoi_points[row_index][col][0])

        return noise_map

    seeds_queue, voronoi_points = generate_voronoi()
    noise_map = JFA(seeds_queue, voronoi_points)

    # perform a final clean-up to make sure that there are no points that have a biome different to the majority of its
    # surrounding points
    directions = [(0, 1), (0, -1), (-1, 1), (-1, 0), (1, 0), (1, -1), (-1, -1), (1, 1)]
    for row_index, row in enumerate(noise_map):
        for col, values in enumerate(row):
            different = [0, 0, 0, 0]
            for direction in directions:
                if 0 <= direction[0] + row_index < height and 0 <= direction[1] + col < width:
                    if noise_map[direction[0] + row_index][direction[1] + col][1] != noise_map[row_index][col][1]:
                        different[biomes.index(noise_map[direction[0] + row_index][direction[1] + col][1])] += 1

            if sum(different) > 4:
                noise_map[row_index][col] = (noise_map[row_index][col][0], biomes[different.index(max(different))])

    return noise_map


def colourise(grid):
    """Converts noise and biome values to their appropriate colour, as they will be displayed in the game window"""

    for row in range(len(grid)):
        for col in range(len(grid[0])):
            noise_value, biome = grid[row][col]

            # converts a float between -1 and 1 to an RGB value between 0 and 255, then converting to hex
            shade = round(255 / 2 * (noise_value + 1))

            colour_mapping = {100: (0, 3, 201), 115: (0, 4, 234), 122: (0, 5, 251), 130: (240, 230, 146),
                              160: {"desert": (255, 215, 47), "plains": (0, 238, 52), "forest": (0, 138, 27),
                                    "caves": (128, 128, 128)},
                              256: {"desert": (239, 200, 42), "plains": (0, 205, 43), "forest": (0, 98, 16),
                                    "caves": (64, 64, 64)}}

            # converts an RGB value to a terrain type colour (e.g. low = water => blue, high = land => green)
            found = False
            for height in colour_mapping.keys():
                if shade < height and not found:
                    found = True
                    if type(colour_mapping[height]) == tuple:
                        colour = colour_mapping[height]
                        if shade < 122:
                            biome = "ocean"
                    else:
                        colour = colour_mapping[height][biome]

            # insert the point back into the grid, with its respective colour and a default False value denoting
            # that there is no object present at this point yet, and 100 denoting that it has not been destroyed at all
            grid[row][col] = (noise_value, biome, colour, None, 100)

    return grid


def generate_objects(grid, terrain_icon_coords, point_size):
    """Populates a grid with natural objects, depending on the biome of a grid portion"""

    object_sparsity = 5

    # generate up to the side length of the noise grid divided by <object density> terrain objects
    for i in range(len(grid) // object_sparsity):
        sx, sy = random.randint(0, len(grid[0])-1), random.randint(0, len(grid)-1)
        if grid[sy][sx][3] is None:
            biome = grid[sy][sx][1]

            # only three biomes generate objects
            if biome != "ocean" and biome != "caves":
                # calculates sprite dimensions, accounting for <point_size> and scaling
                icon_width, icon_height = terrain_icon_coords[biome]["coords"][2:]
                multiplier = terrain_icon_coords[biome]["scaling"] / point_size
                icon_width = math.ceil(icon_width * multiplier)
                icon_height = math.ceil(icon_height * multiplier)

                valid = True
                dy = -1
                coords_to_change = []

                # checks whether all affected points are already clear of any other objects
                while dy <= icon_height and valid:
                    dx = -1
                    while dx <= icon_width and valid:
                        nx, ny = sx + dx, sy + dy
                        if nx < len(grid[0]) and ny < len(grid) and grid[ny][nx][3] is None \
                                and grid[ny][nx][1] == biome:
                            coords_to_change.append((nx, ny))
                        else:
                            valid = False
                        dx += 1
                    dy += 1

                # if all checks are passed, add the object to the grid: True means the starting point of an object's
                # icon, otherwise False
                if valid:
                    for x, y in coords_to_change:
                        state = (x, y) == (sx, sy)
                        grid[y][x] = [*grid[y][x][:3], state]

    return grid
