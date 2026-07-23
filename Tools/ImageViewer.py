import pygame

application_name = "ImageViewer"
application_icon = "./icons/default_icon.png"

background_color = (255,255,255)
canvas = None

clicking = False

def run_once():
    # any initialization should go in there, in order to keep the state fresh every time the tool is opened.
    global image
    image_path = "./media/caught_in_the_act.png"
    image = pygame.image.load(image_path)

def run(window_dict, desktop_instruction):
    global canvas
    canvas = window_dict[application_name].surface
    if desktop_instruction is not None:
        event_type, event_details = desktop_instruction[0], desktop_instruction[1]
    else:
        event_type = None
        event_details = [None]
    logic_output = logic(event_type, event_details)
    draw(logic_output)

def draw(logic_output):
    canvas.fill(background_color)
    scaled_image = pygame.transform.scale(image, canvas.get_size())
    canvas.blit(scaled_image, scaled_image.get_rect())

def logic(event_type, event_details):
    global clicking, image
    if event_details[-1] != application_name:
        return
    match event_type:
        case "mouse":
            pass
        case "keyboard down":
            pass
        case "keyboard up":
            pass
        case _:
            match event_type:
                case _:
                    image_path = event_type
                    image = pygame.image.load(image_path)

def inside_rect(rectangle, xy):
    x, y = xy[0], xy[1]
    if x >= rectangle.left and x <= rectangle.right:
        if y >= rectangle.top and y <= rectangle.bottom:
            return True
    return False
