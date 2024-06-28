import tkinter as tk
from tkinter import ttk

class EvolutionSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("演化之路")

        # 初始化变量
        self.time_passed = 0.0  # 经过的时间，单位为ka
        self.species_count = 1000  # 初始种群数量
        self.reproduction_rate = 0.01  # 繁殖率
        self.death_rate = 0.005  # 死亡率
        self.mutation_rate = 0.001  # 基因突变率初始值
        self.mutation_points = 1000.0  # 基因突变值
        self.complexity = 0  # 复杂度
        self.focus_attribute = "体型"  # 初始重心
        self.running = False
        self.assimilation_boost_active = False
        self.assimilation_boost_duration = 0.0

        # 初始物种属性
        self.attributes = {
            "体型": 1.0,
            "速度": 1.0,
            "力量": 1.0,
            "繁殖": 1.0,
            "智力": 1.0,
            "寿命": 1.0
        }

        self.purchased_mutations = []

        # 创建UI组件
        self.create_widgets()

        # 更新种群数量的任务
        self.update_task = None

    def create_widgets(self):
        # 时间显示标签
        self.time_label = ttk.Label(self.root, text=f"时间: {self.time_passed:.1f} ka")
        self.time_label.pack()

        # 种群数量显示标签
        self.species_label = ttk.Label(self.root, text=f"种群数量: {self.format_species_count(self.species_count)}")
        self.species_label.pack()

        # 属性显示
        self.attribute_labels = {}
        for attribute, value in self.attributes.items():
            label = ttk.Label(self.root, text=f"{attribute}: {value:.2f}")
            label.pack()
            self.attribute_labels[attribute] = label

        # 基因突变率显示标签
        self.mutation_label = ttk.Label(self.root, text=f"基因突变率: {self.mutation_rate:.4f}")
        self.mutation_label.pack()

        # 基因突变值显示标签
        self.mutation_points_label = ttk.Label(self.root, text=f"基因突变值: {self.mutation_points:.2f}")
        self.mutation_points_label.pack()

        # 复杂度显示标签
        self.complexity_label = ttk.Label(self.root, text=f"复杂度: {self.complexity}")
        self.complexity_label.pack()

        # 重心选择
        self.focus_label = ttk.Label(self.root, text="选择重心:")
        self.focus_label.pack()
        self.focus_combobox = ttk.Combobox(self.root, values=list(self.attributes.keys()), state="readonly")
        self.focus_combobox.set(self.focus_attribute)
        self.focus_combobox.pack()
        self.focus_combobox.bind("<<ComboboxSelected>>", self.change_focus)

        # 升级功能按钮
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

        # 已购买突变显示
        self.purchased_label = ttk.Label(self.root, text="已购买突变:")
        self.purchased_label.pack()
        self.purchased_mutations_text = tk.Text(self.root, height=5, width=50, state="disabled")
        self.purchased_mutations_text.pack()

        # 继续/暂停按钮
        self.start_button = ttk.Button(self.root, text="继续", command=self.toggle_simulation)
        self.start_button.pack()

    def format_species_count(self, count):
        return "{:.2e}".format(count)

    def toggle_simulation(self):
        if self.running:
            self.running = False
            self.start_button.config(text="继续")
            if self.update_task:
                self.root.after_cancel(self.update_task)
        else:
            self.running = True
            self.start_button.config(text="暂停")
            self.update_simulation()

    def update_simulation(self):
        if not self.running:
            return

        # 更新时间
        self.time_passed += 0.1

        # 检查同化加成是否激活
        if self.assimilation_boost_active:
            self.assimilation_boost_duration -= 0.1
            if self.assimilation_boost_duration <= 0:
                self.reproduction_rate /= 10
                self.assimilation_boost_active = False

        # 计算新的种群数量
        births = self.species_count * self.reproduction_rate  # 出生数量
        deaths = self.species_count * self.death_rate  # 死亡数量
        self.species_count += births - deaths  # 更新种群数量

        # 更新基因突变值，随时间增加并受种群数量影响
        self.mutation_points += (self.species_count * 0.000001)

        # 更新重心属性，随时间增加并受种群数量影响
        self.attributes[self.focus_attribute] += (self.species_count * 0.0000001)

        # 更新标签
        self.time_label.config(text=f"时间: {self.time_passed:.1f} ka")
        self.species_label.config(text=f"种群数量: {self.format_species_count(self.species_count)}")
        self.mutation_label.config(text=f"基因突变率: {self.mutation_rate:.4f}")
        self.mutation_points_label.config(text=f"基因突变值: {self.mutation_points:.2f}")
        self.complexity_label.config(text=f"复杂度: {self.complexity}")

        # 更新属性显示
        for attribute, value in self.attributes.items():
            self.attribute_labels[attribute].config(text=f"{attribute}: {value:.2f}")

        # 继续更新
        self.update_task = self.root.after(100, self.update_simulation)

    def purchase_upgrade(self, upgrade_function, name):
        if self.mutation_points >= 100:  # 假设每个升级需要100点基因突变值
            self.mutation_points -= 100
            upgrade_function()
            self.complexity += 1  # 增加复杂度
            self.species_count = 1  # 购买突变后将种群数量设为1
            self.activate_assimilation_boost()
            self.purchased_mutations.append(name)
            self.update_attributes_display()

            # 移除已购买选项的按钮
            for button in self.upgrade_buttons:
                if button.cget("text") == name:
                    button.pack_forget()

    def activate_assimilation_boost(self):
        if not self.assimilation_boost_active:
            self.reproduction_rate *= 10
            self.assimilation_boost_duration = 10.0
            self.assimilation_boost_active = True

    def upgrade_spinal_cord(self):
        self.attributes["体型"] *= 1.10
        self.attributes["力量"] *= 1.10
        self.attributes["速度"] *= 1.10

    def upgrade_dorsal_nerve(self):
        self.attributes["速度"] *= 1.15

    def upgrade_postanal_tail(self):
        self.attributes["体型"] += 15
        self.attributes["速度"] *= 1.05

    def change_focus(self, event):
        self.focus_attribute = self.focus_combobox.get()

    def update_attributes_display(self):
        # 更新属性显示
        for attribute, value in self.attributes.items():
            self.attribute_labels[attribute].config(text=f"{attribute}: {value:.2f}")
        self.mutation_points_label.config(text=f"基因突变值: {self.mutation_points:.2f}")
        self.complexity_label.config(text=f"复杂度: {self.complexity}")

        # 更新已购买突变显示
        self.purchased_mutations_text.config(state="normal")
        self.purchased_mutations_text.delete(1.0, tk.END)
        self.purchased_mutations_text.insert(tk.END, "\n".join(self.purchased_mutations))
        self.purchased_mutations_text.config(state="disabled")

        # 更新种群数量显示
        self.species_label.config(text=f"种群数量: {self.format_species_count(self.species_count)}")

# 创建Tkinter窗口
root = tk.Tk()
app = EvolutionSimulator(root)
root.mainloop()
