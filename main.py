import os

from Tools.App import App
from Tools import BattleMap, DiceRoller, TextEditor, ImageViewer, AudioPlayer, DefaultTool, InitiativeTracker, Camera
from Desktop import Desktop
from Message import Message

tool_id = 0

media_dir = "./media/"
media_files = [f for f in os.listdir(media_dir) if os.path.isfile(os.path.join(media_dir, f))]
sound_files, image_files, video_files = [], [], []
for file in media_files:
    file_ext = file.split('.')[-1]
    match file_ext:
        case "png" | "jpg" | "gif":
            file_path = media_dir + file
            image_files.append(file_path)
        case "mp3" | "wav":
            file_path = media_dir + file
            sound_files.append(file_path)

dice_list = ["d4", "d6", "d8", "d10", "d12", "d20", "d100"]

possible_tools = {
    "BattleMap": {
        "module": BattleMap,
        "dropdown": [["Shape >", "Rectangle", "Circle"], ["Palette >", "Stone", "Paper", "Forest"], "Close BattleMap"],
    }, 
    "DiceRoller": {
        "module": DiceRoller,
        "dropdown": [["Add Dice >"] + dice_list, ["Remove Dice >"] + dice_list, "Close DiceRoller"],
    }, 
    "TextEditor": {
        "module": TextEditor,
        "dropdown": ["Close TextEditor"],
    },
    "ImageViewer": {
        "module": ImageViewer,
        "dropdown": image_files + ["Close ImageViewer"],
    },
    "AudioPlayer": {
        "module": AudioPlayer,
        "dropdown": sound_files + ["Close AudioPlayer"],
    },
    "Camera": {
            "module": Camera,
            "dropdown": ["Close Camera"],
        },
    # "DefaultTool": {
    #     "module": DefaultTool,
    #     "dropdown": [["Hello, >", "World!"], "Close DefaultTool"],
    # }, 
    # "InitiativeTracker": {
    #     "module": InitiativeTracker,
    #     "dropdown": ["Close InitiativeTracker"]
    # }
}
tools = []

def init():
    global desktop
    desktop = Desktop((1000,750), possible_tools)
    initial_tools = []
    # initialize each tool individually, so that it can properly manage canvases
    for tool in initial_tools:
        load_tool(tool)
    desktop.application_order.reverse()

def main():
    update_tools()
    running = True
    while running:
        instructions = desktop.logic()
        if len(instructions) == 0:
            # just do a nomral rerun of all tools for their frames
            update_tools()
        elif "stop" in instructions:
            running = False
        else:
            for message in instructions:
                if message is not None:
                    if message.type.split(" ")[0] in ["mouse", "keyboard"]:
                        # give user input over to update
                        update_tools(message)
                    else:
                        parent_app_id, app_instruction = message.receiver, message.content
                        if type(app_instruction) == str and app_instruction.split(' ')[0] == "Close":
                            close_tool(parent_app_id)
                        else:
                            match parent_app_id:
                                case "Desktop":
                                    # we know that it's always going to be an open, until we decide to add more desktop options
                                    app_name = app_instruction.split(" ")[-1]
                                    load_tool(app_name)
                                case _:
                                    # we can just feed the app the dropdown option that's been selected
                                    for tool in tools:
                                        if tool.id == parent_app_id:
                                            # run_tool(tool, [app_instruction, [tool.id]])
                                            run_tool(tool, Message("Desktop", tool.id, "dropdown", app_instruction))
                                            break
        desktop.draw()
        desktop.clock.tick(desktop.fps)

def load_tool(tool_name):
    global desktop, tools, tool_id
    tool_info = possible_tools[tool_name]
    tool_instance = App(tool_id, tool_name, tool_info["module"].application_icon, 
                        tool_info["module"], tool_info["dropdown"])
    tools.append(tool_instance)
    # the try will fail if no application icon is properly initialized
    try:
        desktop.load_icon(tool_id, possible_tools[tool_name]["module"].application_icon)
    except:
        desktop.load_icon(tool_id)
    desktop.open_app(tool_id)
    desktop.tool_list.append(tool_instance)
    tool_id += 1

def close_tool(tool_id):
    global tools
    for tool in tools:
        if tool.id == tool_id:
            tools.remove(tool)
            break
    desktop.close_app(tool_id)

def run_tool(app, instruction):
    return app.run(desktop.window_dict, instruction)

def update_tools(desktop_instruction=None):
    tool_instructions = []
    for tool in tools: 
        x = run_tool(tool, desktop_instruction)
        if x is not None:
            # we can have a list of instructions
            for y in x:
                tool_instructions.append(y)
    if len(tool_instructions) > 0: print(tool_instructions)
    for tool in tools: 
        for instruction in tool_instructions:
            print(instruction)
            # ignoring chain reaction instructions from this level
            if instruction.receiver == tool.name:
                # we need to adjust the id so that it properly reads it
                modified_instruction = Message(instruction.sender, tool.id, instruction.type, instruction.content)
                run_tool(tool, modified_instruction)

if __name__ == "__main__":
    init()
    main()
