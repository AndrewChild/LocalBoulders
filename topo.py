import xml.etree.ElementTree as ET
import os
import cairosvg
import sys


def _mod_file_name(filePath, mod):
    file_bn = os.path.basename(filePath)
    file_bn_list = file_bn.split('.')
    return filePath.replace(file_bn, file_bn_list[0] + mod + '.' + file_bn_list[1])

def _get_route_label(elm, routes, scale):

    elm_id = elm.attrib['id']
    label = routes[elm_id].getRtNum()
    labellen = len(str(label))
    if labellen < 3:
        radius = str(20*scale)
    else:
        radius = str((labellen-2)*4*scale+20*scale)

    circleAttributes = {
        'id': elm_id,
        'style': f'fill:{routes[elm_id].color_hex};fill-opacity:1;stroke:#FFFFFF;stroke-width:{3*scale};stroke-dasharray:none;stroke-opacity:1',
        'cx': elm.attrib['cx'],
        'cy': elm.attrib['cy'],
        'r': radius
    }
    labelAttributes = {
        'id': elm_id + '_label',
        'style': f'font-size:37.3333px;fill:#ffffff;fill-opacity:1;stroke:#ff0000;stroke-width:{1*scale};stroke-dasharray:none;stroke-opacity:1',
        'x': str(float(elm.attrib['cx'])-6*labellen*scale),
        'y': str(float(elm.attrib['cy'])+7*scale),
    }
    textAttributes = {
        'id': elm_id + '_text',
        'x': labelAttributes['x'],
        'y': labelAttributes['y'],
        'style':f'font-style:normal;font-variant:normal;font-weight:bold;font-stretch:normal;font-size:{19*scale}px;font-family:Arial;-inkscape-font-specification:\'Arial Bold\';fill:#FFFFFF;fill-opacity:1;stroke:none',
    }
    return circleAttributes, labelAttributes, textAttributes, label


def update_svg(data_input):
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

    width = root.attrib['width']
    scale = round(data_input.scale*float(width)/1920, 2)

    for subTree in root.findall('./svg:g', namespaces):
        #loop through all "paths" and format them
        elements = subTree.findall('./svg:path', namespaces)
        for elm in elements:
            elm_id = elm.attrib['id']
            if elm_id in data_input.routes:
                dashlineAttributes = {
                    'id': elm_id + '_clone',
                    'style': f'fill:none;stroke:#FFFFFF;stroke-width:{5*scale};stroke-dasharray:{20*scale}, {20*scale}',
                    'd': elm.attrib['d']
                }
                lineAttributes = {
                    'id': elm_id,
                    'style': f'fill:none;stroke:{data_input.routes[elm_id].color_hex};stroke-width:{5*scale};stroke-dasharray:none',
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
    newSVG = data_input.path_o + data_input.fileName.split('.')[0] + '_c.' + data_input.fileName.split('.')[1]

    if os.path.exists(newSVG):
        old_root = ET.parse(newSVG).getroot()
        if ET.tostring(root) == ET.tostring(old_root):
            print(f'File {xmlFile} already up to date')
            return

    print(f'writing {xmlFile} to png')
    newPNG = newSVG.replace('.svg', '.png')
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