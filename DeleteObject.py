import ctypes

import maptype
import mapapi
import mapgdi
import mapsyst
import maperr
import seekapi
import rscapi
import sitapi
import maprscex

import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog

def DeleteObject(hmap:maptype.HMAP,hobj: maptype.HOBJ) -> str:
    retvalues = 0

    if hmap == 0:
        return 0
    
    hobj = mapapi.mapCreateObject(hmap)
    if hmap == 0:
       return 1

    flag = maptype.WO_FIRST
    while (seekapi.mapTotalSeekObject(hmap, hobj, flag)!= 0):
          flag = maptype.WO_NEXT    
    # Запросить порядковый номер объекта в карте
    ObjNumber = mapapi.mapObjectNumber(hobj)
          
    # получить идентификатор (HRSC) для объекта карты
    hres_class = mapapi.mapGetRscIdentByObject(hobj)

    # Определить идентификатор открытой пользовательской карты
    hsite = sitapi.mapGetObjectSiteIdent(hmap, hobj)
    
    # Запросить идентификатор классификатора карты
    hrsc = rscapi.mapGetRscIdent(hmap, hsite)
          
    # Запросить уникальный номер объекта
    objKey = mapapi.mapObjectKey(hobj)

    # Запросить индекс (внутренний код) объекта в классификаторе.
    ObjCode = mapapi.mapObjectCode(hobj)
          
    # Запросить номер слоя объекта ("Layer" = "Segment")
    LayerNumber = mapapi.mapSegmentNumber(hobj)

    # Запросить классификационный код объекта
    ObjExc = mapapi.mapObjectExcode(hobj)

    # Удалить объект карты по его последовательному номеру
    DeleteSiteObjectByNumb = sitapi.mapDeleteSiteObjectByNumber(hmap, hsite, ObjNumber)

    root = tk.Tk()
    root.title("Удаление объекта")
 
    src_label = tk.Label(text="номер объекта: ")

    src_label.grid(row=0, column=0, sticky="w")

    src_value = tk.IntVar()

    src_entry = tk.Entry(width=10, textvariable=src_value)

    src_entry.grid(row=0,column=1, padx=5, pady=5)

    src_value.set(" ")

    ret_value = tk.IntVar()
    ret_value.set(0)

    def Run():

        ret = DeleteSiteObjectByNumb
        ret_value.set(ret)
        root.destroy()
        # показ результата и количества удаленных объектов
        messagebox.showinfo("Результат", f"Удален объект {ObjNumber}")
        root.destroy()

    def Close():
        root.destroy()

    message_button = tk.Button(text="Выполнить", command=Run)
    message_button.grid(row=3,column=1, padx=5, pady=5, sticky="e")
    message_button = tk.Button(text="Отменить", command=Close)
    message_button.grid(row=3,column=2, padx=5, pady=5, sticky="w")

    root.eval('tk::PlaceWindow . center')
    root.resizable(False, False)
    root.mainloop()
  
    if hobj != 0:
       mapapi.mapFreeObject(hobj)  

    return retvalues