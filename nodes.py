
from cProfile import label
from pickle import NONE
from paradox.NENV import *
widgets = import_widgets(__file__)

import flet as ft
import threading
from PySide2.QtCore import QTimer, QRunnable, Slot, Signal, QObject, QThreadPool
import sys
import time
import traceback
import flet
from flet import (
    Checkbox,
    Column,
    FloatingActionButton,
    IconButton,
    OutlinedButton,
    Page,
    Row,
    Tab,
    Tabs,
    Text,
    TextField,
    UserControl,
    colors,
    icons,
)


# BaseNode class 
class NodeBase(Node):
    version = 'v0.1'
    color = '#35f2a7'

class WorkerSignals(QObject):

    finished = Signal()
    error = Signal(tuple)
    result = Signal(object)
    progress = Signal(int)

class Worker(QRunnable):

    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()

        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

        # Add the callback to our kwargs
        self.kwargs['progress_callback'] = self.signals.progress

    @Slot()
    def run(self):
        '''
        Initialise the runner function with passed args, kwargs.
        '''

        # Retrieve args/kwargs here; and fire processing using them
        try:
            result = self.fn(*self.args, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)  # Return the result of the processing
        finally:
            self.signals.finished.emit()  # Done

class DualNodeBase(NodeBase):
    """For nodes that can be active and passive"""

    version = 'v0.1'

    def __init__(self, params, active=True):
        super().__init__(params)

        self.active = active
        if active:
            self.actions['make passive'] = {'method': self.make_passive}
        else:
            self.actions['make active'] = {'method': self.make_active}

    def make_passive(self):
        del self.actions['make passive']

        self.delete_input(0)
        self.delete_output(0)
        self.active = False

        self.actions['make active'] = {'method': self.make_active}

    def make_active(self):
        del self.actions['make active']

        self.create_input(type_='exec', insert=0)
        self.create_output(type_='exec', insert=0)
        self.active = True

        self.actions['make passive'] = {'method': self.make_passive}

    def get_state(self) -> dict:
        return {
            'active': self.active
        }

    def set_state(self, data: dict, version):
        self.active = data['active']

# layout of the application.

class StartApp_Node(NodeBase):
    title = 'Start'
    version = 'v0.1'
    main_widget_class = widgets.ButtonNode_MainWidget
    main_widget_pos = 'between ports'
    init_inputs = [
        
    ]
    init_outputs = [
        NodeOutputBP(type_='exec')
    ]
    # color = '#99dd55'

    def update_event(self, inp=-1):
        # print("Hello world")
        self.exec_output(0)


class ElevatedButton_Node(DualNodeBase):
    title = 'Elevated Button'
    version = 'v0.1'

    init_inputs = [
        NodeInputBP('page'),
    ]

    init_outputs = [
        NodeOutputBP('Button'),
        NodeOutputBP(type_='exec')
    ]

    # color = '#5d95de'

    def __init__(self, params):
        super().__init__(params, active=True)

    def place_event(self):
        self.update()

    def update_event(self, input_called=-1):
        def run(e):
            # print("hello prince")
            self.exec_output(1)

        # if self.active and inp == 0:
        button = ft.ElevatedButton("Button", on_click=run)
        page = self.input(0)
        page.update()        
        self.set_output_val(0,button)


# node for the iconButton 
class IconButton_Node(DualNodeBase):
    title = 'Icon Button'
    version = 'v0.1'

    init_inputs = [
    ]

    init_outputs = [
        NodeOutputBP('Button'),
        NodeOutputBP(type_='exec')
    ]

    # color = '#5d95de'

    def __init__(self, params):
        super().__init__(params, active=True)

    def place_event(self):
        self.update()

    def update_event(self, input_called=-1):
        def run(e):
            # print("hello prince")
            self.exec_output(1)

        # if self.active and inp == 0:
        button = ft.IconButton("Button", on_click=run)      
        self.set_output_val(0,button)


# node for the filledbutton
class FilledButton_Node(DualNodeBase):
    title = 'Filled Button'
    version = 'v0.1'

    init_inputs = [
    ]
    init_outputs = [
        NodeOutputBP('Button'),
        NodeOutputBP(type_='exec')
    ]

    # color = '#5d95de'

    def __init__(self, params):
        super().__init__(params, active=True)

    def place_event(self):
        self.update()

    def update_event(self, input_called=-1):
        def run(e):
            # print("hello prince")
            self.exec_output(1)

        # if self.active and inp == 0:
        button = ft.FilledButton("Button", on_click=run)
        self.set_output_val(0,button)

# node for the properties 
class Properties_Node(DualNodeBase):
    title = 'Properties'
    version = 'v0.1'

    style_code = {
        'select': None,
        'color': 'color',
        'bgcolor': 'bgcolor',
        'font_family':'font_family',
        'value':'value',
        'size':'size',
        'icon':'icon',
        'style':'style',
        'tooltip':'tooltip',
        'max_lines':'max_lines',
        'overflow':'overflow',
        'selectable':'selectable',
        'text_align':'text_align',
        'weight':'weight',
    }

    init_inputs = [
       NodeInputBP('style',dtype=dtypes.Choice(list(style_code.keys())[0], list(style_code.keys()))),
       NodeInputBP("value"),
    ]
    init_outputs = [
        NodeOutputBP('Value'),
    ]
    
    # color = '#5d95de'

    def __init__(self, params):
        super().__init__(params, active=True)
 
    def update_event(self, inp=-1):
        code = self.style_code[self.input(0)]
        value = self.input(1)

        style = {code:value}

        self.set_output_val(0,style)

# node for the row
class Row_Node(DualNodeBase):
    title = 'Row'
    version = 'v0.1'
    init_inputs = [
        NodeInputBP('item1'),
        NodeInputBP('item2'),
        # NodeInputBP(),
    ]
    init_outputs = [
        NodeOutputBP(),
    ]

    # color = '#5d95de'

    def __init__(self, params):
        super().__init__(params, active=True)
 
    def update_event(self, inp=-1):
        row = ft.Row(controls=[self.input(0),self.input(1)])
        self.set_output_val(0,row)

# node for the text 
class Text_Field_Node(DualNodeBase):
    title = 'TextField'
    version = 'v0.1'
    init_inputs = [
        NodeInputBP(dtype=dtypes.Data(size='m')),
    ]
    init_outputs = [
        NodeOutputBP('TextField'),
    ]

    # color = '#5d95de'

    def __init__(self, params):
        super().__init__(params, active=True)
 
    def update_event(self, inp=-1):
        text =ft.TextField(hint_text="Whats needs to be done?",value=self.input(0))
        self.set_output_val(0,text)

# node for the text 
class Text_Node(DualNodeBase):
    title = 'Text'
    version = 'v0.1'
    init_inputs = [
        NodeInputBP(dtype=dtypes.Data(size='m')),
        NodeInputBP('page'),
    ]
    init_outputs = [
        NodeOutputBP('Text'),
    ]

    # color = '#5d95de'
    mycolor = None


    def __init__(self, params):
        super().__init__(params, active=True)
 
    def update_event(self, inp=-1):
        text =ft.Text(value=self.input(0)) 
        page = self.input(1)
        page.update()             
        self.set_output_val(0,text)


# node for the text 
class Image_Node(DualNodeBase):
    title = 'Image'
    version = 'v0.1'
    init_inputs = [
        NodeInputBP('src'),
    ]
    init_outputs = [
        NodeOutputBP('Image'),
    ]

    # color = '#5d95de'

    def __init__(self, params):
        super().__init__(params, active=True)
 
    def update_event(self, inp=-1):
        image =ft.Image(src=self.input(0),width=400,height=400)
        self.set_output_val(0,image)

# node for the font style
class Font_Node(DualNodeBase):
    title = 'Font'
    input_widget_classes = {
        'choose file IW': widgets.ChooseFontInputWidget
    }
    init_inputs = [
        NodeInputBP(add_data={'widget name': 'choose file IW'})
    ]
    init_outputs = [
        NodeOutputBP('color')
    ]

    # color = '#5d95de'

    def __init__(self, params):
        super().__init__(params)

        self.image_filepath = ''

    def view_place_event(self):
        self.input_widget(0).path_chosen.connect(self.path_chosen)
        # self.main_widget_message.connect(self.main_widget().show_path)

    def update_event(self, inp=-1):
        if self.image_filepath == '':
            return

        try:
            self.set_output_val(0, (self.image_filepath))
        except Exception as e:
            print(e)

    def get_state(self):
        data = {'image file path': self.image_filepath}
        return data

    def set_state(self, data, version):
        self.path_chosen(data['csv file path'])
        # self.image_filepath = data['image file path']

    def path_chosen(self, file_path):
        self.image_filepath = file_path
        self.update()

# node for the color selection        
class Color_Node(DualNodeBase):
    title = 'Color'
    input_widget_classes = {
        'choose file IW': widgets.ChooseColorInputWidget
    }
    init_inputs = [
        NodeInputBP(add_data={'widget name': 'choose file IW'})
    ]
    init_outputs = [
        NodeOutputBP('color')
    ]

    # color = '#5d95de'

    def __init__(self, params):
        super().__init__(params)

        self.image_filepath = ''

    def view_place_event(self):
        self.input_widget(0).path_chosen.connect(self.path_chosen)
        # self.main_widget_message.connect(self.main_widget().show_path)

    def update_event(self, inp=-1):
        if self.image_filepath == '':
            return

        try:
            self.set_output_val(0, (self.image_filepath))
        except Exception as e:
            print(e)

    def get_state(self):
        data = {'image file path': self.image_filepath}
        return data

    def set_state(self, data, version):
        self.path_chosen(data['csv file path'])
        # self.image_filepath = data['image file path']

    def path_chosen(self, file_path):
        self.image_filepath = file_path
        self.update()
# node for the home page
class App_Node(DualNodeBase):
    title = 'App'
    version = 'v0.1'
    init_inputs = [
        NodeInputBP(type_='exec'),
        # NodeInputBP('widgets'),
    ]
    
    init_outputs = [
        NodeOutputBP(type_='exec'),
        NodeOutputBP('Page'),
    ]

    # color = '#5d95de'

    def __init__(self, params):
        super().__init__(params, active=True)


    def update_event(self, inp=-1):
    
        if self.active and inp == 0:
            # runing the main app
            def main(page: ft.Page):
                # code = self.input(2)


                # if self.input(0) is not None:

                # for key, value in code.items():
                #         # condition switcher
                #     if key == "color":
                #         page.color = value
                #     elif key == "bgcolor":
                #         page.bgcolor = value
                #     elif key == "width":
                #         page.width = value
                #     elif key == "height":
                #         page.height = value
                #     elif key == "fonts":
                #         page.fonts = value
                #     elif key == "overlay":      
                #         page.overlay = value
                #     elif key == "padding":
                #         page.padding = value                   
                #     elif key == "platform":
                #         page.platform = value
                #     elif key == "rtl":
                #         page.rtl = value 
                #     elif key == "title":
                #         page.title = value
                #     elif key == 'theme_mode':
                #         page.theme_mode = value           
                #     else:
                #         pass
                page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
                # input1 = self.input(1)
          
                # if input1 is not None:
                # page.add(input1)

                page.update()
                                    
                self.set_output_val(1,page)

                self.exec_output(0)

            # calling the main function.
            ft.app(target=main)

        # checking the function for it's state
        elif not self.active:
            print(self.input(0))

class Home_Page_Node(DualNodeBase):
    title = 'HomePage'
    version = 'v0.1'
    init_inputs = [
      NodeInputBP(type_="exec"),
      NodeInputBP('Page'),
      NodeInputBP('Widgets'),

    ]
    init_outputs = [
        NodeOutputBP('properties'),
    ]

    # color = '#5d95de'

    def __init__(self, params):
        super().__init__(params, active=True)
 
    def update_event(self, inp=-1):
        page =  self.input(1)
        widget = self.input(2)
        page.add(widget)
        page.update()


# export the nodes...
export_nodes(
    # register the nodes in the extension
    App_Node,
    StartApp_Node,
    Text_Node,
    Image_Node,
    Text_Field_Node,
    ElevatedButton_Node,
    IconButton_Node,
    FilledButton_Node,
    Color_Node,
    Font_Node,
    Row_Node,
    Properties_Node,
    Home_Page_Node,
  
)