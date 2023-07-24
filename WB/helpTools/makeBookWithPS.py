import photoshop.api as ps


app = ps.Application()
app.displayDialogs = ps.DialogModes.DisplayNoDialogs
#app.displayDialogs = ps.
png_doc = app.open(r"D:\newPrint\print 5001.png")

png_doc.activeLayer = png_doc.layers[0]
png_doc.width
png_doc.height
png_doc.resizeImage(png_doc.width*(1277/png_doc.height) ,1277)
png_doc.activeLayer.copy()

doc = app.load(r"\\192.168.0.33\shared\_Общие документы_\Егор\книги_test.psd")
doc.paste()
png_doc.close()
layer_index = 1
#doc.activeLayer = doc.layers[layer_index]
#doc.activeLayer.move(doc.layers[layer_index + 2], ps.ElementPlacement.PlaceBefore)
a = doc.activeLayer.bounds
x,y = 371,669
x2,y2 = (a[2]-a[0])/2+a[0], (a[3]-a[1])/2+a[1]
doc.activeLayer.translate(x-x2, y-y2)
app.doAction('first','newSetForBook')