import xml.etree.ElementTree as ET
import os
import cairosvg
import sys
from lbResources import mod_file_extension
"""
Contains update_svg() function which opens an svg file associated with a ItemMap object and replaces all place holder 
vectors with formatted vectors
"""


def _getApproximateArialStringWidth(st, min_size=False):
    '''
    Inputs a string and returns the width of the string when renedered in 12 pt arial font in picas. (1pica=12pt)
    '''
    #https://stackoverflow.com/questions/16007743/roughly-approximate-the-width-of-a-string-of-text-in-python
    size = 0 # in milinches
    for s in st:
        if s in 'lij|\' ': size += 37
        elif s in '![]fI.,:;/\\t': size += 50
        elif s in '`-(){}r"': size += 60
        elif s in '*^zcsJkvxy': size += 85
        elif s in 'aebdhnopqug#$L+<>=?_~FZT1234567890': size += 95
        elif s in 'BSPEAKVXY&UwNRCHD': size += 112
        elif s in 'QGOMm%W@': size += 135
        else: size += 50
    if min_size: size = max(size, 190)
    return size * 6 / 1000.0 # Convert to picas


def _gen_label(elm, label, color, scale):
    base_font_size = 36

    elm_id = elm.attrib['id']
    font_size = base_font_size * scale

    # these inputs don't make a ton of sense, but I found them to be effective via trial and error
    radius = str(round(font_size*(0.5*_getApproximateArialStringWidth(label, min_size=True)+0.3), 4))
    text_x_offset = round(0.5*font_size*_getApproximateArialStringWidth(label), 4)
    text_y_offset = round(0.4*base_font_size*scale, 4)

    transform = False
    if 'transform' in elm.keys():
        transform = True

    circleAttributes = {
        'id': elm_id,
        'style': f'fill:{color};fill-opacity:1;stroke:#FFFFFF;stroke-width:{3*scale};stroke-dasharray:none;stroke-opacity:1',
        'cx': elm.attrib['cx'],
        'cy': elm.attrib['cy'],
        'r': radius
    }
    if transform:
        circleAttributes['transform'] = elm.attrib['transform']

    labelAttributes = {
        'id': elm_id + '_label',
        'style': f'font-size:37.3333px;fill:#ffffff;fill-opacity:1;stroke:#ff0000;stroke-width:{1*scale};stroke-dasharray:none;stroke-opacity:1',
        'x': str(float(elm.attrib['cx'])-text_x_offset),
        'y': str(float(elm.attrib['cy'])+text_y_offset),
    }
    textAttributes = {
        'id': elm_id + '_text',
        'x': labelAttributes['x'],
        'y': labelAttributes['y'],
        'style':f'font-style:normal;font-variant:normal;font-weight:bold;font-stretch:normal;font-size:{font_size}px;font-family:Arial;-inkscape-font-specification:\'Arial Bold\';fill:#FFFFFF;fill-opacity:1;stroke:none',
    }
    if transform:
        labelAttributes['transform'] = circleAttributes['transform']
    return circleAttributes, labelAttributes, textAttributes


def _transform(transform_att, coordinates):
    '''
    This function is intended to handle elements with a transform attribute (read about it here: https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/transform)
    if the attribute is present coordinates need to be adjusted according to the transform matrix which has the format
    'matrix(a,b,c,d,e,f)'.
    inputs:
        transform_att (string): transform attribute from svg format
        coordinates (list of strings): xy pair of coordinates to be transformed
    '''
    x, y = [float(i) for i in coordinates]
    if 'matrix' in transform_att:
        trans_matrix = transform_att[7:-1].split(',')  # convert to transform input to list
        a, b, c, d, e, f, = [float(i) for i in trans_matrix]
        new_x = x*a+y*c+e
        new_y = x*b+d*y+f
    elif 'translate' in transform_att:
        trans_matrix = transform_att[10:-1].split(',')  # convert to transform input to list
        a, b = [float(i) for i in trans_matrix]
        new_x = x+a
        new_y = y+b
    else:
        new_x = x
        new_y = y


    return [str(new_x), str(new_y)]


def _update_border(root, ItemMap, namespaces, scale):
    viewBox_i = root.attrib['viewBox']
    viewBox_i = [float(x) for x in viewBox_i.split()]
    width_i = viewBox_i[2] - viewBox_i[0]
    width_f = width_i
    for subTree in root.findall('./svg:g', namespaces):
        #if border is defined try to find the border rectangle and format it
        if ItemMap.border:
            elements = subTree.findall('./svg:rect', namespaces)
            for elm in elements:
                elm_id = elm.attrib['id']
                if elm_id == ItemMap.border:
                    borderAttributes = elm.attrib
                    subTree.remove(elm)
                    if 'transform' in subTree.keys():
                        old_x1, old_y1 = borderAttributes['x'], borderAttributes['y']
                        old_x2 = str(float(old_x1)+float(borderAttributes['width']))
                        old_y2 = str(float(old_y1) + float(borderAttributes['height']))
                        new_x1, new_y1 = _transform(subTree.attrib['transform'], [old_x1, old_y1])
                        new_x2, new_y2 = _transform(subTree.attrib['transform'], [old_x2, old_y2])

                        borderAttributes['x'] = new_x1
                        borderAttributes['y'] = new_y1
                        borderAttributes['width'] = str(float(new_x2)-float(new_x1))
                        borderAttributes['height'] = str(float(new_y2) - float(new_y1))


                    root.attrib['width'] = borderAttributes['width']
                    root.attrib['height'] = borderAttributes['height']
                    root.attrib['viewBox'] = '{} {} {} {}'.format(borderAttributes['x'],
                                                           borderAttributes['y'],
                                                           borderAttributes['width'],
                                                           borderAttributes['height'])
                    width_f = float(borderAttributes['width'])
    scale = round(scale * width_f / width_i, 2)
    return scale


def _crop_to_aspect(root, ItemMap, scale):
    '''
    Checks if an aspect ratio for the map is defined and if so crops the image to fit that aspect
    '''
    if ItemMap.aspect_ratio:
        viewBox_i = root.attrib['viewBox']
        viewBox_i = [float(x) for x in viewBox_i.split()]
        viewBox_f = viewBox_i
        width_i = viewBox_i[2]
        height_i = viewBox_i[3]
        aspect_ratio_i = width_i / height_i
        if aspect_ratio_i < ItemMap.aspect_ratio:
            height_f = width_i / ItemMap.aspect_ratio
            width_f = width_i
            h_adj = (height_i - height_f) / 2
            viewBox_f[1] = viewBox_f[1] + h_adj
            viewBox_f[3] = height_f
        else:
            width_f = height_i * ItemMap.aspect_ratio
            height_f = height_i
            w_adj = (width_i - width_f) / 2
            viewBox_f[0] = viewBox_f[0] + w_adj
            viewBox_f[2] = width_f
        root.attrib['width'] = str(width_f)
        root.attrib['height'] = str(height_f)
        root.attrib['viewBox'] = ' '.join([str(x) for x in viewBox_f])
        scale = round(scale * width_f / width_i, 2)
    return scale

def update_svg(ItemMap):
    newImage = ItemMap.path_o + ItemMap.out_file_name
    newSVG = ItemMap.path_o + mod_file_extension(ItemMap.out_file_name, '.svg')
    xmlFile = ItemMap.path_i + ItemMap.file_name

    # check if file needs to be updated
    # if os.path.exists(newImage):
    #     # if the new image is newer than the input file do not update it
    #     if os.path.getmtime(newImage) > os.path.getmtime(xmlFile):
    #         print(f'File {ItemMap.out_file_name} already up to date')
    #         return

    namespaces = {
        'inkscape': "http://www.inkscape.org/namespaces/inkscape",
        'sodipodi': "http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd",
        'xlink': "http://www.w3.org/1999/xlink",
        'svg': "http://www.w3.org/2000/svg",
    }
    n = r'{http://www.w3.org/2000/svg}'

    tree = ET.parse(xmlFile)
    root = tree.getroot()

    scale = round(ItemMap.scale * float(root.attrib['width']) / 1920, 2) # create a local instance of scale so that the object attribute isn't manipulated
    scale = _update_border(root, ItemMap, namespaces, scale)
    scale = _crop_to_aspect(root, ItemMap, scale)

    for subTree in root.findall('./svg:g', namespaces):
        sub_area_elemets = []
        if hasattr(ItemMap, 'sub_areas'):
            for elm in subTree.findall('./svg:rect', namespaces):
                if elm.attrib['id'] in ItemMap.sub_areas:
                    sub_area_elemets.append(elm)

        #if specific layers are defined skip (empty) all other layers
        if hasattr(ItemMap, 'layers') and ItemMap.layers:
            if '{http://www.inkscape.org/namespaces/inkscape}label' in subTree.attrib.keys():
                if subTree.attrib['{http://www.inkscape.org/namespaces/inkscape}label'] not in ItemMap.layers:
                    #clear all elements from subtree
                    attributes = subTree.attrib
                    subTree.clear()
                    subTree.attrib = attributes
            elif subTree.attrib['id'] not in ItemMap.layers:
                #clear all elements from subtree
                attributes = subTree.attrib
                subTree.clear()
                subTree.attrib = attributes

        if sub_area_elemets:
            for elm in sub_area_elemets:
                sub_area = ItemMap.sub_areas[elm.attrib['id']]
                label = sub_area.getSubAreaLtr()
                color = ItemMap.parent.color_hex
                elm.attrib['cx'] = str(float(elm.attrib['x']) + 0.5 * float(elm.attrib['width']))
                elm.attrib['cy'] = str(float(elm.attrib['y']) + 0.5 * float(elm.attrib['height']))
                circleAttributes, labelAttributes, textAttributes = _gen_label(elm, label, color, scale)
                ET.SubElement(subTree, f'{n}circle', circleAttributes)
                ET.SubElement(subTree, f'{n}text', labelAttributes)
                for elm2 in root.findall('./svg:g/svg:text', namespaces):
                    if elm2.attrib['id'] == labelAttributes['id']:
                        t = ET.SubElement(elm2, f'{n}text', textAttributes).text = str(label)

                #loop through all "paths" and format them
        elements = subTree.findall('./svg:path', namespaces)
        for elm in elements:
            elm_id = elm.attrib['id']
            if elm_id in ItemMap.routes:
                dashlineAttributes = {
                    'id': elm_id + '_clone',
                    'style': f'fill:none;stroke:#FFFFFF;stroke-width:{7*scale};stroke-dasharray:{30*scale}, {30*scale}',
                    'd': elm.attrib['d']
                }
                lineAttributes = {
                    'id': elm_id,
                    'style': f'fill:none;stroke:{ItemMap.routes[elm_id].color_hex};stroke-width:{7 * scale};stroke-dasharray:none',
                    'd': elm.attrib['d']
                }
                if 'marker' in elm.attrib['style']:
                    markerStrings = [x for x in elm.attrib['style'] if 'marker' in x]
                    lineAttributes['style'] = lineAttributes['style'] + ';' + ';'.join(markerStrings)
                elm.attrib['id'] = lineAttributes['id']
                elm.attrib['style'] = lineAttributes['style']
                elm.attrib['d'] = lineAttributes['d']
                ET.SubElement(subTree, f'{n}path', dashlineAttributes)

        #loop through all "ellipses" and format them
        elements = subTree.findall('./svg:ellipse', namespaces) + subTree.findall('./svg:circle', namespaces)
        for elm in elements:
            elm_id = elm.attrib['id']
            if elm_id in ItemMap.routes:

                label = ItemMap.routes[elm_id].getRtNum()
                color = ItemMap.routes[elm_id].color_hex

                circleAttributes, labelAttributes, textAttributes = _gen_label(elm, label, color, scale)
                subTree.remove(elm)
                ET.SubElement(subTree, f'{n}circle', circleAttributes)
                ET.SubElement(subTree, f'{n}text', labelAttributes)
                for elm2 in root.findall('./svg:g/svg:text', namespaces):
                    if elm2.attrib['id'] == labelAttributes['id']:
                        t = ET.SubElement(elm2, f'{n}text', textAttributes).text = str(label)

    # write to file
    ET.indent(tree)

    # check if the new image is actually different and only update if it is
    if os.path.exists(newImage):
        old_root = ET.parse(newSVG).getroot()
        if ET.tostring(root) == ET.tostring(old_root):
            print(f'File {ItemMap.out_file_name} already up to date')
            return

    tree.write(newSVG)
    file_Obj = open(newSVG)
    if ItemMap.size in ['f', 'h']:
        print(f'writing {xmlFile} to png')
        if ItemMap.size == 'h':
            owidth = 600
        else:
            owidth = 1200
        cairosvg.svg2png(file_obj=file_Obj, write_to=newImage, dpi=200, output_width=owidth)
    else:
        print(f'writing {xmlFile} to pdf')
        cairosvg.svg2png(file_obj=file_Obj, write_to=newImage, dpi=200)

    file_Obj.close()
    return


if __name__ == '__main__':
    sys.exit()