import clr
import sys

clr.AddReference("wpf\PresentationFramework")
from System.IO import StreamReader
from System.Windows.Markup import XamlReader
from System.Threading import Thread, ThreadStart, ApartmentState
from System.Windows import Application, Window
from .helper import *
