import os
import json
import base64
import random
import glob
import argparse


def load_data(file_dir, format='.jpg'):
    return glob.glob(os.path.join(file_dir, '*' + format))


def load_json(json_path):
    try:
        assert os.path.splitext(json_path)[-1] == '.json'
        with open(json_path, 'r', encoding='utf-8') as fp:
            data = json.load(fp)
    except Exception as e:
        with open(json_path, 'r') as fp:
            data = json.load(fp)
    return data


def dump_json(json_path, json_data):
    try:
        assert os.path.splitext(json_path)[-1] == '.json' and json_data is not None
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(e)
    return json_path


def get_dict_key(dic, value):
    key = list(dic.keys())[list(dic.values()).index(value)]
    return key


def load_labelme_data(file_name):
    with open(file_name, 'rb') as f:
        image_data = base64.b64encode(f.read()).decode('utf-8')
    return image_data


def random_split(files, rate=0.9):
    random.shuffle(files)
    train_count = int(rate * len(files))
    return files[:train_count], files[train_count:]


def parse_args():
    parser = argparse.ArgumentParser(
        description="labelme annotation to coco or mmseg data format.")
    parser.add_argument(
        "--coco-path",
        type=str,
        default='/data/source_code/dl/all_datasets/coco/',
        help="Directory to labelme images and annotation json files.",
    )
    parser.add_argument(
        "--coco-label-path",
        type=str,
        default='/data/source_code/dl/all_datasets/coco/annotations',
        help="Directory to labelme images and annotation json files.",
    )
    parser.add_argument(
        "--coco-train-path",
        type=str,
        default='/data/source_code/dl/all_datasets/coco/train2017',
        help="Directory to labelme images and annotation json files.",
    )
    parser.add_argument(
        "--coco-val-path",
        type=str,
        default='/data/source_code/dl/all_datasets/coco/val2017',
        help="Directory to labelme images and annotation json files.",
    )
    parser.add_argument(
        "--coco-output",
        type=str,
        default='/data/source_code/dl/all_datasets/coco',
        help="Output json file path.",
    )
    parser.add_argument(
        "--mmseg-path",
        type=str,
        default='/data/source_code/dl/all_datasets/mmseg/',
        help="Directory to labelme images and annotation json files.",
    )
    parser.add_argument(
        "--mmseg-label-path",
        type=str,
        default='/data/source_code/dl/all_datasets/mmseg/annotations',
        help="Directory to labelme images and annotation png files.",
    )
    parser.add_argument(
        "--imagenet-path",
        type=str,
        default='/data/source_code/cv/all_datasets/imagenet/',
        help="Directory to labelme images and annotation json files.",
    )
    parser.add_argument(
        "--labels",
        type=str,
        default=None,
        help="Training labels.",
    )
    parser.add_argument(
        "--width",
        type=int,
        default=1920,
        help="resize width",
    )
    parser.add_argument(
        "--height",
        type=int,
        default=200,
        help="resize height",
    )
    parser.add_argument(
        "--val-rate",
        type=float,
        default=0.1,
        help="val rate",
    )

    return parser.parse_args()
