import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, colorchooser
import os
import io
import contextlib
import tkinter.font as tkfont

class TipiEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("tipi editor v0.5")
        self.root.geometry("1080x650")

        # Default global settings
        self.font_family = 'Courier'
        self.font_size = 12
        self.font_color = 'black'
        self.line_font_sizes = {}  # stocke la taille de police par ligne

        # Logo frame
        self.logo_frame = tk.Frame(root, height=100)
        self.logo_frame.pack(fill='x', pady=5)
        self.logo_label = tk.Label(self.logo_frame, text="Aucun logo", bd=1, relief='solid')
        self.logo_label.pack(side='left', padx=10)

        # Main frame (text + image path)
        self.frame = tk.Frame(root)
        self.frame.pack(fill='both', expand=1)

        # Text area
        self.text_font = tkfont.Font(family=self.font_family, size=self.font_size)
        self.text = tk.Text(self.frame, wrap='word', font=self.text_font, fg=self.font_color)
        self.text.pack(side='left', fill='both', expand=1)

        # Image path label
        self.img_label = tk.Label(self.frame, text="Aucune image sélectionnée")
        self.img_label.pack(side='right', padx=10, pady=10)

        # Python console area
        self.console = tk.Text(root, height=10, bg="black", fg="lime", insertbackground="white")
        self.console.pack(fill='x')
        self.console.insert(tk.END, ">> Console Python prête.\n")
        self.console.config(state='disabled')

        # Menu bar
        self.menu = tk.Menu(root)
        root.config(menu=self.menu)

        # File menu
        file_menu = tk.Menu(self.menu, tearoff=0)
        file_menu.add_command(label="Ouvrir .tipi", command=self.open_tipi)
        file_menu.add_command(label="Enregistrer .tipi", command=self.save_tipi)
        self.menu.add_cascade(label="Fichier", menu=file_menu)

        # Image menu
        img_menu = tk.Menu(self.menu, tearoff=0)
        img_menu.add_command(label="Sélectionner un logo PNG", command=self.select_image)
        self.menu.add_cascade(label="Image", menu=img_menu)

        # Python menu
        run_menu = tk.Menu(self.menu, tearoff=0)
        run_menu.add_command(label="Exécuter le code Python", command=self.run_python_code)
        self.menu.add_cascade(label="Python", menu=run_menu)

        # Configuration menu
        config_menu = tk.Menu(self.menu, tearoff=0)
        config_menu.add_command(label="Taille de police globale", command=self.choose_font_size)
        config_menu.add_command(label="Couleur du texte", command=self.choose_font_color)
        config_menu.add_command(label="Taille de police par ligne", command=self.choose_font_size_line)
        self.menu.add_cascade(label="Configuration", menu=config_menu)

        # Internal state
        self.image_path = ""
        self.logo_img = None

    def select_image(self):
        path = filedialog.askopenfilename(filetypes=[("Images PNG", "*.png")])
        if path:
            self.image_path = path
            self.img_label.config(text=os.path.basename(path))
            try:
                self.logo_img = tk.PhotoImage(file=path)
                self.logo_img = self.logo_img.subsample(max(1, self.logo_img.width()//100), max(1, self.logo_img.height()//100))
                self.logo_label.config(image=self.logo_img, text="")
            except Exception as e:
                messagebox.showwarning("Logo", f"Impossible de charger le logo : {e}")

    def choose_font_size(self):
        size = simpledialog.askinteger("Taille de police", "Entrez la taille de police globale :", initialvalue=self.font_size)
        if size:
            self.font_size = size
            self.text_font.configure(size=self.font_size)

    def choose_font_color(self):
        color = colorchooser.askcolor(title="Choisir la couleur du texte")[1]
        if color:
            self.font_color = color
            self.text.configure(fg=self.font_color)

    def choose_font_size_line(self):
        line = self.text.index("insert").split('.')[0]
        size = simpledialog.askinteger("Taille de police ligne", f"Entrez la taille de police pour la ligne {line} :", initialvalue=self.font_size)
        if size:
            tag = f"line_{line}"
            font = tkfont.Font(family=self.font_family, size=size)
            self.text.tag_configure(tag, font=font)
            self.text.tag_add(tag, f"{line}.0", f"{line}.0 lineend")
            self.line_font_sizes[line] = size

    def save_tipi(self):
        path = filedialog.asksaveasfilename(defaultextension=".tipi",
                                            filetypes=[("Fichier TiPi", "*.tipi")])
        if not path:
            return
        try:
            with open(path, "w", encoding="utf-8") as file:
                file.write("[TEXTE]\n")
                file.write(self.text.get(1.0, tk.END))
                file.write("[IMAGE]\n")
                file.write(self.image_path + "\n")
                file.write("[CONFIG]\n")
                file.write(f"font_size={self.font_size}\n")
                file.write(f"font_color={self.font_color}\n")
                file.write("[LINE_CONFIG]\n")
                for line, size in self.line_font_sizes.items():
                    file.write(f"{line}={size}\n")
            messagebox.showinfo("Enregistré", "Ton fichier .tipi est prêt avec logo et config avancée 🔥")
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de sauvegarder : {e}")

    def open_tipi(self):
        path = filedialog.askopenfilename(filetypes=[("Fichier TiPi", "*.tipi")])
        if not path:
            return
        try:
            content = open(path, "r", encoding="utf-8").read()
            text_part = content.split("[TEXTE]\n")[1].split("[IMAGE]\n")[0]
            remainder = content.split("[IMAGE]\n")[1]
            image_part = remainder.split("[CONFIG]\n")[0].strip()
            config_part = remainder.split("[CONFIG]\n")[1].split("[LINE_CONFIG]\n")[0]
            line_part = remainder.split("[LINE_CONFIG]\n")[1] if "[LINE_CONFIG]" in remainder else ""

            self.text.delete(1.0, tk.END)
            self.text.insert(tk.END, text_part)
            self.image_path = image_part
            self.img_label.config(text=os.path.basename(image_part))

            try:
                self.logo_img = tk.PhotoImage(file=image_part)
                self.logo_img = self.logo_img.subsample(max(1, self.logo_img.width()//100), max(1, self.logo_img.height()//100))
                self.logo_label.config(image=self.logo_img, text="")
            except Exception as e:
                messagebox.showwarning("Logo", f"Logo non chargé : {e}")

            for line in config_part.splitlines():
                if line.startswith("font_size="):
                    try:
                        self.font_size = int(line.split('=',1)[1])
                        self.text_font.configure(size=self.font_size)
                    except:
                        pass
                elif line.startswith("font_color="):
                    self.font_color = line.split('=',1)[1]
                    self.text.configure(fg=self.font_color)

            self.line_font_sizes.clear()
            for entry in line_part.splitlines():
                if '=' in entry:
                    ln, sz = entry.split('=',1)
                    try:
                        sz = int(sz)
                        self.line_font_sizes[ln] = sz
                        tag = f"line_{ln}"
                        font = tkfont.Font(family=self.font_family, size=sz)
                        self.text.tag_configure(tag, font=font)
                        self.text.tag_add(tag, f"{ln}.0", f"{ln}.0 lineend")
                    except:
                        pass
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible d’ouvrir le fichier .tipi : {e}")

    def run_python_code(self):
        code = self.text.get(1.0, tk.END)
        self.save_as_py()
        self.console.config(state='normal')
        self.console.delete(1.0, tk.END)
        try:
            output = io.StringIO()
            with contextlib.redirect_stdout(output), contextlib.redirect_stderr(output):
                exec(code, {})
            result = output.getvalue()
        except Exception as e:
            result = f"Erreur : {e}"
        self.console.insert(tk.END, result)
        self.console.config(state='disabled')

    def save_as_py(self):
        path = filedialog.asksaveasfilename(defaultextension=".py",
                                            filetypes=[("Fichier Python", "*.py")])
        if path:
            try:
                with open(path, "w", encoding="utf-8") as file:
                    file.write(self.text.get(1.0, tk.END))
                messagebox.showinfo("Sauvegardé", f"Le code a été enregistré en {os.path.basename(path)}")
            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible de sauvegarder le fichier Python : {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = TipiEditor(root)
    root.mainloop()
