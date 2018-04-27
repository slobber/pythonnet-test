import clr

clr.AddReference("wpf\PresentationFramework")
from System.Windows.Markup import XamlReader
from System.Threading import Thread, ThreadStart, ApartmentState
from System.Windows import Application, Window

class MyWindow(Window):
    def __init__(self):
        xaml = '''<Window xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
            xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml">
                <Grid>
                    <Label Content="Hello XAML!" HorizontalAlignment="Center" VerticalAlignment="Center"/>
                </Grid>
            </Window>'''
        window = XamlReader.Parse(xaml)
        Application().Run(window)


if __name__ == '__main__':
    thread = Thread(ThreadStart(MyWindow))
    thread.SetApartmentState(ApartmentState.STA)
    thread.Start()
    thread.Join()
