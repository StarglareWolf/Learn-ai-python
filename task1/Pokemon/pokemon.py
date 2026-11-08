from __future__ import annotations
import skills
from skills import Skill
from effects import Effect
import random


class Pokemon:
    name: str
    type: str

    def __init__(self, hp: int, attack: int, defense: int, dodge_rate: int) -> None:
        # 初始化 Pokemon 的属性
        self.hp = hp                                # 当前血量
        self.max_hp = hp                            # 最大血量
        self.attack = attack                        # 攻击
        self.defense = defense                      # 防御
        self.skills = self.initialize_skills()      # 技能
        self.alive = True                           # 生存状态
        self.statuses = []                          # 状态效果
        self.dodge_rate = dodge_rate                  # 躲闪率

    def initialize_skills(self):
        # 抽象方法，子类应实现具体技能初始化
        raise NotImplementedError

    def use_skill(self, skill: Skill, opponent: Pokemon):
        # 使用技能
        print(f"{self.name} 使用 {skill.name}")
        skill.execute(self, opponent)

    def heal_self(self, amount):
        # 为自身恢复生命值
        if not isinstance(amount, int):
            amount = int(amount)

        self.hp += amount
        if self.hp > self.max_hp:
            self.hp = self.max_hp
        print(f"{self.name} 恢复 {amount} HP! 当前 HP: {self.hp}/{self.max_hp}")

    def dodge_success(self):
        if random.randint(1, 100) <= self.dodge_rate:
            return True
        return False

    def receive_damage(self, damage):
        # 计算伤害并减去防御力，更新 HP
        if not isinstance(damage, int):
            damage = int(damage)

        damage -= self.defense
        if damage <= 0:
            print(f"{self.name} 完全防御了这次攻击!")
            return

        self.hp -= damage
        self.hp = max(self.hp, 0)
        print(
            f"{self.name} 受到 {damage} 点伤害! 剩余 HP: {self.hp}/{self.max_hp}"
        )
        if self.hp == 0:
            self.alive = False
            print(f"{self.name} 晕厥!")

    def add_status_effect(self, effect: Effect):
        # 添加状态效果
        self.statuses.append(effect)

    def apply_status_effect(self):
        # 应用所有当前的状态效果，并移除持续时间结束的效果
        for status in self.statuses[:]:  # 使用切片防止列表在遍历时被修改（复制了一份，保护了原列表）
            status.apply(self)
            status.decrease_duration()
            if status.duration <= 0:
                print(f"{self.name} 的 {status.name} 状态效果消退。")
                self.statuses.remove(status)

    def type_effectiveness(self, opponent: Pokemon):
        # 计算属性克制的抽象方法，具体实现由子类提供
        raise NotImplementedError

    def begin(self):
        # 新回合开始时触发的方法
        pass

    def __str__(self) -> str:
        return f"{self.name} 属性: {self.type}"


# GlassPokemon 类, 继承自 Pokemon 类
class GrassPokemon(Pokemon):
    type = "草"              # 类属性，实例共享，不属于单独对象

    def type_effectiveness(self, opponent: Pokemon):
        # 针对敌方 Pokemon 的类型，调整效果倍率
        effectiveness = 1.0     # 效果倍率
        opponent_type = opponent.type

        if opponent_type == "水":
            effectiveness = 2.0
        elif opponent_type == "火":
            effectiveness = 0.5

        return effectiveness

    def begin(self):
        # 每个回合开始时执行玻璃属性特性
        self.grass_attribute()

    def grass_attribute(self):
        # 草属性特性：每回合恢复最大 HP 的 10%
        amount = self.max_hp * 0.1
        self.hp += amount
        if self.hp > self.max_hp:
            self.hp = self.max_hp
        print(
            f"{self.name} 恢复了 {amount} HP! 当前 HP: {self.hp}/{self.max_hp}"
        )

# Bulbasaur 类，继承自 GrassPokemon    妙蛙种子
class Bulbasaur(GrassPokemon):
    name = "妙蛙种子"    # 默认 type 为 GrassPokemon 的 type

    def __init__(self, hp=100, attack=50, defense=10, dodge_rate = 10) -> None:
        # 初始化 Bulbasaur 的属性
        super().__init__(hp, attack, defense, dodge_rate)    # 调用父类的构造函数

    def initialize_skills(self):
        # 初始化技能，具体技能是 SeedBomb 和 ParasiticSeeds
        return [skills.SeedBomb(damage=50), skills.ParasiticSeeds(amount=10)]


class ElectricPokemon(Pokemon):
    type = "电"
    def type_effectiveness(self, opponent: Pokemon):
        effectiveness = 1.0
        opponent_type = opponent.type


        if opponent_type == "水":
            effectiveness = 2.0
        if opponent_type == "草":
            effectiveness = 0.5
        return effectiveness

    def begin(self):
        self.electric_attribute()

    # 这里先这样子处理，等一下来改
    def electric_attribute(self):
        if self.dodge_success():
            return self.skills

class PikaChu(ElectricPokemon):
    name = "皮卡丘"

    def __init__(self, hp = 80, attack = 35, defense = 5, dodge_rate = 30) -> None:
        super().__init__(hp, attack, defense, dodge_rate)

    def initialize_skills(self):
        return [skills.Thunderbolt(damage = self.attack), skills.QuickAttack(damage = self.attack)]