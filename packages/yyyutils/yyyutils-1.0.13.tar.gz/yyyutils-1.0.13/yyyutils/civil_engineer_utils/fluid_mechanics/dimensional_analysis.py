from sympy.core.mul import Mul
from sympy import *
from sympy.physics.units import Quantity, meter, kg, second
import dataclasses
import json
from sympy.physics.units import Dimension
from yyyutils.json_utils import JSONUtils
import re
from yyyutils.regex_utils import RegexUtils


class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Mul):
            return {'Mul': str(obj)}
        if isinstance(obj, Quantity):
            return str(obj)
        return super().default(obj)


@dataclasses.dataclass
class PhysicalQuantity:
    d: Quantity = Quantity('L', meter)  # 长度
    m: Quantity = Quantity('M', kg)  # 质量
    t: Quantity = Quantity('T', second)  # 时间
    v: Quantity = d / t  # 速度
    a: Quantity = v / t  # 加速度
    density: Quantity = m / (d ** 3)  # 密度
    F: Quantity = m * a  # 力
    p: Quantity = m / (d * t ** 2)  # 压强
    g: Quantity = a  # 重力加速度
    W: Quantity = m * g
    A: Quantity = d ** 2  # 面积

    @classmethod
    def from_dict(cls, data):
        """从字典构建 PhysicalQuantity 实例."""
        instance = cls()
        for key, value in data.items():
            setattr(instance, key, eval(value, {'L': instance.d, 'T': instance.t, 'M': instance.m}))
        return instance

    def get_attr_key(self, attr_value):
        """
        实现get_attr_key(d)的结果为'd'
        :return:
        """
        for key, value in self.__dict__.items():
            if value == attr_value:
                return key
        return None

    def generate_name_dict(self):
        """生成实例里面所有物理量的名称映射比如 d -> d(字符串)."""
        name_dict = {}
        for name in self.__dict__.keys():
            name_dict[name] = str(name)
        return name_dict

    def display_quantities(self):
        """输出所有物理量及其值."""
        for name, quantity in self.__dict__.items():
            print(f"{name}: {quantity}")

    def query_quantity(self, name):
        """查询某物理量的值."""
        if hasattr(self, name):
            return '查询到物理量<' + name + '> : ' + str(getattr(self, name))
        else:
            print(f"物理量 '{name}' 不存在。")
            return None


class DimensionalAnalysisUtils:
    def __init__(self):
        self.quantities = {}

    def save_quantity_to_file(self, name, expression, file_path='quantities.json'):
        """
        保存物理量到文件
        :param name: 物理量名称
        :param expression: 物理量表达式，使用 PhysicalQuantity 实例中已有的物理量表示
        :param file_path:
        :return:
        """
        # 如果name字符串的第一个字符是数字，则自动加上一个下划线
        if name[0].isdigit():
            print(f"警告：物理量名称不能以数字开头，将以 {'_' + name} 作为名称保存。")
            name = '_' + name
        self.quantities[name] = str(expression)
        self.__save_quantities_to_file(file_path)

    def __save_quantities_to_file(self, filename='quantities.json'):
        """将物理量保存到文本文件."""
        with open(filename, 'a', encoding='utf-8') as file:
            json_utils = JSONUtils(file_path=filename, cls=CustomEncoder)
            json_utils.update_json(self.quantities)

    def create_physical_quantity_from_file(self, filename='quantities.json'):
        """从文件创建 PhysicalQuantity 实例."""
        try:
            with open(filename, 'r') as file:
                data = json.load(file)
                basic_quantities = PhysicalQuantity.from_dict(data)
                return basic_quantities
        except FileNotFoundError:
            print("文件未找到，无法创建 PhysicalQuantity 实例。")
            return None

    def create_basic_quantities(self):
        """创建基础物理量."""
        basic_quantities = PhysicalQuantity()
        return basic_quantities

    def get_quantity_dimension(self, name, expression, save_to_file=False):
        """
        传入物理量名称以及使用基础物理量的表达式，获取某物理量的量纲
        :param name: 物理量名称
        :param expression: 物理量的表达式 (Quantity 对象)
        :param save_to_file: 是否保存物理量到字典
        :return: 量纲
        """
        if save_to_file:
            # 保存原始表达式的字符串形式
            self.save_quantity_to_file(name, expression)

        # 计算量纲并格式化为字符串形式
        return name + ': ' + str(Dimension(expression))

    def delete_quantity_from_file(self, name, file_path='quantities.json'):
        """
        从文件中删除物理量
        :param name: 物理量名称
        :param file_path: 文件路径
        :return:
        """
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
                if name in data:
                    del data[name]
                    with open(file_path, 'w', encoding='utf-8') as file:
                        json.dump(data, file, indent=4, ensure_ascii=False)
                    print(f"物理量 '{name}' 删除成功。")
                else:
                    print(f"物理量 '{name}' 不存在。")
        except FileNotFoundError:
            print(f"文件 '{file_path}' 不存在。")

    def clear_quantities_from_file(self, file_path='quantities.json'):
        """
        清空文件中的物理量
        :param file_path: 文件路径
        :return:
        """
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump({}, file, indent=4, ensure_ascii=False)
            print(f"文件 '{file_path}' 中的物理量已清空。")
        except FileNotFoundError:
            print(f"文件 '{file_path}' 不存在。")

    def judge_formula_dimension(self, left_side, right_side):
        """
        判断公式的左右两边的量纲是否一致
        :param left_side:
        :param right_side:
        :return:
        """
        left_dimension = Dimension(left_side)
        right_dimension = Dimension(right_side)
        print(f"左边的量纲: {left_dimension}")
        print(f"右边的量纲: {right_dimension}")
        if left_dimension == right_dimension:
            return True
        else:
            return False

    def parse_dimension(self, dimension: Dimension):
        """
        解析量纲对象的字符串表示，提取基量纲和对应的指数
        :param dimension: Dimension 对象
        :return: 一个字典，其中包含基量纲和对应的指数
        """
        dimension_str = str(dimension)
        return RegexUtils.extract_exponents(dimension_str)

    def derivation_formula(self, target_physical_quantity_dict, related_physical_quantities_dict):
        """
        利用Rayleigh推导物理量之间的关系式
        :param target_physical_quantity: 目标物理量字典，{物理量名称: PhysicalQuantity.属性}，只能有一个
        :param related_physical_quantity: 相关物理量字典，{物理量1名称: PhysicalQuantity.属性1, 物理量2名称: PhysicalQuantity.属性2}
        :return:
        """
        # 获取目标物理量的量纲
        if len(target_physical_quantity_dict) != 1:
            print("目标物理量字典只能有一个物理量。")
            return None
        target_name = list(target_physical_quantity_dict.keys())[0]
        print(f"目标物理量为: {target_name}")
        print(f"相关物理量为: {[name for name, dimension in related_physical_quantities_dict.items()]}")
        target_quantity = list(target_physical_quantity_dict.values())[0]
        target_dimension = Dimension(target_quantity)
        # 初始化一个字典来存储相关物理量和它们的指数并设置相关物理量的量纲
        exponents = {}
        related_dimensions = []
        for name, quantity in related_physical_quantities_dict.items():
            exponents[name] = 1
            related_dimensions.append(Dimension(quantity))

        target_base_units = self.parse_dimension(target_dimension)
        related_base_units = {}
        for name, dimension in related_physical_quantities_dict.items():
            res = self.parse_dimension(dimension)
            for base_unit in ['L', 'M', 'T']:
                if base_unit not in res:
                    res[base_unit] = 0
            related_base_units[name] = res

        # print(f"目标物理量的量纲: {target_base_units}")
        # 判断target_base_units里面是否是L、M、T三个基量纲，缺少的补充为0
        for base_unit in ['L', 'M', 'T']:
            if base_unit not in target_base_units:
                target_base_units[base_unit] = 0

        # 通过建立方程来解指数
        from sympy import symbols, Eq, solve

        symbols_dict = {name: symbols(name) for name in related_physical_quantities_dict.keys()}
        T, M, L = symbols('T M L')
        new_related_base_units = {}
        for name, unit in related_base_units.items():
            new_related_base_units[name] = {unit_name: exponent * symbols_dict[name] for unit_name, exponent in
                                            unit.items()}
        # print(symbols_dict)
        # print(new_related_base_units)
        # 建立方程的右边
        rhs_T_exp = 0
        rhs_M_exp = 0
        rhs_L_exp = 0
        for name, unit in new_related_base_units.items():
            rhs_T_exp += unit['T']
            rhs_M_exp += unit['M']
            rhs_L_exp += unit['L']
        # 建立方程的左边
        lhs_T_exp = target_base_units['T']
        lhs_M_exp = target_base_units['M']
        lhs_L_exp = target_base_units['L']
        eqs = [Eq(lhs_T_exp, rhs_T_exp), Eq(lhs_M_exp, rhs_M_exp), Eq(lhs_L_exp, rhs_L_exp)]
        # print(f"lhs_T_exp: {lhs_T_exp}, lhs_M_exp: {lhs_M_exp}, lhs_L_exp: {lhs_L_exp}")
        # print(f"rhs_T_exp: {rhs_T_exp}, rhs_M_exp: {rhs_M_exp}, rhs_L_exp: {rhs_L_exp}")
        # 解方程
        solution = solve(eqs, list(symbols_dict.values()))
        print(f"相关物理量及其指数为: {solution}")
        formula = ''
        for name, exp in solution.items():
            formula += f"{name}^{exp} * "
        formula = target_name + ' = ' + 'K * (' + (formula)[:-3] + ')'
        return formula

    def combine_dimensionless_quantities(self, quantities_dict):
        """
        把多个物理量进行组合成为无量纲量
        :param quantities_dict:
        :return:
        """
        quantities_name = list(quantities_dict.keys())
        print(f"待组合的物理量为{quantities_name}")
        symbol_dict = {name: symbols(name) for name in quantities_name}
        formula = ''
        quantities_unit = {}
        for name, dimension in quantities_dict.items():
            unit = self.parse_dimension(Dimension(dimension))
            for base_unit in ['L', 'M', 'T']:
                if base_unit not in unit:
                    unit[base_unit] = 0
            quantities_unit[name] = unit
        # 建立方程的右边
        rhs_T_exp = 0
        rhs_M_exp = 0
        rhs_L_exp = 0
        for name, unit in quantities_unit.items():
            rhs_T_exp += unit['T'] * symbol_dict[name]
            rhs_M_exp += unit['M'] * symbol_dict[name]
            rhs_L_exp += unit['L'] * symbol_dict[name]
        # 建立方程的左边
        lhs_T_exp = 0
        lhs_M_exp = 0
        lhs_L_exp = 0
        eqs = [Eq(lhs_T_exp, rhs_T_exp), Eq(lhs_M_exp, rhs_M_exp), Eq(lhs_L_exp, rhs_L_exp)]
        # 解方程
        solution = solve(eqs, list(symbol_dict.values()))
        loss_key = list(set(symbol_dict.values()) - set(solution.keys()))
        replace_dict = {}
        var_name = 'abcdefghijklmnopqrstuvwxyz'
        extend_solution = {}
        for i in range(len(loss_key)):
            extend_solution[loss_key[i]] = var_name[i]
            replace_dict[str(loss_key[i])] = var_name[i]
        print(f"相关物理量及其指数为: {solution}")
        for name, exp in solution.items():
            formula += f"{name}^{exp} * "

        for key, value in replace_dict.items():
            if key in formula:
                formula = formula.replace(key, value)

        for name, exp in extend_solution.items():
            formula = formula + f"{name}^{exp} * "
        formula = formula[:-3]

        return '无量纲量的组合为: ' + formula


# 使用示例
utils = DimensionalAnalysisUtils()
basic_quantities = utils.create_physical_quantity_from_file()
# utils.clear_quantities_from_file()
print(utils.derivation_formula({'s': basic_quantities.d},
                               {'W': basic_quantities.W,
                                'g': basic_quantities.g, 't': basic_quantities.t}))
utils.save_quantity_to_file('tao', basic_quantities.F / basic_quantities.A)
print(utils.combine_dimensionless_quantities(
    {'t': basic_quantities.tao, 'p': basic_quantities.density, 'v': basic_quantities.v}))
