import subprocess
import tkinter as tk

import Logcat
import Ping
import Terminal
from Terminal import terminal_connect


class Application(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.num_of_boxes = 2
        self.num_of_ip = 0
        self.ip_address = None
        self.ip_addresses = {}
        self.final_enable = {}
        self.pings = {}
        self.openings = {}
        self.enable_done = [self.num_of_boxes + 1]
        self.entry_IPs = []
        self.final_ip_list = []
        self.enable_list = []
        self.ping_list = []
        self.filenames = []
        self.create_widgets()

    def add_ipaddress(self):
        c = -1
        for self.entryIP in self.entry_IPs:
            c = c + 1
            if self.entryIP != "":
                message = self.entryIP.get()
                self.ip_addresses[self.entryIP] = self.entryIP.get()
                self.final_ip_list = [None] * len(self.ip_addresses)
                counter = 0
                for self.message, self.entryIP in self.ip_addresses.items():
                    if self.entryIP not in (None, ""):
                        self.final_ip_list[counter] = self.entryIP
                        counter = counter + 1
                    else:
                        continue
                self.num_of_ip = counter

    def reset_values(self):
        self.num_of_ip = 0
        self.ip_address = None
        self.ip_addresses = {}
        self.final_enable = {}
        self.pings = {}
        self.openings = {}
        self.enable_done = [self.num_of_boxes + 1]
        self.entry_IPs = []
        self.final_ip_list = []
        self.enable_list = []
        self.ping_list = []
        self.kill_terminal()
        self.master.destroy()  # Destroy the entire GUI window
        self.__init__(tk.Tk())  # Create a new instance of the GUI class

    def kill_terminal(self):
        subprocess.call(['open', '-n', '-g', '-a', 'Terminal'])
        subprocess.call(
            ['osascript', '-e', f'tell application "Terminal" to do script "pkill -a Terminal" in window 1'])
        self.mainloop()

    # # TODO Enable Checkbox
    # def enable_disable(self, i):
    #     self.entryIP = self.entry_IPs[i]
    #     self.pingStat = self.ping_list[i]
    #     self.checkboxEnable_var = self.enable_list[i]
    #     if self.checkboxEnable_var.get():
    #         self.entryIP.config(state='normal')
    #         self.pingStat.config(state='normal')
    #         self.test_ping(i)
    #     else:
    #         self.entryIP.config(state='disabled')
    #         self.pingStat.config(state='disabled', text="_____", background="blue")

    #     for self.checkboxEnable_var in self.enable_list:
    #         message = self.checkboxEnable_var.get()
    #         print(f'{message}')
    #         self.enable_done.append(message)

    # x = 0
    # for self.checkboxEnable_var in self.enable_list:
    #     message = self.checkboxEnable_var
    #     self.final_enable[self.checkboxEnable_var] = message
    #     print(f"{self.final_enable[self.checkboxEnable_var]}")
    #     y = 0
    #     for self.message, self.checkboxEnable_var in self.final_enable.items():
    #
    #         print(self.checkboxEnable_var.state())
    #         y = y + 1
    # # for x in range(self.num_of_boxes):
    # #     print(f"{self.enable_list[x]}\n")


    def open_button(self, i):
        self.openButton = self.openings[i]
        self.entryIP = self.entry_IPs[i]
        print(self.entryIP)
        print(self.openButton)
        subprocess.call(['open', '-n', '-g', '-a', 'Terminal'])
        # time.sleep(1)
        for x in range(self.num_of_ip):
            subprocess.call(['osascript', '-e', f'tell application "Terminal" to do script "open -a TextEdit {self.filenames[x]}" in window 1'])

    def create_widgets(self):

        # Shows the base Text for the User Interface
        # labelEnable = tk.Label(self, text=f"Enable")
        # labelEnable.grid(row=0, column=0)

        labelBox = tk.Label(self, text=f"Box Type")
        labelBox.grid(row=0, column=1)

        labelIP = tk.Label(self, text=f"IP Address")
        labelIP.grid(row=0, column=2)

        labelPing = tk.Label(self, text=f"Ping")
        labelPing.grid(row=0, column=3)

        labelFocus = tk.Label(self, text=f"Focus")
        labelFocus.grid(row=0, column=4)

        labelOpen = tk.Label(self, text=f"Open")
        labelOpen.grid(row=0, column=5)

        # labelTestPing = tk.Label(self, text=f"Test Ping")
        # labelTestPing.grid(row=0, column=6)

        for i in range(self.num_of_boxes):  # Choose the Quantity of VZBoxes you want to test
            # self.checkboxEnable_var = tk.BooleanVar(self)
            # self.checkboxEnable = tk.Checkbutton(self, variable=self.checkboxEnable_var, onvalue=1, offvalue=0,
            #                                      command=lambda i=i: self.enable_disable(i))
            # self.checkboxEnable.grid(row=i + 1, column=0)
            # self.enable_list.append(self.checkboxEnable_var)

            # create the option menu
            self.var = tk.StringVar(self)
            self.var.set("Choose VMS")
            self.option_menu = tk.OptionMenu(self, self.var, "VMS1100", "VMS6100", "QAMLESS")
            self.option_menu.grid(row=i + 1, column=1)

            # create the first text box
            self.entryIP = tk.Entry(self)
            self.entryIP.grid(row=i + 1, column=2)
            self.entry_IPs.append(self.entryIP)
            self.entryIP.bind('<Leave>', lambda event, i=i: self.test_ping(i))

            # create a label with some text -> This Label should update for each value
            self.pingStat = tk.Label(self, text="_____")
            self.pingStat.configure(background="blue")
            self.pingStat.grid(row=i + 1, column=3)
            self.pings[i] = self.pingStat
            self.ping_list.append(self.pingStat)

            # create a button that changes the label text
            self.focusButton = tk.Button(self, text="F")
            self.focusButton.grid(row=i + 1, column=4)

            # TODO Create open button where it opens the file
            # create a button that changes the label text
            self.openButton = tk.Button(self, text="O", command=lambda i=i: self.open_button(i))
            self.openButton.grid(row=i + 1, column=5)
            self.openings[i] = self.openButton

            # # create a button that changes the label text
            # self.terminalButton = tk.Button(self, text="T", command=self.test_ping)
            # self.terminalButton.grid(row=i + 1, column=6)

        # Final buttons which don't have to loop
        self.textStart = tk.Button(self, text="Start", command=self.go_to_terminal)
        self.textStart.grid(row=100, column=0)

        # TODO
        # Reset Functionality
        self.textRestart = tk.Button(self, text="Restart")
        self.textRestart.grid(row=100, column=1)

        # create a button that changes the label text
        self.textStop = tk.Button(self, text="Stop", command=self.kill_terminal)
        self.textStop.grid(row=100, column=2)

        # create a button that changes the label text
        self.textLog = tk.Button(self, text="Open Log Folder")
        self.textLog.grid(row=100, column=3)

    def go_to_terminal(self):
        self.add_ipaddress()
        if len(self.final_ip_list) == 0:
            self.mainloop()
        else:
            if self.final_ip_list is not None:
                filename = terminal_connect(self.num_of_ip, self.final_ip_list)
                for name in filename:
                    self.filenames.append(name)
                    print(f"{name}")



    # TODO Ping Tests Changes color of GUI Done!
    def color_check(self, color_int, counter):
        self.pingStat = self.pings[counter]
        if color_int == 1:
            self.pingStat.config(text="PASS", background="green")
        elif color_int == 2:
            self.pingStat.config(text="????", background="yellow")
        elif color_int == 3:
            self.pingStat.config(text="FAIL", background="red")

        # for self.pingStat in self.ping_list:
        # ping_color_change = -1
        # for y in self.final_ip_list:
        #     ping_color_change = ping_color_change + 1
        #     if y == x:
        #         next_counter = -1
        #         for self.pingStat in self.ping_list:
        #             next_counter = next_counter + 1
        #             if ping_color_change == next_counter:
        #                 if color == 1:
        #                     self.pingStat.grid(row=ping_color_change + 1, column=3)
        #                     self.pingStat.configure(background="green")
        #                 elif color == 2:
        #                     self.pingStat.grid(row=ping_color_change + 1, column=3)
        #                     self.pingStat.configure(background="yellow")
        #                 elif color == 3:
        #                     self.pingStat.grid(row=ping_color_change + 1, column=3)
        #                     self.pingStat.configure(background="red")

        #         if color == 1:
        #             self.pingStat.configure(background="green")
        #         elif color == 2:
        #             self.pingStat.configure(background="yellow")
        #         elif color == 3:
        #             self.pingStat.configure(background="red")
        #         self.ping_list[ping_color_change] = self.pingStat.configure(background="green")
        #
        #
        # if color == 1:
        #     self.pingStat.configure(background="green")
        # elif color == 2:
        #     self.pingStat.configure(background="yellow")
        # elif color == 3:
        #     self.pingStat.configure(background="red")

    def test_ping(self, i):
        # self.add_ipaddress()
        counter = i
        self.entryIP = self.entry_IPs[i]
        x = self.entry_IPs[i].get()
        # counter = counter + 1
        if x != "":
            result = Ping.ping_ip(x)
            color_int = 0
            if x == "":
                color_int = 2
                print("Ping test failed to no IP Address Found")
                self.color_check(color_int, counter)
            elif result:
                color_int = 1
                print(f"Ping successful to {x}")
                self.color_check(color_int, counter)
            else:
                color_int = 3
                print(f"Ping failed to {x}")
                self.color_check(color_int, counter)

        # TODO Logcat has a few problems due to being an older implementation
        # Logcat.start_logcat(self.final_ip_list)
        self.mainloop()


root = tk.Tk()
app = Application(master=root)
app.mainloop()
