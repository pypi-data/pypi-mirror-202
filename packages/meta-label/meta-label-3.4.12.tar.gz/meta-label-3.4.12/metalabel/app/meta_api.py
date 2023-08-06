import numpy as np
import json
import requests


def predict_file(file_path, url):
    image_data = {
        'image_file': open(file_path, 'rb')
    }

    r = requests.post(url, files=image_data)
    if r.status_code == 200:
        defects = json.loads(r.content)['data']['defectList']
        boxes = [[d['topLeft']['x'], d['topLeft']['y'], d['bottomRight']['x'], d['bottomRight']['y']] for d in defects]

        return np.array(boxes)
    else:
        print('Error: {}'.format(file_path))
        return []
