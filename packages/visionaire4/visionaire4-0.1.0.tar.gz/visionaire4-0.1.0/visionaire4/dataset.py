import json
import base64
import imagesize

from pathlib import PosixPath


def _convert_rel2abs(box_x, box_y, box_w, box_h, img_w, img_h):
    return [box_x * img_w, box_y * img_h, box_w * img_w, box_h * img_h]


def _calculate_area(box_w, box_h, img_w, img_h):
    return (box_w * img_w) * (box_h * img_h)


def _decode_b64img(input_json: PosixPath, img_dir: PosixPath, b64_data: str):
    img_path = img_dir.joinpath(f"{input_json.stem}.jpeg")
    img_data = base64.b64decode(b64_data.replace("data:image/jpeg;base64,", ""))
    with img_path.open("wb") as f:
        f.write(img_data)

    return img_path


class Object(object):
    def toJSON(self, indent=2):
        return json.dumps(
            self,
            default=lambda o: o.__dict__,
            indent=indent,
        )


class V4(Object):
    def __init__(self):
        pass

    def dump(self, target_dir: PosixPath, input_json: PosixPath, content: dict):
        out_dir = target_dir.joinpath(input_json.parent.name)
        out_dir.mkdir(parents=True, exist_ok=True)

        self.analytic_name = content["additional_params"]["analytic_name"]
        self.annotation = content["additional_params"]["annotation"]
        self.metadata = content["additional_params"]["metadata"]

        labelpath = out_dir.joinpath(input_json.name)
        with labelpath.open("w") as f:
            f.write(self.toJSON())

        _decode_b64img(input_json, out_dir, content["images"][0])


class COCO(Object):
    def __init__(self):
        self.info = Object()
        self.info.contributor = "v4-edgecase"
        self.info.description = ""
        self.info.url = ""
        self.info.version = ""
        self.info.date_created = ""
        self.info.year = ""

        # create default license
        license = Object()
        license.name = ""
        license.id = 0
        license.url = ""
        self.licenses = [license]

        # define needed lists
        self.images = []
        self.categories = []
        self.annotations = []

        # temp label maps
        self.labels = {}

    def __add_image(
        self,
        target_dir: PosixPath,
        input_json: PosixPath,
        b64_data: str,
        date_captured=0,
    ):
        img_dir = target_dir.joinpath("images")
        img_dir.mkdir(parents=True, exist_ok=True)
        img_path = _decode_b64img(input_json, img_dir, b64_data)
        try:
            w, h = imagesize.get(img_path)
        except:
            raise RuntimeError(
                f"Unbale to probe size of image '{img_path}', "
                "probably contains invalid or empty data."
            )

        img = Object()
        img.id = len(self.images) + 1
        img.width = w
        img.height = h
        img.file_name = img_path.name
        img.license = 0
        img.flickr_url = ""
        img.coco_url = ""
        img.date_captured = date_captured

        self.images.append(img)
        return img.id, img.width, img.height

    def __add_annotation(
        self,
        img_id: int,
        img_w: float,
        img_h: float,
        label: str,
        bounding_box: dict,
        attributes={},
        iscrowd=0,
    ):
        ann = Object()
        ann.id = len(self.annotations) + 1

        ann.category_id = self.labels.setdefault(label, len(self.categories) + 1)
        if len(self.categories) < ann.category_id:
            category = Object()
            category.id = ann.category_id
            category.name = label
            category.supercategory = ""
            self.categories.append(category)

        ann.image_id = img_id
        ann.area = _calculate_area(
            bounding_box["width"],
            bounding_box["height"],
            img_w,
            img_h,
        )
        ann.bbox = _convert_rel2abs(
            bounding_box["left"],
            bounding_box["top"],
            bounding_box["width"],
            bounding_box["height"],
            img_w,
            img_h,
        )

        def_attrs = {"occluded": False, "rotation": 0.0}
        attrs = {**def_attrs, **attributes}
        ann.attributes = attrs
        ann.iscrowd = iscrowd

        self.annotations.append(ann)

    def dump(self, target_dir: PosixPath, input_json: PosixPath, content: dict):
        img_id, img_w, img_h = self.__add_image(
            target_dir, input_json, content["images"][0]
        )
        self.__add_annotation(
            img_id,
            img_w,
            img_h,
            content["additional_params"]["annotation"][0]["label"],
            content["additional_params"]["annotation"][0]["bounding_box"],
            content["additional_params"]["annotation"][0]["attributes"],
        )
