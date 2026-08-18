import pygame

application_name = "ImageViewer"
application_icon = "./icons/default_icon.png"

background_color = (255,255,255)

clicking = False

def run_once():
    # any initialization should go in there, in order to keep the state fresh every time the tool is opened.
    image_path = "./media/caught_in_the_act.png"
    state = [image_path]
    return state

def run(id, state, canvas, instruction):
    logic_output, state = logic(id, state, canvas, instruction)
    draw(canvas, state, logic_output)

def draw(canvas, state, logic_output):
    image_path = state[0]
    image = pygame.image.load(image_path)
    canvas.fill(background_color)
    image = pygame.transform.scale(image, canvas.get_size())
    canvas.blit(image, (0,0))
    # image.resize(canvas.get_size())
    # image.draw(canvas)

def logic(id, state, canvas, instruction):
    global clicking
    image_path = state[0]
    no_output = None, state
    output = None
    if instruction is None or instruction.receiver != id:
        return no_output
    match instruction.type:
        case "mouse":
            pass
        case "keyboard down":
            pass
        case "keyboard up":
            pass
        case _:
            match instruction.type:
                case _:
                    image_path = instruction.content
    state[0] = image_path
    return output, state