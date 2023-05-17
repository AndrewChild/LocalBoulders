"""
Local Boulders Guidebook builder v0.6
"""
import subprocess
import jinja2
import os


#install dir for ghost script. There is probably a better way to do this
GS = r'C:\Program Files\gs\gs10.00.0\bin\gswin64.exe'


def _get_rating_string(rating):
    """
    Returns LaTeX string equivlent to climb strar rating
    """
    if rating < 0:
        rating_string = ''
    elif rating < 1:
        rating_string = r'\ding{73}'
    else:
        rating_string = r'\ding{72}' * rating
    return rating_string

def _set_templateEnv(searchpath):
    """
    Tells JINJA2 how to read templates
    """
    templateLoader = jinja2.FileSystemLoader(searchpath=searchpath)
    templateEnv = jinja2.Environment(
        loader=templateLoader,
        block_start_string='\BLOCK{',
        block_end_string='}',
        variable_start_string='\VAR{',
        variable_end_string='}',
        comment_start_string='\#{',
        comment_end_string='}',
        line_statement_prefix='%%',
        line_comment_prefix='%#',
        trim_blocks=True,
        autoescape=False,
    )
    return templateEnv

def gen_book_LaTeX(book):
    """
    Updates book data structure with LaTeX specific variables then generates a book from templates
    """

    for climb in book.climbs.values():
        climb.rating_LaTeX = _get_rating_string(climb.rating)
        climb.serious_LaTeX = r'\warn' * climb.serious
        if climb.color == 'DarkGoldenrod':
            climb.color = 'Goldenrod' #LaTeX does not know what Goldenrod is
            climb.color_LaTeX = climb.color + '!50'
        elif climb.color == 'DarkRed':
            climb.color = 'red' #LaTeX does not know what DarkRed is
            climb.color_LaTeX = climb.color + '!20'
        else:
            climb.color_LaTeX = climb.color + '!20'
        if climb.name_unconfirmed:
            climb.name_unconfirmed_LaTeX = '*'
        else:
            climb.name_unconfirmed_LaTeX = ''
        if climb.grade_unconfirmed:
            climb.grade_unconfirmed_LaTeX = '*'
        else:
            climb.grade_unconfirmed_LaTeX = ''

    for photo in book.all_photos:
        if photo.route:
            photo.latexRef = ' (Page \\pageref{{{}:{}}})'.format(photo.route.ref, photo.route.name)
        else:
            photo.latexRef = ''
        if photo.description:
            photo.description = photo.description + photo.latexRef

    templateEnv = _set_templateEnv(book.paths['LaTeXTemplates'])
    mainTemplate = templateEnv.get_template("localBoulders.tex")
    acknowledgementsTemplate = templateEnv.get_template("acknowledgements.tex")
    areaTemplate = templateEnv.get_template("areaTemplate.tex")
    indicesTemplate = templateEnv.get_template("indexTemplate.tex")

    f = open(f"{book.paths['LaTeXOut']}guideBook.tex", 'w')
    f.write(mainTemplate.render(book=book))
    f.close()

    f = open(f"{book.paths['LaTeXOut']}acknowledgements.tex", 'w')
    f.write(acknowledgementsTemplate.render(book=book))
    f.close()

    for area in book.areas.values():
        area.histogram()
        f = open(f"{book.paths['LaTeXOut']}" + area.name + '.tex', 'w')
        f.write(areaTemplate.render(area=area))
        f.close()

    f = open(f"{book.paths['LaTeXOut']}index.tex", 'w')
    f.write(indicesTemplate.render(book=book))
    f.close()

    pdf_dir = os.path.relpath(book.paths['pdf'], start=book.paths['LaTeXOut'])
    #this bit calls pdflatex to generate the PDF. Requires a pdflatex install
    process = subprocess.Popen(['pdflatex', '-output-directory', pdf_dir, 'guideBook.tex', ], cwd=book.paths['LaTeXOut'])
    process.wait()

    #this bit calls ghost script to compress the PDF (this saves a lot of space and has no noticable effect on quality)
    #Requires a win 64 ghost script install
    process = subprocess.Popen([GS, '-sDEVICE=pdfwrite', '-dCompatibilityLevel=1.5', '-dNOPAUSE', '-dQUIET',
                                '-dBATCH', '-dPrinted=false', '-sOutputFile=guideBook-compressed.pdf', 'guideBook.pdf', ])
    process.wait()
    os.remove('guideBook.pdf')
    os.rename('guideBook-compressed.pdf', 'guideBook.pdf')
