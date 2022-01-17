import hashlib
import os
import tkinter.filedialog
from tkinter import Button, Entry, Label, Tk

sig_files = []
uniq = set()
deleted = bool
file_counter, duplicate_work = 0, 0


def clicked_dest():
    global destination_folder
    destination_folder = tkinter.filedialog.askdirectory()
    entry_dest.insert(0, destination_folder)


def clicked_work():
    global work_direct
    work_direct = tkinter.filedialog.askdirectory()
    entry_work.insert(0, work_direct)


def clicked_exit():
    raise SystemExit('Pressed Exit key')


def scan_files(patch, file_deleted):
    global file_counter
    global duplicate_work

    for root, dirs, files in os.walk(patch):
        for file in files:
            path = os.path.join(root, file)
            with open(path, 'rb') as f:
                file_counter += 1
                sig = hashlib.md5(open(path, 'rb').read()).hexdigest()
                if not file_deleted:
                    if sig not in uniq:
                        uniq.add(sig)
                        print(f'{str(file_counter)} {sig} {path}')
                else:
                    if sig in uniq:
                        f.close()
                        os.remove(path)
                        print(f'Удален: {path}')
                        duplicate_work += 1


def clicked_run():
    global file_counter
    global duplicate_work

    scan_files(destination_folder, False)
    scan_files(work_direct, True)

    print(f'Обработано файлов: {file_counter}')
    print(f'Удалено дубликатов в конечной папке: {duplicate_work}')


def add_button(title, run_command, x, y, heigh, width):
    Button(
        window,
        text=title,
        background='#555',
        foreground='#ccc',
        command=run_command
    ).place(x=x, y=y, heigh=heigh, width=width)
    return Button


window = Tk()
window.title('Foto Script')
window.geometry('400x150')
window.resizable(False, False)

Label(window, text='Назначение :', font=10).place(x=10, y=5)
entry_dest = Entry(window, font=9)
entry_dest.place(x=10, y=30, width=330)
add_button('...', clicked_dest, 350, 30, 22, 30)
Label(window, text='Обрабатывать :', font=10).place(x=10, y=55)
entry_work = Entry(window, font=9)
entry_work.place(x=10, y=80, width=330)
add_button('...', clicked_work, 350, 80, 22, 30)
add_button('Run', clicked_run, 10, 110, 30, 90)
add_button('Выход', clicked_exit, 300, 110, 30, 90)
window.mainloop()
