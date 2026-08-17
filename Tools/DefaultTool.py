from Message import Message

application_name = "DefaultTool"
application_icon = "./icons/default_icon.png"

background_color = (255,255,255)

clicking = False

def run_once():
    # any initialization should go in there, in order to keep the state fresh every time the tool is opened.
    state = []
    return state

def run(id, state, canvas, instruction):
    logic_output, state = logic(id, state, canvas, instruction)
    instructions = []
    if logic_output == "test instruction":
        instructions.append(Message(application_name, "BattleMap", "dropdown", "Shape > Circle"))
    draw(canvas, state, logic_output)
    return {
        "state": state,
        "instructions": instructions
    }

def draw(canvas, state, logic_output):
    canvas.fill(background_color)

def logic(id, state, canvas, instruction):
    global clicking
    no_output = None, state
    output = None
    # keep track of the state throughout the logic
    if instruction == None or instruction.receiver != id:
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
                    print("Buttons and pos:", buttons_pressed, mouse_pos)
                clicking = True
        case "keyboard down":
            key_pressed = instruction.content
            match key_pressed:
                case "space":
                    output = "test instruction"
                case _:
                    print("Key pressed:", key_pressed)
        case "keyboard up":
            key_pressed = instruction.content
            match key_pressed:
                case _:
                    print("Key released:", key_pressed)
        case "dropdown":
            # here can be a list of the specific submenu options inside the dropdown for this app.
            submenu_path = [x.strip() for x in instruction.content.split(">")]
            print(submenu_path)
            match instruction.type:
                case _:
                    print("Event called:", instruction.content)
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
