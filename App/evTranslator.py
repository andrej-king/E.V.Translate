import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import *  # Импорт диалоговых окон

from gtts import gTTS  # модуль озвучки текста

import os, os.path, shutil  # Работа с системой, доступ к системной информации
# https://pythonworld.ru/moduli/modul-os.html

import random
from random import choice

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"  # Скрыть приветственное сообщение в консоль о pygame
import pygame
from pygame import mixer

import time
import hashlib

import numpy as np


# -----------------------------------------------------------------

# Расположение окна с указанными размерами по средине экрана
def windowsInCenter(width, height, nameApp):
    if width > nameApp.winfo_screenwidth():
        width = int(nameApp.winfo_screenwidth() * 0.95)  # ширина окна - 5%

    if height > nameApp.winfo_screenheight():  # высота окна
        height = int(nameApp.winfo_screenheight() * 0.90)  # высота окна - 10%

    w = nameApp.winfo_screenwidth()  # ширина окна
    h = nameApp.winfo_screenheight()  # высота окна
    w = w // 2
    h = h // 2
    w = w - int(width / 2)  # смещение от середины (отнимаем половину размера окна)
    h = h - int(height / 2)
    nameApp.geometry(f"{width}x{height}+{w}+{h}")  # Размеры окна, рамположение окна по осям x и y


# -----------------------------------------------------------------


# Окно поверх основного, с определенной информацией, и блокировкой возможности дейтствия в это время с основным окном
class open_toplevel_window(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.grab_set()  # Блокирует возможно взаимодействия с основным окном, пока открыто это
        self.focus_set()  # Фокус на окне

    # ----------------------------------------

    def popupmsg(self, msg):
        windowsInCenter(200, 80, self)
        self.resizable(False, False)
        self.wm_title("!")

        label = ttk.Label(self, text=msg, font=NORM_FONT)
        label.pack(pady=10)
        B1 = ttk.Button(self, text="OK", command=self.destroy)
        B1.pack()

    # ----------------------------------------

    def menuAbout(self):
        windowsInCenter(200, 80, self)
        self.resizable(False, False)  # Отключить изменение размера окна. Вертикально, горизонтально

        self.wm_title("About")
        label = ttk.Label(self, text="О программе", font=NORM_FONT)
        label.pack(pady=10)

        B1 = ttk.Button(self, text="OK", command=self.destroy)
        B1.pack()

    # ----------------------------------------

    def add_or_change_text_with_first_word(self, type, first_word=""):
        windowsInCenter(650, 150, self)
        self.resizable(False, False)

        # New Words window
        addFirstWordEntry = Entry(self, width=20, fg="black", bg="white", font=LARGE_FONT_BOLD, borderwidth=5,
                                  relief=tk.FLAT)
        addSecondWordEntry = Entry(self, width=20, fg="black", bg="white", font=LARGE_FONT_BOLD, borderwidth=5,
                                   relief=tk.FLAT)

        txtAddWords = Label(self, text="", font=LARGE_FONT_BOLD)

        # Подтягивание значения с формы перевода
        addFirstWordEntry.delete(0, END)
        addFirstWordEntry.insert(0, first_word.lower())

        if type == "add":
            self.wm_title("Add word")
            lbl = "Добавить в словарь"
            addWordsBtn = Button(self, text="Добавить в словарь", font=LARGE_FONT_BOLD,
                                 command=lambda: add_in_dict(self, "add"))
            # Placeholder для поля ввода
            placeholder(addSecondWordEntry, "Введите перевод")
        elif type == "replace":
            self.wm_title("Replace word")
            lbl = "Исправить"
            addWordsBtn = Button(self, text="Исправить", font=LARGE_FONT_BOLD,
                                 command=lambda: add_in_dict(self, "replace"))
            # Placeholder для поля ввода
            placeholder(addSecondWordEntry, "Введите перевод")

        # Добавить новое слово в словарь
        def add_in_dict(self, type):
            word1 = addFirstWordEntry.get().lower()  # Получить значение из ящика Entry, слово для перевода
            word2 = addSecondWordEntry.get().lower()  # Получить значение из ящика Entry, слово для перевода
            if word1 == "" or word1 == "введите слово" or word2 == "" or word2 == "введите перевод":
                txtAddWords.configure(text="Введите слово и перевод")
            else:
                dictEst, dictRus = file_open(DICTIONARY_PATH)  # Подгрузка списка словаря
                listEst = list(dictEst)
                listRus = list(dictRus)

                if type == "add":
                    if word1 in listRus or word1 in listEst:
                        txtAddWords.configure(text="\'" + word1.capitalize() + "\' уже есть в словаре")
                    elif word2 in listRus or word2 in listEst:
                        txtAddWords.configure(text="\'" + word2.capitalize() + "\' уже есть в словаре")
                    else:
                        # считывание алфавитов
                        letters_est = read_file_arr(LETTERS_EST)
                        letters_rus = read_file_arr(LETTERS_RUS)

                        est_flag = False
                        ru_flag = False
                        wrong_symbols = False

                        # Поиск запрещенных символов
                        if "==" in word1:
                            wrong_symbols = True
                            txtAddWords.configure(text="\'==\' запрещенный символ")
                        elif "==" in word2:
                            wrong_symbols = True
                            txtAddWords.configure(text="\'==\' запрещенный символ")

                        if wrong_symbols == False:
                            # Определение русское слово или эстонское по первой букве
                            for a in word1:
                                if a in letters_rus:
                                    ru_flag = True
                                    break
                                elif a in letters_est:
                                    est_flag = True
                                    break
                            if ru_flag == True:
                                if file_add_text_in_end(DICTIONARY_PATH, word2, word1) == True:
                                    txtAddWords.configure(text="Добавлено успешно")

                                    # Placeholder для поля ввода
                                    placeholder(addFirstWordEntry, "Введите слово")
                                    placeholder(addSecondWordEntry, "Введите перевод")
                                else:
                                    txtAddWords.configure(text="Ошибка. Не добавлено")
                            elif est_flag == True:
                                if file_add_text_in_end(DICTIONARY_PATH, word1, word2) == True:
                                    txtAddWords.configure(text="Добавлено успешно")

                                    # Placeholder для поля ввода
                                    placeholder(addFirstWordEntry, "Введите слово")
                                    placeholder(addSecondWordEntry, "Введите перевод")
                                else:
                                    txtAddWords.configure(text="Ошибка. Не добавлено")

                elif type == "replace":
                    # проверка есть ли заменяемое слово в словаре
                    if word1 in listRus or word1 in listEst:

                        # считывание алфавитов
                        letters_est = read_file_arr(LETTERS_EST)
                        letters_rus = read_file_arr(LETTERS_RUS)

                        est_flag = False
                        ru_flag = False
                        wrong_symbols = False

                        # Поиск запрещенных символов
                        if "==" in word1:
                            wrong_symbols = True
                            txtAddWords.configure(text="\'==\' запрещенный символ")
                        elif "==" in word2:
                            wrong_symbols = True
                            txtAddWords.configure(text="\'==\' запрещенный символ")

                        if wrong_symbols == False:
                            # Определение русское слово или эстонское по первой букве
                            for a in word1:
                                if a in letters_rus:
                                    ru_flag = True
                                    break
                                elif a in letters_est:
                                    est_flag = True
                                    break
                            if ru_flag == True:
                                indx = listRus.index(word1)
                                listEst[indx] = word2
                                if file_text_rewrite(DICTIONARY_PATH, listEst, listRus) == True:
                                    txtAddWords.configure(text="Исправлено")

                                    # Placeholder для поля ввода
                                    placeholder(addFirstWordEntry, "Введите слово")
                                    placeholder(addSecondWordEntry, "Введите исправление")
                                else:
                                    txtAddWords.configure(text="Ошибка. Не исправлено")
                            elif est_flag == True:
                                indx = listEst.index(word1)
                                listRus[indx] = word2
                                if file_text_rewrite(DICTIONARY_PATH, listEst, listRus) == True:
                                    txtAddWords.configure(text="Исправлено")

                                    # Placeholder для поля ввода
                                    placeholder(addFirstWordEntry, "Введите слово")
                                    placeholder(addSecondWordEntry, "Введите исправление")
                                else:
                                    txtAddWords.configure(text="Ошибка. Не исправлено")
                    else:
                        txtAddWords.configure(text="\'" + word1.capitalize() + "\' нету в словаре")

        addFirstWordEntry.place(x=10, y=50)
        addSecondWordEntry.place(x=220, y=50)
        addWordsBtn.place(x=430, y=50)
        txtAddWords.place(x=10, y=90)

        label = ttk.Label(self, text=lbl, font=LARGE_FONT_BOLD)
        label.pack(side=TOP, pady=10)

        B1 = ttk.Button(self, text="OK", command=self.destroy)
        B1.pack(side=BOTTOM, pady=20)


# -----------------------------------------------------------------

# Read file, return 2 lists: est-rus, rus-est
def file_open(file_path):
    # Открываем файл на чтение
    file = open(file_path, "r", encoding="utf-8")
    # Создаем лист для записи в него построчно
    # Словарь
    dictEst = {}
    dictRus = {}
    # Пробегаем построчно
    for line in file:
        # найти индекс разделителя логина и пароля
        n = line.find("==")
        e = line[0:n]  # запись с 0 элемента до разделителя
        v = line[n + 2:len(line) - 1]  # запись от найденного символа до конца строки. - \n
        # запись в словарь - key : value
        dictEst[e] = v
        dictRus[v] = e
    file.close()
    return dictEst, dictRus


def read_file_arr(file_path):
    file = open(file_path, "r", encoding="utf-8")
    arr = []
    for line in file:
        arr.append(line.strip())  # \n не появляется
    file.close()
    return arr


def file_add_text_in_end(file_path, est_word, rus_word):
    file = open(file_path, "a", encoding="utf-8")
    line = est_word + "==" + rus_word
    if file.write(line + "\n"):
        file.close()
        return True
    else:
        file.close()
        return False


def file_text_rewrite(file_path, est_word_list, rus_word_list):
    file = open(file_path, "w", encoding="utf-8")
    for line in range(len(rus_word_list)):
        file.write(est_word_list[line] + "==" + rus_word_list[line] + "\n")
    file.close()
    return True


# -----------------------------------------------------------------
# Placeholder для перевода
def placeholder(entry_id, text):
    entry_id.delete(0, END)
    entry_id.insert(0, text)
    entry_id.configure(state=DISABLED)
    entry_id.config(disabledbackground="#fff", disabledforeground="black")

    def on_click_word(event):
        entry_id.configure(state=NORMAL)
        entry_id.delete(0, END)

        # make the callback only work once
        entry_id.unbind('<Button-1>', on_click_id)

    on_click_id = entry_id.bind('<Button-1>', on_click_word)


# -----------------------------------------------------------------

LARGE_FONT = "Arial 12"
LARGE_FONT_BOLD = "Arial 12 bold"
NORM_FONT = "Arial 10"
NORM_FONT_BOLD = "Arial 10 bold"
SMALL_FONT = "Arial 8"
SMALL_FONT_BOLD = "Arial 8 bold"

GENERAL_BG = "#f0f0f0"  # gray gray0-99

# txt path
DICTIONARY_PATH = "Data/txt/dict.txt"
LETTERS_RUS = "Data/txt/ru.txt"
LETTERS_EST = "Data/txt/et.txt"
CATEGORIES_PATH = "Data/txt/categories"
CATEGORIES_COLORS = "Data/txt/categories/colors.txt"
CATEGORIES_DAYS_OF_THE_WEEK = "Data/txt/categories/days_of_the_week.txt"
CATEGORIES_FAMILY = "Data/txt/categories/family.txt"
CATEGORIES_MONTHS = "Data/txt/categories/months.txt"

# img path
IMG_ICO = ("Data/img/clienticon.ico")

IMG_MENU_VOCABULARY = "Data/img/Vocabulary.png"
IMG_MENU_TRAIN = "Data/img/Brain.png"
IMG_MENU_HOME = "Data/img/Home.png"
IMG_MENU_LINE = "Data/img/Line.png"

IMG_ADD_IN_DICT = "Data/img/Add_in_dict.png"
IMG_FIND_IN_DICT = "Data/img/Find_in_dict.png"

IMG_SPEAKER = "Data/img/Speaker.png"

# sounds path
SOUNDS_PATH = "Data/sounds"

# system sounds path
SYSTEM_SOUNDS_PATH = "Data/system_sounds/"
SYSTEM_SOUNDS_CORRECT = "Data/system_sounds/correct.mp3"
SYSTEM_SOUNDS_INCORRECT = "Data/system_sounds/wrong.mp3"
SYSTEM_SOUNDS_FINISH = "Data/system_sounds/finish.mp3"

# ----------------------------------------------------------------

# Значения для тренировок
nums = []
listEst = []
listRus = []
count_right = 0  # Количество правильных ответов
count_wrong = 0  # Количество неправильных ответов
count_questions = 1  # Количество вопросов
ask_id = 0
general_count_questions = 5


# -----------------------------------------------------------------

# main class
class EVTranslator(tk.Tk):
    # *args для неименованных аргументов;
    # **kwargs для именованных аргументов.
    # Мы используем *args и **kwargs в качестве аргумента, когда заранее не известно, сколько значений мы хотим передать функции.
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.iconbitmap(self, default=IMG_ICO)  # logo near title window, 16 x 16
        tk.Tk.wm_title(self, "Estonian-Russian Translator")  # title window

        # Фрейм основного окна
        container = tk.Frame(self)

        # container.pack(side="top", fill="both", expand=True)
        # container.grid_rowconfigure(0, weight=1)
        # container.grid_columnconfigure(0, weight=1)
        container.pack()

        # Menubar
        menubar = tk.Menu(container)

        # File menu
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Сохранить настройки",
                             command=lambda: open_toplevel_window().popupmsg("Еще не настроено"))
        filemenu.add_separator()  # Разделительная линия в меню
        filemenu.add_command(label="Выход", command=self.custom_exit)
        menubar.add_cascade(label="Файл", menu=filemenu)

        # Help menu
        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="О программе", command=lambda: open_toplevel_window().menuAbout())
        menubar.add_cascade(label="Помощь", menu=helpmenu)

        # Show menubar
        tk.Tk.configure(self, menu=menubar)  # Показать в фрейме

        """ Frame list """
        self.frames = {}
        #
        # # simple swith pages
        for F in (StartPage, PageDictionary, PageFindWord, AddInDict, Training, QuizQuestionsRus,
                  QuizQuestionsEst, TrainingPazzle):  #
            # , ReplaceText):
            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)  # Name page when program start

        # Очистка папки с озвучкой при запуске
        self.clear_sound_dir()

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()  # front page

    def clear_sound_dir(self):
        # Удаление содержимого директории
        folder = SOUNDS_PATH + '/'
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                # Удалить внутренние директории
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                pass

    def custom_exit(self):
        self.clear_sound_dir()
        quit()


# -----------------------------------------------------------------

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # tk.Frame.configure(self, bg="green")

        label = ttk.Label(self, text="Добро пожаловать!", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        # close_button = ttk.Button(self, text="Выход", command=quit)
        # close_button.pack(pady=0, padx=10)

        # ------------------------ Menu ------------------------
        menuFrame = Frame(self)
        menuFrame.pack()

        line_img = PhotoImage(file=IMG_MENU_LINE)
        line1_lbl = Label(menuFrame, image=line_img)
        line1_lbl.image = line_img
        line2_lbl = Label(menuFrame, image=line_img)
        line2_lbl.image = line_img

        vocabulary_img = PhotoImage(file=IMG_MENU_VOCABULARY)
        vocabulary_btn = ttk.Button(menuFrame, image=vocabulary_img,
                                    command=lambda: controller.show_frame(PageDictionary))
        vocabulary_btn.image = vocabulary_img
        vocabulary_btn.pack(side=LEFT)

        line2_lbl.pack(side=LEFT)

        train_img = PhotoImage(file=IMG_MENU_TRAIN)
        train_btn = ttk.Button(menuFrame, image=train_img, command=lambda: controller.show_frame(Training))
        train_btn.image = train_img
        train_btn.pack(side=LEFT)


# -----------------------------------------------------------------

class PageDictionary(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Словарь", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        # tk.Frame.configure(self, bg="green")

        button1 = ttk.Button(self, text="На главную", command=lambda: controller.show_frame(StartPage))
        button1.pack()

        vocabulary_find_img = PhotoImage(file=IMG_FIND_IN_DICT)
        vocabulary_find_btn = ttk.Button(self, image=vocabulary_find_img,
                                         command=lambda: controller.show_frame(PageFindWord))
        vocabulary_find_btn.image = vocabulary_find_img
        vocabulary_find_btn.pack(side=LEFT, padx=10, pady=10)

        vocabulary_add_img = PhotoImage(file=IMG_ADD_IN_DICT)
        vocabulary_add_btn = ttk.Button(self, image=vocabulary_add_img,
                                        command=lambda: controller.show_frame(AddInDict))
        vocabulary_add_btn.image = vocabulary_add_img
        vocabulary_add_btn.pack(side=LEFT, padx=10, pady=10)


# -----------------------------------------------------------------

class PageFindWord(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = ttk.Label(self, text="Найти слово или фразу", font=LARGE_FONT)
        label.pack(pady=10, padx=10)
        label.pack(pady=10, padx=10)

        # убрать текст при выходе со страницы
        def switch_page():
            global tmp_replace_word
            placeholder(dictTextEnter, "Введите слово")
            txtTranslate.configure(text="")
            addInDictBtn.place_forget()
            txtForReplace.place_forget()
            moveToReplaceBtn.place_forget()
            controller.show_frame(StartPage)

        button1 = ttk.Button(self, text="На главную", command=switch_page)
        button1.pack()

        # ------------------------------------------------------------

        def show_translate(type):
            word = dictTextEnter.get().lower()
            lang_flag = ""
            if word == "введите слово" or word == "":
                txtTranslate.configure(text="Введите слово или фразу для перевода")
            else:
                dictEst, dictRus = file_open(DICTIONARY_PATH)  # Подгрузка списка словаря
                listEst = list(dictEst)
                listRus = list(dictRus)

                if type == "text":
                    if word in listRus:
                        txtTranslate.configure(text=dictRus.get(word).capitalize())
                        addInDictBtn.place_forget()
                        txtForReplace.place(x=10, y=175)
                        moveToReplaceBtn.place(x=390, y=172)
                    elif word in listEst:
                        txtTranslate.configure(text=dictEst.get(word).capitalize())
                        addInDictBtn.place_forget()
                        txtForReplace.place(x=10, y=175)
                        moveToReplaceBtn.place(x=390, y=172)
                    else:
                        txtTranslate.configure(text="Поиск не дал результатов. Желаете добавить в словарь?",
                                               font=LARGE_FONT_BOLD)
                        addInDictBtn.place(x=480, y=135)
                        txtForReplace.place_forget()
                        moveToReplaceBtn.place_forget()

                # Озвучивание
                # Соединение переводов на разных языках
                elif type == "sound":

                    if word in listRus:
                        txtTranslate.configure(text=dictRus.get(word).capitalize())
                        addInDictBtn.place_forget()
                        txtForReplace.place(x=10, y=175)
                        moveToReplaceBtn.place(x=390, y=172)
                        lang_flag = "et"  # т.к. искали перевод на эстонский
                    elif word in listEst:
                        txtTranslate.configure(text=dictEst.get(word).capitalize())
                        addInDictBtn.place_forget()
                        txtForReplace.place(x=10, y=175)
                        moveToReplaceBtn.place(x=390, y=172)
                        lang_flag = "ru"  # т.к. искали перевод на эстонский

                    if lang_flag == "et":  # Первым будет русское слово, потом перевод
                        # hash md5 name
                        a = dictRus.get(word) + " - " + word
                        a = bytes(a, 'utf-8')  # 'b - для преобразования строки в bytes.
                        hashName = hashlib.md5(a).hexdigest()  # Создание hash в md5

                        mp3Name = hashName + ".mp3"  # название файла hash.mp3
                        nameAndPath = SOUNDS_PATH + '/' + mp3Name

                        # Проверить существование файла, если файл существует озвучить, иначе создать и озвучить
                        if os.path.isfile(nameAndPath) == False:
                            tts_et = gTTS(dictRus.get(word), lang='et')
                            tts_ru = gTTS(word, lang='ru')

                            with open(nameAndPath, 'wb') as f:
                                tts_et.write_to_fp(f)
                                tts_ru.write_to_fp(f)
                        mixer.init()
                        mixer.music.load(nameAndPath)
                        mixer.music.play()
                        while pygame.mixer.music.get_busy() == True:
                            continue
                        mixer.music.stop()


                    elif lang_flag == "ru":  # Первым будет эстонское слово, потом перевод

                        # hash md5 name
                        a = dictEst.get(word) + " - " + word
                        a = bytes(a, 'utf-8')  # 'b - для преобразования строки в bytes.
                        hashName = hashlib.md5(a).hexdigest()  # Создание hash в md5

                        mp3Name = hashName + ".mp3"  # название файла hash.mp3
                        nameAndPath = SOUNDS_PATH + '/' + mp3Name

                        # Проверить существование файла, если файл существует озвучить, иначе создать и озвучить
                        if os.path.isfile(nameAndPath) == False:
                            tts_ru = gTTS(dictEst.get(word), lang='ru')
                            tts_et = gTTS(word, lang='et')

                            with open(nameAndPath, 'wb') as f:
                                tts_ru.write_to_fp(f)
                                tts_et.write_to_fp(f)

                        mixer.init()
                        mixer.music.load(nameAndPath)
                        mixer.music.play()
                        while mixer.music.get_busy() == True:
                            continue
                        mixer.music.stop()

        # -----------------------------
        dictTextEnter = Entry(self, width=15, fg="black", bg="white", font=LARGE_FONT_BOLD, borderwidth=5,
                              relief=tk.FLAT)  # рамка во внутрь

        dictBtn = Button(self, text="Перевести", font=LARGE_FONT_BOLD, command=lambda: show_translate("text"))

        # Отображение перевода / других сообщений
        txtTranslate = Label(self, text="", font=LARGE_FONT_BOLD)

        # Кнопка озвучки
        speaker_img = PhotoImage(file=IMG_SPEAKER)
        speakerBtn = ttk.Button(self, image=speaker_img, command=lambda: show_translate("sound"))
        speakerBtn.image = speaker_img

        # Добавить в словарь
        addInDictBtn = Button(self, text="Добавить в словарь", font=LARGE_FONT_BOLD,
                              command=lambda: open_toplevel_window().add_or_change_text_with_first_word("add",
                                                                                                        first_word=dictTextEnter.get().lower()))

        txtForReplace = Label(self, text="Нашли ошибку? Помогите улучшить словарь", font=LARGE_FONT_BOLD)
        moveToReplaceBtn = Button(self, text="Исправить", font=LARGE_FONT_BOLD,
                                  command=lambda: open_toplevel_window().add_or_change_text_with_first_word("replace",
                                                                                                            first_word=dictTextEnter.get().lower()))

        # show buttons
        speakerBtn.place(x=280, y=100)
        dictTextEnter.place(x=10, y=100)
        dictBtn.place(x=170, y=100)
        txtTranslate.place(x=10, y=140)

        # Placeholder для поля ввода
        placeholder(dictTextEnter, "Введите слово")


# -----------------------------------------------------------------

class AddInDict(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = ttk.Label(self, text="Добавить в словарь", font=LARGE_FONT_BOLD)
        label.pack(pady=10, padx=10)

        # текст по умолчанию при выходе со страницы
        def switch_page():
            placeholder(addFirstWordEntry, "Введите слово")
            placeholder(addSecondWordEntry, "Введите перевод")
            txtAddWords.configure(text="")
            controller.show_frame(StartPage)

        button1 = ttk.Button(self, text="На главную", command=switch_page)
        button1.pack()

        # New Words window
        addFirstWordEntry = Entry(self, width=20, fg="black", bg="white", font=LARGE_FONT_BOLD, borderwidth=5,
                                  relief=tk.FLAT)
        addSecondWordEntry = Entry(self, width=20, fg="black", bg="white", font=LARGE_FONT_BOLD, borderwidth=5,
                                   relief=tk.FLAT)
        addWordsBtn = Button(self, text="Добавить в словарь", font=LARGE_FONT_BOLD,
                             command=lambda: add_in_dict(self))
        txtAddWords = Label(self, text="", font=LARGE_FONT_BOLD)

        addFirstWordEntry.place(x=10, y=100)
        addSecondWordEntry.place(x=220, y=100)
        addWordsBtn.place(x=430, y=100)
        txtAddWords.place(x=10, y=140)

        # Placeholder для поля ввода
        placeholder(addFirstWordEntry, "Введите слово")
        placeholder(addSecondWordEntry, "Введите перевод")

        # Добавить новое слово в словарь
        def add_in_dict(self):
            word1 = addFirstWordEntry.get().lower()  # Получить значение из ящика Entry, слово для перевода
            word2 = addSecondWordEntry.get().lower()  # Получить значение из ящика Entry, слово для перевода
            if word1 == "" or word1 == "введите слово" or word2 == "" or word2 == "введите перевод":
                txtAddWords.configure(text="Введите слово и перевод")
            else:
                dictEst, dictRus = file_open(DICTIONARY_PATH)  # Подгрузка списка словаря
                listEst = list(dictEst)
                listRus = list(dictRus)

                if word1 in listRus or word1 in listEst:
                    txtAddWords.configure(text="\'" + word1.capitalize() + "\' уже есть в словаре")
                elif word2 in listRus or word2 in listEst:
                    txtAddWords.configure(text="\'" + word2.capitalize() + "\' уже есть в словаре")
                else:
                    # считывание алфавитов
                    letters_est = read_file_arr(LETTERS_EST)
                    letters_rus = read_file_arr(LETTERS_RUS)

                    est_flag = False
                    ru_flag = False
                    wrong_symbols = False

                    # Поиск запрещенных символов
                    if "==" in word1:
                        wrong_symbols = True
                        txtAddWords.configure(text="\'==\' запрещенный символ")
                    elif "==" in word2:
                        wrong_symbols = True
                        txtAddWords.configure(text="\'==\' запрещенный символ")

                    if wrong_symbols == False:
                        # Определение русское слово или эстонское по первой букве
                        for a in word1:
                            if a in letters_rus:
                                ru_flag = True
                                break
                            elif a in letters_est:
                                est_flag = True
                                break
                        if ru_flag == True:
                            if file_add_text_in_end(DICTIONARY_PATH, word2, word1) == True:
                                txtAddWords.configure(text="Добавлено успешно")

                                # Placeholder для поля ввода
                                placeholder(addFirstWordEntry, "Введите слово")
                                placeholder(addSecondWordEntry, "Введите перевод")
                            else:
                                txtAddWords.configure(text="Ошибка. Не добавлено")
                        elif est_flag == True:
                            if file_add_text_in_end(DICTIONARY_PATH, word1, word2) == True:
                                txtAddWords.configure(text="Добавлено успешно")

                                # Placeholder для поля ввода
                                placeholder(addFirstWordEntry, "Введите слово")
                                placeholder(addSecondWordEntry, "Введите перевод")
                            else:
                                txtAddWords.configure(text="Ошибка. Не добавлено")


class Training(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # BG фрейма
        # tk.Frame.configure(self, bg="green")

        label = Label(self, text="Тренировки", font=LARGE_FONT)
        label.pack(pady=5, padx=10)

        button1 = ttk.Button(self, text="На главную", command=lambda: controller.show_frame(StartPage))
        button1.pack(pady=5)

        def stepToQuiz(lang):
            global nums, general_count_questions, listEst, listRus, count_right, count_wrong, count_questions

            # сброс
            count_right = 0  # Количество правильных ответов
            count_wrong = 0  # Количество неправильных ответов
            count_questions = 1  # Количество вопросов
            nums = []
            dictEst, dictRus = file_open(DICTIONARY_PATH)
            listEst = list(dictEst)
            listRus = list(dictRus)
            if len(listEst) == 0:
                controller.show_frame(AddInDict)
            elif len(listEst) < general_count_questions:
                general_count_questions = len(listEst)

            nums = QuizQuestionsRus(self, controller=controller).generation_questions(general_count_questions)

            if lang == "rus":
                controller.show_frame(QuizQuestionsRus)
            elif lang == "est":
                controller.show_frame(QuizQuestionsEst)

        def stepToPazzle():
            controller.show_frame(TrainingPazzle)
            # TrainingPazzle(self, controller=controller).initUI()

        #     TrainingPazzle(self, controller=controller).show_pazzle()

        button2 = ttk.Button(self, text="Викторина вопросов рус", command=lambda: stepToQuiz("rus"))
        button2.pack(pady=5)

        button3 = ttk.Button(self, text="Викторина вопросов эст", command=lambda: stepToQuiz("est"))
        button3.pack(pady=5)

        # button3 = ttk.Button(self, text="Пазлы", command=lambda: controller.show_frame(TrainingPazzle))
        button3 = ttk.Button(self, text="Пазлы", command=stepToPazzle)
        # button3 = ttk.Button(self, text="Пазлы", command=lambda: TrainingPazzle(self, controller=controller).show_pazzle())
        button3.pack(pady=5)

        # bgColor = Frame(self, bg='red', height=100, width=100)
        # bgColor.pack()


# -----------------------------------------------------------------

class QuizQuestionsRus(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        def switch_page():
            # сброс
            count_right = 0  # Количество правильных ответов
            count_wrong = 0  # Количество неправильных ответов
            count_questions = 1  # Количество вопросов
            nums = []
            self.answers = []
            self.questions = []

            trainCountAnswersAndQuestionsLbl.place_forget()
            trainAnswerLbl.place_forget()
            trainAnswerLblWord.place_forget()
            trainAnswerEntry.place_forget()
            trainAnswerRusBtn.place_forget()
            labelResult.pack_forget()

            startBtn.pack()

            controller.show_frame(StartPage)

        label = Label(self, text="Викторина вопросов рус", font=LARGE_FONT)
        label.pack(padx=10)

        button1 = ttk.Button(self, text="На главную", command=switch_page)
        button1.pack(pady=10)

        startBtn = ttk.Button(self, text="Start", command=lambda: change())
        startBtn.pack()

        # train answers
        labelResult = Label(self, text="", font=LARGE_FONT)
        trainCountAnswersAndQuestionsLbl = Label(self, text="",
                                                 font=LARGE_FONT)
        trainAnswerLbl = Label(self, text="Напишите перевод слова:", font=LARGE_FONT_BOLD)
        trainAnswerLblWord = Label(self, text="", font=LARGE_FONT_BOLD)
        trainAnswerEntry = Entry(self, width=15, fg="black", bg="white", font=LARGE_FONT_BOLD, borderwidth=5,
                                 relief=tk.FLAT)

        trainAnswerRusBtn = Button(self, text="Далее", font=LARGE_FONT_BOLD, command=lambda: change())

        self.answers = []
        self.questions = []

        def change():
            global nums, listRus, listEst, count_questions, general_count_questions, count_right, count_wrong

            trainCountAnswersAndQuestionsLbl.place(x=10, y=80)
            trainAnswerLbl.place(x=10, y=115)
            trainAnswerLblWord.place(x=230, y=115)
            trainAnswerEntry.place(x=13, y=150)
            trainAnswerRusBtn.place(x=13, y=195)
            startBtn.pack_forget()

            res = self.show_questions()

            if count_questions > 1:
                # Запись вопросов и ответов, для проверки по окончании теста
                self.questions.append(res)
                self.answers.append(trainAnswerEntry.get().lower())

            trainAnswerEntry.delete(0, END)
            if res != False:
                strCountAnswersAndQuestions = str(count_questions - 1) + " / " + str(general_count_questions)
                trainCountAnswersAndQuestionsLbl.configure(text=strCountAnswersAndQuestions)
                trainAnswerLblWord.configure(text=res)
            else:
                trainCountAnswersAndQuestionsLbl.place_forget()
                trainAnswerLbl.place_forget()
                trainAnswerLblWord.place_forget()
                trainAnswerEntry.place_forget()
                trainAnswerRusBtn.place_forget()

                # -----------------------------------------------------------------------
                # Проверка результатов

                # Удалить лишние записи из списка, для более удобной проверки
                del self.questions[len(self.questions) - 1]
                del self.answers[0]

                correct_answers = []  # правильные ответы

                # Узнать правильные ответы
                for a in range(len(self.questions)):
                    indx = listEst.index(self.questions[a])
                    correct_answers.append(listRus[indx])
                    if listRus[indx] == self.answers[a]:
                        count_right += 1
                    else:
                        count_wrong += 1

                percent_right = int(count_right * 100 / (count_questions - 1))

                resultStr = "Всего вопросов: " + str(count_questions - 1) + "\nПравильных ответов: " + str(
                    count_right) + "(" + str(percent_right) + "%)" + "\nНеправильных ответов: " + str(count_wrong)

                labelResult.configure(text=resultStr)
                labelResult.pack(padx=10)

    # генерирует 5 не повторяющихся вопросов
    def generation_questions(self, count):
        global nums
        nums = []
        dictEst, dictRus = file_open(DICTIONARY_PATH)
        listEst = list(dictEst)
        while len(nums) < count:
            rand = int(random.random() * len(listEst))  # генерируем случайное число от 0 до длины списка
            if rand in nums:
                continue
            else:
                nums.append(rand)
        return nums

    def show_questions(self):
        global nums, count_questions, count_right, count_wrong, general_count_questions, listRus, listEst

        try:
            word = listEst[nums[count_questions - 1]]
            count_questions += 1
            return word
        except:
            return False


# -----------------------------------------------------------------

class QuizQuestionsEst(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        def switch_page():
            # сброс
            count_right = 0  # Количество правильных ответов
            count_wrong = 0  # Количество неправильных ответов
            count_questions = 1  # Количество вопросов
            nums = []
            self.answers = []
            self.questions = []

            trainCountAnswersAndQuestionsLbl.place_forget()
            trainAnswerLbl.place_forget()
            trainAnswerLblWord.place_forget()
            trainAnswerEntry.place_forget()
            trainAnswerRusBtn.place_forget()
            labelResult.pack_forget()

            startBtn.pack()

            controller.show_frame(StartPage)

        label = Label(self, text="Викторина вопросов рус", font=LARGE_FONT)
        label.pack(padx=10)

        button1 = ttk.Button(self, text="На главную", command=switch_page)
        button1.pack(pady=10)

        startBtn = ttk.Button(self, text="Start", command=lambda: change())
        startBtn.pack()

        # train answers
        labelResult = Label(self, text="", font=LARGE_FONT)
        trainCountAnswersAndQuestionsLbl = Label(self, text="",
                                                 font=LARGE_FONT)
        trainAnswerLbl = Label(self, text="Напишите перевод слова:", font=LARGE_FONT_BOLD)
        trainAnswerLblWord = Label(self, text="", font=LARGE_FONT_BOLD)
        trainAnswerEntry = Entry(self, width=15, fg="black", bg="white", font=LARGE_FONT_BOLD, borderwidth=5,
                                 relief=tk.FLAT)

        trainAnswerRusBtn = Button(self, text="Далее", font=LARGE_FONT_BOLD, command=lambda: change())
        trainAnswerEstBtn = Button(self, text="Далее", font=LARGE_FONT_BOLD)  # , command=nextQuestionEst)

        self.answers = []
        self.questions = []

        def change():
            global nums, listRus, listEst, count_questions, general_count_questions, count_right, count_wrong

            trainCountAnswersAndQuestionsLbl.place(x=10, y=80)
            trainAnswerLbl.place(x=10, y=115)
            trainAnswerLblWord.place(x=230, y=115)
            trainAnswerEntry.place(x=13, y=150)
            trainAnswerRusBtn.place(x=13, y=195)
            startBtn.pack_forget()

            res = self.show_questions()

            if count_questions > 1:
                # Запись вопросов и ответов, для проверки по окончании теста
                self.questions.append(res)
                self.answers.append(trainAnswerEntry.get().lower())

            trainAnswerEntry.delete(0, END)
            if res != False:
                strCountAnswersAndQuestions = str(count_questions - 1) + " / " + str(general_count_questions)
                trainCountAnswersAndQuestionsLbl.configure(text=strCountAnswersAndQuestions)
                trainAnswerLblWord.configure(text=res)
            else:
                trainCountAnswersAndQuestionsLbl.place_forget()
                trainAnswerLbl.place_forget()
                trainAnswerLblWord.place_forget()
                trainAnswerEntry.place_forget()
                trainAnswerRusBtn.place_forget()

                # -----------------------------------------------------------------------
                # Проверка результатов

                # Удалить лишние записи из списка, для более удобной проверки
                del self.questions[len(self.questions) - 1]
                del self.answers[0]

                correct_answers = []  # правильные ответы

                # Узнать правильные ответы
                for a in range(len(self.questions)):
                    indx = listRus.index(self.questions[a])
                    correct_answers.append(listEst[indx])
                    if listEst[indx] == self.answers[a]:
                        count_right += 1
                    else:
                        count_wrong += 1

                percent_right = int(count_right * 100 / (count_questions - 1))

                resultStr = "Всего вопросов: " + str(count_questions - 1) + "\nПравильных ответов: " + str(
                    count_right) + "(" + str(percent_right) + "%)" + "\nНеправильных ответов: " + str(count_wrong)

                labelResult.configure(text=resultStr)
                labelResult.pack(padx=10)

    # генерирует 5 не повторяющихся вопросов
    def generation_questions(self, count):
        global nums
        nums = []
        dictEst, dictRus = file_open(DICTIONARY_PATH)
        listEst = list(dictEst)
        while len(nums) < count:
            rand = int(random.random() * len(listEst))  # генерируем случайное число от 0 до длины списка
            if rand in nums:
                continue
            else:
                nums.append(rand)
        return nums

    def show_questions(self):
        global nums, count_questions, count_right, count_wrong, general_count_questions, listRus, listEst

        try:
            word = listRus[nums[count_questions - 1]]
            count_questions += 1
            return word
        except:
            return False


# -----------------------------------------------------------------


class TrainingPazzle(tk.Frame):
    pazzleNums = []

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.initUI()

    def initUI(self):
        label = Label(self, text="Пазл тренировки", font=LARGE_FONT)
        label.pack(pady=10, padx=5)

        button1 = ttk.Button(self, text="На главную", command=lambda: switch_to_page_start())
        button1.pack(pady=5)

        button2 = ttk.Button(self, text="Цвета", command=lambda: switch_page_to_show_game(CATEGORIES_COLORS))
        button2.pack(pady=5)

        button3 = ttk.Button(self, text="Месяцы",
                             command=lambda: switch_page_to_show_game(CATEGORIES_MONTHS))
        button3.pack(pady=5)

        button4 = ttk.Button(self, text="Дни недели",
                             command=lambda: switch_page_to_show_game(CATEGORIES_DAYS_OF_THE_WEEK))
        button4.pack(pady=5)

        button5 = ttk.Button(self, text="Семья",
                             command=lambda: switch_page_to_show_game(CATEGORIES_FAMILY))
        button5.pack(pady=5)



        staticLblTask = Label(self, text="", font=LARGE_FONT)
        wordLbl = Label(self, text="", font=LARGE_FONT_BOLD)
        wordLblAssembly = Label(self, text="", font=LARGE_FONT_BOLD)

        symbolsFrame = Frame(self, height=30, width=1000)

        pazzleCountQuestion = 0

        def switch_to_page_start():
            button2.pack(pady=10)
            button3.pack(pady=10)
            button4.pack(pady=10)
            button5.pack(pady=10)

            staticLblTask.configure(text="")
            wordLbl.configure(text="")
            wordLblAssembly.configure(text="")

            symbolsFrame.place_forget()
            # symbolsFrame.destroy()

            app.show_frame(StartPage)

        def switch_page_to_show_game(category):
            # symbolsFrame = Frame(self, height=30, width=1000)
            button2.pack_forget()
            button3.pack_forget()
            button4.pack_forget()
            button5.pack_forget()


            staticLblTask.configure(text="Соберите: ")
            wordLblAssembly.configure(text="")
            staticLblTask.place(x=10, y=75)
            wordLbl.place(x=100, y=75)
            wordLblAssembly.place(x=10, y=110)

            symbolsFrame.place(x=13, y=150)

            q, wordRus, self.wordEst, nums = self.show_pazzle(pazzleCountQuestion, category)

            wordLbl.configure(text=wordRus)

            # дописывает буквы
            self.word = ""
            self.indx_word = 0

            def pazzleAddSymb(symbol):
                if len(self.word) == 0:
                    # Проверка первого символа, если совпадает с первой буквой ответа, показать, иначе удалить ее
                    self.word += symbol
                    if self.word == self.wordEst[0]:
                        wordLblAssembly.config(text=self.word)
                        self.indx_word += 1
                        mixer.init()
                        pygame.mixer_music.load(SYSTEM_SOUNDS_CORRECT)
                        mixer.music.play()
                    else:
                        self.word = ""
                        mixer.init()
                        pygame.mixer_music.load(SYSTEM_SOUNDS_INCORRECT)
                        mixer.music.play()
                else:
                    self.word += symbol
                    self.indx_word += 1
                    if self.word[len(self.word) - 1] == self.wordEst[len(self.word) - 1]:
                        wordLblAssembly.config(text=self.word)
                        self.indx_word += 1
                        mixer.init()
                        pygame.mixer_music.load(SYSTEM_SOUNDS_CORRECT)
                        mixer.music.play()

                        if self.word == self.wordEst:
                            mixer.init()
                            pygame.mixer_music.load(SYSTEM_SOUNDS_FINISH)
                            mixer.music.play()
                            switch_page_to_show_game(category)
                    else:
                        self.word = self.word[0:len(self.word) - 1]
                        self.indx_word -= 1
                        mixer.init()
                        pygame.mixer_music.load(SYSTEM_SOUNDS_INCORRECT)
                        mixer.music.play()

            # print(q)

            # очистить предыдущие кнопки (очищает кнопки, но в списке extend остается)
            def all_children(window):
                _list = window.winfo_children()

                for item in _list:
                    if item.winfo_children():
                        _list.extend(item.winfo_children())

                return _list

            widget_list = all_children(symbolsFrame)
            for item in widget_list:
                item.destroy()

            # генерация кнопок
            v = []
            s = (1, len(q))
            a = np.zeros((s))
            for i in range(0, a.shape[0]):
                for j in range(0, a.shape[1]):
                    b = tk.Button(symbolsFrame, text=q[j], font=LARGE_FONT_BOLD, bg="white",
                                  command=lambda j=j: pazzleAddSymb(q[j]))  # print(q[j]))
                    b.grid(row=i, column=j, padx=3)
                    # v.append(b)

    def show_pazzle(self, pazzleCountQuestion, category):
        nums, wordsEst, wordsRus = self.generate_question(5, category)

        return self.questions("rus", pazzleCountQuestion, nums, wordsEst, wordsRus)

    def questions(self, type, pazzleCountQuestion, nums, wordsEst, wordsRus):
        if type == "rus":
            wordRusForShow = wordsRus[pazzleCountQuestion]  # рус слово по первому индексу в списке рандомных цифр
            wordEstForAnswer = wordsEst[pazzleCountQuestion]  # эст слово по первому индексу в списке рандомных цифр
            # print(wordRusForShow)
            # print(wordEstForAnswer)

            wordEstForAnswerSymb = []

            # Получаем строку в символах
            for i in wordEstForAnswer:
                wordEstForAnswerSymb.append(i)

            resWithRandomSymb = random.sample(wordEstForAnswerSymb, len(wordEstForAnswerSymb))  # перемешать список
            return resWithRandomSymb, wordRusForShow, wordEstForAnswer, nums

    def generate_question(self, count, categories_path):
        # if lang == "rus":
        nums = []
        wordsEst = []
        wordsRus = []
        dictEst, dictRus = file_open(categories_path)
        listEst = list(dictEst)
        listRus = list(dictRus)

        while len(nums) < count:
            rand = int(random.random() * len(listEst))  # генерируем случайное число от 0 до длины списка
            if rand in nums:
                continue
            else:
                nums.append(rand)

        for i in nums:
            wordsEst.append(listEst[i])
            wordsRus.append(listRus[i])

        # print("nums: ", nums)
        # print("wordsRus: ", wordsRus)
        # print("wordsEst: ", wordsEst)
        return nums, wordsEst, wordsRus


# -----------------------------------------------------------------

app = EVTranslator()

windowsInCenter(1280, 720, app)  # Размер окна
app.resizable(False, False)  # Отключить изменение размера окна. Вертикально, горизонтально
app["bg"] = GENERAL_BG  # bg main

app.mainloop()
