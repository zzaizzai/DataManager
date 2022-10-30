import pathlib

file_name = r"C:\Users\junsa\Desktop\junsai\レオメータ\CBA001-007  200h.xls"
name = pathlib.Path(file_name).stem

print(name.split(" "))
name_split = name.split(" ")

for name in name_split:
    print(name)
    print(name[:6], name[:3], name[3:6])
    # if len(name[:6]) == 6 and name[:3].isalpha() and name[3:].isdigit():
    #     print(name[:6])