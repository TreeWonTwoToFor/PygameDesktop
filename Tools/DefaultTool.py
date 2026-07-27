application_name = "DefaultTool"
application_icon = "./icons/default_icon.png"

background_color = (255,255,255)

clicking = False

def run_once():
    # any initialization should go in there, in order to keep the state fresh every time the tool is opened.
    state = []
    return state

def run(id, state, canvas, desktop_instruction):
    if desktop_instruction is not None:
        event_type, event_details = desktop_instruction[0], desktop_instruction[1]
    else:
        event_type = None
        event_details = [None]
    logic_output, state = logic(event_type, event_details, id, state, canvas)
    draw(canvas, state, logic_output)
    return state

def draw(canvas, state, logic_output):
    canvas.fill(background_color)

def logic(event_type, event_details, id, state, canvas):
    global clicking
    no_output = None, state
    output = None
    # keep track of the state throughout the logic
    if event_details[-1] != id:
        return no_output
    match event_type:
        case "mouse":
            if event_details[0] == "not clicking":
                clicking = False
            else:
                buttons_pressed = event_details[0]
                mouse_pos = event_details[1]
                # print("Default tool event details:", event_details)
                if not mouse_in_window(canvas, mouse_pos):
                    return no_output
                # otherwise, perform mouse logic
                if not clicking: # is this the initial click?
                    print("Buttons and pos:", buttons_pressed, mouse_pos)
                clicking = True
        case "keyboard down":
            key_pressed = event_details[0]
            match key_pressed:
                case _:
                    print("Key pressed:", key_pressed)
        case "keyboard up":
            key_pressed = event_details[0]
            match key_pressed:
                case _:
                    print("Key released:", key_pressed)
        case _:
            # here can be a list of the specific submenu options inside the dropdown for this app.
            submenu_path = [x.strip() for x in event_type.split(">")]
            print(submenu_path)
            match event_type:
                case _:
                    print("Event called:", event_type)
    return output, state

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
