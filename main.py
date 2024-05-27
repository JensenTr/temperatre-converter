"""
    Temperature Converter System

    - Jensen Trillo, **v0.3**, 24/05/2024
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

    def __init__(self):
        class Converter(ctk.CTkFrame):
            @staticmethod
            def __c_to_f(c: float) -> float:
                return (c * (9 / 5)) + 32

            @staticmethod
            def __f_to_c(f: float) -> float:
                return (f - 32) * (5 / 9)

            @staticmethod
            def __validate(s: str, action: str, index: int):
                if int(action) == 1:  # Input
                    if s == 'Too big!':
                        return True
                    # Allow minus sign or number on first character
                    if int(index) == 0 and (s == '-' or s.isdigit()):
                        return True
                    # Count length excluding '-' and '.', ensure only one minus or period
                    elif (new := s.removeprefix('-').replace('.', '')).isdigit() and len(new) < 6 and \
                            s.count('.') <= 1:
                        return True
                    else:
                        return False
                else:  # Deletion
                    return True

            def convert_binding(self, obj: ctk.CTkEntry, convert: ctk.CTkEntry, f_to_c: bool = False):
                def c(_):
                    if (e := obj.get()) != '' and e != '-':  # Not empty or minus sign
                        if not self.__validate(str(
                                insert := round(self.__f_to_c(float(e)) if f_to_c else self.__c_to_f(float(e)), 1)),
                                1, 1):
                            insert = 'Too big!'
                    else:
                        insert = ''
                    convert.delete(0, 'end')
                    convert.insert('end', insert)
                obj.bind('<KeyRelease>', c)

            def __init__(self, master):
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
                    'validatecommand': (master.register(self.__validate), '%P', '%d', '%i'),
                }
                celsius = ctk.CTkEntry(self, *args, **kwargs)
                fahrenheit = ctk.CTkEntry(self, *args, **kwargs)
                self.convert_binding(celsius, fahrenheit), celsius.grid(row=0, column=0)
                self.convert_binding(fahrenheit, celsius, True), fahrenheit.grid(row=0, column=2)
                #
                # Seperator
                ctk.CTkLabel(self, text='<>', font=(JB, 18), text_color='#000000').grid(row=0, column=1, padx=25)
                #
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
