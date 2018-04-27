from win_helper import *
import math


class MyWindow(PythonWin):
    def __init__(self):
        self.i = 0

    def Window_SizeChanged_handler(self, obj, event):
        """监听窗口尺寸变化
        """
        label = self.controls['All']['Label1']
        if obj.WindowState == WindowState.Maximized:
            label.Content = '窗口最大化了'
        elif not math.isnan(obj.Width):
            label.Content = '窗口大小：{}x{}\n窗口位置：{}, {}'.format(obj.Width, obj.Height, obj.Top, obj.Left)

    def Label1_MouseUp_handler(self, obj, event):
        """监听 Label1 上鼠标抬起事件
        """
        self.i += 1
        obj.Content = '点击了 {} 次'.format(self.i)

if __name__ == '__main__':
    MyWindow.run('resize_window.xaml')
