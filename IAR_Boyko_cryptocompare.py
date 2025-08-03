import requests
from tkinter import *
from tkinter import Tk, messagebox
from tkinter import ttk
from tkinter import font
from PIL import Image, ImageTk

cryptos = ['BTC','ETH','XRP','USDT','BNB','SOL','USDC','TRX','DOGE','ADA','HYPE','SUI','XLM','LINK','BCH','HBAR','WBT',
           'AVAX','USDE','TON']

fiats = ['USD','EUR','GBP','BYN','BGN','KRW','INR','CNY','PLN','TRY','UZS','UAH','CHF','JPY']

def select():
    if selected_currency.get() == 'crypto':
        entry_base.config(values=cryptos)
        entry_target.config(values=cryptos)
    else:
        entry_base.config(values=fiats)
        entry_target.config(values=fiats)


def get_rate():
    base = entry_base.get()
    target = entry_target.get()
    try:
        url = f'https://min-api.cryptocompare.com/data/pricemulti?fsyms={base}&tsyms={target}'
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        rate = data[base][target]
        return rate
    except Exception as e:
        messagebox.showerror('Ошибка!','Выберите валюту из предложенного списка!')


def update_win(event = None):
    if get_rate():
        result_label.config(text=f'{entry_base.get()} / {entry_target.get()} = {get_rate()}')
    else:
        result_label.config(text=f'')


def swap():
    base = entry_base.get()
    target = entry_target.get()
    if base != False and target != False:
        entry_base.delete(0,END)
        entry_base.insert(END,target)
        entry_target.delete(0,END)
        entry_target.insert(END, base)
        update_win()

def getout():
    window.destroy()

window = Tk()
window.title('Курсы криптовалют.')
window.geometry('330x280+650+250')

font_titel = font.Font(family= "Aptos", size=12, weight="bold", slant="roman")
font_result = font.Font(family= "Aptos", size=16, weight="bold", slant="roman")

intro_label = ttk.Label(window, text='ВВЕДИТЕ ВАЛЮТУ:', font=font_titel)
intro_label.grid(row=0, columnspan=2,pady=10)

selected_currency = StringVar(value='crypto')  # по умолчанию ничего не выборанно

cr_rbtn = ttk.Radiobutton(text='crypto', value='crypto', variable=selected_currency, command=select)
cr_rbtn.grid(row=1, column=0, padx=10, pady=5)

trg_rbtn = ttk.Radiobutton(text='fiat', value='fiat', variable=selected_currency, command=select)
trg_rbtn.grid(row=1, column=1, padx=10, pady=5)

base_lbl = ttk.Label(window, text='Базовую:')
base_lbl.grid(row=2, column=0)

targ_lbl = ttk.Label(window, text='Номинальную:')
targ_lbl.grid(row=2, column=1,padx=60)

entry_base = ttk.Combobox(window, values=cryptos,width=10)
entry_base.grid(row=3,column=0,padx=25,pady=5)

entry_target = ttk.Combobox(window, values=cryptos,width=10)
entry_target.grid(row=3, column=1,pady=5)

# Загружаем изображение
image = Image.open("swap_icon.png")  # Убедитесь, что путь к файлу правильный
image = image.resize((30, 30), Image.LANCZOS)  # Изменяем размер, если нужно
icon = ImageTk.PhotoImage(image)

swap_btn = ttk.Button(window,image=icon, command=swap, width=20)
swap_btn.place(x=130, y=80)

button = ttk.Button(window, text='Получить курс обмена', command=update_win, width=41)
button.place(x=22, y=125)

result_label = ttk.Label(window, text='', font=font_result)
result_label.place(x=50,y=170)

exit_btn = ttk.Button(window, text='Выход', command=getout)
exit_btn.place(x=115, y=225)

window.mainloop()


