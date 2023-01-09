import re
from enum import Enum
import markdown

"""BUG
Writing '-- ' converts it into '-.'
"""

def markdown_to_gtk(text: str) -> str:
    txt = text
    txt = markdown.markdown(text)
    print("Before: ", txt)
    # Escape characters
    txt = re.sub(r"\\\\", r"&#x005C;", txt)
    txt = re.sub(r"\\\*", r"&#x002A;", txt)
    txt = re.sub(r"\\\_", r"&#x005F;", txt)
    # TODO write down all the escape characters (automate it please)

    # Clear out all <p>, <markup> tags
    txt = re.sub(r"<p>([\w\W]*?)</p>", r"\1", txt)

    # Headings
    txt = re.sub(r"<h1>(.*)</h1>", r"<span font_desc='Fira Code 32'>\1</span>", txt)
    txt = re.sub(r"<h2>(.*)</h2>", r"<span font_desc='Fira Code 30'>\1</span>", txt)
    txt = re.sub(r"<h3>(.*)</h3>", r"<span font_desc='Fira Code 28'>\1</span>", txt)
    txt = re.sub(r"<h4>(.*)</h4>", r"<span font_desc='Fira Code 26'>\1</span>", txt)

    # List
    ## Organise the <ul> tags
    txt = re.sub(r"<ul>\n((\w|\W)*)</ul>", r"\1\n", txt)
    ## Format the bullets
    txt = re.sub(r"<li>(.*)</li>", r"• \1", txt)
    # TODO add support for <ol> tags

    # Line breaks
    txt = re.sub(r"<br>", r"\n", txt)

    # Emphasis
    ## Bold
    txt = re.sub(r"<strong>(.*)</strong>", r"<b>\1</b>", txt)

    ## Italic
    txt = re.sub(r"<em>(.*)</em>", r"<i>\1</i>", txt)

    # Blockquotes
    # TODO use box art to draw nice qoutes

    # Code
    txt = re.sub(r"<code>(.*)</code>", r"<tt>\1</tt>", txt)

    # Horizontal rules
    txt = re.sub(r"<hr />", r"------------------", txt)

    # Links
    ## Handled by that parser

    # Images
    # TODO Add image support

    # HTML support
    ## Inbuilt

    print("After: ", txt)

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