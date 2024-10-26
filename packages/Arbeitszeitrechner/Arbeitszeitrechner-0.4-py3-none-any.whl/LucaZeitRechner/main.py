import customtkinter as ctk
from tkinter import messagebox
from .WorkTimeCalc import *
from customtkinter import *

class App:
    def __init__(self, root):
        self.root = root
        root.title("Arbeitszeitrechner")

        self.starttime_title = ctk.CTkLabel(root, text="Startzeit eingeben")
        self.starttime_title.pack(pady=1)

        self.starttime = ctk.CTkEntry(root)
        self.starttime.pack(pady=1)
        self.starttime.bind("<Return>", lambda event: self.mittag_start.focus())

        self.mittag_start_title = ctk.CTkLabel(root, text="Mittag Start eingeben")
        self.mittag_start_title.pack(pady=1)

        self.mittag_start = ctk.CTkEntry(root)
        self.mittag_start.pack(pady=1)
        self.mittag_start.bind("<Return>", lambda event: self.mittag_end.focus())

        self.mittag_end_title = ctk.CTkLabel(root, text="Mittag Ende eingeben")
        self.mittag_end_title.pack(pady=1)

        self.mittag_end = ctk.CTkEntry(root)
        self.mittag_end.pack(pady=1)
        self.mittag_end.bind("<Return>", lambda event: self.calc_time())

        self.button = ctk.CTkButton(root, text="print", command=self.calc_time)
        self.button.pack(pady=10)

        self.notification = ctk.IntVar()
        self.notification_switch = ctk.CTkCheckBox(root, text="Benachrichtigung beim Erreichen der Zeit", variable=self.notification, onvalue=1, offvalue=0, command= self.update_notification_status)
        self.notification_switch.pack(pady=5)

        self.lbl1 = ctk.CTkLabel(root, text="")
        self.lbl1.pack(pady=5)

        self.lbl2 = ctk.CTkLabel(root, text="")
        self.lbl2.pack(pady=5)

        self.lbl3 = ctk.CTkLabel(root, text="Benachrichtigung aus")
        self.lbl3.pack(pady=5)

        self.lbl4 = ctk.CTkLabel(root, text="Timer off")
        self.lbl4.pack(pady=5)

        self.min_time = 0
        self.max_time = 0
        self.wait_time = 0
        self.wait_time = -1
        # self.workHours = 0
        # self.workMins = validateTime(self.workHours)

    def calc_time(self):
        start_time = self.starttime.get()
        mittag_start = self.mittag_start.get()
        mittag_end = self.mittag_end.get()
        min_max_time = minMax(start_time, mittag_start, mittag_end)
        if not min_max_time:
            messagebox.showinfo(title="Fehler", message="Zeiteingabe ungültig")
        else:
            min_time_t = min_max_time[0]
            max_time_t = min_max_time[1]
            min_time = f"{min_time_t[0]:02}:{min_time_t[1]:02}"
            max_time = f"{max_time_t[0]:02}:{max_time_t[1]:02}"

            self.lbl1.configure(text=f"Minimale Zeit: {min_time}")
            self.lbl2.configure(text=f"Maximale Zeit: {max_time}")
            self.min_time = min_time
            self.max_time = max_time
            self.display_time_until_end()
            
    def update_notification_status(self):
        if self.notification.get() == 0:
            self.lbl3.configure(text="Benachrichtigung aus")
            return
        else:
            self.lbl3.configure(text="Benachrichtigung ein")
            return
    
    def display_time_until_end(self):
        until_end, wait_time = time_until_end(self.min_time)
        self.lbl4.configure(text=until_end)
        self.wait_time = wait_time
        self.stopTimer()
        if self.notification.get() == 1:
            self.timerActive = True
            self.popup()
    
    def popup(self):
        if self.timerActive:
            if self.wait_time <= 0:
                self.lbl4.configure(text="done")
                displayPopup(self, message="8:12 Erreicht!")
                self.stopTimer()
            else:
                self.wait_time -= 1
                self.wait_t = convertMinutes(self.wait_time)
                self.wait_hr = self.wait_t[0]
                self.wait_min = self.wait_t[1]
                self.lbl4.configure(text=f"{self.wait_t[0]:02}:{self.wait_t[1]:02} Minuten übrig")
                self.root.after(60000, self.popup) #nach 60 sekunden funktion erneut ausführen (kein time.sleep)
        else:
            return
    
    def stopTimer(self):
        self.timerActive = False
        self.lbl4.configure(text="Timer off")

def displayPopup(self, message):
    popupWindow = ctk.CTkToplevel(self.root)
    popupWindow.title("Benachrichtigung")
    popupWindow.geometry("290x90")
    popupWindow.wm_attributes("-topmost", 1)
    label = ctk.CTkLabel(popupWindow, text=message)
    label.pack()
    okButton = ctk.CTkButton(popupWindow, text="OK", command=popupWindow.destroy)
    okButton.pack(pady=10)
    popupWindow.grab_set()
    
def main():
    root = ctk.CTk()
    app = App(root)
    root.geometry("300x500")
    root.mainloop()
    
if __name__ == "__main__":
    main()
