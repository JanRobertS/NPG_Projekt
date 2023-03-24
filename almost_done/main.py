import notepad_app
import customtkinter

customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"

if __name__ == "__main__":
    overwrite_file = False
    app = notepad_app.App()
    app.mainloop()
