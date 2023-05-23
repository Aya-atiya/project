from flask import Flask, request, render_template
import torch
import csv

app = Flask(__name__)

# Load YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'custom', 'last.pt')

# Load calorie dataset
filename = "caloridata - Calorie Dataset.csv"
calorie_data = {}

with open(filename, "r") as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        calorie_data[row[0]] = float(row[2])

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        # Check if an image file was uploaded
        if "image" in request.files:
            image_file = request.files["image"]
            image_path = "uploaded_image.jpg"  # Path to save the uploaded image
            image_file.save(image_path)

            # Process the uploaded image with YOLOv5 model
            results = model(image_path)
            
            df = results.pandas().xyxy[0]
            global search_strings
            search_strings = df["name"].unique().tolist()
            food= search_strings
            res=[]
        with open(filename, "r") as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if any(s in row[0] for s in search_strings):
                    result_str = "Calori of "  +row[0] +" in"+ row[1] +" gram"+ " is " + row[2] +" Calories"
                    if result_str not in res:
                        res.append(result_str)
            
            print(res)
           
            
            
            return render_template("results.html", search_strings=search_strings,res=res)

    return render_template("index.html")

@app.route("/calculate", methods=["POST"])
def calculate():
    
    goal = float(request.form["goal"])
    total_calories = 0

    foods = request.form.getlist("food")
    quantities = request.form.getlist("quantity")

    


    for i, food in enumerate(search_strings):
        quantity = float(quantities[i])
        calories = calorie_data[food]* (quantity / 100)
        total_calories += calories
        print(foods)

        

    return render_template("summary.html", total_calories=total_calories, goal=goal)
if __name__ == "__main__":
    app.run(debug=True)
