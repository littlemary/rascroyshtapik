from tkinter import *
import pymysql

con = pymysql.connect(host='127.0.0.1',
		      user='root',
                      password='',
 			db= 'zavod')


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
    for widget in frame_tab3.winfo_children():
        widget.destroy()
    frame_tab3.grid(row=5, column=0, columnspan="5")
    with con.cursor() as cur:
        # Read a single record
        sql = "SELECT * FROM `options` order by id asc"
        cur.execute(sql)
        i = 1
        labelrow4 = {}
        labelrow1h = Label(frame_tab3, width="30", text="Параметр", font=("Tahoma", 10), padx=10, pady=10, bg="lightgreen")
        labelrow1h.grid(row=0, column=0)
        labelrow2h = Label(frame_tab3, width="30", text=u"Текущее значение", font=("Tahoma", 10), padx=10, pady=10, bg="lightgreen")
        labelrow2h.grid(row=0, column=1)
        labelrow2h = Label(frame_tab3, width="30", text=u"Новое значение", font=("Tahoma", 10), padx=10, pady=10, bg="lightgreen")
        labelrow2h.grid(row=0, column=2)
        if cur.rowcount > 0:
            for row in cur:
                labelrow1 = Label(frame_tab3, width="30", text=row[1], font=("Tahoma", 10), padx=10, pady=10)
                labelrow1.grid(row=i, column=0, padx=1, pady=1)
                labelrow2 = Label(frame_tab3, width="30", text=row[2], font=("Tahoma", 10), padx=10, pady=10)
                labelrow2.grid(row=i, column=1, padx=1, pady=1)
                labelrow3[row[0]] = Entry(frame_tab3, width="30")
                labelrow3[row[0]].insert(0, row[2])
                labelrow3[row[0]].grid(row=i, column=2)
                labelrow4[row[0]]=Button(frame_tab3, text="Сохранить", width="30", command=lambda k=row[0]: saveoption(k))
                labelrow4[row[0]].grid(row=i, column=3)
                i = i + 1

    frame_tab3.grid(row=5, column=0, columnspan="5")
    frame_tab3.grid_remove()
root = Tk()


lbl_head = Label(root, text=u"РАСКРОЙ ШТАПИКА: Настройки", font=("Tahoma", 15), bg="white")
lbl_message = Label(root, text="", font=("Tahoma", 12), width="0", height="0", bg="white")
lbl_message.grid(row=1, columnspan=4)
lbl_head.grid(row=0, column=0)


mycolor2 = '#40E0D0'
frame_tab3 = Frame(root, bg=mycolor2, bd=25)

labelhead = Label(frame_tab3, text=u"Настройки")
labelhead.grid(row=1, columnspan=4)
labelrow3 = {}

showoptiongrid()
frame_tab3.grid()

root.title(u"Раскрой штапика")
root.geometry('2056x1024')
root.configure(bg="white")
root.mainloop()
