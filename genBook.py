"""
Local Boulders Guidebook builder v0.6
"""
import subprocess
import jinja2
import sys
import os


def gen_book(book):
    # This stuff just tells JINJA2 how to read templates
    templateLoader = jinja2.FileSystemLoader(searchpath=sys.path[1])
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
    mainTemplate = templateEnv.get_template("./templates/localBoulders.tex")
    introTemplate = templateEnv.get_template("./templates/introTemplate.tex")
    areaTemplate = templateEnv.get_template("./templates/areaTemplate.tex")
    indicesTemplate = templateEnv.get_template("./templates/indicesTemplate.tex")

    f = open(f'./sections/guideBook.tex', 'w')
    f.write(mainTemplate.render(book=book))
    f.close()

    for area in book.areas.values():
        f = open('./sections/areas/' + area.name + '.tex', 'w')
        f.write(areaTemplate.render(area=area))
        f.close()

    f = open(f'./sections/indices.tex', 'w')
    f.write(indicesTemplate.render(book=book))
    f.close()

    # Removing these files prevents LaTeX from crashing for stupid reasons
    # if os.path.exists('./guideBook.aux'):
    #     os.remove('./guideBook.aux')
    # if os.path.exists('./guideBook.log'):
    #     os.remove('./guideBook.log')
    process = subprocess.Popen(['pdflatex', '-output-directory', '../', 'guideBook.tex', ], cwd=r'./sections')
    process.wait()
