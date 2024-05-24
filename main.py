"""
    Temperature Converter System

    - Jensen Trillo, **v0.2**, 24/05/2024
    - ``Python 3.11.6``
"""
import customtkinter as ctk
from signal import signal, SIGINT, SIGTERM
from PIL import Image
from pywinstyles import set_opacity
ctk.set_appearance_mode('system')
ctk.FontManager().load_font('assets/JetBrainsMonoNL-Bold.ttf')
ctk.FontManager().load_font('assets/JetBrainsMonoNL-Regular.ttf')
ctk.FontManager().load_font('assets/segoeui.ttf')
JB = 'JetBrains Mono NL'


class GUI(ctk.CTk):
    def __kill_handler(self):
        self.quit()

    @staticmethod
    def __c_to_f(c: float) -> float:
        return (c * (9/5)) + 32

    @staticmethod
    def __f_to_c(f: float) -> float:
        return (f - 32) * (5/9)

    def __init__(self):
        class Converter(ctk.CTkFrame):
            def __init__(self, master):
                def validate(s: str, action: str):
                    if int(action) == 1:  # Input
                        # Allow periods + do not count them in total length + only one period
                        return s.replace('.', '').isdigit() and len(s.replace('.', '')) < 6 and s.count('.') < 2
                    else:  # Deletion
                        return True

                super().__init__(master, 380, 350, 0, fg_color='transparent')
                self.grid_propagate(False), self.grid_anchor('center')
                args = [
                    120, 80, 10, 0
                ]
                kwargs = {
                    'fg_color': '#ECECEC',
                    'text_color': '#222222',
                    'font': (JB, 26),
                    'justify': 'center',
                    'validate': 'key',
                    'validatecommand': (master.register(validate), '%P', '%d'),
                }
                celsius = ctk.CTkEntry(self, *args, **kwargs)
                fahrenheit = ctk.CTkEntry(self, *args, **kwargs)
                #
                celsius.grid(row=0, column=0)
                # Seperator
                ctk.CTkLabel(self, text='<>', font=(JB, 18), text_color='#000000').grid(row=0, column=1, padx=25)
                fahrenheit.grid(row=0, column=2)
                # Symbol images (after 1ms to get proper X & Y)
                celsius_img = ctk.CTkLabel(self, text='', image=ctk.CTkImage(Image.open('assets/celsius.png'),
                                                                             size=(32, 32)))
                fahrenheit_img = ctk.CTkLabel(self, text='', image=ctk.CTkImage(Image.open('assets/fahrenheit.png'),
                                                                                size=(32, 32)))
                set_opacity(celsius_img, color='#FFFCFC'), set_opacity(fahrenheit_img, color='#FFFCFC')
                self.after(1, lambda: celsius_img.place(x=celsius.winfo_x() + 110, y=celsius.winfo_y() - 20))
                self.after(1, lambda: fahrenheit_img.place(x=fahrenheit.winfo_x() + 110, y=fahrenheit.winfo_y() - 20))
        
        class History(ctk.CTkScrollableFrame):
            """ Scrollable frame for storing calculations. """
            def __init__(self, master):
                super().__init__(master, 250, 350, 0, fg_color='#CACACA')

        super().__init__(fg_color='#FFFCFC')
        signal(SIGINT, self.__kill_handler), signal(SIGTERM, self.__kill_handler)
        self.geometry('700x400'), self.resizable(False, False), self.title('Temperature Converter')
        #   __________
        self.grid_propagate(False), self.grid_anchor('center')
        #   COMPONENTS
        Converter(self).grid(row=0, column=0, padx=(25, 0))
        History(self).grid(row=0, column=1, padx=(0, 25))
        #
        self.mainloop()
        

if __name__ == '__main__':
    GUI()
