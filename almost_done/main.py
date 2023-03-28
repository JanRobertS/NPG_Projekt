from email import encoders
import smtplib
import tkinter
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import customtkinter
import os

attachments = []

customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"


def SavedNotes(notes_dir):
    # returns list of notes in folder
    notes = [os.path.splitext(filename)[0] for filename in os.listdir(notes_dir) if
             filename.endswith(".txt") and filename != "Create New File"]
    notes.append("Create New File")
    return notes


def send_note(title, text, email_reciver):
    # hasło: mquoianwvzurwhyj
    # dane do wysyłania emaila
    email_sender = 'testmailnpg123@gmail.com'
    email_password = 'mquoianwvzurwhyj'

    em = MIMEMultipart()
    em['From'] = email_sender
    em['To'] = email_reciver
    em['Subject'] = title

    em.attach(MIMEText(text, 'plain'))

    # dodanie stopki i notatki
    # em.set_content(f"{text}\n\nPozdrawiam,\nJan Robert Skarbon")

    # adding attachment
    for attachment_path in attachments:
        attachment = open(attachment_path, "rb")
        p = MIMEBase('application', 'octet-stream')
        p.set_payload(attachment.read())
        encoders.encode_base64(p)
        p.add_header('Content-Disposition', "attachment; filename= %s" % attachment_path)
        em.attach(p)

    # wysyła email
    session = smtplib.SMTP('smtp.gmail.com', 587)  # use gmail with port
    session.starttls()  # enable security
    session.login(email_sender, email_password)  # login with mail_id and password
    content = em.as_string()
    session.sendmail(email_sender, email_reciver, content)
    session.quit()


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
        self.entry_email.grid(row=4, column=2, columnspan=2, padx=(5, 10), pady=(10, 5), sticky="nsew")

        # create entry for attachment
        self.entry_attachment = customtkinter.CTkEntry(self, placeholder_text="attachment absolute address")
        self.entry_attachment.grid(row=4, column=0, columnspan=2, padx=(10, 5), pady=(10, 5), sticky="nsew")

        # save file button
        self.save_button = customtkinter.CTkButton(self, text="Save", command=self.SaveFile)
        self.save_button.grid(row=0, column=1, padx=(5, 5), pady=(10, 10), sticky="nsew")

        # send file button
        self.send_button = customtkinter.CTkButton(self, text="Send", command=self.SendFile)
        self.send_button.grid(row=5, column=3, padx=(5, 10), pady=(5, 10), sticky="nsew")

        # delete file button
        self.delete_button = customtkinter.CTkButton(self, text="Delete", command=self.DeleteFile)
        self.delete_button.grid(row=0, column=3, padx=(5, 10), pady=(10, 10), sticky="nsew")

        # delete attachment button
        self.delete_attach_button = customtkinter.CTkButton(self, text="Delete attachment", command=self.DeleteAttach)
        self.delete_attach_button.grid(row=5, column=1, padx=(5, 5), pady=(5, 10), sticky="nsew")

        # add atachment file button
        self.add_attach = customtkinter.CTkButton(self, text="Add atachment", command=self.AddAtach)
        self.add_attach.grid(row=5, column=0, padx=(10, 5), pady=(5, 10), sticky="nsew")

        # look into attachments
        self.check_attach = customtkinter.CTkOptionMenu(self, values=attachments, command=self.CheckAttach)
        self.check_attach.grid(row=5, column=2, padx=(5, 5), pady=(5, 10))
        self.check_attach.set("Attachments")  # set initial value

        # open file
        self.open_file = customtkinter.CTkOptionMenu(self, values=SavedNotes(self.notes_dir), command=self.OpenFile)
        self.open_file.grid(row=0, column=2, padx=(5, 5), pady=(10, 10))
        self.open_file.set("Open")  # set initial value

    def OpenFile(self, choice):
        # clears view for new file
        if choice == "Create New File":
            self.textbox.delete("0.0", "end")
            self.entry_name.delete("0", "end")
            self.entry_name.configure(placeholder_text="FileName")
            self.entry_name.insert("0", choice)
            return
        # clear view
        self.textbox.delete("0.0", "end")
        self.entry_name.delete("0", "end")
        # open file
        with open(os.path.join(self.notes_dir, choice + ".txt")) as f:
            note_text = f.read()
        self.textbox.insert("0.0", note_text)
        self.entry_name.insert("0", choice)

    def SaveFile(self):
        # error if file name is empty
        if self.entry_name.get() == "":
            tkinter.messagebox.showerror(title="Error", message="Empty file name")
            return
        # get content
        note_name = self.entry_name.get()
        note_text = self.textbox.get("0.0", "end")
        # save note
        note_path = os.path.join(self.notes_dir, note_name + ".txt")  # utwórz ścieżkę do pliku notatki
        with open(note_path, "w") as f:
            f.write(note_text)  # zapisz notatkę do pliku
        self.open_file.configure(values=SavedNotes(self.notes_dir))
        tkinter.messagebox.showinfo(title="Success!", message="Saved Successfully")

    def SendFile(self):
        if self.entry_email.get() == "":
            tkinter.messagebox.showerror(title="Error", message="Enter email address")
            return
        send_note(self.entry_name.get(), self.textbox.get("0.0", "end"), self.entry_email.get())
        tkinter.messagebox.showinfo(title="Success!", message="Email sent")

    def DeleteFile(self):
        # delete note from folder
        path = os.path.join(self.notes_dir, self.entry_name.get() + ".txt")
        if os.path.exists(path):
            os.remove(path)
        else:
            tkinter.messagebox.showerror(title="Error", message="Wrong file name")
            return
        # delete note from list of notes
        self.open_file.configure(values=SavedNotes(self.notes_dir))
        # clear view
        self.open_file.set("Open")
        self.textbox.delete("0.0", "end")
        self.entry_name.delete("0", "end")
        tkinter.messagebox.showinfo(title="Success!", message="Deleted successfully")

    def AddAtach(self):
        # get content from attachment entry
        attachment_path = self.entry_attachment.get()
        # check if path exists
        if not os.path.exists(attachment_path):
            tkinter.messagebox.showerror(title="Error", message="Wrong path name")
            return
        # append list of attachments
        attachments.append(attachment_path)
        self.entry_attachment.delete('0', 'end')
        # update dropdown menu
        self.check_attach.configure(values=attachments)

    def CheckAttach(self, choice):
        # insert attachment path into entry
        self.entry_attachment.delete('0', 'end')
        self.entry_attachment.insert('0', choice)
        self.check_attach.set("Attachments")

    def DeleteAttach(self):
        # get content from entry
        attachment_path = self.entry_attachment.get()
        # check if path exists
        if not os.path.exists(attachment_path):
            tkinter.messagebox.showerror(title="Error", message="Wrong path name")
            return
        # remove attachment from list and update dropdown menu
        attachments.remove(attachment_path)
        self.entry_attachment.delete('0', 'end')
        self.check_attach.configure(values=attachments)
        tkinter.messagebox.showinfo(title="Success!", message="Deleted successfully")


if __name__ == "__main__":
    app = App()
    app.mainloop()
