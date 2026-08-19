import pygame
import tkinter as tk
from tkinter.filedialog import askopenfilename
tk.Tk().withdraw()

application_name = "AudioPlayer"
application_icon = "./icons/audio_icon.png"

background_color = (75,75,75)

clicking = False

pygame.font.init()
font_size = 25
offset = 5
font = pygame.font.Font("Comfortaa.ttf", font_size)
text_color = (255,255,255)

audio = pygame.mixer.music
button_size = (64, 64)
button_dict = {
    "play": pygame.image.load("./icons/play_button.png"),
    "pause": pygame.image.load("./icons/pause_button.png")
}

def run_once():
    playing = False
    # default audio setup
    audio_path = "./media/Raison Detre.mp3"
    audio.load(audio_path)
    audio.set_volume(0.1)
    audio.play()
    audio.pause()
    # UI interface
    button_list = ["pause"]
    state = [playing, audio_path, button_list]
    return state

def run(id, state, canvas, instruction):
    logic_output, state = logic(id, state, canvas, instruction)
    draw(canvas, state, logic_output)
    return {"state": state}

def draw(canvas, state, logic_output):
    audio_path, button_list = state[1], state[2]
    canvas.fill(background_color)
    audio_text = audio_path.split('/')[-1].split('.')[:1][0]
    audio_name = font.render(audio_text, True, text_color)
    audio_name_location = 0,0
    canvas.blit(audio_name, audio_name_location)
    button_pos = [offset, audio_name.get_height() + offset]
    for button_name in button_list:
        button = button_dict[button_name]
        canvas.blit(button, button_pos)
        button_pos[0] += button.get_rect()[0] + offset

def logic(id, state, canvas, instruction):
    global clicking
    playing, audio_path, button_list = state
    no_output = None, state
    output = None
    if instruction is None or instruction.receiver != id:
        return no_output
    match instruction.type:
        case "mouse":
            if instruction.content == "not clicking":
                clicking = False
            else:
                buttons_pressed = instruction.content[0]
                mouse_pos = instruction.content[1]
                if not mouse_in_window(canvas, mouse_pos):
                    return no_output
                # otherwise, perform mouse logic
                if not clicking: # is this the initial click?
                    # I'm not sure what the best way to track the position of the buttons are.
                    # my current guess is sprites, but I don't need it for this first version
                    pass
                    # for button in button_list:
                    #     if inside_rect(button.get_rect(), mouse_pos):
                    #         if button_list.index(button) == 0:
                    #             # in this case, it's the play/pause button
                    #             toggle_play()
                clicking = True
        case "keyboard down":
            if instruction.content == "space":
                playing, button_list = toggle_play(playing, button_list)
        case "keyboard up":
            pass
        case "dropdown":
            if instruction.content == "Open":
                audio_path = askopenfilename()
                audio.load(audio_path)
                audio.play()
                if playing == False:
                    audio.pause()
    state = [playing, audio_path, button_list]
    return output, state

def toggle_play(playing, button_list):
    playing = not playing
    if playing:
        audio.unpause()
        for i in range(len(button_list)):
            if button_list[i] == "pause":
                button_list[i] = "play"
                break
    else:
        audio.pause()
        for i in range(len(button_list)):
            if button_list[i] == "play":
                button_list[i] = "pause"
                break
    return playing, button_list

def mouse_in_window(canvas, mouse_position):
    canvas_size = canvas.get_size()
    if mouse_position[0] > 0 and mouse_position[0] <= canvas_size[0]:
        if mouse_position[1] > 0 and mouse_position[1] <= canvas_size[1]:
            return True
    return False

def inside_rect(rectangle, xy):
    x, y = xy[0], xy[1]
    if x >= rectangle.left and x <= rectangle.right:
        if y >= rectangle.top and y <= rectangle.bottom:
            return True
    return False
