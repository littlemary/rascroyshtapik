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
    val_name=labelrow1[id].get()

    with con:
        cur = con.cursor()
        sql="update options set value=%s, name=%s where id=%s";
        strarr = (val, val_name, id)
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
    canvas = Canvas(frame_tab3, bg="grey")
    canvas.grid(row=0, column=0)

    # Create a vertical scrollbar linked to the canvas.
    vsbar = Scrollbar(frame_tab3, orient=VERTICAL, command=canvas.yview)
    vsbar.grid(row=0, column=1, sticky=NS)
    canvas.configure(yscrollcommand=vsbar.set)

    # Create a horizontal scrollbar linked to the canvas.
    hsbar = Scrollbar(frame_tab3, orient=HORIZONTAL, command=canvas.xview)
    hsbar.grid(row=1, column=0, sticky=EW)
    canvas.configure(xscrollcommand=hsbar.set)

    # Create a frame on the canvas to contain the buttons.
    frame_c = Frame(canvas, bg="grey", bd=2)

    with con.cursor() as cur:
        # Read a single record
        sql = "SELECT * FROM `options` order by id asc"
        cur.execute(sql)
        i = 4
        labelrow4 = {}
        labelrow1h = Label(frame_c, width="5", text="ID", font=("Tahoma", 10), padx=10, pady=10, bg="lightgreen")
        labelrow1h.grid(row=0, column=0)
        labelrow1h = Label(frame_c, width="30", text="Параметр", font=("Tahoma", 10), padx=10, pady=10, bg="lightgreen")
        labelrow1h.grid(row=0, column=1)
        labelrow2h = Label(frame_c, width="30", text=u"Текущее значение", font=("Tahoma", 10), padx=10, pady=10, bg="lightgreen")
        labelrow2h.grid(row=0, column=2)
        labelrow2h = Label(frame_c, width="30", text=u"Новое значение", font=("Tahoma", 10), padx=10, pady=10, bg="lightgreen")
        labelrow2h.grid(row=0, column=3)
        if cur.rowcount > 0:
            for row in cur:
                labelrowid = Label(frame_c, width="5", text=row[0], font=("Tahoma", 10), padx=10, pady=10)
                labelrowid.grid(row=i, column=0, padx=1, pady=1)
                labelrow1[row[0]] = Entry(frame_c, width="30")
                labelrow1[row[0]].insert(0, row[1])
                labelrow1[row[0]].grid(row=i, column=1)
                labelrow2 = Label(frame_c, width="30", text=row[2], font=("Tahoma", 10), padx=10, pady=10)
                labelrow2.grid(row=i, column=2, padx=1, pady=1)
                labelrow3[row[0]] = Entry(frame_c, width="30")
                labelrow3[row[0]].insert(0, row[2])
                labelrow3[row[0]].grid(row=i, column=3)
                labelrow4[row[0]]=Button(frame_c, text="Сохранить", width="30", command=lambda k=row[0]: saveoption(k))
                labelrow4[row[0]].grid(row=i, column=4)
                i = i + 1


    canvas.create_window((0, 0), window=frame_c, anchor=NW)
    frame_c.update_idletasks()  # Needed to make bbox info available.
    bbox = canvas.bbox(ALL)  # Get bounding box of canvas with Buttons.
    ROWS, COLS = i, 4  # Size of grid.
    ROWS_DISP = 12  # Number of rows to display.
    COLS_DISP = 4  # Number of columns to display.
    w, h = bbox[2] - bbox[1], bbox[3] - bbox[1]
    dw, dh = int((w / COLS) * COLS_DISP), int((h / ROWS) * ROWS_DISP)
    canvas.configure(scrollregion=bbox, width=dw, height=dh)

    frame_tab3.grid(row=5, column=0, columnspan="5")
    frame_tab3.grid_remove()
root = Tk()


lbl_head = Label(root, text=u"РАСКРОЙ ШТАПИКА: Настройки", font=("Tahoma", 15), bg="white")
lbl_message = Label(root, text="", font=("Tahoma", 12), width="0", height="0", bg="white")
lbl_message.grid(row=1, columnspan=5)
lbl_head.grid(row=0, column=0)



labelrow3 = {}
labelrow1 = {}
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
root.geometry('1050x1024')
root.configure(bg="white")
root.mainloop()
