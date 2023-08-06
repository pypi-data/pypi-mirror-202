import json
import os
import base64
import cv2
import numpy as np
from PIL import Image


def labelme_shapes(polygons, categories):
    shapes = []
    for i, polygon in enumerate(polygons):
        shape = {}
        shape['label'] = categories[i]
        shape['points'] = []

        x = polygon[::2]  # 奇数个是x的坐标
        y = polygon[1::2]  # 偶数个是y的坐标
        for j in range(0, len(x)):
            shape['points'].append([float(x[j]), float(y[j])])
        shape['group_id'] = None
        shape['shape_type'] = "polygon"
        shape['flags'] = {}
        shapes.append(shape)
    return shapes


def mask_to_polygons(mask):
    mask = np.ascontiguousarray(mask)
    res = cv2.findContours(mask.astype("uint8"), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    hierarchy = res[-1]
    if hierarchy is None: return []
    contours = res[-2]
    area = [cv2.contourArea(c) for c in contours]
    if len(area) == 0: return []
    max_idx = np.argmax(area)
    res = [cv2.approxPolyDP(cnt, min(1.0, 0.01 * cv2.arcLength(cnt, True)), True) for i, cnt in enumerate(contours) if
           i == max_idx]
    res = [x.flatten() for x in res]
    return list(res[0])


def get_polygons(masks):
    polygons = [mask_to_polygons(x) for x in masks]

    return polygons


def load_image_data(file_name):
    with open(file_name, 'rb') as f:
        image_data = base64.b64encode(f.read()).decode('utf-8')
    return image_data


def gen_label(polygons, categories, file_name, width, height):
    data = {}
    data['version'] = "4.5.9"
    data['flags'] = {}
    data['shapes'] = labelme_shapes(polygons, categories) if polygons is not None else []
    data['imagePath'] = os.path.basename(file_name)
    data['imageData'] = load_image_data(file_name)
    data['imageHeight'] = height
    data['imageWidth'] = width

    file_path = '%s.json' % os.path.splitext(file_name)[0]
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def meta_label(image_path, masks=None, labels=None):
    image_source = np.asarray(Image.open(image_path).convert('RGB'))
    polygons = get_polygons(masks) if masks is not None and labels is not None else None
    gen_label(polygons, labels, image_path, image_source.shape[1], image_source.shape[0])


if __name__ == "__main__":
    local_image_path = 'assets/Pic_2023_04_11_132658_3.jpg'
    meta_label(local_image_path)
