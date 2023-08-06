import cv2
import torch
from groundingdino.util.slconfig import SLConfig
from groundingdino.models import build_model
from groundingdino.util import box_ops
from groundingdino.util.utils import clean_state_dict
from groundingdino.util.inference import load_image, predict


class MetaDetection:
    def __init__(self,
                 det_config_file="models/GroundingDINO_SwinB.cfg.py",
                 det_model_path='models/groundingdino_swinb_cogcoor.pth',
                 device='cuda'):
        # load det model
        args = SLConfig.fromfile(det_config_file)
        self.det_model = build_model(args)
        args.device = device
        checkpoint = torch.load(det_model_path, map_location='cpu')
        self.det_model.load_state_dict(clean_state_dict(checkpoint['model']), strict=False)
        self.det_model.eval()
        self.det_model.to(device)
        self.device = device

    def predict(self, image_path, text_prompt="bottles", box_thresh=0.2, text_thresh=0.1):
        image_source, image_transform = load_image(image_path)
        boxes, _, _ = predict(model=self.det_model, image=image_transform, caption=text_prompt,
                              box_threshold=box_thresh, text_threshold=text_thresh, device=self.device)
        H, W, _ = image_source.shape
        boxes = box_ops.box_cxcywh_to_xyxy(boxes) * torch.Tensor([W, H, W, H])

        return boxes.numpy()


if __name__ == "__main__":
    m = MetaDetection()

    local_image_path = 'assets/Pic_2023_04_11_132658_3.jpg'

    boxes = m.predict(local_image_path, text_prompt="bottles")

    image = cv2.imread(local_image_path)
    for i, box in enumerate(boxes):
        x1, y1, x2, y2 = int(box[0]), int(box[1]), int(box[2]), int(box[3])
        cv2.rectangle(image, (x1, y1), (x2, y2), (255, 0, 255), 2)

    cv2.imwrite("boxes.png", image)
