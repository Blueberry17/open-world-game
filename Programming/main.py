import math
import random
import os
import sys
import abc


def file_error_protocol(file):
    """A procedure that deals with when a file cannot be found, outputting an error message quitting the program"""

    print(f"Error: file '{file}' not found, please ensure that all game files are within the same folder as main.py.")
    sys.exit(1)


# hides PyGame welcome message
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

try:
    import pygame

except ModuleNotFoundError:
    print("Error: PyGame module not found, please make sure that PyGame is installed in the same folder as main.py.")
    print("See https://pypi.org/project/pygame/ for installation details.")
    sys.exit(1)

pygame.init()

try:
    import terrain_gen

except ModuleNotFoundError:
    file_error_protocol("terrain_gen.py")


# initialise terrain sprite variables
TERRAIN_ICON_FILES = {"plains": "berry bush sprite.png",
                      "desert": "cactus sprite.png",
                      "forest": "tree sprite.png"}

TERRAIN_ICON_COORDS = {"plains": {"coords": [62, 77, 392, 344], "scaling": 0.1},
                       "desert": {"coords": [62, 46, 138, 164], "scaling": 0.3},
                       "forest": {"coords": [2, 41, 68, 87], "scaling": 0.8}}

# initialise terrain
WIDTH, HEIGHT, SPACING, POINT_SIZE = 2, 2, 100, 10
terrain = terrain_gen.generate(WIDTH, HEIGHT, SPACING, TERRAIN_ICON_COORDS, POINT_SIZE)

# initialise window variables
VIEW_SIZE = 75
WINDOW_WIDTH, WINDOW_HEIGHT = VIEW_SIZE * POINT_SIZE, VIEW_SIZE * POINT_SIZE
WORLD_WIDTH, WORLD_HEIGHT = WIDTH * SPACING, HEIGHT * SPACING


# initialise attack types, so that they can be attached to mob types
class MobAttack:
    """A mixin class for neutral and aggressive mobs' attack protocol"""

    # noinspection PyUnresolvedReferences
    def attack(self, user_health, user_hit):
        if user_hit == 0:
            user_health -= self.attack_damage
            user_hit = 10

        else:
            user_hit -= 1

        return user_health, user_hit


# initialise game variables
USER_ICON_COORDS = {"idle": [9, 61, 15, 35], "horizontal": [70, 12, 21, 34], "up": [106, 108, 15, 33],
                    "down": [105, 59, 15, 35]}
HUNGER_INTERVAL = 40
HOTBAR_INTERVAL = 1
TEXT_COLOUR = (0, 0, 0)
OUTLINE_COLOUR = (255, 255, 255)

# initialise widely-accessed user variables
mob_list = []
user_toolbar = {"sword": "wood", "axe": "wood", "pickaxe": "wood", "shovel": "wood"}
user_inventory = dict()
terrain_tool_type = {"pickaxe": ["caves"], "shovel": ["desert", "plains", "forest"]}
food_item_values = {"beef": 10, "chicken": 15, "fish": 5}


class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text

    def draw(self, surface):
        """Procedure that displays a button within the game window"""

        pygame.draw.rect(surface, (0, 122, 255), self.rect, border_radius=8)
        text_surface = large_settings_font.render(self.text, True, (255, 255, 255))
        surface.blit(text_surface, (self.rect.x + self.rect.width // 2 - text_surface.get_width() // 2,
                                    self.rect.y + self.rect.height // 2 - text_surface.get_height() // 2))

    def is_clicked(self, pos):
        """Checks whether a user left-click is within the space of the button"""
        return self.rect.collidepoint(pos)


# initialise settings variables
large_settings_font = pygame.font.SysFont("Impact", 50)
small_settings_font = pygame.font.SysFont("Impact", 20)
pause_button = Button(WINDOW_WIDTH - 180, 20, 140, 60, "Pause")
help_button = Button(WINDOW_WIDTH//2 - 100, 140, 200, 80, "Help")
quit_button = Button(WINDOW_WIDTH//2 - 100, 260, 200, 80, "Quit")
back_button = Button(WINDOW_WIDTH//2 - 100, WINDOW_HEIGHT - 120, 200, 80, "Back")

# initialise hotbar constants
SLOT_SIZE = 50
SLOT_MARGIN = 10
SLOT_BORDER_RADIUS = 3
INVENTORY_SLOTS = 8
INVENTORY_KEYS = ["K_1", "K_2", "K_3", "K_4", "K_5", "K_6", "K_7", "K_8"]
TOOLBAR_SLOTS = 4
TOOLBAR_KEYS = ["K_a", "K_b", "K_c", "K_d"]

INVENTORY_ICON_COORDS = {"beef": [65, 99, 373, 288],
                         "chicken": [85, 104, 330, 290],
                         "diamond": [92, 92, 330, 330],
                         "dirt": [122, 306, 735, 474],
                         "fish": [6, 6, 200, 200],
                         "iron": [153, 336, 673, 429],
                         "sand": [71, 109, 284, 186],
                         "stone": [164, 201, 164, 88],
                         "wood": [143, 127, 184, 230]}

# item order, origin position, length of sprite sides
TOOLBAR_ICONS_COORDS = [["sword", "axe", "pickaxe", "shovel"], ["diamond", "iron", "wood"], [32, 80], 16]

# noinspection SpellCheckingInspection
MOB_ICON_COORDS = {"chicken": {"idle": [2, 53, 12, 11], "scaling": 3},
                   "cow": {"idle": [3, 1, 31, 23], "scaling": 2.5},
                   "fish": {"idle": [10, 171, 16, 6], "scaling": 2.1},
                   "ghost": {"idle": [345, 52, 27, 43], "scaling": 1.5},
                   "scorpion": {"idle": [5, 6, 24, 22], "scaling": 1.5},
                   "shark": {"idle": [209, 321, 93, 32], "scaling": 1.2},
                   "wolf": {"idle": {False: [64, 1, 18, 13], True: [64, 18, 18, 13]}, "scaling": 3},
                   "zombie": {"idle": [91, 313, 26, 49], "scaling": 1.3}}

MOB_BIOMES = {
    "plains": [(20, ["chicken", 1], "land", "chicken", "Passive"), (50, ["beef", 2], "land", "cow", "Passive")],
    "forest": [(40, None, "land", "wolf", "Neutral", 10)],
    "desert": [(30, None, "land", "scorpion", "Aggressive", 10)],
    "caves": [(100, ["diamond", 1], "land", "ghost", "Aggressive", 20),
              (80, ["iron", 1], "land", "zombie", "Aggressive", 10)],
    "ocean": [(10, ["fish", 1], "water", "fish", "Passive"), (60, None, "water", "shark", "Aggressive", 15)]
}

# these values are in parallel with those in MOB_BIOMES
MOB_DENSITY = {
    "plains": [0.8, 0.2],
    "forest": [1],
    "desert": [1],
    "caves": [0.1, 0.9],
    "ocean": [0.8, 0.2]
}

DIRECTIONS = [(0, 1), (0, -1), (1, 1), (1, -1), (-1, -1), (1, 0), (-1, 0), (-1, 1)]


def main():
    """Driver function for the main game loop"""

    # initialise PyGame window
    running = True
    paused = False
    pause_menu_state = None
    clock = pygame.time.Clock()
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("CraftMine")
    player_x, player_y = WORLD_WIDTH // 2, WORLD_HEIGHT // 2

    # keeps track of total ticks in-game, limiting how often mobs can move
    window_age = 0
    user_delay = 0

    # user running stats
    user_health = 100
    user_hunger = 100
    user_hit = 0
    selected_toolbar_slot = 0
    selected_inventory_slot = 0

    # defining <red_overlay> for a death event
    red_overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    red_overlay.fill((255, 0, 0))
    red_overlay_opacity = 0

    while running:
        if not paused:
            pygame.mouse.set_visible(False)
            window_age += 1

            # respawn the user if they have died
            if user_health <= 0:
                player_x, player_y = WORLD_WIDTH // 2, WORLD_HEIGHT // 2
                user_health = 100
                user_hunger = 100
                red_overlay_opacity = 200
                item_tax()

            # check that the user is not delayed before moving, otherwise wait
            if user_delay == 0:
                player_x, player_y, x_min, y_min, user_delay, user_hit = (
                    shift_interface(window, player_x, player_y, terrain, window_age, user_hit))
            else:
                user_delay -= 1

            # mob refresh must be after terrain refresh so that mobs are graphically overlayed
            user_health, user_hit = mob_refresh(
                window, player_x, player_y, x_min, y_min, window_age, user_health, user_hit)

            # simulate hunger behaviour every <HUNGER_INTERVAL> ticks
            if window_age % HUNGER_INTERVAL == 0:
                user_health, user_hunger = simulate_hunger(user_health, user_hunger)

            # display user stats / other messages
            display_user_info(window, user_health, user_hunger)

            # update & display hotbar data
            selected_toolbar_slot = display_hotbar(window, "toolbar", selected_toolbar_slot)
            selected_inventory_slot = display_hotbar(window, "inventory", selected_inventory_slot)

            # display pause button
            pause_button.draw(window)

            # display mouse cursor as target icon
            display_cursor(window)

            if red_overlay_opacity > 0:
                red_overlay_opacity -= 10
                red_overlay.set_alpha(red_overlay_opacity)
                window.blit(red_overlay, (0, 0))

            # check if left click is being held down
            if pygame.mouse.get_pressed()[0]:
                mouse_pos_x, mouse_pos_y = pygame.mouse.get_pos()
                # calculates a mouse click's grid position, based on its proximity to the minimum window boundaries
                position = (round((mouse_pos_x + x_min * POINT_SIZE) // POINT_SIZE),
                            round((mouse_pos_y + y_min * POINT_SIZE) // POINT_SIZE))
                action_type = TOOLBAR_ICONS_COORDS[0][selected_toolbar_slot]

                if action_type == "sword" or action_type == "axe":
                    user_attack(action_type, position)
                else:
                    gather_terrain(window, action_type, terrain, position)

            # check if the user is trying to perform an action
            keys = pygame.key.get_pressed()
            if keys[pygame.K_u]:
                upgrade_tool(window, selected_toolbar_slot)
            elif keys[pygame.K_e]:
                user_hunger = eat_item(window, selected_inventory_slot, user_hunger)

        else:
            pygame.mouse.set_visible(True)
            if pause_menu_state == "pause":
                display_pause_menu(window)
            elif pause_menu_state == "help":
                display_help_menu(window)

        for event in pygame.event.get():
            # follow proper protocol for quit event
            if event.type == pygame.QUIT:
                running = False

            # pause game toggle
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if pause_menu_state == "pause":
                        paused = not paused
                    else:
                        pause_menu_state = "pause"

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if pause_button.is_clicked(mouse_pos):
                    paused = True
                    pause_menu_state = "pause"

                # toggling between pause menu states
                if paused:
                    if pause_menu_state == "pause":
                        if help_button.is_clicked(mouse_pos):
                            pause_menu_state = "help"
                        elif quit_button.is_clicked(mouse_pos):
                            running = False
                    elif pause_menu_state == "help":
                        if back_button.is_clicked(mouse_pos):
                            pause_menu_state = "pause"

        # refresh display, limited to 10 times per second (i.e. the user can move at a maximum of 10 points per second)
        pygame.display.flip()
        clock.tick(15)

    pygame.quit()


def display_pause_menu(window):
    """Displays the pause menu to the user, allowing them to quit the game or get help"""

    window.fill((50, 50, 50))
    info_text = large_settings_font.render("Press ESC to return to the game", True, (255, 255, 255))
    window.blit(info_text, (WINDOW_WIDTH // 2 - info_text.get_width() // 2, 30))
    help_button.draw(window)
    quit_button.draw(window)


def display_help_menu(window):
    """Displays the help menu to the user"""

    window.fill((50, 50, 50))
    info_text = large_settings_font.render("Press ESC to return to the game", True, (255, 255, 255))
    window.blit(info_text, (WINDOW_WIDTH // 2 - info_text.get_width() // 2, 30))
    help_title_text = large_settings_font.render("Help section:", True, (255, 255, 255))
    window.blit(help_title_text, (WINDOW_WIDTH // 2 - help_title_text.get_width() // 2, 120))

    raw_help_text = ["CraftMine is an open-world 2D adventure game where the aim is to gather materials",
                     "through exploring the world, gathering materials, and defeating mobs.",
                     "Use arrow keys to navigate the world.",
                     "Use 1-8 keys to navigate through your inventory",
                     "Use a-d keys to navigate through your toolbar.",
                     "To upgrade to an iron tool, you need five iron, and five diamonds to upgrade to a",
                     "diamond tool. Press the 'u' key to upgrade a selected tool.",
                     "Gain health through having a high enough hunger score, and gain hunger points by",
                     "pressing the 'e' key to eat a selected item.",
                     "To damage a mob, left click it, to mine the terrain, hold down left click with",
                     "the correct tool.",
                     "",
                     "Most importantly, enjoy!"]

    line = 0
    for text in raw_help_text:
        line += 1
        help_text = small_settings_font.render(text, True, (255, 255, 255))
        window.blit(help_text, (WINDOW_WIDTH // 2 - help_text.get_width() // 2, 180 + line*28))

    back_button.draw(window)


def display_cursor(window):
    """Displays the user's cursor as a target, showing what they are aiming at clearly"""

    cursor_img = pygame.image.load("../Icons/target sprite.png")
    cursor_img = pygame.transform.scale(cursor_img, (30, 30))
    cursor_rect = cursor_img.get_rect(center=pygame.mouse.get_pos())
    window.blit(cursor_img, cursor_rect)


def mob_refresh(window, player_x, player_y, x_min, y_min, window_age, user_health, user_hit):
    """Simulates one tick of mob behaviour for all mobs within a user's window frame view"""

    mob_count = 0
    for mob in mob_list:
        mob_x, mob_y = mob.position

        # check if mob is within range of user sprite, with padding
        if abs(player_x - mob_x) < VIEW_SIZE + 10 and abs(player_y - mob_y) < VIEW_SIZE + 10:
            mob_count += 1

            if mob.health < 0:
                mob.die()

            else:
                # check how a mob should move and whether it should move
                if isinstance(mob, AggressiveMob) or (isinstance(mob, NeutralMob) and mob.hostile):
                    passive_movement = False

                    # if an attacking mob has collided with a user, execute attack protocol
                    user_width, user_height = get_user_sprite("idle", dimensions_only=True)
                    mob_width, mob_height = get_sprite_dimensions(mob.mob_type)
                    if intersects([player_x, player_y, user_width, user_height], [mob_x, mob_y, mob_width, mob_height]):
                        user_health, user_hit = mob.attack(user_health, user_hit)

                    # otherwise move the mob aggressively towards the user if the user is very close
                    elif abs(player_x - mob_x) < VIEW_SIZE // 2 - 10 and abs(player_y - mob_y) < VIEW_SIZE // 2 - 10:
                        if window_age % 6 == 0:
                            mob.move(player_position=(player_x, player_y), passive=False)

                    else:
                        mob.next_movements = None
                        passive_movement = True
                else:
                    passive_movement = True

                if passive_movement and window_age % 2 == 0:
                    mob.move()

                icon, scaling = mob.get_sprite("idle")
                icon = pygame.transform.scale(icon, (icon.get_width() * scaling, icon.get_height() * scaling))

                # calculates a mob's relative window position, based on its proximity to the minimum window boundaries
                position = ((mob_x - x_min) * POINT_SIZE, (mob_y - y_min) * POINT_SIZE)

                # apply a red tinting to highlight a successful player attack, if necessary
                if mob.hit > 0:
                    icon.fill((255, 0, 0, 100), special_flags=pygame.BLEND_ADD)
                    mob.hit -= 1

                # out of range check does not need to be performed, .blit() deals with this
                window.blit(icon, position)

    # make sure that there are not too many mobs generating in the user's proximity (lag + realism issues)
    if mob_count < 6:
        # random chance of a new mob generating each tick
        if random.random() < 0.2:
            generate_mob(player_x, player_y)

    return user_health, user_hit


def generate_mob(player_x, player_y):
    """Generates a new mob within a user's window frame view"""

    # chose random pair of coordinates within window
    nx, ny = (player_x + random.randint(-VIEW_SIZE // 2, VIEW_SIZE // 2),
              player_y + random.randint(-VIEW_SIZE // 2, VIEW_SIZE // 2))

    # check whether coords are in bounds and not too close to the user
    if 0 <= nx < WORLD_WIDTH and 0 <= ny < WORLD_HEIGHT and abs(nx - player_x) > 5 and abs(ny - player_y) > 5:
        biome = terrain[ny][nx][1]
        # determine which mob to choose given a biome, using the mob densities for each biome
        mob_choice_value = random.random()
        found = False
        mob_index = 0

        # chose the respective mob in the biome given the random value
        while mob_index < len(MOB_DENSITY[biome]):
            mob_density = MOB_DENSITY[biome][mob_index]
            mob_choice_value -= mob_density
            if mob_choice_value <= 0 and not found:
                new_mob = MOB_BIOMES[biome][mob_index]
                found = True
            mob_index += 1

        # check whether the new mob's sprite is fully on land / water, and doesn't overlap with any existing mobs
        mob_width, mob_height = get_sprite_dimensions(new_mob[3])
        if (nx + mob_width) < WORLD_WIDTH and (ny + mob_height) < WORLD_HEIGHT:
            if new_mob[2] == get_terrain_type(terrain, (nx + mob_width, ny + mob_height)) and \
                    overlaps(nx, ny, mob_width, mob_height) == 0:
                # add on attack strength for neutral and aggressive mobs
                add_on = ""
                if new_mob[4] != "Passive":
                    add_on += f", {new_mob[5]}"

                # use eval() to instantiate an instance of the new mob
                added_mob = eval(
                    f"{new_mob[4]}Mob({(nx, ny)}, {new_mob[0]}, {new_mob[1]}, '{new_mob[2]}', '{new_mob[3]}'{add_on})")
                mob_list.append(added_mob)


def shift_interface(window, player_x, player_y, terrain, window_age, user_hit):
    """Updates the game window and a player's (x, y) coordinates"""

    # detect key presses - multiple are handled at once for diagonal movement, opposite keys cancel each other out
    keys = pygame.key.get_pressed()
    direction = "idle"
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= 1
        direction = "left"
    if keys[pygame.K_RIGHT] and player_x < WORLD_WIDTH - 1 - (USER_ICON_COORDS["horizontal"][2] // POINT_SIZE):
        player_x += 1
        direction = "right"
    if keys[pygame.K_UP] and player_y > 0:
        player_y -= 1
        direction = "up"
    if keys[pygame.K_DOWN] and player_y < WORLD_HEIGHT - 1 - (USER_ICON_COORDS["down"][3] // POINT_SIZE * 2):
        player_y += 1
        direction = "down"

    # calculate window dimensions
    x_min = max(0, min(player_x - VIEW_SIZE // 2, WORLD_WIDTH - VIEW_SIZE))
    y_min = max(0, min(player_y - VIEW_SIZE // 2, WORLD_HEIGHT - VIEW_SIZE))
    x_max = x_min + VIEW_SIZE
    y_max = y_min + VIEW_SIZE

    for row in range(y_min, y_max):
        for col in range(x_min, x_max):
            colour = terrain[row][col][2]

            # convert world coordinates to window coordinates (scaling)
            window_x = (col - x_min) * POINT_SIZE
            window_y = (row - y_min) * POINT_SIZE

            pygame.draw.rect(window, colour, (window_x, window_y, POINT_SIZE, POINT_SIZE))

    for row in range(y_min-VIEW_SIZE-20, y_max):
        for col in range(x_min-VIEW_SIZE-20, x_max):
            if terrain[row][col][3]:
                biome = terrain[row][col][1]
                sprite, scaling = get_terrain_sprite(biome)
                sprite = pygame.transform.scale(sprite, (sprite.get_width() * scaling, sprite.get_height() * scaling))
                position = ((col - x_min) * POINT_SIZE, (row - y_min) * POINT_SIZE)
                window.blit(sprite, position)


    # display the user's sprite at the specified dimensions
    player_window_x = (player_x - x_min) * POINT_SIZE
    player_window_y = (player_y - y_min) * POINT_SIZE

    user_sprite = get_user_sprite(direction)

    # apply a red tinting to highlight a successful mob attack, if necessary
    if user_hit > 0:
        user_sprite.fill((255, 0, 0, 100), special_flags=pygame.BLEND_ADD)
        user_hit -= 1

    window.blit(user_sprite, (player_window_x, player_window_y))

    if get_terrain_type(
            terrain, (player_x, math.ceil(player_y + USER_ICON_COORDS["idle"][3] / POINT_SIZE))) == "water":
        user_delay = 2

        # ensure synchronisation with mobs
        if window_age % 2 != 0:
            user_delay -= 1

    else:
        user_delay = 0

    return player_x, player_y, x_min, y_min, user_delay, user_hit


def get_item_sprite(hotbar_type, item_type):
    """Function that returns a surface object for a given inventory item that PyGame can render"""

    if hotbar_type == "inventory":
        try:
            sprite_sheet = pygame.image.load("../Icons/Items/" + item_type + " sprite.png").convert_alpha()
            sprite_coords = INVENTORY_ICON_COORDS[item_type]
            sprite = sprite_sheet.subsurface(sprite_coords)

        except FileNotFoundError:
            file_error_protocol(item_type + " sprite.png")

    else:
        try:
            sprite_sheet = pygame.image.load("../Icons/toolbar sprites.png").convert_alpha()
            sprite_order, material_order, origin, length = TOOLBAR_ICONS_COORDS
            tool_type, tool_material = item_type

            # choose the right type of tool from the sprite sheet
            y_add = sprite_order.index(tool_type) * length
            # choose the right material of tool from the sprite sheet
            x_add = material_order.index(tool_material) * length * 2

            sprite_coords = [origin[0] + x_add, origin[1] + y_add, length, length]
            sprite = sprite_sheet.subsurface(sprite_coords)

        except FileNotFoundError:
            file_error_protocol(item_type + " sprite.png")

    return sprite


def get_terrain_sprite(biome):
    """Function that returns a surface object for the user's sprite that PyGame can render"""

    sprite_coords = TERRAIN_ICON_COORDS[biome]["coords"]
    icon_file = TERRAIN_ICON_FILES[biome]

    try:
        sprite_sheet = pygame.image.load("../Icons/Objects/" + icon_file).convert_alpha()
        sprite = sprite_sheet.subsurface(sprite_coords)

    except FileNotFoundError:
        file_error_protocol(icon_file)

    return sprite, TERRAIN_ICON_COORDS[biome]["scaling"]


def get_user_sprite(direction, dimensions_only=False):
    """Function that returns a surface object for the user's sprite that PyGame can render"""

    try:
        sprite_sheet = pygame.image.load("../Icons/player sprites.png").convert_alpha()

    except FileNotFoundError:
        file_error_protocol("player sprites.png")

    scaling = 2

    if dimensions_only:
        dimensions = USER_ICON_COORDS["idle"][2:]
        to_return = []
        for num in dimensions:
            to_return.append(math.ceil(num * scaling / POINT_SIZE))

    else:
        # check whether the sprite needs to be flipped (when the player moves left)
        to_flip = False
        if direction == "left" or direction == "right":
            if direction == "left":
                to_flip = True
            direction = "horizontal"

        sprite_coords = USER_ICON_COORDS[direction]
        sprite = sprite_sheet.subsurface(sprite_coords)

        if to_flip:
            sprite = pygame.transform.flip(sprite, True, False)

        to_return = pygame.transform.scale(sprite, (sprite.get_width() * scaling, sprite.get_height() * scaling))

    return to_return


def get_sprite_dimensions(mob_type):
    """A getter for accessing a mob's sprite width and height"""

    dimensions = MOB_ICON_COORDS[mob_type]["idle"]
    # for neutral mobs with two skins, just pick the passive one as both have the same dimensions
    if isinstance(dimensions, dict):
        dimensions = dimensions[False]

    # adjust for scaling factor and pixel (point) size, rounding up
    scaling = MOB_ICON_COORDS[mob_type]["scaling"]
    width = math.ceil(dimensions[2] * scaling / POINT_SIZE)
    height = math.ceil(dimensions[3] * scaling / POINT_SIZE)

    return width, height


def intersects(sprite1, sprite2):
    """Determines whether two coordinate boxes intersect with each other, assuming top has a smaller y-value than
    bottom, using the Separating Axis Theorem"""

    sprite1_top_right = (sprite1[0] + sprite1[2], sprite1[1])
    sprite1_bottom_left = (sprite1[0], sprite1[1] + sprite1[3])
    sprite2_top_right = (sprite2[0] + sprite2[2], sprite2[1])
    sprite2_bottom_left = (sprite2[0], sprite2[1] + sprite2[3])

    result = (sprite1_top_right[0] < sprite2_bottom_left[0] or sprite1_bottom_left[0] > sprite2_top_right[0] or
                sprite1_top_right[1] > sprite2_bottom_left[1] or sprite1_bottom_left[1] < sprite2_top_right[1])

    return not result


def overlaps(nx, ny, sprite_width, sprite_height):
    """Uses intersects() to determine how many mob sprites a specified object intersects with"""

    intersections = 0
    overlapping_mobs = []

    for mob in mob_list:
        mob_width, mob_height = get_sprite_dimensions(mob.mob_type)
        if intersects([nx, ny, sprite_width, sprite_height],
                      [mob.position[0], mob.position[1], mob_width, mob_height]):
            intersections += 1
            overlapping_mobs.append(mob)

    # only occurs when user is attacking mobs
    if sprite_width == 1:
        to_return = overlapping_mobs
    else:
        to_return = intersections

    return to_return


def get_terrain_type(terrain, position):
    """Given a position in a terrain grid, returns whether that point is land or water"""

    x, y = position

    if terrain[y][x][1] == "ocean":
        terrain = "water"
    else:
        terrain = "land"

    return terrain


def create_text_outline(window, text, position):
    """Renders an outline by drawing text multiple times around the main text"""

    x, y = position
    outline_size = 2
    font = pygame.font.SysFont("impact", 22)

    for ox, oy in DIRECTIONS:
        outline_surface = font.render(text, True, OUTLINE_COLOUR)
        window.blit(outline_surface, (x + ox * outline_size, y + oy * outline_size))

    # overlays the actual text over all the off
    text_surface = font.render(text, True, TEXT_COLOUR)
    window.blit(text_surface, (x, y))


def display_user_info(window, user_health, user_hunger):
    """Renders text for health and hunger stats for the user"""

    create_text_outline(window, f"Health: {user_health}", (30, 30))
    create_text_outline(window, f"Hunger: {user_hunger}", (30, 60))


def user_attack(action_type, position):
    """Procedure that deals with a user mouseclick event, detecting and attack a mob at that location"""

    mouse_x, mouse_y = position
    overlapping_mobs = overlaps(mouse_x, mouse_y, 1, 1)

    # make upgraded weapons do more damage
    if user_toolbar[action_type] == "diamond":
        damage_multiplier = 3
    elif user_toolbar[action_type] == "iron":
        damage_multiplier = 2
    else:
        damage_multiplier = 1

    for mob in overlapping_mobs:
        # check whether the attack cooldown is in place
        if mob.hit == 0:
            # affect mob stats differently, dependent on weapon—
            if action_type == "sword":
                mob.health -= 20 * damage_multiplier
                mob.hit = 10
            else:
                mob.health -= 30 * damage_multiplier
                mob.hit = 15

            # make neutral mobs hostile
            if isinstance(mob, NeutralMob):
                mob.hostile = True


def simulate_hunger(user_health, user_hunger):
    if user_hunger == 0:
        user_health -= 1
    else:
        user_hunger -= 1

    if user_hunger > 50 and user_health < 100:
        user_health += 1

    return user_health, user_hunger


def eat_item(window, selected_inventory_slot, user_hunger):
    """Protocol for when a user attempts to eat something in their inventory slot"""

    if selected_inventory_slot < len(user_inventory):
        item = list(user_inventory.keys())[selected_inventory_slot]
    else:
        item = None

    if item in food_item_values:
        if user_hunger < 100:
            user_hunger = min(100, user_hunger + food_item_values[item])
            # remove food item from user inventory
            if user_inventory[item] == 1:
                user_inventory.pop(item)
            else:
                user_inventory[item] -= 1
        else:
            create_text_outline(window, "Hunger already full!", (WINDOW_WIDTH // 2 - 85, 100))
    else:
        create_text_outline(window, "Item cannot be eaten!", (WINDOW_WIDTH // 2 - 96, 100))

    return user_hunger


def item_tax():
    """Taxes 20% of a user's items when they die"""

    for item, quantity in user_inventory.items():
        new_quantity = math.ceil(quantity * 0.8)
        user_inventory[item] = new_quantity


def add_to_inventory(item, quantity=1):
    """Adds <quantity> number of <item> to a user's inventory"""

    if item in user_inventory:
        user_inventory[item] += quantity
    else:
        user_inventory[item] = quantity


def get_hotbar_icon(hotbar_type, item):
    """Fetches and rescales a hotbar icon"""

    icon = get_item_sprite(hotbar_type, item)
    item_icon = pygame.transform.scale(icon, (SLOT_SIZE - 10, SLOT_SIZE - 10))

    return item_icon


def display_hotbar(window, hotbar_type, selected_slot):
    """Procedural subroutine that displays an up-to-date version of a user hotbar"""

    if hotbar_type == "toolbar":
        hotbar_slots = TOOLBAR_SLOTS
        user_hotbar = user_toolbar
        user_keys = TOOLBAR_KEYS
        hotbar_y_expression = "20"
    else:
        hotbar_slots = INVENTORY_SLOTS
        user_hotbar = user_inventory
        user_keys = INVENTORY_KEYS
        hotbar_y_expression = "WINDOW_HEIGHT - HOTBAR_HEIGHT - 20"

    # detect whether a different inventory slot should be highlighted
    keys = pygame.key.get_pressed()
    for key in user_keys:
        # converts string to pygame constant
        key_constant = getattr(pygame, key)

        if keys[key_constant]:
            if key in TOOLBAR_KEYS:
                # convert letter to numerical value
                selected_slot = TOOLBAR_KEYS.index(key)
            else:
                selected_slot = int(key[-1])-1

    # load item icons
    item_icons = []
    if hotbar_type == "inventory":
        item_counts = []
        for item, count in user_hotbar.items():
            item_counts.append(count)
            item_icons.append(get_hotbar_icon(hotbar_type, item))
    else:
        for item in user_hotbar.items():
            item_icons.append(get_hotbar_icon(hotbar_type, item))

    # hotbar position
    HOTBAR_WIDTH, HOTBAR_HEIGHT = (SLOT_SIZE + SLOT_MARGIN) * hotbar_slots + SLOT_MARGIN, 60
    hotbar_x = (WINDOW_WIDTH - HOTBAR_WIDTH) // 2
    # evaluates the string expression declared above
    hotbar_y = eval(hotbar_y_expression)

    # draw hotbar background
    pygame.draw.rect(window, (50, 50, 50), (hotbar_x, hotbar_y, HOTBAR_WIDTH, HOTBAR_HEIGHT), border_radius=10)

    # draw inventory slots
    for item in range(hotbar_slots):
        slot_x = hotbar_x + (SLOT_SIZE + SLOT_MARGIN) * item + SLOT_MARGIN
        slot_y = hotbar_y + (HOTBAR_HEIGHT - SLOT_SIZE) // 2
        slot_rect = pygame.Rect(slot_x, slot_y, SLOT_SIZE, SLOT_SIZE)
        # highlight selected slot
        if selected_slot == item:
            border_color = (255, 0, 0)
        else:
            border_color = (0, 0, 0)
        pygame.draw.rect(window, border_color, slot_rect, SLOT_BORDER_RADIUS)

        # draw item icon in the slot, if available
        if item < len(item_icons):
            window.blit(item_icons[item], (slot_x+5, slot_y+5))
            if hotbar_type == "inventory":
                # draw item count
                create_text_outline(window, str(item_counts[item]), (slot_x + SLOT_SIZE - 15, slot_y + SLOT_SIZE - 20))

    return selected_slot


def gather_terrain(window, action_type, terrain, position):
    """Procedure that attempts to gather blocks from the terrain at <position>"""

    x_pos, y_pos = position
    current_biome = terrain[y_pos][x_pos][1]

    # check whether the user is using the correct tool for the terrain
    if current_biome in terrain_tool_type[action_type]:
        if terrain[y_pos][x_pos][4] <= 0:
            # convert terrain to item to add
            if current_biome == "desert":
                item_to_add = "sand"
            elif current_biome == "forest" or current_biome == "plains":
                item_to_add = "dirt"
            else:
                item_to_add = "stone"
            add_to_inventory(item_to_add, 1)
            # restore a point's destroyed status to initial value (100)
            terrain[y_pos][x_pos] = terrain[y_pos][x_pos][:4] + (100,)

        else:
            # make upgraded tools destroy terrain more quickly
            if user_toolbar[action_type] == "diamond":
                destroy_multiplier = 3
            elif user_toolbar[action_type] == "iron":
                destroy_multiplier = 2
            else:
                destroy_multiplier = 1
            # partially destroy point
            terrain[y_pos][x_pos] = terrain[y_pos][x_pos][:4] + (terrain[y_pos][x_pos][4] - 10*destroy_multiplier,)

    else:
        create_text_outline(window, f"{action_type.capitalize()} cannot destroy {current_biome} ground!",
                            (WINDOW_WIDTH // 2 - 170, 100))


def upgrade_tool(window, selected_toolbar_slot):
    """Protocol for a user attempting to upgrade a tool, checking whether the user has enough resources"""

    # use the toolbar ordering to see what tool the toolbar slot relates to
    tool = TOOLBAR_ICONS_COORDS[0][selected_toolbar_slot]
    tool_material = user_toolbar[tool]

    upgrade_failed = False

    # calculate the type of material needed to upgrade, if already diamond then no upgrade can be done
    if tool_material == "wood":
        if "iron" in user_inventory:
            user_required_material_count = user_inventory["iron"]
        else:
            user_required_material_count = 0
        if user_required_material_count >= 5:
            user_toolbar[tool] = "iron"
        else:
            upgrade_failed = "iron"

    elif tool_material == "iron":
        if "diamond" in user_inventory:
            user_required_material_count = user_inventory["diamond"]
        else:
            user_required_material_count = 0
        if user_required_material_count >= 5:
            user_toolbar[tool] = "diamond"
        else:
            upgrade_failed = "diamonds"

    else:
        create_text_outline(window, f"Tool already fully upgraded!", (WINDOW_WIDTH // 2 - 125, 100))
        upgrade_failed = None

    if upgrade_failed is False:
        material_used = user_toolbar[tool]
        if user_inventory[material_used] == 5:
            user_inventory.pop(material_used)
        else:
            user_inventory[material_used] -= 5

    if upgrade_failed == "diamonds":
        create_text_outline(window, "More diamonds needed for upgrade!", (WINDOW_WIDTH // 2 - 160, 100))
    elif upgrade_failed == "iron":
        create_text_outline(window, "More iron needed for upgrade!", (WINDOW_WIDTH // 2 - 140, 100))


def passive_movement(mob_type, position, movement, next_movements, find_movement=False):
    """Algorithm for a mob that wonders passively"""

    if next_movements is None:
        if random.randint(1, 15) == 1 or find_movement:
            direction = random.choice(DIRECTIONS)
            steps = random.randint(1, 8)
            next_movements = (direction, steps)

    if next_movements is not None:
        direction, steps = next_movements
        dx, dy = direction
        mob_x, mob_y = position
        nx, ny = mob_x + dx, mob_y + dy
        failed = False

        # check whether mob is in bounds, referencing the mob's dimensions
        sprite_width, sprite_height = get_sprite_dimensions(mob_type)

        nx_to_check = nx
        if dx == 1:
            nx_to_check += sprite_width

        ny_to_check = ny
        if dy == 1:
            ny_to_check += sprite_height

        if 0 <= nx_to_check < WORLD_WIDTH and 0 <= ny_to_check < WORLD_HEIGHT:
            # check whether the mob is staying on land / in water, using the mob's icon's width
            pos_to_check = (nx_to_check, ny_to_check)
            new_terrain_type = get_terrain_type(terrain, pos_to_check)

            if movement == new_terrain_type and overlaps(nx, ny, sprite_width, sprite_height) < 2 and \
                    terrain[ny + sprite_height * dy][nx + sprite_width * dx][3] is None:
                position = (nx, ny)
                if steps == 1:
                    next_movements = None
                else:
                    next_movements = (direction, steps - 1)

            else:
                failed = True
        else:
            failed = True

        if failed:
            next_movements = None

    return position, next_movements


def aggressive_movement(mob_type, start, end, movement, next_movements):
    """Algorithm for a mob that aggressively pathfinds towards the user"""

    failed = True
    path = A_Star(start, end, terrain)

    if path is not None and len(path) > 0:
        # check whether mob is in bounds, referencing the mob's dimensions
        sprite_width, sprite_height = get_sprite_dimensions(mob_type)

        nx, ny = path[0]
        nx_to_check = nx
        ny_to_check = ny
        dx = nx - start[0]
        dy = ny - start[1]
        if dx == 1:
            nx_to_check += sprite_width
        if dy == 1:
            ny_to_check += sprite_height

        if 0 <= nx_to_check < WORLD_WIDTH and 0 <= ny_to_check < WORLD_HEIGHT and \
                terrain[ny_to_check][nx_to_check][3] is None:
            # check whether the mob is staying on land / in water, using the mob's icon's width
            pos_to_check = (nx_to_check, ny_to_check)
            new_biome_type = get_terrain_type(terrain, pos_to_check)

            if movement == new_biome_type:
                failed = False
                if overlaps(nx, ny, sprite_width, sprite_height) < 2:
                    position = path[0]
                    next_movements = path.pop()
                else:
                    # move randomly if other mobs in the way to get out of way
                    next_movements = None
                    while next_movements is None:
                        position, next_movements = passive_movement(mob_type, start, movement, next_movements, True)

    if failed:
        position = start
        next_movements = None

    return position, next_movements


class Mob(abc.ABC):
    """Abstract bass class for all mobs"""

    def __init__(self, position, max_health, drops, movement, mob_type):
        self.position = position
        self.health = max_health
        self.max_health = max_health
        self.drops = drops
        self.movement = movement
        self.next_movements = None
        self.mob_type = mob_type
        self.icon_file = f"{mob_type} sprite.png"
        self.hit = 0

    def move(self, player_position=None, passive=True):
        """Function that changes a mob's position, depending on its hostility and type of terrain travelling over"""

        if passive:
            self.position, self.next_movements = passive_movement(
                self.mob_type, self.position, self.movement, self.next_movements)

        else:
            self.position, self.next_movements = aggressive_movement(
                self.mob_type, self.position, player_position, self.movement, self.next_movements)

    def die(self):
        """Procedure that deals with the process of a mob's death"""

        # check if the mob drops something
        if self.drops is not None:
            item, quantity = self.drops
            add_to_inventory(item, quantity)

        if self in mob_list:
            mob_list.remove(self)
        del self

    def get_sprite(self, sprite_type):
        """Function that returns a surface object for a mob sprite that PyGame can render"""

        sprite_coords = MOB_ICON_COORDS[self.mob_type][sprite_type]

        try:
            sprite_sheet = pygame.image.load("../Icons/Mobs/" + self.icon_file).convert_alpha()

        except FileNotFoundError:
            file_error_protocol(self.icon_file)

        return sprite_sheet.subsurface(sprite_coords), MOB_ICON_COORDS[self.mob_type]["scaling"]


class PassiveMob(Mob):
    """Class for all passive mobs"""

    def __init__(self, position, max_health, drops, movement, mob_type):
        super().__init__(position, max_health, drops, movement, mob_type)

    def __repr__(self):
        return f"mob type: {self.mob_type}, position: {self.position}, health: {self.health}, max health: " + \
            f"{self.max_health}, drops: {self.drops}, movement type: {self.movement}, movement queue: " + \
            f"{self.next_movements}"


class NeutralMob(Mob, MobAttack):
    """Class for all neutral mobs"""

    def __init__(self, position, max_health, drops, movement, mob_type, attack_damage):
        super().__init__(position, max_health, drops, movement, mob_type)
        self.attack_damage = attack_damage
        self.hostile = False

    def __repr__(self):
        return f"mob type: {self.mob_type}, position: {self.position}, health: {self.health}, max health: " + \
            f"{self.max_health}, drops: {self.drops}, movement type: {self.movement}, movement queue: " + \
            f"{self.next_movements}, hostile: {self.hostile}, attack damage: {self.attack_damage}"

    def get_sprite(self, sprite_type):
        """Overriding of the base class function, taking hostility into account"""

        sprite_coords = MOB_ICON_COORDS[self.mob_type][sprite_type][self.hostile]

        try:
            sprite_sheet = pygame.image.load("../Icons/Mobs/" + self.icon_file).convert_alpha()

        except FileNotFoundError:
            file_error_protocol(self.icon_file)

        return sprite_sheet.subsurface(sprite_coords), MOB_ICON_COORDS[self.mob_type]["scaling"]


class AggressiveMob(Mob, MobAttack):
    """Class for all aggressive mobs"""

    def __init__(self, position, max_health, drops, movement, mob_type, attack_damage):
        super().__init__(position, max_health, drops, movement, mob_type)
        self.attack_damage = attack_damage

    def __repr__(self):
        return f"mob type: {self.mob_type}, position: {self.position}, health: {self.health}, max health: " + \
            f"{self.max_health}, drops: {self.drops}, movement type: {self.movement}, movement queue: " + \
            f"{self.next_movements}, attack damage: {self.attack_damage}"


def A_Star(start, end, grid):
    """Implementation of A* algorithm for a 2D grid of values indicating whether each cell in the grid is an obstacle or
    not, returning the almost perfectly optimised path from a start to end location in the grid, using heuristics"""

    def heuristic(start, end):
        """Heuristic for A* algorithm, calculating the Pythagorean distance between two 2D grid points"""

        return math.sqrt((start[0] - end[0]) ** 2 + (start[1] - end[1]) ** 2)

    open_set = PriorityQueue() # nodes to be evaluated
    open_set.enqueue(start, 0)

    path = dict() # stores the best path to a node
    gScore = dict() # cost from one node to another node
    gScore[start] = 0
    fScore = dict() # estimated total cost (gScore + heuristic)
    fScore[start] = heuristic(start, end)

    while not open_set.isEmpty():
        current_node = open_set.pop() # pop the element with the lowest priority

        if current_node == end:
            # if a path has been found from the start to the end, reconstruct and return this path
            sequence = []
            while current_node in path:
                sequence.append(current_node)
                current_node = path[current_node]
            return list(reversed(sequence))

        neighbours = []
        for direction in [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]:
            x_pos, y_pos = current_node[0] + direction[0], current_node[1] + direction[1]
            # checks if in bounds and not an obstacle
            if 0 <= x_pos < len(grid[0]) and 0 <= y_pos < len(grid) and terrain[y_pos][x_pos][3] is None:
                neighbours.append((x_pos, y_pos))

        for neighbour in neighbours:
            # new cost from <current_node> to <neighbour>
            new_gScore = gScore[current_node] + 1

            # check whether the new cost is the minimum cost
            if neighbour not in gScore or new_gScore < gScore[neighbour]:
                # update the cost from <current_node> to <neighbour> & the heuristic cost from <start> to <neighbour>
                gScore[neighbour] = new_gScore
                fScore[neighbour] = gScore[neighbour] + heuristic(neighbour, end)
                path[neighbour] = current_node

                # if the neighbour has not yet been explored at all, add it to the priority queue
                if neighbour not in open_set:
                    open_set.enqueue(neighbour, fScore[neighbour])

    # if no path can be found, the mob cannot move towards the player
    return None


class PriorityQueue(object):
    """Priority queue implementation as required by the A* algorithm, popping the lowest priority items first"""

    def __init__(self):
        self.queue = []

    def __iter__(self):
        """Returns an iterable object so that iterable methods like 'in' can be used on the queue"""

        return iter(self.queue)

    def isEmpty(self):
        """Returns a boolean for whether the queue is empty"""

        return len(self.queue) == 0

    def enqueue(self, data, priority):
        """Adds a new element to the priority queue"""

        self.queue.append((data, priority))

    def pop(self):
        """Pops the lowest priority item in the priority queue"""

        min_priority = float("inf")
        for item in self.queue:
            # if the item has a lower priority, it becomes the prospective item to pop
            if item[1] < min_priority:
                min_data, min_priority = item
        self.queue.remove((min_data, min_priority))

        return min_data


if __name__ == "__main__":
    main()
    print("Program successfully quit. See you soon!")
