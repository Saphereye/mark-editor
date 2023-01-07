import re
from enum import Enum

def markdown_to_gtk(text: str) -> str:
    txt = text
    # Not ignoring '<' symbol
    txt = re.sub(r"<", r'&#x003C;', txt)
    txt = re.sub(r">", r'&#x003E;', txt)
    # Bullet
    txt = re.sub(r"- (.+)\n", r"• \1\n", txt)
    # Bold
    txt = re.sub(r" \*(.+)\* ", r"<b>\1</b>", txt)
    # Italics
    txt = re.sub(r" /(.+)/ ", r"<i>\1</i>", txt)
    # Big
    txt = re.sub(r"# (.+)\n", r"<big>\1</big>\n", txt)
    # Subscript
    txt = re.sub(r"\_([0-9a-zA-Z]+?)( |\n){1}", r"<sub>\1</sub>\2", txt)
    # Superscript
    txt = re.sub(r"\^(.+?)( |\n){1}", r"<sup>\1</sup>\2", txt)
    # Underline
    txt = re.sub(r" \_(.+)\_ ", r"<u>\1</u>", txt)
    # Monospace
    txt = re.sub(r"\`(.+)\`", r"<tt>\1</tt>", txt)
    # Table
    tables = re.findall(r"\`\`\n([\s\S]*?)\n\`\`", txt)
    while(tables != []):
        tables = re.findall(r"\`\`\n([\s\S]*?)\n\`\`", txt)
        substitute_str = markdown_to_pretty_table(tables.pop())
        txt = re.sub(r"\`\`\n([\s\S]*?)\n\`\`", substitute_str, txt)
    # Strikethrough
    txt = re.sub(r"\~([0-9a-zA-Z ]+)\~", r"<s>\1</s>", txt)
    
    print(txt)

    return txt

def markdown_to_pretty_table(table: str) -> str:
    table = table.split('\n')
    ptable: list[list[str]] = []

    # Generate a 2d array containing all the items
    ptable.append([i.strip() for i in table[0].split('|') if i != ''])
    for i in range(2, len(table)):
        ptable.append([i.strip() for i in table[i].split('|') if i != ''])

    # Calculate string with max length
    max_len = 0

    for i in ptable:
        for j in i:
            if len(j) > max_len:
                max_len = len(j)

    # Print ptable formatted using max length
    output_string = "┌" + ("─"*max_len + "┬")*(len(ptable[0])-1) + ("─"*max_len + "┐") + '\n'
    row_num = 0
    for i in ptable:
        for j in i:
            output_string += f"│{j.ljust(max_len)}"
        row_num+=1
        if row_num == 1:
            output_string += "│\n├" + ("─"*max_len + "┼")*(len(ptable[0])-1) + f"{'─'*max_len}┤"
        else:
            output_string += "│"
        output_string += '\n'
    output_string += "└" + ("─"*max_len + "┴")*(len(ptable[0])-1) + ("─"*max_len + "┘") + '\n'


    return output_string
    

if __name__ == "__main__":
    table = """| Col 1 | Col 2 | Col 3  |
|-------|-------|--------|
| a     | 1     | 23     |
| bh    | 4bh   | 45n hj |
| a+b   | c*d   | 456    |"""
    print(markdown_to_pretty_table(table))