import logging
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

logger = logging.getLogger(__name__)


class Files:
    def __init__(self):
        self.image_path = Path("images")
        self.video_path = Path("videos")
        self.timestamped_image_path = Path("timestamped_images")

    def list_images(self, day):
        image_list = list(self.image_path.glob(f"{day}/*.jpg"))
        image_list.sort()

        return image_list

    def get_days(self):
        days = [d.name for d in self.image_path.glob("*")]
        days.sort()

        return days

    def create_timestamped_image(self, filepath):
        # check if we've already timestamped this image
        if Path(
            f"{self.timestamped_image_path}/{filepath.parent.name}/{filepath.name}"
        ).exists():
            return

        filepath = Path(filepath)
        # e.g. filepath = "requested_images/20230811/20230811_150729.jpg";
        img = Image.open(filepath)

        # resize the image, but keep the aspect ratio
        img.thumbnail((1000, 1000))

        # Call draw Method to add 2D graphics in an image
        draw = ImageDraw.Draw(img)

        datetime_exif = img._getexif()[36867]

        font_size = 32
        font = ImageFont.truetype("DejaVuSansMono.ttf", font_size)
        # text_width = draw.textlength(datetime_exif,font)
        x = 5  # left align
        y = img.height - font_size - 5  # bottom align
        draw.text(
            (x, y),
            datetime_exif,
            font=font,
            fill=(255, 255, 255),
            stroke_fill=(0, 0, 0),
            stroke_width=1,
        )

        dir_name = filepath.parent.name

        # create the directory if it doesn't exist
        Path(f"{self.timestamped_image_path}/{dir_name}").mkdir(
            parents=True, exist_ok=True
        )

        logger.info(
            f"Saving {filepath.name} to {self.timestamped_image_path}/{dir_name}/{filepath.name}"
        )

        # Save the edited image
        img.save(
            f"{self.timestamped_image_path}/{dir_name}/{filepath.name}",
            "JPEG",
            quality=100,
            optimize=True,
            progressive=True,
        )


def run():
    files = Files()
    days = files.get_days()

    for day in days:
        image_list = files.list_images(day)

        for image in image_list:
            files.create_timestamped_image(image)


if __name__ == "__main__":
    logging.basicConfig(
        # level=opts["--log-level"],
        level="INFO",
        format="[%(asctime)s] <%(levelname)s> [%(name)s] %(message)s",
        force=True,
    )
    run()
