
from flask import Blueprint,Flask, send_file, render_template, g

from files import Files
from zmq_sender import ZmqSender


# Create a blueprint
rendered_routes = Blueprint("rendered_routes", __name__)

app = Flask(__name__)

# This function will run before every request
@rendered_routes.before_request
def before_request():
    files = Files()
    g.image_days_list = files.get_days()

# Define a context processor to automatically pass data to templates
@rendered_routes.context_processor
def inject_stuff():
    return {"image_days_list": g.image_days_list}

@rendered_routes.route("/get_current_image")
async def get_current_image():
    return render_template("image.html", image_path="/image/now", title="Current Image")


@rendered_routes.route("/")
def hello_world():
    files = Files()
    latest_image = files.get_latest_image()
    # print(latest_image)
    return render_template("index.html", latest_image=latest_image, title="Home")

@rendered_routes.route("/day/<day>")
def show_day(day):
    files = Files()

    return render_template("image_list.html", day=day, image_list=files.list_images(day), title=day)

@rendered_routes.route("/videos")
def show_videos():
    files = Files()

    return render_template("video_list.html", video_list=files.list_videos(), title="Videos")


@rendered_routes.route("/view_video/<filename>")
def show_video(filename):
    return render_template("video.html", video_path=f"/video/{filename}", title=filename)

@rendered_routes.route("/view/<directory>/<filename>")
def view_image(directory, filename):
    return render_template("image.html", image_path=f"/image/{directory}/{filename}", title=filename)


@app.route("/video/<filename>")
def show_video(filename):
    video_path = f"/home/ryan/timelapse/videos/{filename}"
    print("a", video_path)
    return send_file(video_path)

@app.route("/image/<directory>/<filename>")
def show_image(directory, filename):
    image_path = f"/home/ryan/timelapse/images/{directory}/{filename}"
    return send_file(image_path)

@app.route("/requested_image/<directory>/<filename>")
def show_requested_image(directory, filename):
    image_path = f"/home/ryan/timelapse/requested_images/{directory}/{filename}"
    return send_file(image_path)

@app.route("/image/now")
async def show_current_image():
    sender = ZmqSender(zmq_connect_address="tcp://127.0.0.1:5555")
    filename = await sender.send_json({"action": "capture_current_image"})

    image_path = f"/home/ryan/timelapse/{filename}"

    return send_file(image_path)

app.register_blueprint(rendered_routes)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)