import re

def markdown_to_gtk(text: str) -> str:
    txt = text
    # Bullet
    txt = re.sub(r"- ([0-9a-zA-Z ]+)\n", r"• \1\n", txt)
    # Bold
    txt = re.sub(r"\*([0-9a-zA-Z ]+)\*", r"<b>\1</b>", txt)
    # Italics
    txt = re.sub(r"/([0-9a-zA-Z ]+)/", r"<i>\1</i>", txt)
    # Big
    txt = re.sub(r"# (.+)\n", r"<big>\1</big>\n", txt)
    # Underline
    txt = re.sub(r"\_([0-9a-zA-Z ]+)\_", r"<u>\1</u>", txt)
    # Subscript
    txt = re.sub(r"\_([0-9a-zA-Z]+)( |\n){1}", r"<sub>\1</sub>\2", txt)
    # Superscript
    txt = re.sub(r"\^([0-9a-zA-Z]+)( |\n){1}", r"<sup>\1</sup>\2", txt)
    # Monospace
    txt = re.sub(r"\`([0-9a-zA-Z ]+)\`", r"<tt>\1</tt>", txt)
    # Code Block
    txt = re.sub(r"```([\s\S]*?)```", r"<tt>\1</tt>", txt)
    # Strikethrough
    txt = re.sub(r"\~([0-9a-zA-Z ]+)\~", r"<s>\1</s>", txt)

    return txt