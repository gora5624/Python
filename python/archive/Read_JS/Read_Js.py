from my_lib import scan_dir

File_list = scan_dir(r"D:\mask")
for file in File_list:
    brand_name = file.split("\\")[2]
    dir_model = brand_name + "/"
    model_name = file.split("\\")[3][0:-4]
    model_path = file.split("\\")[3]
    site_name = model_name
    pre_data = {}
    print(model_name)
