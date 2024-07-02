class EvolutionModel:
    def __init__(self):
        self.time_passed = 0.0  # 经过的时间，单位为ka
        self.species_count = 1000  # 初始种群数量
        self.reproduction_rate = 0.01  # 繁殖率
        self.death_rate = 0.005  # 死亡率
        self.mutation_rate = 0.001  # 基因突变率初始值
        self.mutation_points = 0.0  # 基因突变值
        self.complexity = 0  # 复杂度
        self.focus_attribute = "体型"  # 初始重心
        self.running = False
        self.assimilation_boost_active = False
        self.assimilation_boost_duration = 0.0

        self.attributes = {
            "体型": 1.0,
            "速度": 1.0,
            "力量": 1.0,
            "繁殖": 1.0,
            "智力": 1.0,
            "寿命": 1.0
        }

        self.niche = {
            "空间位置": "森林",
            "资源利用": "食物、水、栖息地",
            "时间维度": "昼行性",
            "生态关系": "竞争、捕食、共生",
            "功能角色": "消费者"
        }

        self.purchased_mutations = []

    def update_simulation(self):
        if not self.running:
            return

        self.time_passed += 0.1

        if self.assimilation_boost_active:
            self.assimilation_boost_duration -= 0.1
            if self.assimilation_boost_duration <= 0:
                self.reproduction_rate /= 10
                self.assimilation_boost_active = False

        births = self.species_count * self.reproduction_rate
        deaths = self.species_count * self.death_rate
        self.species_count += births - deaths

        self.mutation_points += (self.species_count * 0.000001)
        self.attributes[self.focus_attribute] += (self.species_count * 0.0000001)

    def purchase_upgrade(self, upgrade_function, name):
        if self.mutation_points >= 100:
            self.mutation_points -= 100
            upgrade_function()
            self.complexity += 1
            self.species_count = 1
            self.activate_assimilation_boost()
            self.purchased_mutations.append(name)
            return True
        return False

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
