import math
import pygame

application_name = "BattleMap"
application_icon = "./icons/compass_icon.png"

clicking = False

border = 25
outline_width = 2
grid_size = (0,0)
tile_size = (50, 50)
start_location = (border,border)

palette_dict = {
    "paper": {"background color": (255, 255, 255), "outline color": (0, 0, 0), "tile color": (240, 240, 200)},
    "stone": {"background color": (50, 50, 50), "outline color": (0, 0, 0), "tile color": (100, 100, 100)}, 
    "forest": {"background color": (56, 39, 36), "outline color": (9, 84, 30), "tile color": (10, 115, 40)},
}

def run_once():
    # NOTE: add a return for the state
    # state defining the state
    shape_option = "rectangle"
    color_palette = "stone"
    return [shape_option, color_palette] 

# def run(window_dict, desktop_instruction):
def run(id, state, canvas, desktop_instruction):
    # NOTE: param 1 is state, 2 is canvas instead of window dict
    # canvas = window_dict[application_name].surface
    if desktop_instruction is not None:
        event_type, event_details = desktop_instruction[0], desktop_instruction[1]
    else:
        event_type = None
        event_details = [None]
    # NOTE: give logic the state, draw the canvas, and return the state
    x = logic(event_type, event_details, id, state, canvas)
    if x is not None:
        state = x
    draw(canvas, state)
    return state

def draw(canvas, state):
    shape_option, color_palette = state[0], state[1]
    palette = palette_dict[color_palette]
    canvas.fill(palette["background color"])
    if grid_size[0] == 0 or grid_size[1] == 0:
        # we don't have the grid size, so don't draw anything
        return 
    outline_color, tile_color = palette["outline color"], palette["tile color"]
    match shape_option:
        case "rectangle": draw_rectangle(canvas, outline_color, tile_color)
        case "circle": draw_circle(canvas, outline_color, tile_color)

def logic(event_type, event_details, id, state, canvas):
    global grid_size, clicking
    shape_option, color_palette = state
    grid_size = (canvas.get_width()-border)//tile_size[0], (canvas.get_height()-border)//tile_size[1]
    if event_details[-1] != id:
        return
    match event_type:
        case "mouse":
            if event_details[0] == "not clicking":
                clicking = False
            else:
                buttons_pressed = event_details[0]
                mouse_pos = event_details[1]
                # print("Default tool event details:", event_details)
                if not mouse_in_window(canvas, mouse_pos):
                    return
                # otherwise, perform mouse logic
                if not clicking: # is this the initial click?
                    print("Buttons and pos:", buttons_pressed, mouse_pos)
                clicking = True
        case "keyboard down":
            key_pressed = event_details[0]
            print("Key pressed:", key_pressed)
        case "keyboard up":
            pass
        case _:
            # here can be a list of the specific submenu options inside the dropdown for this app.
            submenu_path = [x.strip() for x in event_type.split(">")]
            match submenu_path[0]:
                case "Shape":
                    if submenu_path[1] in ["Rectangle", "Circle"]:
                        shape_option = submenu_path[1].lower()
                case "Palette":
                    if submenu_path[1] in ["Stone", "Paper", "Forest"]:
                        color_palette = submenu_path[1].lower()
    state = [shape_option, color_palette]
    return state

def draw_rectangle(canvas, outline_color, tile_color):
    map_outline = pygame.rect.Rect(start_location[0]-outline_width, start_location[1]-outline_width,
                                    tile_size[0]*grid_size[0]+outline_width*2, tile_size[1]*grid_size[1]+outline_width*2)
    pygame.draw.rect(canvas, outline_color, map_outline)
    draw_location = [start_location[0], start_location[1]]
    for col in range(grid_size[0]):
        for square in range(grid_size[1]):
            tile_outline = pygame.rect.Rect(*draw_location, *tile_size)
            tile = pygame.rect.Rect(draw_location[0]+outline_width, draw_location[1]+outline_width, 
                                    tile_size[0]-outline_width*2, tile_size[1]-outline_width*2)
            pygame.draw.rect(canvas, outline_color, tile_outline)
            pygame.draw.rect(canvas, tile_color, tile)
            draw_location[1] += tile_size[1]
        draw_location[0] += tile_size[0]
        draw_location[1] -= tile_size[1] * grid_size[1]

def draw_circle(canvas, outline_color, tile_color):
    def distance_function(xy1, xy2):
        x1, y1 = xy1
        x2, y2 = xy2
        return math.sqrt((x1-x2)**2 + (y1-y2)**2)
    circle_radius = min(grid_size[0]+1, grid_size[1]+1)//2
    draw_location = [start_location[0], start_location[1]]
    for col in range(grid_size[0]):
        for square in range(grid_size[1]):
            if distance_function((col, square), (grid_size[0]//2, grid_size[1]//2)) < circle_radius:
                tile_outline = pygame.rect.Rect(*draw_location, *tile_size)
                tile = pygame.rect.Rect(draw_location[0]+outline_width, draw_location[1]+outline_width, 
                                        tile_size[0]-outline_width*2, tile_size[1]-outline_width*2)
                pygame.draw.rect(canvas, outline_color, tile_outline)
                pygame.draw.rect(canvas, tile_color, tile)
            draw_location[1] += tile_size[1]
        draw_location[0] += tile_size[0]
        draw_location[1] -= tile_size[1] * grid_size[1]
    # pygame.draw.circle(canvas, outline_color, (canvas.get_width()//2, canvas.get_height()//2), 
    #                    min(canvas.get_width()//2-border, canvas.get_height()//2-border))

def mouse_in_window(canvas, mouse_position):
    canvas_size = canvas.get_size()
    if mouse_position[0] > 0 and mouse_position[0] <= canvas_size[0]:
        if mouse_position[1] > 0 and mouse_position[1] <= canvas_size[1]:
            return True
    return False