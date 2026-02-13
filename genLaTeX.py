"""
Local Boulders Guidebook builder v0.6
"""
import subprocess
import jinja2
import os
from pathlib import Path
from dataStructure.base_classes.LBItem import LBItem


def _get_rating_string(rating):
    """
    Returns LaTeX string equivalent to climb star rating
    """
    if rating < 0:
        rating_string = ''
    elif rating < 1:
        rating_string = r'\ding{73}'
    else:
        rating_string = r'\ding{72}' * rating
    return rating_string


def _format_attributes_for_LaTeX(book):
    """
    Updates book data structure with LaTeX specific variables
    """
    for container_type in [book.areas, book.subareas, book.formations, book.climbs]:
        for item in container_type.values():
            # format newlines in strings for LaTeX. I.e., all text lines should end with \\
            item.description = item.description.replace('\n', r'\\'+'\n')

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


def _populate_templates(book):
    """
    Create LaTeX input from Jinja templates
    """
    templateLoader = jinja2.FileSystemLoader(book.paths['LaTeXTemplates'])
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


def _postprocess_LaTeX(book):
    """
    Postprocess generated LaTeX input files to fix special dependencies that are hard to account for in Jinja
    """
    for tex_inp in list(Path(book.paths['LaTeXOut']).glob('*.tex')):
        if Path(tex_inp).stem == 'intro':
            # don't format the intro section
            continue

        with open(tex_inp, 'r') as f:
            # Read all non-empty lines into a list
            lines = [line for line in f if line.strip()]

            # check for special cases if none add line to list of new lines
            lines_new = [lines[0]]
            for i in range(1,len(lines)):
                if (r'\end{multicols}' in lines[i]) and (r'\begin{multicols}' in lines[i-1]):
                    # if multi cols is being started and immediately ended remove both lines
                    lines_new.pop()
                elif (r'\newpage' in lines[i]) and (r'\begin{multicols}' in lines[i-1]):
                    # make multicols begin after new page to prevent blank pages from being generated
                    if (r'\includepdf' in lines[i-2]):
                        # skip newpage command after page insert command
                        continue
                    else:
                        lines_new.pop()
                        lines_new.append(lines[i])
                        lines_new.append(lines[i-1])
                else:
                    lines_new.append(lines[i])

        with open(tex_inp, 'w') as f:
            f.writelines(lines_new)


def _generate_PDF(book):
    """
    Runs MikTex and ghostscript (optional) from the command line
    """
    pdf_dir = os.path.relpath(book.paths['pdf'], start=book.paths['LaTeXOut'])
    # this bit calls pdflatex to generate the PDF. Requires a pdflatex install.
    process = subprocess.Popen(
        ['pdflatex', '-output-directory', pdf_dir, 'guideBook.tex', 'makeindex ' + pdf_dir + 'guideBook.tex'],
        cwd=book.paths['LaTeXOut'])
    process.wait()
    # PDF latex gets called twice to ensure that page number refs are correct
    process = subprocess.Popen(
        ['pdflatex', '-output-directory', pdf_dir, 'guideBook.tex', 'makeindex ' + pdf_dir + 'guideBook.tex'],
        cwd=book.paths['LaTeXOut'])
    process.wait()

    # this bit calls ghost script to compress the PDF (this saves a lot of space and has no noticable effect on quality)
    # Requires a win 64 ghost script install
    if book.options['use_ghost_script']:
        process = subprocess.Popen(['gswin64', '-sDEVICE=pdfwrite', '-dCompatibilityLevel=1.5',
                                    '-dNOPAUSE', '-dQUIET', '-dBATCH', '-dPrinted=false', '-dAutoRotatePages=/None',
                                    '-sOutputFile=guideBook-compressed.pdf', 'guideBook.pdf'])
        process.wait()
        os.remove('guideBook.pdf')
        os.rename('guideBook-compressed.pdf', f'{book.file_name}.pdf')


def gen_book_LaTeX(book):
    """
    Updates book data structure with LaTeX specific variables then generates a book from templates
    """
    _format_attributes_for_LaTeX(book)
    _populate_templates(book)
    _postprocess_LaTeX(book)
    _generate_PDF(book)
