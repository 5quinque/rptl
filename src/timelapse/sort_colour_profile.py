import logging
import math
import shutil

from PIL import Image

from pathlib import Path


logger = logging.getLogger(__name__)


class Files:
    def __init__(self):
        self.image_path = Path("/home/ryan/timelapse/images")
        self.video_path = Path("/home/ryan/timelapse/videos")
        self.timestamped_image_path = Path("/home/ryan/timelapse/timestamped_images")
        self.profiled_image_path = Path("/home/ryan/timelapse/group_test")

    def list_images(self, day):
        image_list = list(self.timestamped_image_path.glob(f"{day}/*.jpg"))
        image_list.sort()

        return image_list

    def get_days(self):
        days = [ d.name for d in self.timestamped_image_path.glob("*") ]
        days.sort()

        return days

    def colour_profile(self, img):
        # Get width and height of Image
        width, height = img.size
    
        # Initialize Variable
        r_total = 0
        g_total = 0
        b_total = 0
    
        count = 0
    
        # Iterate through every fifth pixel in image and add rgb values to total
        # so we can get an average later
        for x in range(0, width, 5):
            for y in range(0, height, 5):
                # r,g,b value of pixel
                r, g, b = img.getpixel((x, y))
    
                r_total += r
                g_total += g
                b_total += b
                count += 1

        return f"{self.round_to_ten(r_total/count)}{self.round_to_ten(g_total/count)}{self.round_to_ten(b_total/count)}"

    def round_to_ten(self, value):
        return math.ceil(math.floor(value / 10) * 10)

    def get_colour_profiles(self):
        return list(self.profiled_image_path.glob("*/*"))

    def get_all_profiled_images(self):
        return list(self.profiled_image_path.glob("*/*/*.jpg"))

    def create_colour_profile(self, filepath):
        image = Image.open(filepath)

        _img = image.convert("RGB", palette=Image.ADAPTIVE, colors=8)
        colour_profile = self.colour_profile(_img)

        dir_name = filepath.parent.name

        # create the directory if it doesn't exist
        Path(f"{self.profiled_image_path}/{dir_name}/{colour_profile}").mkdir(parents=True, exist_ok=True)

        logger.info(f"Saving {filepath.name} to {self.profiled_image_path}/{dir_name}/{colour_profile}/{filepath.name}")

        # copy filepath to self.profiled_image_path
        shutil.copy(filepath, f"{self.profiled_image_path}/{dir_name}/{colour_profile}/{filepath.name}")


def main():
    files = Files()
    days = files.get_days()

    profiled_images = files.get_all_profiled_images()
    profiled_images_names = [ image.name for image in profiled_images ]


    for day in days:
        image_list = files.list_images(day)

        for image in image_list:
            if image.name in profiled_images_names:
                logger.debug(f"Skipping {image.name} as it's already been profiled")
                continue

            files.create_colour_profile(image)


    days = {}
    colour_profiles = files.get_colour_profiles()
    for profile in colour_profiles:
        # get size of profile directory
        size = len(list(profile.glob("*.jpg")))
        logger.info(f"{profile} has {size} images")

        # create days[profile.parent.name] if it doesn't exist
        if profile.parent.name not in days:
            days[profile.parent.name] = []

        days[profile.parent.name].append((profile.name, size))
        # days[profile.parent.name] = size
        # logger.info(f"{profile.name}")

    # print(days)
    for day in days:
        # print highest value for each day
        highest = max(days[day], key=lambda x: x[1])
        logger.info(f"{day}: {highest}")
        # logger.info(f"{day}: {days[day]}")

        # remove all colour_profile directorys not in the highest value
        for profile in days[day]:
            if profile[0] != highest[0]:
                logger.info(f"Removing {profile[0]}")
                shutil.rmtree(f"{files.profiled_image_path}/{day}/{profile[0]}")


if __name__ == "__main__":
    logging.basicConfig(
        # level=opts["--log-level"],
        level="INFO",
        format="[%(asctime)s] <%(levelname)s> [%(name)s] %(message)s",
        force=True,
    )
    main()