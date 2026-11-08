import random
from typing import TYPE_CHECKING
import effects

if TYPE_CHECKING:
    from pokemon import Pokemon
# 因为 pokemon 文件中已经导入了 skills 和 effects，这里如果直接导入 pokemon, 会出现 A 导入 B, 然后 B 导入 A 的情况。在 C++ 中可以，因为是分开编译，但是 python 中 import 相当于直接编译那个文件，相互嵌套导入就会死局

class Skill:
    name: str

    def __init__(self, damage) -> None:
        self.damage = damage
        pass

    # 执行
    def execute(self, user: "Pokemon", opponent: "Pokemon"):
        raise NotImplementedError

    def change_damage(self, user: "Pokemon", opponent: "Pokemon") -> int:
        damage = self.damage
        damage *= opponent.type_effectiveness(user)
        if not isinstance(damage, int):
            damage = int(damage)
        return damage

    def __str__(self) -> str:
        return f"{self.name}"


class SeedBomb(Skill):
    name = "Seed Bomb"

    def __init__(self, damage: int, activation_chance: int = 15) -> None:
        super().__init__(damage)
        self.activation_chance = activation_chance  # 确保激活几率被正确初始化

    # Pokemon 用引号引起来是为了延迟求值，防止出现作用域不存在该类名。因为导入 Pokemon 使用的是 TYPE_CHECKING
    def execute(self, user: "Pokemon", opponent: "Pokemon") -> None:
        # 造成伤害
        if opponent.dodge_success():
            print(f"{opponent.name} 躲开了这次攻击!")
            return
        damage = self.change_damage(user, opponent)
        opponent.receive_damage(damage)
        print(
            f"{user.name} 使用 {self.name}, 对 {opponent.name} 造成 {damage} 点伤害 "
        )

        # 判断是否触发状态效果
        if random.randint(1, 100) <= self.activation_chance:
            opponent.add_status_effect(effects.PoisonEffect())
            print(f"{opponent.name} 被技能 {self.name} 中毒加成!")
        else:
            print(f"本回合技能 {self.name} 对 {opponent.name} 的中毒加成失败。")


class ParasiticSeeds(Skill):
    name = "Parasitic Seeds"

    def __init__(self, amount: int) -> None:
        super().__init__(0)
        self.amount = amount

    def execute(self, user: "Pokemon", opponent: "Pokemon") -> None:
        # 给使用者添加治疗效果
        user.add_status_effect(effects.HealEffect(self.amount))
        print(f"{user.name} 使用技能 {self.name} 恢复 {self.amount} HP")

        # 给对手添加中毒效果
        opponent.add_status_effect(effects.PoisonEffect())
        print(f"{opponent.name} 被技能 {self.name} 中毒加成!")

class Thunderbolt(Skill):
    name = "Thunderbolt"

    def __init__(self, damage, activation_chance: int = 10) -> None:
        super().__init__(damage)
        self.activation_chance = activation_chance


    def execute(self, user: "Pokemon", opponent: "Pokemon") -> None:
        if opponent.dodge_success():
            print(f"{opponent.name} 躲开了这次攻击!")
            return
        damage = self.change_damage(user, opponent)
        damage *= 1.4
        if not isinstance(damage, int) :
            damage = int(damage)

        opponent.receive_damage(damage)
        print(
            f"{user.name} 使用 {self.name}, 对 {opponent.name} 造成 {damage} 点伤害 "
        )

        # 判断是否触发状态效果
        if random.randint(1, 100) <= self.activation_chance:
            opponent.add_status_effect(effects.ParalysisEffect())
            print(f"{opponent.name} 受到技能 {self.name} 麻痹!")
        else:
            print(f"本回合技能 {self.name} 对 {opponent.name} 的麻痹作用失败。")


class QuickAttack(Skill):
    name = "Quick Attack"
    def __init__(self, damage: int, activation_chance: int = 10) -> None:
        super().__init__(damage)
        self.activation_chance = activation_chance

    def execute(self, user: "Pokemon", opponent: "Pokemon") -> None:
        if opponent.dodge_success():
            print(f"{opponent.name} 躲开了这次攻击!")
            return

        damage = self.change_damage(user, opponent)
        opponent.receive_damage(damage)
        print(
            f"{user.name} 使用 {self.name}, 对 {opponent.name} 造成 {damage} 点伤害 "
        )

        # 判断是否触发状态效果
        if random.randint(1, 100) <= self.activation_chance:
            opponent.receive_damage(damage)
            print(f"{opponent.name} 再次受到技能 {self.name} 的攻击, 受到 {damage} 点伤害!")
        else:
            print(f"本回合技能 {self.name} 对 {opponent.name} 的二次攻击失败。")



