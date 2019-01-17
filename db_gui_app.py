import sqlite3

class DB:
    """
    Класс для работы с базой данных.
    """
    def __init__(self):
        self.con = sqlite3.connect("uhtt.db")
        self.cur = self.con.cursor()
    
    def __del__(self):
        self.con.close()

from tkinter import *

def search_barcodes(barcodes, db_cursor):
    """
    Поиск штрикодов из списка в бд.
    """
    print("ищу коды")
    result = []
    for bc in barcodes:
        print(bc)
        print(type(bc))
        db_cursor.execute("SELECT * from uhtt_barcode where UPCEAN=?;", (bc,))
        # _ кортеж с инфой из колонок или None, если ничего не найдено
        _ = db_cursor.fetchone()
        if _ :
            result.append(_[2] + " " + _[1])
        else:
            result.append("{} не найден".format(bc))
    return result
    
def get_items_by_barcodes(barcodes, widget, db_cursor):
    """
    Обрабочик для кнопки "Поиск".
    Принимает список штрикодов barcodes, выполняет поиск товаров по данным штрикодам,
    и выводит инфу о товарах на через widget.
    """
    print("зашел в гет итемс")
    info = search_barcodes(barcodes, db_cursor)
    for _ in info:
        widget.insert(END, _)
        widget.insert(END, "\n")    
        print("добавил текст")
        
    
# топ-лвл виджет
root = Tk()
db = DB()
# создание виджетов
barcode_list_text = Text(root,height=20,width=20,font='Arial 14')
goods_info_text = Text(root,height=20,width=60,font='Arial 14')
search_button = Button(root, bg="red", text="Поиск", command=(lambda: get_items_by_barcodes(barcode_list_text.get("1.0", END).split(), goods_info_text, db.cur)))

# расположение виджетов
barcode_list_text.pack(side=LEFT)
goods_info_text.pack(side=RIGHT)
search_button.pack(side=BOTTOM)
root.mainloop()
del(db)