import pygame

application_name = "ImageViewer"
application_icon = "./icons/default_icon.png"

background_color = (255,255,255)

clicking = False

def run_once():
    # any initialization should go in there, in order to keep the state fresh every time the tool is opened.
    image_path = "./media/caught_in_the_act.png"
    image = pygame.image.load(image_path)
    state = [image]
    return state

def run(id, state, canvas, desktop_instruction):
    if desktop_instruction is not None:
        event_type, event_details = desktop_instruction[0], desktop_instruction[1]
    else:
        event_type = None
        event_details = [None]
    logic_output, state = logic(event_type, event_details, id, state, canvas)
    draw(canvas, state, logic_output)

def draw(canvas, state, logic_output):
    image = state[0]
    canvas.fill(background_color)
    scaled_image = pygame.transform.scale(image, canvas.get_size())
    canvas.blit(scaled_image, scaled_image.get_rect())

def logic(event_type, event_details, id, state, canvas):
    global clicking
    image = state[0]
    no_output = None, state
    output = None
    if event_details[-1] != id:
        return no_output
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
    state[0] = image
    return output, state
