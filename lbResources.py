import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import numpy as np
import webcolors
import qrcode


def _is_int(object):
    """
    Checks if an object (string or number) can be cast as an integer
    """
    try:
        int(object)
        return True
    except ValueError:
        return False


def _get_grade_number_YDS(grade):
    # iterate through each character is the grade
    grade = str(grade).replace(' ','')[2:]
    grade_number = []
    for i in grade:
        if _is_int(i):
            grade_number.append(i)
        elif i == '?':
            grade_number.append('-2.5')
        else:
            break
    grade = grade[len(grade_number):]
    grade_number = float(''.join(grade_number)) + .5

    grade = [0.3 if i == '+' else i for i in grade]
    grade = [-0.3 if i == '-' else i for i in grade]
    grade = [-0.2 if i == 'a' else i for i in grade]
    grade = [-0.1 if i == 'b' else i for i in grade]
    grade = [0.1 if i == 'c' else i for i in grade]
    grade = [0.2 if i == 'd' else i for i in grade]
    if len(grade) > 1:
        grade = [np.average([grade[0], grade[2]])]
    if len(grade) > 0:
        grade_number = grade_number + grade[0]
    return grade_number


def _get_grade_number_Hueco(grade):
    if _is_int(grade):
        return int(grade)
    else:
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
            grade_number = np.average([int(x) for x in grade.split('/')])
    return grade_number


def _get_grade_number(grade: str):
    """
    Takes the grade string and converts it to a number.
    In the case of non numeric values specific negative numbers will be used.
    ? = -2
    B = -1
    in the case of +/- a .1 will be added or subtracted accordingly
    in the case of split grade a .5 will be added to the lower number.
    """

    # Check if the grade is YDS or Hueco V
    if len(str(grade)) > 1 and str(grade)[1] == '.':
        grade_scale = 'YDS'
        return _get_grade_number_YDS(grade), grade_scale
    else:
        grade_scale = 'Hueco'
        return _get_grade_number_Hueco(grade), grade_scale


def get_grade_atts(grade):
    """ generate the grade attributes
    """
    grade_number, grade_scale = _get_grade_number(grade)
    colors = ['black', 'green', 'RoyalBlue', 'DarkGoldenrod', 'DarkRed']

    if grade_scale == 'Hueco':
        if grade_number == -2:
            color = colors[0]
        elif grade_number <= 3:
            color = colors[1]
        elif grade_number <= 6:
            color = colors[2]
        elif grade_number <= 9:
            color = colors[3]
        else:
            color = colors[4]
    else:
        if grade_number == -2:
            color = colors[0]
        elif grade_number <= 10:
            color = colors[1]
        elif grade_number <= 12:
            color = colors[2]
        elif grade_number <= 14:
            color = colors[3]
        else:
            color = colors[4]

    color_hex = webcolors.name_to_hex(color)
    return color, color_hex, grade_number, grade_scale


def genHistogram(area):
    print(f'Creating Route Histogram for {area.name}')
    areaRoutes = []
    for subArea in area.subareas.values():
        for formation in subArea.formations.values():
            for route in formation.routes.values():
                areaRoutes.append(route)
                for variation in route.variations.values():
                    areaRoutes.append(variation)

    instances = np.zeros(20)
    for route in areaRoutes:
        if route.grade_scale == 'Hueco':
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