import os
from msilib.schema import Directory
from random import choice, randint, random
from tkinter import Label

from kivy.app import App
from kivy.clock import Clock
from kivy.config import Config
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen, ScreenManager, SlideTransition
from kivy.uix.textinput import TextInput
from numpy import isin

import ShortFun

Window.size = (450, 800)
# Window.size = (1080, 1920)
Config.set("graphics", "resizable", False)


def download_verb_list():
    import git

    if not os.path.exists(f"baza"):
        os.makedirs(f"baza")
    else:
        pass
    git_url = "https://github.com/Teramid/Baza.git"
    repo_dir = "baza"
    git.Repo.clone_from(git_url, repo_dir)


# checking path and base exist, if not download
def check_path_base():
    level_verbs = ["A", "B", "C"]
    for level in level_verbs:
        if os.path.exists(f"baza/nieregularne/{level}") and os.path.isdir(
            f"baza/nieregularne/{level}"
        ):
            pass
        else:
            download_verb_list()


# Create verbs resource to learn with the selected repetition, level and size
def make_verbs_resource(repeat=3, level="A", size=10):
    check_path_base()
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
        make_verbs_resource()
        super(Irregular, self).__init__(**kw)

    def handle_keypress(self, window, keycode, *args):
        if isinstance(keycode, int) and keycode == 13:
            self.right_button_down()

    def on_pre_enter(self, *args):
        make_verbs_resource(irr_m.repeat, irr_m.lvl, irr_m.size_base)
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


class Dict_menu(Screen):
    def chosen_dict(self, instance):
        Dict_menu.chos = " ".join(x for x in instance.text.split()[:-2])
        if self.button == "diction":
            sm.current = "dict_quiz"
        else:
            print("to drugie")

    def initit_dicts_list(self):
        directory = "baza\Dictionary"
        if os.path.exists(directory) and os.path.isdir(directory):
            pass
        else:
            os.makedirs(directory)
        # Add dynamic buttons to the button_layout
        files = os.listdir(directory)
        dicts = {}
        if len(files) == 0:
            empty_label = Button(
                text=f"Brak dostępnych zasobów\nUtwórz nową bazę",
                font_size=20,
                size_hint=(1, None),
                height=100,
                halign="center",
                valign="middle",
            )
            self.ids.scroll_menu_dict.add_widget(empty_label)
        else:
            for file in files:
                with open(f"{directory}/{file}", "r") as f:
                    count_line = sum(1 for line in f)
                dicts.update({file: count_line})
            for key, value in dicts.items():
                if value == 1:
                    value = f"{value} słowo"
                elif value in (2, 3, 4):
                    value = f"{value} słowa"
                else:
                    value = f"{value} słów"
                boxdict = BoxLayout(
                    orientation="horizontal",
                    spacing=3,
                    padding=3,
                    size_hint=(1, None),
                    height=40,
                )
                button = Button(
                    text=f"{key[:-4]} ({value})",
                    font_size=20,
                    on_release=self.chosen_dict,
                    size_hint=(0.9, None),
                    height=40,
                )
                edit_button = Button(
                    background_normal="icons\edit_icon.png",
                    on_release=self.edit_button_down,
                    size_hint=(None, None),
                    height=40,
                    width=40,
                )
                remove_button = Button(
                    background_normal="icons\delete_icon.png",
                    size_hint=(None, None),
                    height=40,
                    width=30,
                    on_release=self.remove_button_down,
                )
                boxdict.add_widget(button)
                boxdict.add_widget(edit_button)
                boxdict.add_widget(remove_button)
                self.ids.scroll_menu_dict.add_widget(boxdict)

    def __init__(self, **kw):
        super().__init__(**kw)
        self.initit_dicts_list()

    def on_pre_enter(self, *args):
        self.ids.scroll_menu_dict.clear_widgets()
        DmCw.resource_name = ""
        self.initit_dicts_list()

    def back_button_down_dict(self):
        self.parent.remove_widget(Dict_menu())
        sm.current = "menu"

    def return_box_name(self, instance):
        for child in instance.parent.children:
            if isinstance(child, Button):
                if len(child.text) > 0:
                    return " ".join(x for x in child.text.split()[:-2])

    def edit_button_down(self, instance):
        button_name = self.return_box_name(instance)
        DmCw.resource_name = button_name
        sm.current = "create_res"

    class Remove_accept_popup(Popup):
        pass

    def remove_file(self):
        os.remove(f"baza/Dictionary/{self.button_name}.txt")
        self.on_pre_enter()

    def yes_remove_button(self, instance):
        self.popup.dismiss()
        self.remove_file()

    def remove_button_down(self, instance):
        self.button_name = self.return_box_name(instance)
        if os.path.exists(f"baza/Dictionary/{self.button_name}.txt"):
            self.popup = Dict_menu.Remove_accept_popup(
                title=f'Czy na pewno chcesz usunąć bazę: "{self.button_name}"',
                title_align="center",
                content=Button(text="Tak", on_release=(self.yes_remove_button)),
                size_hint=(0.6, 0.13),
                pos_hint={"center_x": 0.5, "center_y": 0.5},
            )
            self.popup.open()
            """os.remove(f"baza/Dictionary/{button_name}.txt")
            self.on_pre_enter()"""

    class Create_window_popup(Popup):
        def create_button_down(self):
            DmCw.resource_name = self.ids.base_name.text
            self.clear_widgets()
            sm.current = "create_res"


DmCw = Dict_menu.Create_window_popup


class Create_window(Screen):
    def on_pre_enter(self, *args):
        self.ids.add_words.clear_widgets()
        self.init_create_window()

    def init_create_window(self):
        self.ids.create_text_box.text = (
            f'Dodaj wyrażenia do bazy\n"{DmCw.resource_name}"'
        )
        if os.path.exists(f"baza/Dictionary/{DmCw.resource_name}.txt"):
            with open(f"baza/Dictionary/{DmCw.resource_name}.txt", "r") as f:
                f = [lines.strip().split("/") for lines in f.readlines()]
            Mydict = {}
            Mydict.update({x[0]: x[1] for x in f})
            self.boxText = self.ids.add_words
            for key, value in Mydict.items():
                self.textinput_create(key, value)
        else:
            self.boxText = self.ids.add_words
            for x in range(4):
                self.textinput_create()
        self.add_button_show()

    def textinput_create(self, key="", value=""):
        boxText = BoxLayout(
            orientation="horizontal", spacing=5, size_hint=(1, None), height=40
        )
        textinput1 = TextInput(
            text=key,
            # halign="center",
            # valign="middle",
            font_size=20,
            write_tab=False,
            multiline=False,
        )
        textinput2 = TextInput(
            # halign="center",
            # valign="middle",
            font_size=20,
            text=value,
            write_tab=False,
            multiline=False,
        )
        boxText.add_widget(textinput1)
        boxText.add_widget(textinput2)
        self.boxText.add_widget(boxText)

    def add_button_show(self):
        add_button = Button(
            text=f"+",
            font_size=20,
            size_hint=(1, None),
            height=40,
            on_release=self.add_textinput_button,
        )
        self.boxText.add_widget(add_button)

    def accept_button_down_create(self):
        Mydict = {}
        for box in self.ids.add_words.children:
            minibox = []
            for text_input in box.children:
                if len(text_input.text) > 0:
                    minibox.append(text_input.text)
            if len(minibox) > 1:
                Mydict.update({minibox[1].strip(): minibox[0].strip()})
        with open(f"baza/Dictionary/{DmCw.resource_name}.txt", "w") as f:
            for key, value in Mydict.items():
                f.write(f"{key.lower()}/{value.lower()}\n")

    def back_button_down(self):
        self.parent.remove_widget(Create_window())
        sm.current = "dict_menu"

    def add_textinput_button(self, instance):
        self.textinput_create()
        self.boxText.remove_widget(instance)
        self.add_button_show()

    class Accept_Create_popup(Popup):
        def __init__(self, create_window_instance, **kwargs):
            super().__init__(**kwargs)
            self.create_window_instance = create_window_instance

        def Accept_Create_down(self):
            self.create_window_instance.accept_button_down_create()
            sm.current = "dict_menu"


class DictionaryQuiz(Screen):
    last_word = ""

    def random_word(self):
        while True:
            DictionaryQuiz.choose_word = choice(list(self.repeat_dict.keys()))
            if self.repeat_dict.get(self.choose_word) == 0:
                continue
            else:
                if self.choose_word == self.last_word and len(self.dict) > 1:
                    continue
                else:
                    DictionaryQuiz.last_word = self.choose_word
                    break

    def handle_keypress(self, window, keycode, *args):
        if isinstance(keycode, int) and keycode == 13:
            self.right_button_down()

    def set_focus_dict_answer(self, dt):
        self.ids.dict_answer.focus = True

    def on_pre_enter(self):
        direct = f"baza/Dictionary/{Dict_menu.chos}.txt"
        DictionaryQuiz.dict = {}
        DictionaryQuiz.repeat_dict = {}
        DictionaryQuiz.full_correct = 0
        # normal state
        self.ids.right_button.background_normal = "icons/accept_icon.png"
        self.ids.dict_answer.disabled = False
        self.ids.dict_answer.text = ""
        ##############################
        if os.path.exists(direct):
            with open(direct, "r") as f:
                f = [lines.strip().split("/") for lines in f.readlines()]
        for line in f:
            if len(line) > 1:
                self.dict.update({line[1]: line[0]})
                self.repeat_dict.update({line[1]: 1})
        self.random_word()
        self.ids.repeat_quest.text = str(self.repeat_dict.get(self.choose_word))
        DictionaryQuiz.len_dict = len(self.dict)
        self.ids.full_correct_answer.text = str(
            f"{self.full_correct} / {self.len_dict}"
        )
        self.ids.size_base.text = str(len(self.dict))
        self.ids.dict_quest.text = self.choose_word
        Clock.schedule_once(self.set_focus_dict_answer, 0.2)
        Window.bind(on_key_down=self.handle_keypress)

    def back_button_down(self):
        self.parent.remove_widget(DictionaryQuiz())
        Window.unbind(on_key_down=self.handle_keypress)
        sm.current = "dict_menu"

    def correct_widget(self, bool_answer):
        if bool_answer:
            self.ids.correct_widget_dict.text = "Correct"
            self.ids.correct_widget_dict.opacity = 1
            self.ids.correct_widget_dict.color = (0, 0.7, 0, 1)
        else:
            self.ids.correct_widget_dict.text = (
                f'Should be "{self.dict.get(self.choose_word)}"'
            )
            self.ids.correct_widget_dict.opacity = 1
            self.ids.correct_widget_dict.color = (0.7, 0, 0, 1)

    def check_answer_dict(self):
        self.ids.dict_answer.disabled = True
        answer = self.ids.dict_answer.text
        x = self.repeat_dict.get(self.choose_word)
        if answer.strip() == self.dict.get(self.choose_word):
            x -= 1
            self.correct_widget(True)
        else:
            x += 1
            self.correct_widget(False)
        if x == 0:
            DictionaryQuiz.dict.pop(self.choose_word)
            DictionaryQuiz.repeat_dict.pop(self.choose_word)
            DictionaryQuiz.full_correct += 1
            self.ids.full_correct_answer.text = str(
                f"{self.full_correct} / {self.len_dict}"
            )
        else:
            DictionaryQuiz.repeat_dict.update({self.choose_word: x})

    def accept_icon_dict(self):
        self.check_answer_dict()

    def next_icon_dict(self):
        self.random_word()
        self.ids.correct_widget_dict.opacity = 0
        self.ids.dict_answer.disabled = False
        self.ids.dict_answer.text = ""
        self.ids.dict_quest.text = self.choose_word
        self.ids.repeat_quest.text = str(self.repeat_dict.get(self.choose_word))
        Clock.schedule_once(self.set_focus_dict_answer, 0.2)

    def right_button_down(self):
        if self.ids.right_button.background_normal == "icons/accept_icon.png":
            self.accept_icon_dict()
            self.ids.right_button.background_normal = "icons/next_icon.png"
        else:
            if len(self.dict) == 0:
                sm.remove_widget(DictionaryQuiz())
                Window.unbind(on_key_down=self.handle_keypress)
                sm.current = "dict_menu"
            else:
                self.ids.right_button.background_normal = "icons/accept_icon.png"
                self.next_icon_dict()
            # Clock.schedule_once(self.set_focus_text_quest_1, 0.2)


class Menu(Screen):
    def button_1_down(self):
        sm.remove_widget(Menu())
        sm.current = "irr_menu"
        pass

    def button_2_down(self):
        sm.remove_widget(Menu())
        Dict_menu.button = "diction"
        sm.current = "dict_menu"

    def button_3_down(self):
        sm.remove_widget(Menu())
        Dict_menu.button = "fiszki"
        sm.current = "dict_menu"


class MenuApp(App):
    global sm
    sm = ScreenManager()

    def build(self):
        sm.add_widget(Menu(name="menu"))
        sm.add_widget(Irregular_Menu(name="irr_menu"))
        sm.add_widget(Irregular(name="irregular"))
        sm.add_widget(Finish_Window(name="finish_irr"))
        sm.add_widget(Dict_menu(name="dict_menu"))
        sm.add_widget(Create_window(name="create_res"))
        sm.add_widget(DictionaryQuiz(name="dict_quiz"))
        return sm


if __name__ == "__main__":
    MenuApp().run()
