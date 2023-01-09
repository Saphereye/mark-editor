symbols = "\\*_`{}[]<>()#+-.!|"
# txt = re.sub(r"\\\\", r"&#x005C;", txt)
for i in symbols:
    print(f"""txt = re.sub(r"\\\\\{i}", r"&#x00{hex(ord(i))[-2:].upper()};", txt)""")