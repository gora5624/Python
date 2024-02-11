import photoshop.api as ps
import os

app = ps.Application()
app.displayDialogs = ps.DialogModes.DisplayNoDialogs
for file in os.listdir(r'\\192.168.0.33\shared\_Общие документы_\Егор\_Принты книги 1000_10012024\под натяжку'):
    if not os.path.exists(os.path.join(r'\\rab\Диск для принтов сервак Егор\книжки новые2\Черный',file.replace('.jpg.png',''))):
        png_doc = app.open(os.path.join(r'\\192.168.0.33\shared\_Общие документы_\Егор\_Принты книги 1000_10012024\под натяжку',file))
        startRulerUnits = app.preferences.rulerUnits
        if png_doc.activeLayer.kind != ps.LayerKind.TextLayer:
            x2 = (png_doc.width * png_doc.resolution) / 2
            y2 = png_doc.height * png_doc.resolution
            sel_area = ((0, 0), (x2, 0), (x2, y2), (0, y2))
            png_doc.selection.select(sel_area, ps.SelectionType.ReplaceSelection, 0, False)

            png_doc.selection.copy()
            app.preferences.rulerUnits = ps.Units.Pixels

        png_doc.activeLayer = png_doc.layers[0]
        png_doc.width
        png_doc.height
        png_doc.resizeImage(png_doc.width*(1195/png_doc.height) ,1195)
        png_doc.activeLayer.copy()

        doc = app.load(r"\\192.168.0.33\shared\_Общие документы_\Егор\книги_test.psd")
        doc.paste()
        png_doc.close()
        layer_index = 3
        doc.activeLayer = doc.layers[layer_index]
        a = doc.activeLayer.bounds
        x,y = 839,681
        x2,y2 = (a[2]-a[0])/2+a[0], (a[3]-a[1])/2+a[1]
        doc.activeLayer = doc.layers[layer_index]
        doc.activeLayer.translate(x-x2, y-y2)
        doc.activeLayer.resize(100,100,ps.AnchorPosition.BottomCenter)

        if startRulerUnits != app.preferences.rulerUnits:
            app.preferences.rulerUnits = startRulerUnits


        options = ps.PNGSaveOptions()
        jpg = os.path.join(r'\\rab\Диск для принтов сервак Егор\книжки новые2\Черный',file.replace('.jpg.png',''))
        doc.saveAs(jpg, options, asCopy=True)
        doc.activeLayer.remove()