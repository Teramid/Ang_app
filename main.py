from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.config import Config
from kivy.core.window import Window
from kivy.properties import StringProperty
from kivy.uix.button import Button
from kivy.clock import Clock


import os
from random import randint


# Download resources
def download_verb_list():
    from urllib.request import urlopen
    from bs4 import BeautifulSoup

    """_summary_
    Funkcja tworząca baze czasowników nieregularnych
    """

    html = "https://www.ang.pl/gramatyka/czasowniki-verbs/czasowniki-nieregularne"
    req = urlopen(html)

    soup = BeautifulSoup(req.read(), "html5lib")

    words = soup.find_all(class_=["ang", "pol"])
    word_list = []
    for x in words:
        word_list.append(x.get_text())
        try:
            word_list.remove("przykłady »\n\t\t\twzory odmian »")
        except:
            pass

    verb_irr = []
    for nr, word in enumerate(word_list):
        if word[0] == "p" and word[1] == "l" and word[2] == "a" and word[3] == "y":
            list = [x for x in word]
            word = "".join(x for x in list[4:])
            word_list[nr] = word
        if (nr + 1) % 4 == 0:
            verb_irr.append(
                [word_list[nr - 3], word_list[nr - 2], word_list[nr - 1], word_list[nr]]
            )

    for nr, verb in enumerate(verb_irr):
        nameFile = ""
        numberFile = nr + 1
        if numberFile < 10:
            nameFile = "00" + str(numberFile) + ".txt"
        elif numberFile >= 0 and numberFile < 100:
            nameFile = "0" + str(numberFile) + ".txt"
        else:
            nameFile = str(numberFile) + ".txt"
        nameFile = "baza/" + nameFile
        if not os.path.exists("baza"):
            os.makedirs("baza")
        else:
            pass
        f = open(nameFile, "w")
        f.write("\n".join(x for x in verb))
    print("Pobrano", len(verb_irr), "czasowników")
    Enter_press = input("Wciśnij enter aby kontynuować")
    f.close()


# check path to resources
def check_path_base():
    if os.path.exists("baza") and os.path.isdir("baza"):
        pass
    else:
        download_verb_list()


# create dict
def make_dict_and_index(repeat=3):
    files = os.listdir("baza")
    Files_Number = len(files)
    dict = {}
    for nr, x in enumerate(files):
        file_name = "baza/" + x
        f = open(file_name, "r")
        f = f.readlines()
        if len(f[3].split(", ")) > 3:
            list = f[3].split(", ")
            list[3] = "\n" + list[3]
            f[3] = ", ".join(verb for verb in list)
        dict.update(
            {nr + 1: [f[0].rstrip(), f[1].rstrip(), f[2].rstrip(), f[3], file_name[5:]]}
        )

    dictNumber = {}
    for i in range(1, Files_Number + 1):
        dictNumber.update({i: repeat})

    return Files_Number, dict, dictNumber


# choose random number
def random_verb(dictNumber, Files_Number):
    x = True
    while x:
        choose_File = int(randint(1, Files_Number))
        if dictNumber.get(choose_File) == 0:
            continue
        else:
            return choose_File


# check answer
def check_correct_answer(Answer, choose_File, dict, dictNumber, Full_Answer):
    Answer_Correct = []
    for i in range(len(Answer)):
        if (
            Answer[i].strip().lower() in dict[choose_File][i].split(", ")
            or Answer[i].strip().lower() in dict[choose_File][i].split()
            or Answer[i].strip().lower() == dict[choose_File][i]
        ):
            Answer_Correct.append(True)
        else:
            Answer_Correct.append(False)

    x = dictNumber.get(choose_File)
    if False not in Answer_Correct:
        x -= 1
    else:
        x += 1
    dictNumber.update({choose_File: x})
    if x == 0:
        Full_Answer += 1
    else:
        pass

    return Answer_Correct, dictNumber, Full_Answer


form_name = [
    "Bezokolicznik (infinitive): ",
    "II forma (past tense): ",
    "III forma (past participle): ",
]

Window.size = (450, 800)
Config.set("graphics", "resizable", False)
check_path_base()
Files_Number, dict, dictNumber = make_dict_and_index()
choose_File = random_verb(dictNumber, Files_Number)
Full_Answer = 0
Full_Ans_Str = str(Full_Answer) + "/" + str(Files_Number)


class Main(FloatLayout):
    repteat_quest = StringProperty(str(dictNumber.get(choose_File)))
    full_correct_answer = StringProperty(Full_Ans_Str)
    size_base = StringProperty(str(Files_Number))
    quest_file = StringProperty(str(dict[choose_File][4]))
    quest_0 = StringProperty(str(dict[choose_File][3]))
    quest_1 = StringProperty(form_name[0])
    quest_2 = StringProperty(form_name[1])
    quest_3 = StringProperty(form_name[2])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(on_key_down=self.handle_keypress)
        self.ids.text_quest_1.focus = True

    def handle_keypress(self, window, keycode, *args):
        if isinstance(keycode, int) and keycode == 13:
            self.right_button_down()
            self.ids.right_button.release = (
                self.ids.right_button.background_normal,
                self.ids.right_button.background_down,
            ) = (
                self.ids.right_button.background_down,
                self.ids.right_button.background_normal,
            )

    def right_button_down(self):
        if self.ids.right_button.background_normal == "icons/accept_icon.png":
            self.accept_button_down()
        else:
            self.next_button_down()

    def check_label_change(self, bool_ans, answer_id, text_id, number):
        if bool_ans:
            answer_id.text = "Correct"
            answer_id.color = (0, 0.7, 0, 1)
            text_id.disabled = True
            answer_id.opacity = 1
        else:
            should = f'Should be "{dict[choose_File][number]}"'
            answer_id.text = should
            answer_id.color = (0.7, 0, 0, 1)
            text_id.disabled = True
            answer_id.opacity = 1

    def normal_label_state(self):
        self.ids.text_quest_1.text = ""
        self.ids.check_answer_1.opacity = 0
        self.ids.check_answer_1.color = (1, 1, 1, 1)
        self.ids.text_quest_1.disabled = False

        self.ids.text_quest_2.text = ""
        self.ids.check_answer_2.opacity = 0
        self.ids.check_answer_2.color = (1, 1, 1, 1)
        self.ids.text_quest_2.disabled = False

        self.ids.text_quest_3.text = ""
        self.ids.check_answer_3.opacity = 0
        self.ids.check_answer_3.color = (1, 1, 1, 1)
        self.ids.text_quest_3.disabled = False

        for text_input_string in self.ids.values():
            if isinstance(text_input_string, TextInput):
                text_input_string.text = ""

    def accept_button_down(self):
        Answer = []
        Answer.append(self.ids.text_quest_1.text)
        Answer.append(self.ids.text_quest_2.text)
        Answer.append(self.ids.text_quest_3.text)
        global Full_Answer
        global dictNumber
        Answer_Correct, dictNumber, Full_Answer = check_correct_answer(
            Answer, choose_File, dict, dictNumber, Full_Answer
        )
        text_input = [
            self.ids.text_quest_1,
            self.ids.text_quest_2,
            self.ids.text_quest_3,
        ]
        check_answer = [
            self.ids.check_answer_1,
            self.ids.check_answer_2,
            self.ids.check_answer_3,
        ]
        if False not in Answer_Correct:
            for i in range(len(text_input)):
                self.check_label_change(
                    Answer_Correct[i], check_answer[i], text_input[i], i
                )
        else:
            for i in range(len(text_input)):
                self.check_label_change(
                    Answer_Correct[i], check_answer[i], text_input[i], i
                )
        global Full_Ans_Str
        Full_Ans_Str = str(Full_Answer) + "/" + str(Files_Number)
        self.full_correct_answer = Full_Ans_Str
        self.repteat_quest = str(dictNumber.get(choose_File))

    def set_focus_text_quest_1(self, dt):
        self.ids.text_quest_1.focus = True

    def next_button_down(self):
        self.normal_label_state()
        global choose_File
        choose_File = random_verb(dictNumber, Files_Number)
        self.repteat_quest = str(dictNumber.get(choose_File))
        self.size_base = str(Files_Number)
        self.quest_file = str(dict[choose_File][4])
        self.quest_0 = str(dict[choose_File][3])
        self.quest_1 = form_name[0]
        self.quest_2 = form_name[1]
        self.quest_3 = form_name[2]
        Clock.schedule_once(self.set_focus_text_quest_1, 0.1)

    def back_button_down(self):
        exit()


class MainApp(App):
    def build(self):
        return Main()


if __name__ == "__main__":
    MainApp().run()
