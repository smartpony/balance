from Tkinter import *
from datetime import datetime
from calendar import monthrange
import re
import urllib2


# Окно из Меню -> Параметры
class ParamWindow(Toplevel):
    # Функция сохранения параметров в конфиг-файл
    def save_to_config(self):
        # Считать текущий конфиг и заменить в нём ПИН-ы
        config_file = open('config.ini', 'r').read()
        PIN1 = self.entry_pin1.get()
        PIN2 = self.entry_pin2.get()
        regex = re.compile('PIN1=.*')        
        config_file = regex.sub('PIN1='+PIN1, config_file)
        regex = re.compile('PIN2=.*')        
        config_file = regex.sub('PIN2='+PIN2, config_file)
        # Записать новый конфиг в файл
        config_file_new = open('config.ini', 'w')
        config_file_new.write(config_file)
        config_file_new.close()
        # Закрыть окно
        self.destroy()

    # Инициализация класса
    def __init__(self, parent, config):
        # Инициализация суперкласса
        Toplevel.__init__(self, parent)

        # Положение, размер и заголовок окна
        self.title('Parameters')
        self.geometry('245x120+1500+700')
        self.resizable(0, 0)

        # PIN1
        self.label_pin1 = Label(self,
            width=5,
            text='PIN1:',
            font=('Courier New', '12'))
        self.label_pin1.grid(row=0,
            column=0,
            padx=20,
            pady=(14, 3),
            sticky=W)
        self.entry_pin1 = Entry(self, width=20)
        if config:
            self.entry_pin1.insert(0, config['pin1'])
        self.entry_pin1.grid(row=0,
            column=1,
            pady=(14, 3),
            sticky=W)

        # PIN2
        self.label_pin2 = Label(self,
            width=5,
            text='PIN2:',
            font=('Courier New', '12'))
        self.label_pin2.grid(row=1,
            column=0,
            padx=20,
            pady=(0, 3),
            sticky=W)
        self.entry_pin2 = Entry(self, width=20)
        if config:
            self.entry_pin2.insert(0, config['pin2'])
        self.entry_pin2.grid(row=1,
            column=1,
            pady=(0, 3),
            sticky=W)

        # Кнопка применить настройки
        self.button_apply = Button(self,
            width=8,
            height=1,
            text='OK',
            font=('Courier New', '10'),
            command=self.save_to_config)
        self.button_apply.grid(row=3,
            columnspan=2,
            padx=(35, 0),
            pady=8,
            sticky=W)

        # Кнопка отменить изменения
        self.button_cancel = Button(self,
            width=8,
            height=1,
            text='Cancel',
            font=('Courier New', '10'),
            command=self.destroy)
        self.button_cancel.grid(row=3,
            columnspan=2,
            padx=(125, 0),
            pady=8,
            sticky=W)


# Функция получения баланса и расчёт оставшихся дней
def get_balance():
    # Считать конфиг
    config = read_config()
    # Забрать счёт с сервера
    #goodnet_xml = urllib2.urlopen(config['url']).read()
    money = 500.25
    # Выдать результат
    label_balance_value['text'] = str(money) + ' RUB'
    now = datetime.now()
    month_days = monthrange(now.year, now.month)[1]
    label_days_value['text'] = int(money//(config['month_pay']/month_days))


# Открыть окно настроек
def open_params():
    param_window = ParamWindow(root, read_config())


# Считывание переменных из конфига
def read_config():
    config_file = open('config.ini', 'r')
    for line in config_file.readlines():
        if line[:4] == 'PIN1':
            PIN1 = line[5:].rstrip()
        elif line[:4] == 'PIN2':
            PIN2 = line[5:].rstrip()
        elif line[:8] == 'Interval':
            INTERVAL = line[9:].rstrip()
        elif line[:8] == 'MonthPay':
            MONTH_PAY = int(line[9:].rstrip())
        elif line[:6] == 'Server':
            URL = line[7:].rstrip()
    config_file.close()
    if PIN1 and PIN2 and INTERVAL and MONTH_PAY and URL:
        return({'pin1': PIN1,
            'pin2': PIN2,
            'interval': INTERVAL,
            'month_pay': MONTH_PAY,
            'url': URL})




# Окно с заголовком и минимальным размером
root = Tk()
root.title('Goodnet')
root.geometry('280x120+1500+700')
root.resizable(0, 0)


# Меню вверху окна
top_menu = Menu()
# Добавить меню в окно
root.config(menu=top_menu)
# Кнопка для меню, tearoff - меню нельзя вытащить из окна
menu_button = Menu(top_menu, tearoff=0)
# Добавить кнопку в меню
top_menu.add_cascade(label='Menu', menu=menu_button)
# Добавить пункты в кнопку
menu_button.add_command(label='Parameters', command=open_params)
menu_button.add_command(label='Exit', command=root.quit)

# Текст с балансом
label_balance = Label(root,
    width=8,
    text='balance:',
    font=('Courier New', '12'))
label_balance.grid(row=0,
    column=0, 
    padx=20,
    pady=(10, 3),
    sticky=W)
label_balance_value = Label(root,
    text='120.35 RUB',
    font=('Courier New', '12'))
label_balance_value.grid(row=0,
    column=1,
    padx=5,
    pady=(10,3),
    sticky=W)

# Осталось дней
label_days = Label(root,
    width=10,
    text='days left:',
    font=('Courier New', '12'))
label_days.grid(row=1,
    padx=20,
    pady=(0,10),
    column=0,
    sticky=W)
label_days_value = Label(root,
    text='10',
    font=('Courier New', '12'))
label_days_value.grid(row=1,
    padx=5,
    pady=(0,10),
    column=1,
    sticky=W)

# Кнопка обновления баланса с сервера
button_get = Button(root,
    width=12,
    height=1,
    text='update',
    font=('Courier New', '10'),
    command=get_balance)
button_get.grid(row=2,
    padx=(20,0),
    pady=5,
    columnspan=2)


# Поехали
get_balance()
root.mainloop()