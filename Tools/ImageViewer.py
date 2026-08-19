import pygame
import tkinter as tk
from tkinter.filedialog import askopenfilename
tk.Tk().withdraw()

application_name = "ImageViewer"
application_icon = "./icons/image_icon.png"

background_color = (50,50,100)

clicking = False

def run_once():
    # any initialization should go in there, in order to keep the state fresh every time the tool is opened.
    image_path = ""
    state = [image_path]
    return state

def run(id, state, canvas, instruction):
    if state[0] != "" and len(state) == 1:
        state.append(pygame.image.load(state[0]))
    logic_output, state = logic(id, state, canvas, instruction)
    draw(canvas, state, logic_output)
    return {"state": state}

def draw(canvas, state, logic_output):
    image_path = state[0]
    canvas.fill(background_color)
    if len(state) == 1:
        pass
    else:
        image = pygame.transform.scale(state[1], canvas.get_size())
        canvas.blit(image, (0,0))

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
        case "dropdown":
            if instruction.content == "Open":
                image_path = askopenfilename()
                image = pygame.image.load(image_path)
                if len(state) == 1: 
                    state.append(image)
                else:
                    state[1] = image
                # image_path = instruction.content
    state[0] = image_path
    return output, state