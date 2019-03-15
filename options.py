from tkinter import *
import pymysql

con = pymysql.connect(host='127.0.0.1',
		      user='root',
                      password='',
 			db= 'zavod')

def addoption():
    global labelrow1add
    global labelrow2add
    valadd1 = labelrow1add.get()
    valadd2 = labelrow2add.get()
    if valadd1=='':
        lbl_message["text"] = u"Введите название параметра"
        lbl_message["bg"] = "red"
        lbl_message["width"] = "100"
        lbl_message["height"] = "5"
        return 0
    if valadd2=='':
        lbl_message["text"] = u"Введите значение параметра"
        lbl_message["bg"] = "red"
        lbl_message["width"] = "100"
        lbl_message["height"] = "5"
        return 0

    with con:
        cur = con.cursor()
        sql="insert into options set value=%s, name=%s";
        strarr = (valadd2, valadd1)
        cur.execute(sql, strarr)
        con.commit()
    showoptiongrid()
    frame_tab3.grid()
    lbl_message["text"]=u"Запись сохранена"
    lbl_message["bg"]="red"
    lbl_message["width"] = "100"
    lbl_message["height"] = "5"

def saveoption(id):
    val=labelrow3[id].get()
    with con:
        cur = con.cursor()
        sql="update options set value=%s where id=%s";
        strarr = (val, id)
        cur.execute(sql, strarr)
        con.commit()
    showoptiongrid()
    frame_tab3.grid()
    lbl_message["text"]=u"Запись сохранена"
    lbl_message["bg"]="red"
    lbl_message["width"] = "100"
    lbl_message["height"] = "5"

def showoptiongrid():
    global  labelrow1add
    global  labelrow2add

    for widget in frame_tab3.winfo_children():
        widget.destroy()
    frame_tab3.grid(row=5, column=0, columnspan="5")
    with con.cursor() as cur:
        # Read a single record
        sql = "SELECT * FROM `options` order by id asc"
        cur.execute(sql)
        i = 4
        labelrow4 = {}
        labelrow1h = Label(frame_tab3, width="5", text="ID", font=("Tahoma", 10), padx=10, pady=10, bg="lightgreen")
        labelrow1h.grid(row=0, column=0)
        labelrow1h = Label(frame_tab3, width="30", text="Параметр", font=("Tahoma", 10), padx=10, pady=10, bg="lightgreen")
        labelrow1h.grid(row=0, column=1)
        labelrow2h = Label(frame_tab3, width="30", text=u"Текущее значение", font=("Tahoma", 10), padx=10, pady=10, bg="lightgreen")
        labelrow2h.grid(row=0, column=2)
        labelrow2h = Label(frame_tab3, width="30", text=u"Новое значение", font=("Tahoma", 10), padx=10, pady=10, bg="lightgreen")
        labelrow2h.grid(row=0, column=3)
        if cur.rowcount > 0:
            for row in cur:
                labelrow1 = Label(frame_tab3, width="5", text=row[0], font=("Tahoma", 10), padx=10, pady=10)
                labelrow1.grid(row=i, column=0, padx=1, pady=1)
                labelrow1 = Label(frame_tab3, width="30", text=row[1], font=("Tahoma", 10), padx=10, pady=10)
                labelrow1.grid(row=i, column=1, padx=1, pady=1)
                labelrow2 = Label(frame_tab3, width="30", text=row[2], font=("Tahoma", 10), padx=10, pady=10)
                labelrow2.grid(row=i, column=2, padx=1, pady=1)
                labelrow3[row[0]] = Entry(frame_tab3, width="30")
                labelrow3[row[0]].insert(0, row[2])
                labelrow3[row[0]].grid(row=i, column=3)
                labelrow4[row[0]]=Button(frame_tab3, text="Сохранить", width="30", command=lambda k=row[0]: saveoption(k))
                labelrow4[row[0]].grid(row=i, column=4)
                i = i + 1

    frame_tab3.grid(row=5, column=0, columnspan="5")
    frame_tab3.grid_remove()
root = Tk()


lbl_head = Label(root, text=u"РАСКРОЙ ШТАПИКА: Настройки", font=("Tahoma", 15), bg="white")
lbl_message = Label(root, text="", font=("Tahoma", 12), width="0", height="0", bg="white")
lbl_message.grid(row=1, columnspan=5)
lbl_head.grid(row=0, column=0)



labelrow3 = {}
labelrowaddh = Label(root, width="150", text="НОВАЯ ЗАПИСЬ", font=("Tahoma", 10), padx=10, pady=10, bg="yellow")
labelrowaddh.grid(row=2, columnspan=5, padx=1, pady=1)
labelrow1h = Label(root, width="80", text="Название параметра", font=("Tahoma", 10), padx=10, pady=10,
                   bg="lightgreen")
labelrow1h.grid(row=3, columnspan=3, padx=1, pady=1)
labelrow1h = Label(root, width="30", text="Значение параметра", font=("Tahoma", 10), padx=10, pady=10,
                   bg="lightgreen")
labelrow1h.grid(row=3, column=3, padx=1, pady=1)
labelrowbut = Button(root, text="Добавить запись", width="30", command=addoption)
labelrowbut.grid(row=4, column=4)
labelrow1add = Entry(root, width="80")
labelrow2add = Entry(root, width="30")

labelrow1add.grid(row=4, columnspan=3)
labelrow2add.grid(row=4, column=3)

mycolor2 = '#40E0D0'
frame_tab3 = Frame(root, bg=mycolor2, bd=25)

showoptiongrid()
frame_tab3.grid()

root.title(u"Раскрой штапика")
root.geometry('2056x1024')
root.configure(bg="white")
root.mainloop()
