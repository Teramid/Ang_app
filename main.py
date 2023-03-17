from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.textinput import TextInput
from kivy.config import Config
from kivy.core.window import Window
from kivy.properties import StringProperty
from kivy.clock import Clock
import ShortFun
import numpy as np
import os
from random import randint, choice, random

from main_beta import Full_Answer

Window.size = (450, 800)
Config.set("graphics", "resizable", False)


def download_verb_list():
    pass


def check_path_base():
    level_verbs = ["A", "B", "C"]
    for level in level_verbs:
        if os.path.exists(f"baza/nieregularne/{level}") and os.path.isdir(
            f"baza/nieregularne/{level}"
        ):
            pass
        else:
            download_verb_list()


def make_verb_base(repeat=3, level="A", size=10):
    files = [x + 1 for x in range(len(os.listdir(f"baza/nieregularne/{level}")))]
    Files_Number = len(files)
    random_list = []
    size = Files_Number if size > Files_Number else size
    while len(random_list) < size:
        x = choice(files)
        random_list.append(x)
        files.remove(x)
    ir.Dict = {}
    ir.Dict_Repeat = {}
    for i in random_list:
        file_name = f"baza/nieregularne/{level}/{str(i).zfill(3)}.txt"
        with open(file_name, "r") as f:
            f = f.readlines()
            if len(f[3].split(", ")) > 3:
                list = f[3].split(", ")
                list[3] = "\n" + list[3]
                f[3] = ", ".join(verb for verb in list)
            ir.Dict.update({i: [f[0].rstrip(), f[1].rstrip(), f[2].rstrip(), f[3]]})
        ir.Dict_Repeat.update({i: repeat})
    return ir.Dict, ir.Dict_Repeat


# print(make_verb_base())


def random_verb(dictNumber, last_File):
    while True:
        ir.choose_File = choice(list(dictNumber.keys()))
        if dictNumber.get(ir.choose_File) == 0:
            continue
        else:
            if ir.choose_File == last_File and len(dictNumber) > 1:
                continue
            else:
                break


class Irregular(Screen):
    Full_Answer = 0
    Size_Dict = 0

    def initialization(self):
        random_verb(self.Dict_Repeat, 0)
        self.ids.quest_0.text = self.Dict[self.choose_File][3]
        self.ids.full_correct_answer.text = f"{self.Full_Answer} / {self.Size_Dict}"
        self.ids.repeat_quest.text = str(self.Dict_Repeat.get(self.choose_File))

    def set_focus_text_quest_1(self, dt):
        self.ids.text_quest_1.focus = True

    def __init__(self, **kw):
        make_verb_base()
        # self.initialization()
        super(Irregular, self).__init__(**kw)

    def handle_keypress(self, window, keycode, *args):
        if isinstance(keycode, int) and keycode == 13:
            self.right_button_down()

    def on_pre_enter(self, *args):
        make_verb_base(irr_m.repeat, irr_m.lvl, irr_m.size_base)
        ir.Size_Dict = len(self.Dict)
        self.ids.size_base.text = str(self.Size_Dict)
        self.ids.right_button.background_normal = "icons/accept_icon.png"
        ir.Full_Answer = 0
        self.normal_state()
        self.initialization()
        Clock.schedule_once(self.set_focus_text_quest_1, 0.2)
        Window.bind(on_key_down=self.handle_keypress)

    def right_button_down(self):
        if self.ids.right_button.background_normal == "icons/accept_icon.png":
            self.accept_icon()
            self.ids.right_button.background_normal = "icons/next_icon.png"
        else:
            if ir.Full_Answer == self.Size_Dict:
                sm.remove_widget(Irregular())
                Window.unbind(on_key_down=self.handle_keypress)
                sm.current = "finish_irr"
            else:
                self.ids.right_button.background_normal = "icons/accept_icon.png"
                self.next_icon()
                Clock.schedule_once(self.set_focus_text_quest_1, 0.2)

    def check_answers(self, Answer):
        Correct = []
        for i, ans in enumerate(Answer):
            if (
                ans.strip() in self.Dict[self.choose_File][i].split(", ")
                or ans.strip() in self.Dict[self.choose_File][i].split()
                or ans.strip() == self.Dict[self.choose_File][i]
            ):
                Correct.append(True)
            else:
                Correct.append(False)
        x = self.Dict_Repeat.get(self.choose_File)
        x = x - 1 if False not in Correct else x + 1
        if x == 0:
            ir.Dict_Repeat.pop(self.choose_File)
            ir.Dict.pop(self.choose_File)
            ir.Full_Answer += 1
        else:
            ir.Dict_Repeat.update({self.choose_File: x})

        for i, bool in enumerate(Correct):
            self.ids[f"text_quest_{i+1}"].disabled = True
            self.ids[f"check_answer_{i+1}"].opacity = 1
            if bool:
                self.ids[f"check_answer_{i+1}"].text = "Correct"
                self.ids[f"check_answer_{i+1}"].color = (0, 0.7, 0, 1)
            else:
                self.ids[
                    f"check_answer_{i+1}"
                ].text = f'Should be "{self.Dict[self.choose_File][i]}"'
                self.ids[f"check_answer_{i+1}"].color = (0.7, 0, 0, 1)
        return Correct

    def accept_icon(self):
        self.check_answers(
            [
                self.ids.text_quest_1.text.lower(),
                self.ids.text_quest_2.text.lower(),
                self.ids.text_quest_3.text.lower(),
            ]
        )
        self.ids.repeat_quest.text = str(self.Dict_Repeat.get(self.choose_File))
        self.ids.full_correct_answer.text = f"{self.Full_Answer} / {self.Size_Dict}"

    def normal_state(self):
        for i in range(1, 4):
            self.ids[f"text_quest_{i}"].text = ""
            self.ids[f"check_answer_{i}"].opacity = 0
            self.ids[f"check_answer_{i}"].color = (1, 1, 1, 1)
            self.ids[f"text_quest_{i}"].disabled = False

    def next_icon(self):
        self.normal_state()
        random_verb(self.Dict_Repeat, self.choose_File)
        self.ids.quest_0.text = self.Dict[self.choose_File][3]
        self.ids.repeat_quest.text = str(self.Dict_Repeat.get(self.choose_File))

    def back_button_down(self):
        sm.remove_widget(Irregular())
        Window.unbind(on_key_down=self.handle_keypress)
        sm.current = "menu"


ir = Irregular


class Finish_Window(Screen):
    def button_play_again(self):
        self.parent.remove_widget(Finish_Window())
        sm.current = "irregular"

    def button_change_level(self):
        sm.current = "irr_menu"

    def button_back_to_menu(self):
        self.parent.remove_widget(Finish_Window())
        sm.current = "menu"


class Irregular_Menu(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)

    def on_pre_enter(self, *args):
        self.ids.text_repeat.text = str(3)
        self.ids.text_size_dict.text = str(10)

    def button_A_down(self):
        sm.remove_widget(Irregular_Menu())
        irr_m.repeat = int(self.ids.text_repeat.text)
        irr_m.size_base = int(self.ids.text_size_dict.text)
        irr_m.lvl = "A"
        sm.current = "irregular"

    def button_B_down(self):
        sm.remove_widget(Irregular_Menu())
        irr_m.repeat = int(self.ids.text_repeat.text)
        irr_m.size_base = int(self.ids.text_size_dict.text)
        irr_m.lvl = "B"
        sm.current = "irregular"

    def button_C_down(self):
        sm.remove_widget(Irregular_Menu())
        irr_m.repeat = int(self.ids.text_repeat.text)
        irr_m.size_base = int(self.ids.text_size_dict.text)
        irr_m.lvl = "C"
        sm.current = "irregular"

    def back_button_down_irr(self):
        self.parent.remove_widget(Irregular_Menu())
        sm.current = "menu"


irr_m = Irregular_Menu


class Menu(Screen):
    def button_1_down(self):
        sm.remove_widget(Menu())
        sm.current = "irr_menu"
        pass

    def button_2_down(self):
        print("button2")

    def button_3_down(self):
        print("button3")


class MenuApp(App):
    global sm
    sm = ScreenManager()

    def build(self):
        sm.add_widget(Menu(name="menu"))
        sm.add_widget(Irregular_Menu(name="irr_menu"))
        sm.add_widget(Irregular(name="irregular"))
        sm.add_widget(Finish_Window(name="finish_irr"))
        return sm


if __name__ == "__main__":
    MenuApp().run()
