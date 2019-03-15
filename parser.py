from tkinter import *
from tkinter import filedialog as fd
import serial
import re
import time
from ctypes import *
import xml.dom.minidom
import pymysql
iscolab=int(0)
curshtapik = int(0)
langsarray = []
langsbuttonarray = {}



#ser=serial.Serial("COM3", 19200, dsrdtr = 1,timeout = 0)
con = pymysql.connect(host='127.0.0.1',
		      user='root',
                      password='',
 			db= 'zavod')

def writePortGoPos(dat,positionText):
    print(dat)

    dateInput = dat[4:] + dat[0:4]
    date="01"+"10"+"1002"+"0002"+"04"+dateInput
    sum = 0
    for x in range(0, len(date), 2):
        namber = date[x:x + 2]
        sum = sum + int(namber, base=16)
    lrcHex=str(hex(((abs(sum) ^ 0xffff) + 1) & 0xffff))
    lrc = lrcHex[-2:].upper()
    date = ":" + date + lrc + "\r\n"
    if ser.isOpen():
        try:
            ser.write(bytes(date, encoding='ascii'))
        except Exception as e:
            lbl_message["text"] = u"Ошибка. " + str(e)
            lbl_message["bg"] = "red"
            lbl_message["width"] = "100"
            lbl_message["height"] = "3"
            return 0
    else:
        lbl_message["text"] = u"Не получается отослать данные на мотор"
        lbl_message["bg"] = "red"
        lbl_message["width"] = "100"
        lbl_message["height"] = "3"
        return 0

    print(bytes(date, encoding='ascii'))
    dateGoPos=":01050806FF00ED\r\n"
    if ser.isOpen():
        try:
            ser.write(bytes(dateGoPos, encoding='ascii'))
        except Exception as e:
            lbl_message["text"] = u"Ошибка. " + str(e)
            lbl_message["bg"] = "red"
            lbl_message["width"] = "100"
            lbl_message["height"] = "3"
            return 0
    return 1


def writePortCalib(dat,positionText):
    dateInput = dat[4:] + dat[0:4]
    date="01"+"10"+"1000"+"0002"+"04"+dateInput
    sum = 0
    for x in range(0, len(date), 2):
        namber = date[x:x + 2]
        sum = sum + int(namber, base=16)
    lrcHex = str(hex(((abs(sum) ^ 0xffff) + 1) & 0xffff))
    lrc = lrcHex[-2:].upper()
    date = ":" + date + lrc + "\r\n"
    if ser.isOpen():
        try:
            ser.write(bytes(date, encoding='ascii'))
        except Exception as e:
            lbl_message["text"] = u"Ошибка. " + str(e)
            lbl_message["bg"] = "red"
            lbl_message["width"] = "100"
            lbl_message["height"] = "3"
            return 0
    else:
        lbl_message["text"] = u"Не получается отослать данные на порт"
        lbl_message["bg"] = "red"
        lbl_message["width"] = "100"
        lbl_message["height"] = "3"
        return 0

    dateCalib=":01050800FF00F3\r\n"
    if ser.isOpen():
        try:
            ser.write(bytes(dateCalib, encoding='ascii'))
        except Exception as e:
            lbl_message["text"] = u"Ошибка. " + str(e)
            lbl_message["bg"] = "red"
            lbl_message["width"] = "100"
            lbl_message["height"] = "3"
            return 0
    else:
        lbl_message["text"] = u"Не получается отослать данные на порт"
        lbl_message["bg"] = "red"
        lbl_message["width"] = "100"
        lbl_message["height"] = "3"
        return 0
    return 1
    #print(bytes(dateCalib, encoding='ascii'))

def firstcolaboration():
    global optionsrow
    global iscolab
    calobrationPos = float(optionsrow[3])
    encoderDivider = float(optionsrow[4])

    positionText = calobrationPos
    positionInt=int(calobrationPos*encoderDivider)
    positionHex=str(hex(positionInt))
    position=positionHex[2:]
    for i in range(5):
        if (len(position)<8):
            position='0'+position[0:]
    dat = position.upper()
    writePortCalib(dat,positionText)
    lbl_message["text"] = u"Станок отколиброван. Можете продолжить работу"
    lbl_message["bg"] = "lightgreen"
    lbl_message["width"] = "100"
    lbl_message["height"] = "3"
    iscolab=1

def sendtoport(itemval):
    global optionsrow
    minPos = float(optionsrow[1])
    maxPos = float(optionsrow[2])
    shift1 = float(optionsrow[5])
    shift2 = float(optionsrow[6])
    shift3 = float(optionsrow[7])
    encoderDivider=float(optionsrow[4])

    position = float(itemval)
    positionText = position
    if (position <= 1000):
        shift = shift1
    elif (1000 < position and position <= 2000):
        shift = shift2
    elif (position > 2000):
        shift = shift3
    position=position+shift

    if (minPos < position and position < maxPos):

        positionInt = int(position  * encoderDivider)
        positionHex = str(hex(positionInt))
        position = positionHex[2:]
        for i in range(5):
            if (len(position) < 8):
                position = '0' + position[0:]
        dat = position.upper()
        writePortGoPos(dat, positionText)


def importfromxml():
    lbl_message["text"] = u"Подождите... Идет импортирование данных"
    lbl_message["bg"] = "lightgreen"
    lbl_message["width"] = "100"
    lbl_message["height"] = "3"

    filename = fd.askopenfilename(filetypes=(("XML files", "*.xml"),("all files", " *.*")
                                                       ))
    if filename:
        try:
            doc = xml.dom.minidom.parse(filename)
        except:
            lbl_message["text"] = u"Не могу открыть файл"
            lbl_message["bg"] = "red"
            lbl_message["width"] = "100"
            lbl_message["height"] = "3"
            return

    with con:
        cur = con.cursor()
        cur.execute("truncate articles")
        cur.execute("truncate items")
        con.commit()

    staffs = doc.getElementsByTagName("ITEM")
    a_id=0
    notwrite=0
    for staff in staffs:
        itemtype = staff.getElementsByTagName("ITEMTYPE")[0].firstChild.data
        profart = staff.getElementsByTagName("PROFART")[0].firstChild.data
        profname = staff.getElementsByTagName("PROFNAME")[0].firstChild.data
        color = staff.getElementsByTagName("COLOR")[0].firstChild.data
        proflong = staff.getElementsByTagName("LONG")[0].firstChild.data
        anglel=staff.getElementsByTagName("ANGLEL")[0].firstChild.data
        angler=staff.getElementsByTagName("ANGLER")[0].firstChild.data
        profilpol=staff.getElementsByTagName("PROFILPOL")[0].firstChild.data
        paralmode=staff.getElementsByTagName("PARALMODE")[0].firstChild.data
        paralmodenum=staff.getElementsByTagName("PARALMODENUM")[0].firstChild.data
        curnewbar=staff.getElementsByTagName("CURNEWBAR")[0].firstChild.data
        profloutong = staff.getElementsByTagName("OFFCUTOUTLONG")[0].firstChild.data
        storagenum = staff.getElementsByTagName("STORAGENUM")[0].firstChild.data
        storagetype = staff.getElementsByTagName("STORAGETYPE")[0].firstChild.data
        cellid = staff.getElementsByTagName("CELLID")[0].firstChild.data
        offcutinid = staff.getElementsByTagName("OFFCUTINID")[0].firstChild.data
        offcutinlong = staff.getElementsByTagName("OFFCUTINLONG")[0].firstChild.data
        offcutoutid = staff.getElementsByTagName("OFFCUTOUTID")[0].firstChild.data
        offcutoutlong = staff.getElementsByTagName("OFFCUTOUTLONG")[0].firstChild.data

        #проверка на 1\2 нитки. Если вторая нитка, то не пишем в базу ни штапек, ни итемы
        if (itemtype=="1" and paralmodenum=="2"):
            notwrite=1
        elif (itemtype=="1" and paralmodenum!="2"):
            notwrite=0

        if (notwrite==0):
            if (itemtype=="1"):
                sql="insert into articles set articul=%s, name=%s, length=%s, lengthobr=%s, paralelmod=%s"
                strarr = (profart, profname, proflong, profloutong, paralmode)
                cur.execute(sql, strarr)
                con.commit()
                a_id = cur.lastrowid
            else:
                sql="insert into items set a_id=%s, profart=%s, profname=%s, color=%s, longs=%s, anglel=%s, angler=%s, profilpol=%s, paralmode=%s, paralmodenum=%s, curnewbar=%s, storagenum=%s, storagetype=%s, cellid=%s, offcutinid=%s, offcutinlong=%s, offcutoutid=%s, offcutoutlong=%s"
                strarr=(a_id, profart, profname, color, proflong, anglel, angler, profilpol, paralmode, paralmodenum, curnewbar, storagenum, storagetype, cellid, offcutinid, offcutinlong, offcutoutid, offcutoutlong)
                cur.execute(sql, strarr)
                con.commit()
    lbl_message["text"] = u"Импорт завершен"
    lbl_message["bg"] = "red"
    lbl_message["width"] = "100"
    lbl_message["height"] = "3"
    showgrid(1, 0)

def senditem_ruchnoy(langs):
    global langsarray
    global optionsrow
    if iscolab == 0:
        lbl_message["text"] = u"Станок не отколиброван. Нажмите ОТКОЛИБРОВАТЬ."
        lbl_message["bg"] = "red"
        lbl_message["width"] = "100"
        lbl_message["height"] = "3"
        return (0)
    minPos = float(optionsrow[1])
    maxPos = float(optionsrow[2])
    if langs < minPos or langs > maxPos:
        lbl_message["text"] = u"Значение должно лежать в пределах от " + optionsrow[1] + " до " + optionsrow[2]
        lbl_message["bg"] = "red"
        lbl_message["width"] = "100"
        lbl_message["height"] = "3"
        return (0)
    sendtoport(langs)
    labelItemCur.configure(text=str(langs))

    if langs not in langsarray:
        lenarr = len(langsarray)
        if lenarr<15:
           langsarray.append(langs)
           langsbuttonarray[lenarr].configure(text=str(langs))

def senditemruchnoy_button(k):
    if k < 0 or k > 15:
        return 0
    position = float(langsarray[k])
    senditem_ruchnoy(position)
    return 1

def senditemruchnoy(*args):
    lbl_message["text"] = ""
    lbl_message["width"] = "100"
    lbl_message["height"] = "1"
    lbl_message["bg"] = "white"
    global posToGo
    try:
        position = float(posToGo.get())
    except:
        lbl_message["text"] = u"Введите цифры"
        lbl_message["bg"] = "red"
        lbl_message["width"] = "100"
        lbl_message["height"] = "3"
        return

    posToGo.delete(0, END)
    senditem_ruchnoy(position)
    return 1


def showtab2_table():
    global langsbuttonarray
    global optionsrow
    minPos = optionsrow[1]
    maxPos = optionsrow[2]


    labelItem = Label(frame_tab2, text="Текущая позиция:", font='Tahoma 25')
    labelItem.grid(row=0,columnspan=6)

    labelItemCur.grid(row=1, columnspan=6)

    posToGo.grid(row=3, columnspan=6)
    posToGo.bind('<Return>', lambda event: senditemruchnoy())

    textlabel = 'Введите позицию от ' + minPos + ' до ' + maxPos + ' и нажмите Enter'

    labelPos= Label(frame_tab2, text=textlabel)
    labelPos.grid(row=4,columnspan=6)

    labeLastPosition = Label(frame_tab2, text="Отправить предыдущие позиции",width=45, height=5, pady=4 , font='Tahoma 15')
    labeLastPosition.grid(row=5, columnspan=6)

    x=0
    y=6
    for i in range(15):
        try:
            buttext = langsarray[i]
        except:
            buttext = ''
        langsbuttonarray[i] = Button(frame_tab2, text=buttext, width="15", command=lambda k=i: senditemruchnoy_button(k))
        if x==5:
            x=0
            y=y+1
        x = x+1
        langsbuttonarray[i].grid(row=y, column=x)


def skipitem(id):
    with con:
        cur = con.cursor()
        sql="update items set status=1 where id=%s";
        strarr = (id)
        cur.execute(sql, strarr)
        sql = "SELECT `a_id` FROM `items` WHERE `id`=%s"
        cur.execute(sql, (id))
        if cur.rowcount>0:
            resultnext = cur.fetchone()
            showgrid(resultnext[0], 1)
        con.commit()

def senditem(a_id):
    if iscolab == 0:
        lbl_message["text"] = u"Станок не отколиброван. Нажмите ОТКОЛИБРОВАТЬ."
        lbl_message["bg"] = "red"
        lbl_message["width"] = "100"
        lbl_message["height"] = "3"
        return (0)

    with con:
        cur = con.cursor()
        sql = "SELECT id, longs FROM `items` WHERE a_id=%s and status=0 order by id asc"
        cur.execute(sql, (a_id))
        if cur.rowcount>0:
            result = cur.fetchone()
            longs = result[1]
            sendtoport(longs)
            sql = "update items set status=1 where id=%s";
            strarr = (result[0])
            cur.execute(sql, strarr)
            con.commit()
        else:
            lbl_message["text"] = u"Все позиции порезаны. Нажмите на следующий штапик."
            lbl_message["bg"] = "red"
            lbl_message["width"] = "100"
            lbl_message["height"] = "3"
            return (0)

    showgrid(a_id, 0)

def resenditem(item_id):
    with con:
        cur = con.cursor()
        sql = "SELECT id, longs, a_id FROM `items` WHERE id=%s"
        cur.execute(sql, (item_id))
        if cur.rowcount>0:
            result = cur.fetchone()
            longs = result[1]
            sendtoport(longs)
            a_id = result[2]
    showgrid(a_id, 0)

def showtab1():
    but_tab1.configure(bg="yellow")
    but_tab2.configure(bg="lightgrey")
    frame_tbl.grid()
    frame_tab2.grid_remove()
    but_send.focus()

def showtab2():
    but_tab1.configure(bg="lightgrey")
    but_tab2.configure(bg="yellow")
    frame_tbl.grid_remove()
    frame_tab2.grid()
    showtab2_table()
    lbl_message["text"] = ""
    lbl_message["width"] = "100"
    lbl_message["height"] = "1"
    lbl_message["bg"]="white"
    posToGo.focus()

def showgrid(pos, clearmessage):
    if clearmessage==1:
        lbl_message["text"] = ""
        lbl_message["width"] = "100"
        lbl_message["height"] = "1"
        lbl_message["bg"]="white"
    for widget in frame_tbl.winfo_children():
        widget.destroy()
    frame_tbl.grid(row=5, column=0, columnspan="5")
    global curshtapik
    global but_send
    with con.cursor() as cur:
        # Read a single record
        sql = "SELECT `id` FROM `articles` WHERE `id`>%s order by id asc"
        cur.execute(sql, (pos))
        if cur.rowcount>0:
            resultnext = cur.fetchone()
            but_prev = Button(frame_tbl, text="->", bg="red", command=lambda: showgrid(resultnext[0], 1))
            but_prev.grid(row=1, column=3)

        sql = "SELECT `id` FROM `articles` WHERE `id`<%s order by id desc"
        cur.execute(sql, (pos))
        if cur.rowcount > 0:
            resultprev = cur.fetchone()
            but_next = Button(frame_tbl, text="<-", bg="red", command=lambda: showgrid(resultprev[0], 1))
            but_next.grid(row=1, column=0)
        but_send = Button(frame_tbl, text=u"Отослать текущую позицию",
                          width=30, height=2,
                          font=("Tahoma", 20),
                          bg="orange", command=lambda: senditem(pos))
        but_send.grid(row=2, columnspan=5)


    with con.cursor() as cur:
        # Read a single record
        sql = "SELECT `articul`, `name`, `id`, paralelmod FROM `articles` WHERE `id`=%s"
        cur.execute(sql, (pos))
        if cur.rowcount>0:
            result = cur.fetchone()
            if curshtapik==0:
                curshtapik = result[0]
            if curshtapik!=result[0]:
                lbl_message["text"] = u"Обратите внимание! Поменялся ортикул штапика."
                lbl_message["bg"] = "red"
                lbl_message["width"] = "100"
                lbl_message["height"] = "3"
                curshtapik = result[0]
            else:
                lbl_message["text"] = ""
                lbl_message["width"] = "100"
                lbl_message["height"] = "1"
                lbl_message["bg"] = "white"
            lbl = Label(frame_tbl, text="Артикул", font=("Tahoma", 15))
            lbl.grid(row=3, column=0, padx=1, pady=1)
            lbl = Label(frame_tbl, text=result[0], font=("Tahoma", 15))
            lbl.grid(row=3, column=1, columnspan=2, padx=1, pady=1)
            lbl = Label(frame_tbl, text="Наименование", font=("Tahoma", 15))
            lbl.grid(row=4, column=0, padx=1, pady=1)
            lbl = Label(frame_tbl, text=result[1], font=("Tahoma", 15))
            lbl.grid(row=4, column=1, padx=1, pady=1)
            lbl = Label(frame_tbl, text="Количество ниток", font=("Tahoma", 15))
            lbl.grid(row=5, column=0, padx=1, pady=1)
            if result[3]==1:
                nit='две'
            else:
                nit = 'одна'
            lbl = Label(frame_tbl, text=nit, font=("Tahoma", 15))
            lbl.grid(row=5, column=1, padx=1, pady=1)

            frame2_c = Frame(frame_tbl)
            frame2_c.grid(row=6, columnspan="3", sticky=NW)
            # Add a canvas in that frame.
            canvas = Canvas(frame2_c, bg="Yellow")
            canvas.grid(row=0, column=0)

            # Create a vertical scrollbar linked to the canvas.
            vsbar = Scrollbar(frame2_c, orient=VERTICAL, command=canvas.yview)
            vsbar.grid(row=0, column=1, sticky=NS)
            canvas.configure(yscrollcommand=vsbar.set)

            # Create a horizontal scrollbar linked to the canvas.
            hsbar = Scrollbar(frame2_c, orient=HORIZONTAL, command=canvas.xview)
            hsbar.grid(row=1, column=0, sticky=EW)
            canvas.configure(xscrollcommand=hsbar.set)

            # Create a frame on the canvas to contain the buttons.
            frame2 = Frame(canvas, bg="grey", bd=2)

            lbl = Label(frame2, width="30", text="Длина", font=("Tahoma", 10), padx=10, pady=5, bg="lightgreen")
            lbl.grid(row=0, column=0, padx=1, pady=1)
            lbl = Label(frame2, width="30", text="Ячейка", font=("Tahoma", 10), padx=10, pady=5, bg="lightgreen")
            lbl.grid(row=0, column=1, padx=1, pady=1)
            lbl = Label(frame2, width="30", text="Статус", font=("Tahoma", 10), padx=10, pady=5, bg="lightgreen")
            lbl.grid(row=0, column=2, padx=1, pady=1)
            lbl = Label(frame2, width="30", text="Действия", font=("Tahoma", 10), padx=10, pady=5, bg="lightgreen")
            lbl.grid(row=0, column=3, padx=1, pady=1)

            with con.cursor() as cur:
                i = 1
                # Read a single record
                sql = "SELECT * FROM `items` WHERE `a_id`=%s"
                cur.execute(sql, (result[2]))
                positem=0
                for row in cur:
                    if row[19]==0 and positem==0:
                        positem=row[0]
                    if row[19]==1 :
                        colorbg="lightgrey"
                    elif row[0]==positem:
                        colorbg = "yellow"
                    else:
                        colorbg="lightblue"
                    lbl = Label(frame2, width="30", text=row[5], font=("Tahoma", 10), bg=colorbg, padx=10, pady=5)
                    lbl.grid(row=i, column=0, padx=1, pady=1)
                    lbl = Label(frame2, width="30", text=row[14a], font=("Tahoma", 10), bg=colorbg, padx=10, pady=5)
                    lbl.grid(row=i, column=1, padx=1, pady=1)
                    if row[19]==1 :
                        lbl = Label(frame2, width="30", text="Порезана", font=("Tahoma", 10), bg=colorbg, padx=10, pady=5)
                        lbl.grid(row=i, column=2)
                        but_calib = Button(frame2, text="Перерезать", bg="red", width="25", command=lambda k=row[0]: resenditem(k))
                        but_calib.grid(row=i, column=3)
                    elif row[0] == positem:
                        lbl = Label(frame2, width="30", text="Текущая", font=("Tahoma", 10), bg=colorbg, padx=10, pady=5)
                        lbl.grid(row=i, column=2)
                        but_calib = Button(frame2, text="Пропустить", bg="lightblue", width="25", command=lambda k=row[0]: skipitem(k))
                        but_calib.grid(row=i, column=3)
                    else:
                        lbl = Label(frame2, width="30", text="Новая", font=("Tahoma", 10), bg=colorbg, padx=10, pady=5)
                        lbl.grid(row=i, column=2)
                    i=i+1

            canvas.create_window((0, 0), window=frame2, anchor=NW)

            frame2.update_idletasks()  # Needed to make bbox info available.
            bbox = canvas.bbox(ALL)  # Get bounding box of canvas with Buttons.
            # print('canvas.bbox(tk.ALL): {}'.format(bbox))
            LABEL_BG = "#ccc"  # Light gray.
            ROWS, COLS = 13, 9  # Size of grid.
            ROWS_DISP = 10  # Number of rows to display.
            COLS_DISP = 9  # Number of columns to display.

            # Define the scrollable region as entire canvas with only the desired
            # number of rows and columns displayed.
            w, h = bbox[2] - bbox[1], bbox[3] - bbox[1]
            dw, dh = int((w / COLS) * COLS_DISP), int((h / ROWS) * ROWS_DISP)
            canvas.configure(scrollregion=bbox, width=dw, height=dh)

            but_send.focus_set()
    return




#main block
root = Tk()



with con.cursor() as cur:
    # Read a single record
    sql = "SELECT * FROM `options` order by id asc"
    cur.execute(sql)
    optionsrow = {}
    if cur.rowcount > 0:
        for row in cur:
            optionsrow[row[0]] = row[2]


#ser=serial.Serial(comtext, 19200, dsrdtr = 1,timeout = 0)


lbl_head = Label(root, text=u"РАСКРОЙ ШТАПИКА", font=("Tahoma", 15), bg="white")
lbl_message = Label(root, text="", font=("Tahoma", 12), width="0", height="0", bg="white")
lbl_message.grid(row=1, columnspan=4)
but_calib1 = Button(root,
           text= u"Отколибровать",
           width=30, height=1,
           font=("Tahoma", 12),
           bg="lightblue", command=firstcolaboration
                  )

but_import = Button(root,
           text= u"Импорт данных из файла",
           width=30, height=1,
           font=("Tahoma", 12),
           bg="orange", command=importfromxml
                  )

lbl_head.grid(row=0, column=0)
but_calib1.grid(row=2,column=2, padx=5, pady=30)
but_import.grid(row=2,column=3, padx=5, pady=30)

but_tab1 = Button(root,
                  text=u"Автоматический режим",
                  width=30, height=1,
                  font=("Tahoma", 10),
                  bg="yellow", command=showtab1)
but_tab2 = Button(root,
                  text=u"Ручной режим",
                  width=30, height=1,
                  font=("Tahoma", 10),
                  bg="lightgrey", command=showtab2)
but_tab1.grid(row=3,column=0)
but_tab2.grid(row=3,column=1)


mycolor1 = '#eeeeee'

frame_tbl = Frame(root, bg=mycolor1, borderwidth=25)
frame_tbl.grid(row=5, column=0, columnspan="5")
frame_tab2 = Frame(root, bg=mycolor1, bd=25)
frame_tab2.grid(row=5, column=0, columnspan="5")



posToGo = Entry(frame_tab2, width=30, bd=20, bg="lightyellow", font='Helvetica 25')
labelItemCur = Label(frame_tab2, text="", font='Tahoma 25')


comtext = "COM"+optionsrow[8]
showgrid(1, 0)

ser = serial.Serial()
ser.port = comtext
ser.baudrate = 9600
ser.dsrdtr = 1
ser.timeout=0
try:
    ser.open()
except Exception as e:
    lbl_message["text"] = u"Ошибка. " + str(e)
    lbl_message["bg"] = "red"
    lbl_message["width"] = "100"
    lbl_message["height"] = "3"




root.title(u"Раскрой штапика")
root.geometry('1024x768')
root.configure(bg="white")
root.mainloop()
