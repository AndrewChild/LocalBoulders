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
            grade_number.append('-1.5')
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
        grade_str = 'V'+str(grade)
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
        grade_str = str(grade)
        if grade_number == -1:
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
    return color, color_hex, grade_number, grade_scale, grade_str


def genHistogram(area):
    print(f'Creating Route Histogram for {area.name}')

    # Count how many instances of a climb ther are at each grade.
    # Boulder list has form [?, B, 0, 1, ...]
    # Route list has form [?, 5.0, 5.1, ..., 5.10, 5.11, ...]
    boulder_instances = [0]*20
    route_instances = [0]*17
    for route in area.routes.values():
        if route.grade_scale == 'Hueco':
            boulder_instances[int(round(route.gradeNum))+2] += 1
        else:
            route_instances[int(round(route.gradeNum))+1] += 1
    for route in area.variations.values():
        if route.grade_scale == 'Hueco':
            boulder_instances[int(round(route.gradeNum))+2] += 1
        else:
            route_instances[int(round(route.gradeNum))+1] += 1

    # assign color and label to each Boulder grade bin
    boulder_colors = []
    boulder_labels = []
    for i in range(len(boulder_instances)):
        boulder_colors.append(get_grade_atts(i-2)[1])
        if i == 0:
            boulder_labels.append('V?')
        elif i == 1:
            boulder_labels.append('VB')
        else:
            boulder_labels.append(f'V{i-2}')

    # assign color and label to each Route grade bin
    route_colors = []
    route_labels = []
    for i in range(len(route_instances)):
        if i == 0:
            route_colors.append(get_grade_atts(f'5.?')[1])
            route_labels.append('5.?')
        else:
            route_colors.append(get_grade_atts(f'5.{i-1}')[1])
            route_labels.append(f'5.{i-1}')

    # combine boulders and routes into one list
    instances = boulder_instances + route_instances
    colors = boulder_colors + route_colors
    labels = boulder_labels + route_labels

    # search for bins that have zero climbs in them
    zero_bin_indexes = []
    for i, bin in enumerate(instances):
        if bin == 0:
            zero_bin_indexes.append(i)
    # delete zero bins
    for bin_index in reversed(zero_bin_indexes):
        instances.pop(bin_index)
        colors.pop(bin_index)
        labels.pop(bin_index)

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