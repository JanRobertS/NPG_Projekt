from email.message import EmailMessage
import ssl
import smtplib
import tkinter
import customtkinter
import os


def SavedNotes(notes_dir):
    # returns list of notes in folder
    return [os.path.splitext(filename)[0] for filename in os.listdir(notes_dir) if filename.endswith(".txt")]


def send_note(title, text, email_reciver):
    # hasło: mquoianwvzurwhyj
    # dane do wysyłania emaila
    email_sender = 'testmailnpg123@gmail.com'
    email_password = 'mquoianwvzurwhyj'

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_reciver
    em['Subject'] = title
    em.set_content(text)

    context = ssl.create_default_context()

    # wysyła email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_reciver, em.as_string())


class App(customtkinter.CTk):
    def __init__(self):

        self.notes_dir = "notes"  # nazwa folderu, w którym będą przechowywane notatki
        if not os.path.exists(self.notes_dir):
            os.makedirs(self.notes_dir)

        super().__init__()

        # configure window
        self.title("Notepad")
        self.geometry(f"{580}x{580}")

        # configure grid layout (4x3)
        # noinspection PyTypeChecker
        self.grid_columnconfigure((0, 1, 2), weight=1)
        # noinspection PyTypeChecker
        self.grid_rowconfigure((1, 2, 3), weight=1)

        # create textbox
        self.textbox = customtkinter.CTkTextbox(self)
        self.textbox.grid(row=1, column=0, rowspan=3, columnspan=4, padx=(10, 10), pady=(10, 10), sticky="nsew")

        # create entry for file name
        self.entry_name = customtkinter.CTkEntry(self, placeholder_text="FileName")
        self.entry_name.grid(row=0, column=0, columnspan=1, padx=(10, 10), pady=(10, 10), sticky="nsew")

        # create entry for email
        self.entry_email = customtkinter.CTkEntry(self, placeholder_text="email@domain.com")
        self.entry_email.grid(row=4, column=0, columnspan=2, padx=(10, 10), pady=(10, 10), sticky="nsew")

        # save file button
        self.save_button = customtkinter.CTkButton(self, text="Save", command=self.SaveFile)
        self.save_button.grid(row=0, column=1, padx=(5, 5), pady=(10, 10), sticky="nsew")

        # new file button
        self.new_file_button = customtkinter.CTkButton(self, text="New", command=self.NewFile)
        self.new_file_button.grid(row=0, column=2, padx=(5, 5), pady=(10, 10), sticky="nsew")

        # send file button
        self.send_button = customtkinter.CTkButton(self, text="Send", command=self.SendFile)
        self.send_button.grid(row=4, column=2, padx=(10, 10), pady=(10, 10), sticky="nsew")

        # delete file button
        self.send_button = customtkinter.CTkButton(self, text="Delete", command=self.DeleteFile)
        self.send_button.grid(row=4, column=3, padx=(5, 5), pady=(10, 10), sticky="nsew")

        # open file
        self.open_file = customtkinter.CTkOptionMenu(self, values=SavedNotes(self.notes_dir), command=self.OpenFile)
        self.open_file.grid(row=0, column=3, padx=(5, 5), pady=(10, 10))
        self.open_file.set("Open")  # set initial value

    def OpenFile(self, choice):
        # clear view
        self.textbox.delete("0.0", "end")
        self.entry_name.delete("0", "end")
        # open file
        with open(os.path.join(self.notes_dir, choice + ".txt")) as f:
            note_text = f.read()
        self.textbox.insert("0.0", note_text)
        self.entry_name.insert("0", choice)
        self.open_file.set("Open")

    def SaveFile(self):
        if self.entry_name.get() == "":
            tkinter.messagebox.showerror(title="Error", message="Empty file name")
        # get content
        note_name = self.entry_name.get()
        note_text = self.textbox.get("0.0", "end")
        # save note
        note_path = os.path.join(self.notes_dir, note_name + ".txt")  # utwórz ścieżkę do pliku notatki
        with open(note_path, "w") as f:
            f.write(note_text)  # zapisz notatkę do pliku
        self.open_file.configure(values=SavedNotes(self.notes_dir))
        tkinter.messagebox.showwinfo(title="Success!", message="Saved Successfully")

    def NewFile(self):
        # clear view
        self.textbox.delete("0.0", "end")
        self.entry_name.delete("0", "end")
        # name file NewFile
        self.entry_name.configure(placeholder_text="FileName")

    def SendFile(self):
        send_note(self.entry_name.get(), self.textbox.get("0.0", "end"), self.entry_email.get())
        tkinter.messagebox.shoinfo(title="Success!", message="Email sent")

    def DeleteFile(self):
        # delete note from folder
        path = os.path.join(self.notes_dir, self.entry_name.get() + ".txt")
        if os.path.exists(path):
            os.remove(path)
        else:
            tkinter.messagebox.showerror(title="Error", message="Wrong file name")
        # delete note from list of notes
        self.open_file.configure(values=SavedNotes(self.notes_dir))
        # clear view
        self.open_file.set("Open")
        self.textbox.delete("0.0", "end")
        self.entry_name.delete("0", "end")
        tkinter.messagebox.showwinfo(title="Success!", message="Deleted successfully")
