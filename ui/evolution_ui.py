import tkinter as tk
from tkinter import ttk
from models.evolution_model import EvolutionModel

class EvolutionUI:
    def __init__(self, root):
        self.root = root
        self.root.title("演化之路")
        
        self.model = EvolutionModel()

        self.create_widgets()

        self.update_task = None

    def create_widgets(self):
        self.time_label = ttk.Label(self.root, text=f"时间: {self.model.time_passed:.1f} ka")
        self.time_label.pack()

        self.species_label = ttk.Label(self.root, text=f"种群数量: {self.format_species_count(self.model.species_count)}")
        self.species_label.pack()

        self.attribute_labels = {}
        for attribute, value in self.model.attributes.items():
            label = ttk.Label(self.root, text=f"{attribute}: {value:.2f}")
            label.pack()
            self.attribute_labels[attribute] = label

        self.mutation_label = ttk.Label(self.root, text=f"基因突变率: {self.model.mutation_rate:.4f}")
        self.mutation_label.pack()

        self.mutation_points_label = ttk.Label(self.root, text=f"基因突变值: {self.model.mutation_points:.2f}")
        self.mutation_points_label.pack()

        self.complexity_label = ttk.Label(self.root, text=f"复杂度: {self.model.complexity}")
        self.complexity_label.pack()

        self.focus_label = ttk.Label(self.root, text="选择重心:")
        self.focus_label.pack()
        self.focus_combobox = ttk.Combobox(self.root, values=list(self.model.attributes.keys()), state="readonly")
        self.focus_combobox.set(self.model.focus_attribute)
        self.focus_combobox.pack()
        self.focus_combobox.bind("<<ComboboxSelected>>", self.change_focus)

        self.upgrade_buttons = []
        self.upgrades = {
            "脊索: 体型+10%，力量+10%，速度+10%": self.upgrade_spinal_cord,
            "背神经索: 速度+15%": self.upgrade_dorsal_nerve,
            "肛后尾: 体型+15，速度+5%": self.upgrade_postanal_tail
        }
        for name, command in self.upgrades.items():
            button = ttk.Button(self.root, text=name, command=lambda c=command, n=name: self.purchase_upgrade(c, n))
            button.pack()
            self.upgrade_buttons.append(button)

        self.purchased_label = ttk.Label(self.root, text="已购买突变:")
        self.purchased_label.pack()
        self.purchased_mutations_text = tk.Text(self.root, height=5, width=50, state="disabled")
        self.purchased_mutations_text.pack()

        self.niche_label = ttk.Label(self.root, text="生态位:")
        self.niche_label.pack()
        self.niche_text = tk.Text(self.root, height=6, width=50, state="disabled")
        self.niche_text.pack()
        self.update_niche_display()

        self.start_button = ttk.Button(self.root, text="继续", command=self.toggle_simulation)
        self.start_button.pack()

    def format_species_count(self, count):
        return "{:.2e}".format(count)

    def toggle_simulation(self):
        if self.model.running:
            self.model.running = False
            self.start_button.config(text="继续")
            if self.update_task:
                self.root.after_cancel(self.update_task)
        else:
            self.model.running = True
            self.start_button.config(text="暂停")
            self.update_simulation()

    def update_simulation(self):
        if not self.model.running:
            return

        self.model.update_simulation()
        
        self.time_label.config(text=f"时间: {self.model.time_passed:.1f} ka")
        self.species_label.config(text=f"种群数量: {self.format_species_count(self.model.species_count)}")
        self.mutation_label.config(text=f"基因突变率: {self.model.mutation_rate:.4f}")
        self.mutation_points_label.config(text=f"基因突变值: {self.model.mutation_points:.2f}")
        self.complexity_label.config(text=f"复杂度: {self.model.complexity}")

        for attribute, value in self.model.attributes.items():
            self.attribute_labels[attribute].config(text=f"{attribute}: {value:.2f}")

        self.update_task = self.root.after(100, self.update_simulation)

    def purchase_upgrade(self, upgrade_function, name):
        if self.model.purchase_upgrade(upgrade_function, name):
            self.update_attributes_display()
            for button in self.upgrade_buttons:
                if button.cget("text") == name:
                    button.pack_forget()

    def upgrade_spinal_cord(self):
        self.model.upgrade_spinal_cord()

    def upgrade_dorsal_nerve(self):
        self.model.upgrade_dorsal_nerve()

    def upgrade_postanal_tail(self):
        self.model.upgrade_postanal_tail()

    def change_focus(self, event):
        self.model.focus_attribute = self.focus_combobox.get()

    def update_attributes_display(self):
        for attribute, value in self.model.attributes.items():
            self.attribute_labels[attribute].config(text=f"{attribute}: {value:.2f}")
        self.mutation_points_label.config(text=f"基因突变值: {self.model.mutation_points:.2f}")
        self.complexity_label.config(text=f"复杂度: {self.model.complexity}")

        self.purchased_mutations_text.config(state="normal")
        self.purchased_mutations_text.delete(1.0, tk.END)
        self.purchased_mutations_text.insert(tk.END, "\n".join(self.model.purchased_mutations))
        self.purchased_mutations_text.config(state="disabled")

        self.species_label.config(text=f"种群数量: {self.format_species_count(self.model.species_count)}")

    def update_niche_display(self):
        self.niche_text.config(state="normal")
        self.niche_text.delete(1.0, tk.END)
        niche_info = "\n".join([f"{key}: {value}" for key, value in self.model.niche.items()])
        self.niche_text.insert(tk.END, niche_info)
        self.niche_text.config(state="disabled")
