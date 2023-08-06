import cv2
import numpy as np
import torch
from PIL import Image
from segment_anything import build_sam, SamPredictor


class MetaSegment:
    def __init__(self, seg_model_path="models/sam_vit_h_4b8939.pth", device='cuda'):
        # load seg model
        sam = build_sam(checkpoint=seg_model_path)
        sam.to(device)
        self.seg_model = SamPredictor(sam)
        self.device = device

    def predict(self, image_path, boxes=None):
        image_source = Image.open(image_path).convert("RGB")
        image_source = np.asarray(image_source)
        self.seg_model.set_image(image_source)

        if boxes is None:
            transformed_boxes = None
        else:
            transformed_boxes = torch.from_numpy(boxes)
            transformed_boxes = self.seg_model.transform.apply_boxes_torch(transformed_boxes, image_source.shape[:2])
            transformed_boxes = transformed_boxes.to(self.device)

        masks, _, _ = self.seg_model.predict_torch(point_coords=None, point_labels=None, boxes=transformed_boxes,
                                                   multimask_output=False)

        return masks[:, 0, :, :].cpu().numpy()


if __name__ == "__main__":
    m = MetaSegment()

    local_image_path = 'assets/Pic_2023_04_11_132658_3.jpg'

    masks = m.predict(local_image_path, boxes=np.array([[2016, 1398, 2341, 2025], [105, 1307, 350, 1773]]))

    image = cv2.imread(local_image_path)
    for i, mask in enumerate(masks):
        h, w = mask.shape[-2:]
        image = (1 - mask.reshape(h, w, 1)) * image

    cv2.imwrite("masks.png", image)
