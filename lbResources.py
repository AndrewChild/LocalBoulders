import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import numpy as np
import numbers
import webcolors
import qrcode


def get_grade_atts(grade):
    try:
        int(grade)
    except ValueError:
        if grade == '?':
            gradeNum = -2
        elif grade == 'B':
            gradeNum = -1
        elif grade[-1] == '+':
            gradeNum = int(grade[0])+0.1
        elif grade.split('/') == '/':
            gradeNum = int(grade[0])+0.5
        elif grade[-1] == '-':
            gradeNum = int(grade[0])-0.1
        else:
            gradeNum= np.average([int(x) for x in grade.split('/')])
    else:
        gradeNum = grade

    if gradeNum == -2:
        color = 'black!20'
        color_hex = webcolors.name_to_hex('black')
    elif gradeNum <= 3:
        color = 'green!20'
        color_hex = webcolors.name_to_hex('green')
    elif gradeNum <= 6:
        color = 'RoyalBlue!20'
        color_hex = webcolors.name_to_hex('RoyalBlue')
    elif gradeNum <= 9:
        color = 'Goldenrod!50'
        color_hex = webcolors.name_to_hex('DarkGoldenrod')
    else:
        color = 'red!20'
        color_hex = webcolors.name_to_hex('DarkRed')
    return color, color_hex, gradeNum


def get_rating_string(rating):
    if rating < 0:
        rating_string = ''
    elif rating < 1:
        rating_string = r'\ding{73}'
    else:
        rating_string = r'\ding{72} ' * rating
    return rating_string


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


def create_qr(s, name):
    qr_code = qrcode.make(s)
    qr_code.save(f'./maps/qr/{name}_qr.png')