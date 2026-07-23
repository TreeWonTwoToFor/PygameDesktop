import pygame

application_name = "AudioPlayer"
application_icon = "./icons/default_icon.png"

background_color = (75,75,75)
canvas = None

clicking = False

pygame.font.init()
font_size = 25
offset = 5
font = pygame.font.Font("Comfortaa.ttf", font_size)
text_color = (255,255,255)

audio = pygame.mixer.music
button_size = (64, 64)
play_button = pygame.image.load("./icons/play_button.png")
pause_button = pygame.image.load("./icons/pause_button.png")

def run_once():
    global playing, button_list, audio_path
    playing = False
    # default audio setup
    audio_path = "./media/Raison Detre.mp3"
    audio.load(audio_path)
    audio.set_volume(0.1)
    audio.play()
    audio.pause()
    # UI interface
    button_list = [pause_button]

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
    audio_name = font.render(audio_path.split('/')[-1], True, text_color)
    audio_name_location = 0,0
    canvas.blit(audio_name, audio_name_location)
    button_pos = [offset, audio_name.get_height() + offset]
    for button in button_list:
        canvas.blit(button, button_pos)
        button_pos[0] += button.get_rect()[0] + offset

def logic(event_type, event_details):
    global clicking, playing, button_list
    if event_details[-1] != application_name:
        return
    match event_type:
        case "mouse":
            if event_details[0] == "not clicking":
                clicking = False
            else:
                buttons_pressed = event_details[0]
                mouse_pos = event_details[1]
                # print("Default tool event details:", event_details)
                if not mouse_in_window(mouse_pos):
                    return None
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
            if event_details[0] == "space":
                toggle_play()
        case "keyboard up":
            pass
        case _:
            match event_type:
                case _:
                    audio_path = event_type
                    audio.load(audio_path)

def toggle_play():
    global playing, button_list
    playing = not playing
    if playing:
        audio.unpause()
        old_index = button_list.index(pause_button)
        button_list.remove(pause_button)
        button_list.insert(old_index, play_button)
    else:
        audio.pause()
        old_index = button_list.index(play_button)
        button_list.remove(play_button)
        button_list.insert(old_index, pause_button)

def mouse_in_window(mouse_position):
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
