"""
Local Boulders Guidebook builder v0.6
"""
import subprocess
import jinja2
import sys


def gen_book(book):
    allRoutes = []
    allPhotos = []
    for area in book.areas.values():
        allPhotos = allPhotos + area.photos
        for subArea in area.subareas.values():
            allPhotos = allPhotos + subArea.photos
            for boulder in subArea.boulders.values():
                allPhotos = allPhotos + boulder.photos
                for route in boulder.routes.values():
                    allRoutes.append(route)
                    route.num = route.getRtNum()
                    for variation in route.variations.values():
                        allRoutes.append(variation)

    book.allRoutes = allRoutes
    book.allPhotos = allPhotos
    book.allPhotos = allPhotos

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
    acknowledgementsTemplate = templateEnv.get_template("./templates/acknowledgements.tex")
    introTemplate = templateEnv.get_template("./templates/introTemplate.tex")
    areaTemplate = templateEnv.get_template("./templates/areaTemplate.tex")
    indicesTemplate = templateEnv.get_template("./templates/indexTemplate.tex")

    f = open(f'./sections/guideBook.tex', 'w')
    f.write(mainTemplate.render(book=book))
    f.close()

    f = open(f'./sections/acknowledgements.tex', 'w')
    f.write(acknowledgementsTemplate.render(book=book))
    f.close()

    for area in book.areas.values():
        area.histogram()
        f = open('./sections/areas/' + area.name + '.tex', 'w')
        f.write(areaTemplate.render(area=area))
        f.close()

    f = open(f'./sections/index.tex', 'w')
    f.write(indicesTemplate.render(book=book))
    f.close()

    process = subprocess.Popen(['pdflatex', '-output-directory', '../', 'guideBook.tex', ], cwd=r'./sections')
    process.wait()
