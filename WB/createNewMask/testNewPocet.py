import os
from PIL import Image

for d in os.listdir(r'\\192.168.0.33\shared\_Общие документы_\Егор\Архив масок ВБ\NewPocket'):
    img = Image.open(os.path.join(r'\\192.168.0.33\shared\_Общие документы_\Егор\Архив масок ВБ\NewPocket', d, '1.png'))
    BrandCaseImg = Image.open(r"F:\Downloads\2CASE.png")
    img.paste(BrandCaseImg, (3365, 676), BrandCaseImg)
    img.save(os.path.join(r'\\192.168.0.33\shared\_Общие документы_\Егор\Архив масок ВБ\NewPocket', d, '1.png'))
    img = Image.open(os.path.join(r'\\192.168.0.33\shared\_Общие документы_\Егор\Архив масок ВБ\NewPocket', d, '3.png'))
    BrandCaseImg = Image.open(r"F:\Downloads\2CASE_02.png")
    img.paste(BrandCaseImg, (3520, 5603), BrandCaseImg)
    img.save(os.path.join(r'\\192.168.0.33\shared\_Общие документы_\Егор\Архив масок ВБ\NewPocket', d, '3.png'))
    # img.show()