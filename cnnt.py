from flask import Flask, request, render_template
from denoise import denoise_image
from ocr import get_text
from translate import translate_text

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        img_file = request.files["image"]
        clean_img = denoise_image(img_file)
        text = get_text(clean_img)
        translated = translate_text(text)
        return render_template("index.html", output=translated)
    return render_template("index.html", output="")

if __name__ == "__main__":
    app.run(debug=True)
