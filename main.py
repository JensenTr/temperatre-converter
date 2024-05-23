"""
    Temperature Converter System

    - Jensen Trillo, **v0.1**, 23/05/2024
    - ``Python 3.11.6``
"""
import customtkinter as ctk
from signal import signal, SIGINT, SIGTERM
ctk.set_appearance_mode('system')
ctk.FontManager().load_font('assets/JetBrainsMonoNL-Bold.ttf')
ctk.FontManager().load_font('assets/JetBrainsMonoNL-Regular.ttf')
ctk.FontManager().load_font('assets/segoeui.ttf')


class GUI(ctk.CTk):
    def __init__(self):
        super().__init__(fg_color='#FFFCFC')
        signal(SIGINT, self.__kill_handler), signal(SIGTERM, self.__kill_handler)
        self.geometry('500x612'), self.resizable(False, False), self.title('Temperature Converter')
        self.mainloop()
        

if __name__ == '__main__':
    GUI()
