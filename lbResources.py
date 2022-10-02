import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import numpy as np
import webcolors
import qrcode
from PIL import Image


def _get_grade_number(grade: str):
    """ Takes the grade string and converts it to a number. 
    In the case of non numeric values specific negative numbers will be used.
    ? = -2
    B = -1
    in the case of +/- a .1 will be added or subtracted accordingly
    in the case of split grade a .5 will be added to the lower number.
    """

    try:
        grade_number = int(grade)

    except ValueError:
        if grade == '?':
            grade_number = -2
        elif grade == 'B':
            grade_number = -1
        elif grade[-1] == '+':
            grade_number = int(grade[:-1])+0.1
        elif '/' in grade:
            split_grades = grade.split("/")
            grade_number = int(split_grades[0])+0.5
        elif grade[-1] == '-':
            grade_number = int(grade[:-1])-0.1
        else:
            grade_number= np.average([int(x) for x in grade.split('/')])

    return grade_number


def get_grade_atts(grade):
    """ generate the grade attributes
    """
    grade_number = _get_grade_number(grade)

    if grade_number == -2:
        color = 'black'
    elif grade_number <= 3:
        color = 'green'
    elif grade_number <= 6:
        color = 'RoyalBlue'
    elif grade_number <= 9:
        color = 'DarkGoldenrod'
    else:
        color = 'DarkRed'
    color_hex = webcolors.name_to_hex(color)
    return color, color_hex, grade_number


def genHistogram(area):
    print(f'Creating Route Histogram for {area.name}')
    areaRoutes = []
    for subArea in area.subareas.values():
        for boudler in subArea.boulders.values():
            for route in boudler.routes.values():
                areaRoutes.append(route)
                for variation in route.variations.values():
                    areaRoutes.append(variation)

    instances = np.zeros(20)
    for route in areaRoutes:
        instances[int(round(route.gradeNum))+2] += 1

    while instances[-1] == 0 and len(instances) != 1:
        instances = instances[:-1]

    colors = []
    labels = []
    for i in range(len(instances)):
        colors.append(get_grade_atts(i-2)[1])
        if i == 0:
            labels.append('?')
        elif i == 1:
            labels.append('B')
        else:
            labels.append(f'V{i-2}')

    ind = np.arange(len(instances))    # the x locations for the groups
    width = 0.8     # the width of the bars: can also be len(x) sequence

    fig, ax = plt.subplots()

    ax.bar(ind, instances, width, color=colors)

    ax.axhline(0, color='grey', linewidth=0.8)
    ax.set_xticks(ind, labels=labels)
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))

    plt.savefig(f'./maps/plots/{area.name}.png')


def create_qr(path, s, name):
    qr_code = qrcode.make(s)
    qr_code.save(f'{path}{name}_qr.png')

def get_aspect_ratio(filePath):
    """
    inputs the file path of an image and returns the aspect ratio of the image
    """
    im = Image.open(filePath)
    width, height = im.size
    return width/height