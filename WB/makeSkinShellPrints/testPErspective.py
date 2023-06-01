from itertools import chain
from wand.color import Color
from wand.image import Image
from PIL import Image as Img
import io

with Image(filename=r"D:\print 2.png") as cover, Image(filename=r"\\rab\Диск для принтов сервак Егор\Принты со светом все\Все\print 3.png") as template:
    w, h = cover.size
    etalonW, etalonH = 519, 1149
    XScale = w/etalonW
    YScale = h/etalonH
    cover.virtual_pixel = 'transparent'
    source_points = (
        (0, 0),
        (w, 0),
        (w, h),
        (0, h)
    )
    destination_points = (
        (0*XScale, 151*YScale),
        (321*XScale, 137*YScale),
        (519*XScale, 895*YScale),
        (201*XScale, 981*YScale)
    )
    order = chain.from_iterable(zip(source_points, destination_points))
    arguments = list(chain.from_iterable(order))
    cover.distort('perspective', arguments)

    # Overlay cover onto template and save
    template.composite(cover,left=0,top=0)
    pil_image = Img.open(io.BytesIO(cover.make_blob("png")))
    pil_image.show()
    # cover.save(filename=r"D:\Модели SkinShell\Чехол Xiaomi 13 Lite силикон с зак.кам. черный противоуд\Карточки\1tt.png")

