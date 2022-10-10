import xml.etree.ElementTree as ET
import os
import cairosvg
import sys


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


def _mod_file_name(filePath, mod):
    file_bn = os.path.basename(filePath)
    file_bn_list = file_bn.split('.')
    return filePath.replace(file_bn, file_bn_list[0] + mod + '.' + file_bn_list[1])


def _get_route_label(elm, routes, scale):
    base_font_size = 36

    elm_id = elm.attrib['id']
    label = routes[elm_id].getRtNum()
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
        'style': f'fill:{routes[elm_id].color_hex};fill-opacity:1;stroke:#FFFFFF;stroke-width:{3*scale};stroke-dasharray:none;stroke-opacity:1',
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
    return circleAttributes, labelAttributes, textAttributes, label


def update_svg(data_input, layer_mode=False):
    namespaces = {
        'inkscape': "http://www.inkscape.org/namespaces/inkscape",
        'sodipodi': "http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd",
        'xlink': "http://www.w3.org/1999/xlink",
        'svg': "http://www.w3.org/2000/svg",
    }
    n = r'{http://www.w3.org/2000/svg}'

    xmlFile = data_input.path_i + data_input.fileName
    tree = ET.parse(xmlFile)
    root = tree.getroot()

    for subTree in root.findall('./svg:g', namespaces):
        #if border is defined try to find the border rectangle and format it
        if data_input.border:
            elements = subTree.findall('./svg:rect', namespaces)
            for elm in elements:
                elm_id = elm.attrib['id']
                if elm_id == data_input.border:
                    borderAttributes = elm.attrib
                    subTree.remove(elm)
                    root.attrib['width'] = borderAttributes['width']
                    root.attrib['height'] = borderAttributes['height']
                    root.attrib['viewBox'] = '{} {} {} {}'.format(borderAttributes['x'],
                                                           borderAttributes['y'],
                                                           borderAttributes['width'],
                                                           borderAttributes['height'])

    width = root.attrib['width']
    scale = round(data_input.scale*float(width)/1920, 2)

    for subTree in root.findall('./svg:g', namespaces):
        #setting if specific layers are defined skip all other layers
        if data_input.layers:
            if '{http://www.inkscape.org/namespaces/inkscape}label' in subTree.attrib.keys():
                if subTree.attrib['{http://www.inkscape.org/namespaces/inkscape}label'] not in data_input.layers:
                    root.remove(subTree)
                    continue
            elif subTree.attrib['id'] not in data_input.layers:
                root.remove(subTree)
                continue

        #loop through all "paths" and format them
        elements = subTree.findall('./svg:path', namespaces)
        for elm in elements:
            elm_id = elm.attrib['id']
            if elm_id in data_input.routes:
                dashlineAttributes = {
                    'id': elm_id + '_clone',
                    'style': f'fill:none;stroke:#FFFFFF;stroke-width:{7*scale};stroke-dasharray:{30*scale}, {30*scale}',
                    'd': elm.attrib['d']
                }
                lineAttributes = {
                    'id': elm_id,
                    'style': f'fill:none;stroke:{data_input.routes[elm_id].color_hex};stroke-width:{7*scale};stroke-dasharray:none',
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
            if elm_id in data_input.routes:

                circleAttributes, labelAttributes, textAttributes, label = _get_route_label(elm, data_input.routes, scale)
                elm.clear()
                ET.SubElement(subTree, f'{n}circle', circleAttributes)
                ET.SubElement(subTree, f'{n}text', labelAttributes)
                for elm2 in root.findall('./svg:g/svg:text', namespaces):
                    if elm2.attrib['id'] == labelAttributes['id']:
                        t = ET.SubElement(elm2, f'{n}text', textAttributes).text = str(label)

    # write to file
    newSVG = data_input.path_o + data_input.outFileName.split('.')[0] + '.svg'

    if os.path.exists(newSVG):
        old_root = ET.parse(newSVG).getroot()
        if ET.tostring(root) == ET.tostring(old_root):
            print(f'File {xmlFile} already up to date')
            return

    print(f'writing {xmlFile} to png')
    newPNG = newSVG.replace('.svg', '.png')
    ET.indent(tree)
    tree.write(newSVG)
    fileObj = open(newSVG)
    if data_input.size == 'h':
        owidth = 600
    else:
        owidth = 1200

    cairosvg.svg2png(file_obj=fileObj,
                     write_to=newPNG, dpi=200, output_width=owidth
                     )
    fileObj.close()
    return


if __name__ == '__main__':
    sys.exit()