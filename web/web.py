from datetime import datetime
from pathlib import Path

from flask import Flask, send_file, render_template

from zmq_sender import ZmqSender

app = Flask(__name__)


class Images:
    def __init__(self):
        self.image_path = Path("/home/ryan/timelapse/images")
        # self.image_list = self.list_images()

    def list_images(self, day):
        image_list = list(self.image_path.glob(f"{day}/*.jpg"))
        image_list.sort()

        return image_list
    
    def get_days(self):
        days = [ d.name for d in self.image_path.glob("*") ]
        days.sort()

        return days

    # def filepath_to_timestamp(self, filepath: str):
    #     # filepath is in the format 20230803_014801.jpg

    #     # first, split the filename into date and time
    #     date, time = Path(filepath).stem.split("_")
    #     # then, split the date into year, month, day
    #     year, month, day = date[:4], date[4:6], date[6:]
    #     # then, split the time into hour, minute, second
    #     hour, minute, second = time[:2], time[2:4], time[4:]
    #     # then, return a datetime object
    #     return datetime(int(year), int(month), int(day), int(hour), int(minute), int(second))

    # def get_timestamps(self):
    #     years = self.get_years()
    #     timestamps = {}
    #     for year in years:
    #         months = self.get_months(year)
    #         timestamps[year] = {}
    #         for month in months:
    #             days = self.get_days(year, month)
    #             timestamps[year][month] = {}
    #             for day in days:
    #                 hours = self.get_hours(year, month, day)
    #                 timestamps[year][month][day] = {}
    #                 for hour in hours:
    #                     minutes = self.get_minutes(year, month, day, hour)
    #                     timestamps[year][month][day][hour] = {}
    #                     for minute in minutes:
    #                         timestamps[year][month][day][hour][minute] = {}
    #     return timestamps

    # def get_years(self):
    #     years = []
    #     for image in self.image_list:
    #         timestamp = self.filepath_to_timestamp(image.name)
    #         year = timestamp.year
    #         if year not in years:
    #             years.append(year)
    #     return years

    # def get_months(self, year):
    #     months = []
    #     for image in self.image_list:
    #         timestamp = self.filepath_to_timestamp(image.name)
    #         if timestamp.year == year:
    #             month = timestamp.month
    #             if month not in months:
    #                 months.append(month)
    #     return months

    # def get_days(self, year, month):
    #     days = []
    #     for image in self.image_list:
    #         timestamp = self.filepath_to_timestamp(image.name)
    #         if timestamp.year == year and timestamp.month == month:
    #             day = timestamp.day
    #             if day not in days:
    #                 days.append(day)
    #     return days

    # def get_hours(self, year, month, day):
    #     hours = []
    #     for image in self.image_list:
    #         timestamp = self.filepath_to_timestamp(image.name)
    #         if timestamp.year == year and timestamp.month == month and timestamp.day == day:
    #             hour = timestamp.hour
    #             if hour not in hours:
    #                 hours.append(hour)
    #     return hours

    # def get_minutes(self, year, month, day, hour):
    #     minutes = []
    #     for image in self.image_list:
    #         timestamp = self.filepath_to_timestamp(image.name)
    #         if timestamp.year == year and timestamp.month == month and timestamp.day == day and timestamp.hour == hour:
    #             minute = timestamp.minute
    #             if minute not in minutes:
    #                 minutes.append(minute)
    #     return minutes

@app.route("/get_current_image")
async def get_current_image():
    return render_template("image.html", image_path="/image/now", title="Current Image")
    # return send_file(image_path)


@app.route("/")
def hello_world():
    images = Images()
    day_list = "<ul>"
    for day in images.get_days():
        day_list += f"<li><a href='/day/{day}'>{day}</a></li>"

    # for image in images.image_list:
    #     image_list += f"<li><a href='/image/{image.name}'>{image.name}</a></li>"
    day_list += "<ul>"
    return f"{day_list}<p>Hello, World!</p>"

@app.route("/day/<day>")
def show_day(day):
    images = Images()
    image_list = "<ul>"
    for image in images.list_images(day):
        image_list += f"<li><a href='/image/{day}/{image.name}'>{image.name}</a></li>"
    image_list += "</ul>"
    return f"{image_list}<p>Hello, World!</p>"

@app.route("/image/<directory>/<filename>")
def show_post(directory, filename):
    image_path = f"/home/ryan/timelapse/images/{directory}/{filename}"
    return send_file(image_path)


@app.route("/image/now")
async def show_current_image():
    sender = ZmqSender(zmq_connect_address="tcp://127.0.0.1:5555")
    filename = await sender.send_json({"action": "capture_current_image"})

    image_path = f"/home/ryan/timelapse/{filename}"

    return send_file(image_path)

