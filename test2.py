import re
text ="""id: 1054820423 ,
username: @saaman_pc 
balance of user : 0
balance increase amount:‌ 180 T H"""
pattern = r"balance increase amount:‌ \d+"

x=re.findall(pattern=pattern,string=text)[0].split()[3]
print(x)