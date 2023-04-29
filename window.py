import os
from tkinter import *
from tkinter import filedialog
from tkinter.messagebox import showinfo
from database import sqlite_connection

global description
global image_frame
global image_bytes

window = Tk()
cursor = sqlite_connection.cursor()

listbox = Listbox(window, width=35, height=50)


def create_window():
    window.title('Знаменитые писатели России')
    binds()

    window.geometry('1280x720')
    window.minsize(1280, 720)
    window.maxsize(1280, 720)

    create_interface()
    menu_bar()
    key_info()
    window.focus()
    window.mainloop()
    if os.path.exists('temp.png'):
        os.remove('temp.png')


def menu_bar():
    menubar = Menu(window)

    file_menu = Menu(menubar, tearoff=0)
    help_menu = Menu(menubar, tearoff=0)

    file_menu.add_command(label='Найти...', command=search_popup)
    file_menu.add_separator()

    file_menu.add_command(label='Добавить F2', command=add_popup)
    file_menu.add_command(label='Удалить F3', command=remove_event)
    file_menu.add_command(label='Изменить F4', command=edit_popup)
    file_menu.add_separator()

    file_menu.add_command(label='Выход Ctrl+X', command=window.quit)
    help_menu.add_command(label='Содержание', command=consistence)
    help_menu.add_separator()

    help_menu.add_command(label='О программе', command=about_program)

    menubar.add_cascade(label='Фонд', menu=file_menu)
    menubar.add_cascade(label='Справка', menu=help_menu)

    window.config(menu=menubar)


def key_info():
    label = Label(window, fg='white', bg='blue', text='F1-справка F2-добавить F3-удалить F4-изменить')
    label.pack(fill=X, side=BOTTOM)


def consistence():
    popup = Toplevel()
    popup.focus()

    popup.title('Содержание')
    popup.geometry("345x145")
    popup.minsize(345, 145)
    popup.maxsize(345, 145)

    label = Label(popup, justify=LEFT,
                  text='База данных \'Знаменитые математики России\'\nПозволяет: добавлять / изменять / удалять\nинформацию.\nКлавиши программы:\nF1-вызов справки по программе,\nF2-добавить в базу данных,\nF3-удалить из базы данных,\nF4-изменить запись в базе данных')
    label.pack(side=TOP, anchor='w')

    exit_button = Button(popup, text='Закрыть', command=popup.destroy)
    exit_button.place(x=280, y=110)


def about_program():
    showinfo('О программе', 'База данных \'Знаменитые математики России\'\n(c) Ильин А.В, Russia, 2023')


def binds():
    window.bind('<Control-x>', window_destroy_bind)
    window.bind('<F2>', add_bind)
    window.bind('<F3>', remove_bind)
    window.bind('<F4>', edit_bind)
    window.bind('<F10>', open_menu_bind)


def create_interface():
    fio_request = cursor.execute('''SELECT fio FROM writer''').fetchall()

    for i in range(len(fio_request)):
        listbox.insert(END, fio_request[i][0])

    listbox.pack(expand=True, fill=Y)
    listbox.place(x=1, y=1)
    listbox.bind('<<ListboxSelect>>', selection)

    person_photo('empty_img.png')
    person_description('')


def person_photo(img):
    global image_frame

    image_frame = Frame(window, width=605, height=690)
    image_frame.place(x=215, y=1)
    image_frame.picture = PhotoImage(file=img)

    image_frame.label = Label(image_frame, image=image_frame.picture, width=605, height=690)
    image_frame.label.pack()


def image_scale(image, width, height):
    w = image.width()
    h = image.height()
    if (w + h) < (width + height):
        return image.zoom(2)
    subsample = int((width + height) / (w + h))
    return image.subsample(subsample, subsample)


def person_description(desc):
    global description

    description = Text(window, width=50)
    description.insert(INSERT, desc)
    description.pack(expand=True, fill=Y, anchor=E)
    description.config(font=('Times New Roman', 14), state=DISABLED)


def selection(e):
    get_selection()


def get_selection():
    global description
    global image_frame

    selection_list = ['empty_img.png', '']

    selection = listbox.curselection()

    if len(selection) != 0:
        photo_request = cursor.execute('''SELECT photo FROM writer WHERE fio=?''',
                                       (listbox.get(selection[0]),)).fetchone()

        if photo_request[0] is not None:
            image_frame.destroy()
            person_photo(extract_from_binary(photo_request[0]))
            selection_list[0] = extract_from_binary(photo_request[0])
        else:
            image_frame.destroy()
            person_photo('empty_img.png')

        description_request = cursor.execute('''SELECT description FROM writer WHERE fio=?''',
                                             (listbox.get(selection[0]),)).fetchone()

        if description_request[0] is not None:
            description.destroy()
            person_description(description_request[0])
            selection_list[1] = description_request[0]
        else:
            description.destroy()
            person_description('')

        return selection_list


def window_destroy_bind(e):
    window.quit()


def open_menu_bind(e):
    pass


def add_bind(e):
    add_popup()


def add_popup():
    menu_popup('', '', 'empty_img.png', 'Добавить')


def menu_popup(name, description, photo, action):
    global image_bytes
    with open(photo, 'rb') as file:
        image_bytes = file.read()

    popup = Toplevel(window)
    popup.geometry('768x432')
    popup.resizable(FALSE, FALSE)
    popup.grab_set()
    popup.focus()

    name_label = Label(popup, text='ФИО')
    name_label.place(x=10, y=5)
    name_field = Entry(popup, width=50)
    name_field.insert(INSERT, name)
    name_field.place(x=10, y=30)

    description_label = Label(popup, text='Описание')
    description_label.place(x=10, y=50)
    description_field = Text(popup, width=37)
    description_field.insert(INSERT, description)
    description_field.place(x=10, y=74)

    image_label = Label(popup, text='Фото')
    image_label.place(x=400, y=5)
    image_frame_popup = Frame(popup, width=300, height=350, bg='white')
    image_frame_popup.place(x=400, y=30)
    image_frame_popup.picture = PhotoImage(file=photo)
    image_frame_popup.label = Label(image_frame_popup, image=image_frame_popup.picture, width=300, height=350)
    image_frame_popup.label.pack()

    if action == 'Добавить':
        add_button = Button(popup, text=action, command=lambda: add_confirmation(popup,
                                                                                     name_field.get(),
                                                                                     description_field.get('1.0', END),
                                                                                     image_bytes))
    else:
        add_button = Button(popup, text=action, command=lambda: edit_confirmation(popup,
                                                                             name_field.get(),
                                                                             description_field.get('1.0', END),
                                                                             image_bytes))
    exit_button = Button(popup, text='Закрыть', command=popup.destroy)
    search_button = Button(popup, text='Обзор', command=lambda: get_image_bytes(image_frame_popup))

    add_button.place(x=700, y=400)
    exit_button.place(x=640, y=400)
    search_button.place(x=520, y=390)


def get_image_bytes(image_frame_popup):
    global image_bytes
    image_bytes = convert_to_binary()

    image = extract_from_binary(image_bytes)
    image_frame_popup.picture = PhotoImage(file=image)
    image_frame_popup.label.destroy()
    image_frame_popup.label = Label(image_frame_popup, image=image_frame_popup.picture, width=300, height=350)
    image_frame_popup.label.pack()


def convert_to_binary():
    with open(filedialog.askopenfilename(), 'rb') as file:
        blob_data = file.read()
    return blob_data


def extract_from_binary(blob):
    with open('temp.png', 'wb') as temp:
        temp.write(blob)
    return temp.name


def add_confirmation(popup, name_text, description_text, image):
    global description
    global image_frame

    if len(name_text) != 0:
        listbox.insert(END, name_text)
        cursor.execute('''INSERT INTO writer(fio, description, photo) VALUES(?,?,?)''',
                       (name_text, description_text, image))
        if len(listbox.curselection()) != 0:
            listbox.selection_clear(0, END)
        listbox.selection_set(listbox.get(0, END).index(name_text))
        selection('')
        sqlite_connection.commit()
    popup.destroy()


def edit_confirmation(popup, name_text, description_text, image):
    global description
    global image_frame

    if len(name_text) != 0:
        cursor.execute('''UPDATE writer SET description = ?, photo = ? WHERE fio = ?''',
                       (description_text, image, name_text))
        if len(listbox.curselection()) != 0:
            listbox.selection_clear(0, END)
        listbox.selection_set(listbox.get(0, END).index(name_text))
        selection('')
        sqlite_connection.commit()
    popup.destroy()


def remove_bind(e):
    remove_event()


def remove_event():
    selection = listbox.curselection()
    if len(selection) == 1:
        cursor.execute('''DELETE FROM writer WHERE fio=?''', (listbox.get(selection[0]),))
        listbox.delete(selection[0])
        sqlite_connection.commit()

        description.destroy()
        person_description('')

        image_frame.destroy()
        person_photo('empty_img.png')


def edit_bind(e):
    edit_popup()


def edit_popup():
    selection = listbox.curselection()
    if len(selection) != 0:
        selection_list = get_selection()
        menu_popup(listbox.get(selection[0]), selection_list[1], selection_list[0], 'Изменить')


def search_popup():
    popup = Toplevel()
    popup.grab_set()
    popup.geometry('200x50')
    popup.resizable(FALSE, FALSE)

    popup.label = Label(popup, text='Поиск')
    popup.label.pack(anchor=NW, padx=5)

    entry_text = StringVar()
    popup.entry = Entry(popup, textvariable=entry_text)
    popup.entry.pack(anchor=SW, padx=5)

    popup.button = Button(popup, text='Найти', command=lambda: search_selection(popup, popup.entry.get()))
    popup.button.place(x=145, y=20)


def search_selection(popup, text):
    if len(text) != 0 and text in listbox.get(0, END):
        if len(listbox.curselection()) != 0:
            listbox.selection_clear(0, END)
        listbox.selection_set(listbox.get(0, END).index(text))
        selection('')
        popup.destroy()
