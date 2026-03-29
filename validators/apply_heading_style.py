from docx.shared import Pt, Cm
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.oxml.ns import qn

def apply_heading_style(paragraph, text):
    """
    Применяет ГОСТ-стиль к абзацу (жирный, Times New Roman 14, без абзацного отступа, выравнивание влево).
    """
    try:
        paragraph.style = 'Normal'
    except:
        paragraph.style = 'Обычный'
    paragraph.clear()
    run = paragraph.add_run(text)
    run.font.bold = True
    run.font.name = "Times New Roman"
    run.font.size = Pt(14)
    run._element.rPr.rFonts.set(qn('w:eastAsia'), 'Times New Roman')
    paragraph.paragraph_format.first_line_indent = Cm(0)
    paragraph.alignment = WD_PARAGRAPH_ALIGNMENT.LEFT