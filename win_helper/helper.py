import clr
import sys

clr.AddReference("wpf\PresentationFramework")
from System.IO import StreamReader
from System.Windows.Markup import XamlReader
from System.Threading import Thread, ThreadStart, ApartmentState, ParameterizedThreadStart
from System.Windows import Application, Window, WindowState


class PythonWin(Window):
    def __init__(self):
        self.window = None
        self.controls = None

    emptyWindowXaml = '''<Window xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
    xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml">
        <Grid>
            <Label Content="这是一个窗口" HorizontalAlignment="Center" VerticalAlignment="Center"/>
        </Grid>
    </Window>'''

    @classmethod
    def _thread(cls, xaml=None):
        app = cls()
        app._load(xaml)

        Application().Run(app.window)

    def _load(self, xaml=None):
        '''创建一个 Xaml 窗口程序

        :param xaml: xaml 文件路径或者 xaml 格式的 xml 字符串
        '''
        window = None
        if not xaml:
            xaml = PythonWin.emptyWindowXaml

        if xaml.startswith('<Window xmlns'):
            window = XamlReader.Parse(xaml)
        else:
            stream = StreamReader(xaml)
            window = XamlReader.Load(stream.BaseStream)
        self.window = window
        self.controls = {'All': {}}
        self._get_windows_controls(window)
        self.auto_bind_events()

        invert_op = getattr(self, "load", None)
        if callable(invert_op):
            getattr(self, 'load')()


    @classmethod
    def run(cls, xaml=None):
        '''调用 run 函数启动窗口程序

        :param xaml: xaml 文件路径或者 xaml 格式的 xml 字符串
        '''
        thread = Thread(ParameterizedThreadStart(cls._thread))
        thread.SetApartmentState(ApartmentState.STA)
        thread.Start(xaml)
        thread.Join()

    def auto_bind_events(self):
        '''按照约定命名方法可以自动将方法绑定到事件上

        命名规则：
        对象名称_事件名称_handler(self, 事件发生对象, 事件对象)
        对象名称区分大小写，按照 xaml 中的组件 Name 来设置对象名称
        事件名称区分大小写，按照文档选择相应的事件
        '''
        method_list = [func for func in dir(self) if callable(getattr(self, func)) and func.lower().endswith('_handler')]
        for method in method_list:
            try:
                name, event, _ = method.split('_')
                if name in self.controls['All']:
                    event_handler = getattr(self.controls['All'][name], event)
                    event_handler += getattr(self, method)
            except Exception as e:
                pass

    def _get_windows_controls(self, control):
        s = str(control.__class__)
        if s == "<class 'System.Windows.Window'>":
            self.controls['All']['Window'] = control
        elif "System.Windows.Controls." in s and hasattr(control, "Name") and len(control.Name) > 0:
            control_type = s[s.find("'") + 1: s.rfind("'")]
            control_type = control_type[control_type.rfind('.') + 1:]
            if control_type not in self.controls:
                self.controls[control_type] = {}
            self.controls[control_type][control.Name] = control
            self.controls['All'][control.Name] = control

        if hasattr(control, "Children"):
            for cc in control.Children:
                self._get_windows_controls(cc)
        elif hasattr(control, "Child"):
            self._get_windows_controls(control.Child)
        elif hasattr(control, "Content") and type(control.Content) != str:
            self._get_windows_controls(control.Content)
