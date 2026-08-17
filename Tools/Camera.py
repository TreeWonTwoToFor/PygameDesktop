import cv2
import pygame

application_name = "Camera"
application_icon = "./icons/camera_icon.png"

background_color = (255,255,255)

clicking = False

def run_once():
    # any initialization should go in there, in order to keep the state fresh every time the tool is opened.
    camera = cv2.VideoCapture(0)
    state = [camera]
    return state

def run(id, state, canvas, instruction):
    logic_output, state = logic(id, state, canvas, instruction)
    draw(canvas, state, logic_output)
    return state

def draw(canvas, state, logic_output):
    canvas.fill(background_color)
    ret, frame = state[0].read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    camera_frame = pygame.surfarray.make_surface(frame)
    # rotates to be uprights, scales to the canvas size, then flips to not be mirrored
    camera_frame = pygame.transform.flip(pygame.transform.scale(pygame.transform.rotate(camera_frame, 270), canvas.get_size()), 1, 0)
    canvas.blit(camera_frame, (0,0))

def logic(id, state, canvas, instruction):
    global clicking
    no_output = None, state
    return no_output