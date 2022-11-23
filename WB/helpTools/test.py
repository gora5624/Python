import os
import pandas

logoPath = r'\\192.168.0.33\shared\_Общие документы_\Егор\Все принты\Принты под пластины PDF\лого'
fullPath = r'\\192.168.0.33\shared\_Общие документы_\Егор\Все принты\Принты под пластины PDF\полные'
pdfPath = r'F:\L XL'
logo2 = r'F:\PDF\лого'
full2= r'F:\PDF\полные'
for file in os.listdir(logoPath):
    if not os.path.isdir(os.path.join(logoPath,file)):
        try:
            os.rename(os.path.join(pdfPath,file), os.path.join(logo2,file))
        except:
            try:
                os.rename(os.path.join(pdfPath,file.replace('pdf','cdr')), os.path.join(logo2,file.replace('pdf','cdr')))
            except:
                try:
                    os.rename(os.path.join(pdfPath,file.replace('cdr','pdf')), os.path.join(logo2,file.replace('cdr','pdf')))
                except:
                    print(file)