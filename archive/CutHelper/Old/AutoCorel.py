from pywinauto.application import Application
import time

WidthList = '409'
HieghtList = '1009'
app = Application(backend="uia").start(
    'C:\Program Files\Corel\CorelDRAW Graphics Suite 2020\Programs64\CorelDRW.exe')
app.window(class_name="CorelDRAW22").wait('visible', timeout=30)
dlg = app.window(class_name="CorelDRAW22")
dlg.set_focus()
time.sleep(5)
dlg.type_keys("+ t")
dlg_2 = dlg.window(class_name='#32770')
dlg_3 = dlg_2.window(control_type='Edit').type_keys(
    'D:\Заказ_на_резку_03.02.21_мат.xlsx')
dlg_2.window(control_type='Button', best_match='OK').click()
app.window(class_name='TeBinFm').wait('visible', timeout=40)
dlg_4 = app.window(class_name='TeBinFm').descendants()

dlg_4[19].type_keys(WidthList)
dlg_4[23].type_keys(HieghtList)
dlg_4[31].click()
