import math
from enum import Enum
from win_helper import *


class Operator(Enum):
    """用来标记上一次的运算符
    """
    Empty = 0
    Add = '+'
    Subtract = '-'
    Multiply = '*'
    Divide = '/'
    Clear = -1


def pretty_str(num):
    """对小数转换字符串增加一个修饰，删除“.0”，让小数看上去是整数

    :param num: 一个小数
    :return: 一个格式化好的字符串
    """
    s = str(num)
    if s[-2:] == '.0':
        s = s[:-2]
    return s


class MyWindow(PythonWin):
    def __init__(self):
        """初始化函数，设置类成员变量
        """
        self.last_operator = Operator.Empty
        self.result = 0
        self.entry = None
        self.info = None
        self.memory = None
        self.memory_value = 0

    def load(self):
        """对类实例中的变量赋值，并添加自定义的事件绑定
        """
        self.last_operator = Operator.Empty
        self.result = 0
        self.entry = self.controls['TextBox']['Entry']
        self.entry.Text = '0'
        self.info = self.controls['TextBlock']['Info']
        self.memory = self.controls['TextBlock']['Memory']
        self.memory_value = 0
        self.window.SizeChanged += self.change_font_size
        for key, control in self.controls['Button'].items():
            if key[:6] == 'Number':
                control.Click += self.insert_number
            if key[:9] == 'Calculate':
                control.Click += self.calculate
            if key[:6] == 'Memory':
                control.Click += self.memory_control
            if key[:4] == 'Edit':
                control.Click += self.edit_entry

    def change_font_size(self, o, e):
        """当窗口调整时，使按钮文字自适应
        """
        controlsize = self.window.Height / 20.0 if self.window.Height >= 300 else 12.0
        Application.Current.Resources.Remove('ControlFontSize')
        Application.Current.Resources.Add('ControlFontSize', controlsize)

    def edit_entry(self, o, e):
        """编辑按钮的响应
        """
        edit_str = o.Name[4:]
        if edit_str == 'DeleteLast':
            if len(self.entry.Text) > 0 and self.entry.Text[-1] == '.':
                self.entry.Text = self.entry.Text[:-1]
            if len(self.entry.Text) > 0:
                self.entry.Text = self.entry.Text[:-1]
            if len(self.entry.Text) > 0 and self.entry.Text[-1] == '.':
                self.entry.Text = self.entry.Text[:-1]
            if self.entry.Text == '':
                self.entry.Text = '0'
        elif edit_str == 'ClearEntry':
            self.entry.Text = '0'
        elif edit_str == 'ClearAll':
            self.last_operator = Operator.Empty
            self.entry.Text = '0'
            self.info.Text = ''
            self.result = 0

    def memory_control(self, o, e):
        """记忆按钮的响应
        """
        mem_str = o.Name[6:]
        if mem_str == 'Clear':
            self.memory.Text = ''
            self.memory_value = 0
        elif mem_str == 'Recall':
            if self.memory.Text == '':
                return
            self.entry.Text = pretty_str(self.memory_value)
        elif mem_str == 'Save':
            self.last_operator = Operator.Clear
            self.memory_value = float(self.entry.Text)
            if self.memory_value != 0:
                self.memory.Text = 'M'
            else:
                self.memory.Text = ''
        elif mem_str == 'Add':
            self.last_operator = Operator.Clear
            self.memory_value += float(self.entry.Text)
            if self.memory_value != 0:
                self.memory.Text = 'M'
            else:
                self.memory.Text = ''
        elif mem_str == 'Subtract':
            self.last_operator = Operator.Clear
            self.memory_value -= float(self.entry.Text)
            if self.memory_value != 0:
                self.memory.Text = 'M'
            else:
                self.memory.Text = ''

    def insert_number(self, o, e):
        """数字按钮的响应
        """
        if o.Name == 'NumberZero':
            if self.last_operator == Operator.Clear:
                self.entry.Text = '0'
                self.last_operator = Operator.Empty
            if self.entry.Text != '0':
                self.entry.Text += o.Content.Text
        elif o.Name == 'DecimalDot':
            if self.last_operator == Operator.Clear:
                self.entry.Text = '0'
            self.entry.Text += '.'
        elif self.entry.Text == '0':
            self.entry.Text = o.Content.Text
        else:
            self.entry.Text += o.Content.Text

    def calculate(self, o, e):
        """运算符按钮的响应
        """
        ope_str = o.Name[9:]
        if ope_str in ('Add', 'Subtract', 'Multiply', 'Divide'):
            if self.last_operator != Operator.Clear and self.last_operator != Operator.Empty:
                self.calculate_result(o)
            self.last_operator = Operator[ope_str]
            self.result = float(self.entry.Text)
            self.entry.Text = '0'
            self.info.Text = pretty_str(self.result) + ' ' + Operator[ope_str].value + ' '
        elif ope_str == 'Negative':
            self.result = -float(self.entry.Text)
            self.entry.Text = pretty_str(self.result)
        elif ope_str == 'Reciprocal':
            temp = float(self.entry.Text)
            if temp != 0:
                temp = 1.0 / temp
            self.entry.Text = pretty_str(temp)
            self.last_operator = Operator.Clear
        elif ope_str == 'Sqrt':
            temp = float(self.entry.Text)
            self.entry.Text = pretty_str(math.sqrt(temp))
            self.last_operator = Operator.Clear
        elif ope_str == 'Square':
            temp = float(self.entry.Text)
            self.entry.Text = pretty_str(temp * temp)
            self.last_operator = Operator.Clear
        elif ope_str == 'Result':
            self.calculate_result(o)

    def calculate_result(self, o):
        """计算结果
        """
        temp = self.result
        self.result = float(self.entry.Text)
        if self.last_operator == Operator.Add:
            self.entry.Text = pretty_str(temp + self.result)
            self.last_operator = Operator.Clear
        elif self.last_operator == Operator.Subtract:
            self.entry.Text = pretty_str(temp - self.result)
            self.last_operator = Operator.Clear
        elif self.last_operator == Operator.Multiply:
            self.entry.Text = pretty_str(temp * self.result)
            self.last_operator = Operator.Clear
        elif self.last_operator == Operator.Divide:
            self.entry.Text = pretty_str(temp / self.result)
            self.last_operator = Operator.Clear

        if self.last_operator == Operator.Clear:
            self.info.Text = ''


if __name__ == '__main__':
    MyWindow.run('calc.xaml')
