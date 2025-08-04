import os
import requests
from tkinter import *
from tkinter import Tk, messagebox as mb
from tkinter import filedialog as fd
from tkinter import ttk
from tkinter import font
from PIL import Image, ImageTk
from comet_ml.logging_extensions.rich_decoration.environment import width

cryptos = ['BTC','ETH','XRP','USDT','BNB','SOL','USDC','TRX','DOGE','ADA','HYPE','SUI','XLM','LINK','BCH','HBAR','WBT',
           'AVAX','USDE','TON']
fiats = ['USD','EUR','GBP','BYN','BGN','KRW','INR','CNY','PLN','TRY','UZS','UAH','CHF','JPY']

def select():
    """Подтягивает тип валюты в соответствии с выбором - fiat или crypto"""
    if selected_currency.get() == 'crypto':
        entry_base.config(values=cryptos)
        entry_target.config(values=cryptos)
    else:
        entry_base.config(values=fiats)
        entry_target.config(values=fiats)


def get_rate():
    """Запрашиваем курс криптовалюты на удаленном ресурсе"""
    base = entry_base.get()
    target = entry_target.get()
    try:
        url = f'https://min-api.cryptocompare.com/data/pricemulti?fsyms={base}&tsyms={target}'
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        rate = data[base][target]
        return rate
    except Exception:
        messagebox.showerror('Ошибка!','Выберите валюту из предложенного списка!')


def update_win(event = None):
    """Оформляем и выводим результат запроса..."""
    rate = get_rate()
    if rate:
        string = f'{entry_base.get()} / {entry_target.get()}: {rate}'
        result_label.config(text=string)
        logger.insert(1.0,f'{string}\n')
    else:
        result_label.config(text=f'')


def swap():
    """ Меняет валюты местами для получения кросс-курса"""
    base = entry_base.get()
    target = entry_target.get()
    if base and target:
        entry_base.delete(0,END)
        entry_base.insert(END,target)
        entry_target.delete(0,END)
        entry_target.insert(END, base)


def start_progress():
    progress['value'] = 0
    progress.start(30)
    window.after(3000, lambda: [progress.stop(), update_win()])


def export_logger():
    """ Создает файл с результатами запросов"""
    file_name = 'logger_export.txt'
    save_path = fd.askdirectory()
    if save_path:
        file_path = os.path.join(save_path,file_name)
        with open(file_path,'w', encoding='utf-8') as f:
            origin = logger.get(1.0, END).split('\n')
            for line in origin:
                f.write(f'{line}\n')
        mb.showinfo('К сведению!', f'Файл "{file_name}" сохранен в папке: {save_path}')


def getout():
    """Выходим из приложения."""
    window.destroy()

window = Tk()
window.title('Курсы криптовалют.')
window.geometry('330x320+650+250')

# создаем набор вкладок
notebook = ttk.Notebook()
notebook.pack()

# создаем пару фреймвов
frame1 = Frame(notebook)
frame2 = Frame(notebook)
frame3 = Frame(notebook)
frame1.grid()
frame2.grid()
frame3.grid()
frame1.config(width=300, height=400)


# добавляем фреймы в качестве вкладок
notebook.add(frame1, text="Кусры криптовалют", )
notebook.add(frame2, text="Логгер")
notebook.add(frame3, text="Справка")

style = ttk.Style()
style.configure("Custom.Horizontal.TProgressbar", troughcolor='#f0f0f0', background='#AE5BF0')

font_titel = font.Font(family= "Aptos", size=12, weight="bold", slant="roman")
font_result = font.Font(family= "Calibri", size=10, weight="normal", slant="roman")
font_logger = font.Font(family= "Arial Narrow", size=10, weight="normal", slant="roman")

intro_label = ttk.Label(frame1, text='ВВЕДИТЕ ВАЛЮТУ:', font=font_titel)
intro_label.grid(row=1, columnspan=2,pady=3)

selected_currency = StringVar(value='crypto')  # по умолчанию выборана crypto

cr_rbtn = ttk.Radiobutton(frame1,text='crypto', value='crypto', variable=selected_currency, command=select)
cr_rbtn.grid(row=2, column=0, padx=10, pady=5)

trg_rbtn = ttk.Radiobutton(frame1,text='fiat', value='fiat', variable=selected_currency, command=select)
trg_rbtn.grid(row=2, column=1, padx=10, pady=5)

base_lbl = ttk.Label(frame1, text='Базовую:')
base_lbl.grid(row=3, column=0)

targ_lbl = ttk.Label(frame1, text='Номинальную:')
targ_lbl.grid(row=3, column=1,padx=60)

entry_base = ttk.Combobox(frame1, values=cryptos,width=10)
entry_base.grid(row=4,column=0,padx=25,pady=5)

entry_target = ttk.Combobox(frame1, values=cryptos,width=10)
entry_target.grid(row=4, column=1,pady=5)

# Загружаем изображение
image = Image.open("swap_icon.png")  # Убедитесь, что путь к файлу правильный
image = image.resize((30, 30), Image.LANCZOS)  # Изменяем размер, если нужно
icon = ImageTk.PhotoImage(image)

swap_btn = ttk.Button(frame1,image=icon, command=swap, width=20)
swap_btn.place(x=130, y=80)

button = ttk.Button(frame1, text='Получить курс обмена', command=start_progress, width=41)
button.place(x=22, y=130)

progress = ttk.Progressbar(frame1,style="Custom.Horizontal.TProgressbar", mode='determinate', length=260)
progress.place(x=20, y=237)  # Измените координаты по необходимости

result_label = ttk.Label(frame1, text='', font=font_result)
result_label.place(x=20,y=170)

exit_btn = ttk.Button(frame1, text='Выход', command=getout)
exit_btn.place(x=115, y=200)


logger = Text(frame2, font=font_logger, width=40, height=15, bg='white', fg='black')
logger.pack(side=LEFT)

scroll = ttk.Scrollbar(frame2 ,orient='vertical', command=logger.yview)
scroll.pack(side=RIGHT)
logger.config(yscrollcommand=scroll.set)

btn = ttk.Button(frame2, text='Экспорт', width=8, command=export_logger)
btn.pack()

text = (''
'Настоящее Программное обеспечение (ПО\n\
представляет собой Итоговую Аттестационную\n\
работу студента\nБойко С.А\n\
по программе профессиональной переподготовки\n\
«Азбука цифры. Программирование на языке\n\
Python от базового уровня до продвинутого»\n\
Центра повышения квалификации и \n\
профессиональной подготовки «Основание» \n\
при Томском Государственной Университете.')

about_lbl = ttk.Label(frame3,text=text)
about_lbl.pack(side='top')

img = PhotoImage(file='Logo.png')
a = Label(frame3,image=img,compound=BOTTOM)
a.pack()

window.mainloop()