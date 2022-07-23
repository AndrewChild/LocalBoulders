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
        rating_string = r'\ding{72} ' * rating
    return rating_string


def gen_book_LaTeX(book):
    """
    Updates book data structure with LaTeX specific variables then generates a book from templates
    """

    for route in book.all_routes:
        route.rating_LaTeX = _get_rating_string(route.rating)
        route.serious_LaTeX = r'\warn ' * route.serious
        if route.color == 'DarkGoldenrod':
            route.color = 'Goldenrod' #LaTeX does not know what Goldenrod is
            route.color_LaTeX = route.color + '!50'
        elif route.color == 'DarkRed':
            route.color = 'red' #LaTeX does not know what DarkRed is
            route.color_LaTeX = route.color + '!20'
        else:
            route.color_LaTeX = route.color + '!20'

    for photo in book.all_photos:
        if photo.route:
            photo.latexRef = ' (See Page \\pageref{{{}:{}}})'.format(photo.route.ref, photo.route.name)
        else:
            photo.latexRef = ''


    # This stuff just tells JINJA2 how to read templates
    templateLoader = jinja2.FileSystemLoader(searchpath=book.paths['LaTeXTemplates'])
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
        f = open(f"{book.paths['LaTeXOut']}areas/" + area.name + '.tex', 'w')
        f.write(areaTemplate.render(area=area))
        f.close()

    f = open(f"{book.paths['LaTeXOut']}index.tex", 'w')
    f.write(indicesTemplate.render(book=book))
    f.close()

    process = subprocess.Popen(['pdflatex', '-output-directory', os.path.relpath(book.paths['pdf'], start=book.paths['LaTeXOut']), 'guideBook.tex', ], cwd=book.paths['LaTeXOut'])
    process.wait()
