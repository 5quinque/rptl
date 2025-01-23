from pathlib import Path


class Files:
    def __init__(self):
        self.image_path = Path("/home/ryan/timelapse/images")
        self.video_path = Path("/home/ryan/timelapse/videos")

    def list_images(self, day):
        image_list = list(self.image_path.glob(f"{day}/*.jpg"))
        image_list.sort()

        return image_list

    def get_days(self):
        days = [d.name for d in self.image_path.glob("*")]
        days.sort()

        return days

    def get_latest_day(self):
        days = self.get_days()
        return days[-1]

    def get_latest_image(self):
        latest_day_path = self.image_path / self.get_latest_day()
        image_list = list(latest_day_path.glob("*.jpg"))
        image_list.sort()
        return image_list[-1]

    def list_videos(self):
        video_list = list(self.video_path.glob("*.mp4"))
        video_list.sort()

        return video_list

