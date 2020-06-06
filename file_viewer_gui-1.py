"""
File Viewer with GUI
I, Paul Coleman, verify that this work is my own.
This is a simple GUI-based book reader app designed by me.
"""
from tkinter import Tk, sys, Label, Text, Scrollbar, simpledialog, \
    Button, NONE, END, HORIZONTAL, NORMAL, DISABLED, Frame
from functools import partial

class FileViewer:
    """Class for File Viewer GUI"""
    def __init__(self):
        """Init function for class"""
        num_args = len(sys.argv)
        assert num_args >= 2, "You need to enter a filename"
        self.input_file = sys.argv[1]
        if num_args > 2:
            self.view_size = int(sys.argv[2])
        else:
            self.view_size = 20

        self.output_lines = ""
        with open(self.input_file, 'r+') as self.filename:
            self.offsets = self.calculate_offsets(self.filename, self.view_size)

        self.filename.close()
        self.current_offset = self.offsets[0]
        self.next_offset = self.offsets[1]
        self.num_offsets = len(self.offsets) - 1
        self.old_offset = 0

        self.master = Tk()
        self.master.rowconfigure(5, weight=10)
        self.master.rowconfigure(5, pad=4)
        self.master.title("GUI File Viewer")
        self.master.iconbitmap('logo.ico')
        self.label = Label(text=self.input_file + " - Page 1")
        self.label.grid(columnspan=6, pady=4, padx=5)

        self.text_area = Text(self.master, height=self.view_size, width=50, wrap=NONE)
        self.text_area.grid(row=1, column=0, columnspan=7, rowspan=4, padx=3, sticky='NSEW')

    def print_page(self, f_name, offset, page_number, input_offset=-1):
        """Print the page data"""
        f_name.seek(offset)
        if input_offset == -1:
            self.output_lines = f_name.readlines()
        else:
            self.output_lines = f_name.readlines(input_offset - offset - 1)

        self.text_area.config(state=NORMAL)
        text = self.input_file + " - Page " + str(page_number + 1)
        self.label.configure(text=text)
        self.text_area.delete(1.0, END)
        for f_line in self.output_lines:
            self.text_area.insert(END, f_line)
        self.text_area.config(state=DISABLED)


    def get_data_for_page(self, f_name, total_num_offsets, input_page, offset_arr):
        """Print the page data with number"""
        if input_page + 1 > total_num_offsets:
            self.print_page(f_name, offset_arr[input_page], input_page)
        else:
            self.print_page(f_name, offset_arr[input_page], input_page, offset_arr[input_page + 1])


    def calculate_offsets(self, f_name, num_lines):
        """Function to calculate offsets for all pages"""
        self.offsets = [0]  # Records beginning of file
        counter = 1
        while f_name.readline():
            if counter == num_lines:
                counter = 0
                self.offsets.append(f_name.tell())  # Record start of the page
            counter += 1
        return self.offsets

    def quit_gui(self):
        """Function to close GUI"""
        self.master.destroy()


    def page_selection(self, f_name):
        """Function to return a specific page"""
        page_number = simpledialog.askinteger(title='Page Number', prompt='Enter page number',
                                              parent=self.master, minvalue=0, maxvalue=None)
        if page_number > self.num_offsets + 1:
            page_number = 1
        if page_number < 1:
            page_number = self.num_offsets + 1
        self.current_offset = page_number - 1
        self.old_offset = self.current_offset
        self.get_data_for_page(f_name, self.num_offsets, self.current_offset, self.offsets)


    def view(self, f_name, prompt):
        """View function code for the page reader"""
        if prompt == 'd':
            self.current_offset = 0 if self.old_offset + 1 > self.num_offsets \
                else self.old_offset + 1
            self.old_offset = self.current_offset
            self.get_data_for_page(f_name, self.num_offsets, self.current_offset, self.offsets)
        elif prompt == 'u':
            self.current_offset = self.num_offsets if self.old_offset - 1 < 0 \
                else self.old_offset - 1
            self.old_offset = self.current_offset
            self.get_data_for_page(f_name, self.num_offsets, self.current_offset, self.offsets)
        elif prompt == 't':
            self.current_offset = 0
            self.old_offset = self.current_offset
            self.print_page(f_name, self.offsets[self.current_offset], self.current_offset,
                            self.offsets[self.current_offset + 1])
        elif prompt == 'b':
            self.current_offset = self.num_offsets
            self.old_offset = self.current_offset
            self.print_page(f_name, self.offsets[self.current_offset], self.current_offset)


# GUI CODE BELOW #
if __name__ == "__main__":
    FILE_VIEWER = FileViewer()
    with open(FILE_VIEWER.input_file, 'r+') as filename:
        LINE_TO_PRINT = [next(filename) for x in range(FILE_VIEWER.view_size)]
        for line in LINE_TO_PRINT:
            FILE_VIEWER.text_area.insert(END, line)

        SCROLL_HORIZONTAL = Scrollbar(FILE_VIEWER.master, orient=HORIZONTAL)
        FILE_VIEWER.text_area.configure(xscrollcommand=SCROLL_HORIZONTAL.set)
        SCROLL_HORIZONTAL.grid(row=6, columnspan=6, padx=5, sticky='NSEW')
        SCROLL_HORIZONTAL.config(command=FILE_VIEWER.text_area.xview)

        FRAME_BUTTONS = Frame(FILE_VIEWER.master)

        TOP_BUTTON = Button(FRAME_BUTTONS, text="Top", fg="red")
        TOP_BUTTON.grid(row=5, column=1, sticky='NSEW')
        TOP_BUTTON.config(command=partial(FILE_VIEWER.view, filename, 't'))

        UP_BUTTON = Button(FRAME_BUTTONS, text="Up", fg="red")
        UP_BUTTON.grid(row=5, column=2, sticky='NSEW')
        UP_BUTTON.config(command=partial(FILE_VIEWER.view, filename, 'u'))

        DOWN_BUTTON = Button(FRAME_BUTTONS, text="Down", fg="red")
        DOWN_BUTTON.grid(row=5, column=3, sticky='NSEW')
        DOWN_BUTTON.config(command=partial(FILE_VIEWER.view, filename, 'd'))

        BOTTOM_BUTTON = Button(FRAME_BUTTONS, text="Bottom", fg="red")
        BOTTOM_BUTTON.grid(row=5, column=4, sticky='NSEW')
        BOTTOM_BUTTON.config(command=partial(FILE_VIEWER.view, filename, 'b'))

        PAGE_BUTTON = Button(FRAME_BUTTONS, text="Page", fg="red")
        PAGE_BUTTON.grid(row=5, column=5, sticky='NSEW')
        PAGE_BUTTON.config(command=partial(FILE_VIEWER.page_selection, filename))

        QUIT_BUTTON = Button(FRAME_BUTTONS, text="Quit", fg="red", command=FILE_VIEWER.quit_gui)
        QUIT_BUTTON.grid(row=5, column=6, sticky='NSEW')

        FRAME_BUTTONS.grid(columnspan=6, row=5, sticky='NSEW', pady=4)

        FILE_VIEWER.text_area.config(state=DISABLED)
        FILE_VIEWER.text_area.grid()
        FILE_VIEWER.master.mainloop()

        filename.close()
