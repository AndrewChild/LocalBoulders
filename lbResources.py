import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import numpy as np
import numbers
import webcolors
import qrcode


def get_grade_atts(grade):
    gradeNum = grade
    if grade == '?':
        color = 'black!20'
        color_hex = webcolors.name_to_hex('black')
        gradeNum = 42069 # set numeric value of unknown routes arbitrarily high
    elif grade <= 3:
        color = 'green!20'
        color_hex = webcolors.name_to_hex('green')
    elif grade <= 6:
        color = 'RoyalBlue!20'
        color_hex = webcolors.name_to_hex('RoyalBlue')
    elif grade <= 9:
        color = 'Goldenrod!50'
        color_hex = webcolors.name_to_hex('Goldenrod')
    else:
        color = 'red!20'
        color_hex = webcolors.name_to_hex('red')
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

    instances = np.zeros(19)
    for route in areaRoutes:
        if isinstance(route.grade, numbers.Number):
            instances[int(route.grade)] += 1

    while instances[-1] == 0 and len(instances) != 1:
        instances = instances[:-1]

    instances = np.append(instances, [len(areaRoutes)-sum(instances)])
    colors = []
    labels = []
    for i in range(len(instances)-1):
        colors.append(get_grade_atts(i)[1])
        labels.append(f'V{i}')
    colors.append(get_grade_atts('?')[1])
    labels.append('V?')

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