import tkinter


class Window(tkinter.Frame):

    def __init__(self, geometry, master=None):
        super().__init__(master)
        self.master = master
        self.geometry = geometry
        self.init_window()

    def init_window(self):
        self.master.title("SystemsSolver GUI")

        self.pack(fill=tkinter.BOTH, expand=1)
        quit_button = tkinter.Button(self, text="Quit", command=self.client_exit)
        quit_button.place(x=0, y=0)

    def client_exit(self):
        exit()


class SolverGUI:

    def __init__(self):
        self._size = (800, 300)
        self._root = tkinter.Tk()
        self._app = Window(geometry=self._size, master=self._root)
        self._root.geometry("{}x{}".format(*self._size))

    def start(self):
        self._root.mainloop()
