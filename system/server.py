from flask import Flask, request, render_template
import os
import detect
import uuid

# create the flask app
app = Flask(__name__)

# if the upload directory does
# not exist, make sure to create it
UPLOAD_DIR = "uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "image" in request.files:
            image = request.files["image"]
            if image.filename == "":
                return "No selected file"

            # get the file extension (suffix) of the image
            file_extension = os.path.splitext(image.filename)[1]

            # generate a random uuid for the image
            file_name = os.path.join(UPLOAD_DIR, str(uuid.uuid4())) + file_extension

            # save the image
            image.save(file_name)

            # read the licence plate from the image and return it
            return detect.read_licence_plate_text(file_name)

    # if the request was not post, return the default index.html file
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
