"""
Local Boulders Guidebook builder v0.6
"""
import subprocess
import jinja2
import os


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
        extensions=['jinja2.ext.loopcontrols']
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
            photo.latexRef = ' \\vpageref[][Description]{{{}:{}}}'.format(photo.route.ref, photo.route.item_id)
        else:
            photo.latexRef = ''
        if photo.description:
            photo.latex_description = photo.description + photo.latexRef
    for map in book.all_maps:
        map.latex_description = map.description

    templateEnv = _set_templateEnv(book.paths['LaTeXTemplates'])
    mainTemplate = templateEnv.get_template("localBoulders.tex")
    acknowledgementsTemplate = templateEnv.get_template("acknowledgements.tex")
    areaTemplate = templateEnv.get_template("areaTemplate.tex")
    indicesTemplate = templateEnv.get_template("indexTemplate.tex")

    f = open(f"{book.paths['LaTeXOut']}guideBook.tex", 'w', encoding="utf-8")
    f.write(mainTemplate.render(book=book))
    f.close()

    f = open(f"{book.paths['LaTeXOut']}acknowledgements.tex", 'w', encoding="utf-8")
    f.write(acknowledgementsTemplate.render(book=book))
    f.close()

    for area in book.areas.values():
        f = open(f"{book.paths['LaTeXOut']}" + area.item_id + '.tex', 'w', encoding="utf-8")
        f.write(areaTemplate.render(area=area))
        f.close()

    f = open(f"{book.paths['LaTeXOut']}index.tex", 'w', encoding="utf-8")
    f.write(indicesTemplate.render(book=book))
    f.close()

    paths_to_srcub = [f'{book.file_name}.pdf', 'guideBook.aux', 'guideBook.log']
    for p in paths_to_srcub:
        if os.path.exists(p):
            os.remove(p)

    pdf_dir = os.path.relpath(book.paths['pdf'], start=book.paths['LaTeXOut'])
    #this bit calls pdflatex to generate the PDF. Requires a pdflatex install.
    process = subprocess.Popen(['pdflatex', '-output-directory', pdf_dir, 'guideBook.tex', 'makeindex ' + pdf_dir + 'guideBook.tex'], cwd=book.paths['LaTeXOut'])
    process.wait()
    #PDF latex gets called twice to ensure that page number refs are correct
    process = subprocess.Popen(['pdflatex', '-output-directory', pdf_dir, 'guideBook.tex', 'makeindex ' + pdf_dir + 'guideBook.tex'], cwd=book.paths['LaTeXOut'])
    process.wait()

    #this bit calls ghost script to compress the PDF (this saves a lot of space and has no noticable effect on quality)
    #Requires a win 64 ghost script install
    if book.options['use_ghost_script']:
        process = subprocess.Popen(['gswin64', '-sDEVICE=pdfwrite', '-dCompatibilityLevel=1.5',
                                    '-dNOPAUSE', '-dQUIET', '-dBATCH', '-dPrinted=false',
                                    '-sOutputFile=guideBook-compressed.pdf', 'guideBook.pdf'])
        process.wait()
        os.remove('guideBook.pdf')
        os.rename('guideBook-compressed.pdf', f'{book.file_name}.pdf')
