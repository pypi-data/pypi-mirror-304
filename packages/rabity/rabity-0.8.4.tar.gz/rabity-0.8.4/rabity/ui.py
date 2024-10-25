import customtkinter as ctk
from colorama import Fore, Style
from tqdm.auto import tqdm
import time


class ui():
    buttons = 0
    def app(size, name = "RabityUi", icon = None, color = None):
        app = ctk.CTk()
        app.geometry(size)
        app.title(name)
        if icon is not None:
            app.iconbitmap(icon)
        if color is not None:
            app.configure(fg_color=color)
        return app
    def configure(parent):
        ctks = ctk
        return ctks
    def label(text, parent):
        label = ctk.CTkLabel(master=parent, text=text)
        label.pack()
        return label
    def show_progress():
        for _ in tqdm(range(1), desc=Fore.LIGHTMAGENTA_EX + "[LOG] " + Fore.BLUE + "Processing", colour='green'):
            time.sleep(0.5)
    def button(name, command, parent):
        ui.buttons += 1
        button = ctk.CTkButton(master=parent,text=name, command=command)
        button.pack()
        print(Fore.WHITE + "[LOG]" + Fore.CYAN + f" Loaded " + Fore.GREEN + f"{ui.buttons}/{ui.buttons}" + Fore.CYAN + f" Buttons With Name {name}" + Style.RESET_ALL)
        

        return button
    def run(parent):
        if __name__ == "__main__":
            print(Fore.WHITE + "[LOG]" + Fore.CYAN + " UI Loaded" + Style.RESET_ALL)
            parent.mainloop()
