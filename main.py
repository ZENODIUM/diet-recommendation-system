from flask import *
import pickle
import pandas as pd
import csv
app = Flask(__name__)
with open('food_model.pickle', 'rb') as file:
    model = pickle.load(file)
food_data = pd.read_csv('done_food_data.csv')
def read_csv(file_path, sort_by='Descrip'):
    with open(file_path, 'r') as f:
        reader = csv.DictReader(f)
        rows = [row for row in reader]
        sorted_rows = sorted(rows, key=lambda x: x[sort_by])
        return sorted_rows

@app.route("/")
def index():
    return render_template("mainpage.html")

@app.route("/predict", methods=['POST'])
def predict():
    # get the user input from the form
    input_1 = float(request.form['input_1'])
    input_2 = float(request.form['input_2'])
    input_3 = float(request.form['input_3'])
    
    # create an input array for the model
    inputs = [[input_1, input_2, input_3]]
    
    # make a prediction using the loaded model
    prediction = model.predict(inputs)
    
    # format the prediction as a string
    if prediction[0] == 'Muscle_Gain':
        result = 'Muscle Gain'
    if prediction[0] == 'Weight_Gain':
        result = 'Weight Gain'
    if prediction[0] == 'Weight_Loss':
        result = 'Weight Loss'
    else:
        result = 'General food'
    
    # render the prediction result on a new page
    return render_template("mainpage.html", result=result)

@app.route("/musclegain", methods=['POST'])
def musclegain():
    vegetarian = request.form.getlist('vegetarian')
    iron = request.form.getlist('iron')
    calcium = request.form.getlist('calcium')
    anyfoods = request.form.getlist('anyfoods')
    if 'iron' in iron:
        muscle_gain_datas = food_data[(food_data['category'] == 'Muscle_Gain') & (food_data['Iron_mg'] > 6)]
    if 'calcium' in calcium:
        muscle_gain_data = food_data[(food_data['category'] == 'Muscle_Gain') & (food_data['Calcium_mg'] > 150)]
    if 'vegetarian' in vegetarian:
        exclude_keywords = ['Egg','Fish', 'meat', 'beef','Chicken','Beef','Deer','lamb','crab','pork','Frog legs','Pork','Turkey','flesh','Ostrich','Emu','cuttelfish','Seaweed','crayfish','shrimp','Octopus']
        muscle_gain_data = food_data[(food_data['category'] == 'Muscle_Gain') & (~food_data['Descrip'].str.contains('|'.join(exclude_keywords)))]
    if 'anyfoods' in anyfoods:    
        muscle_gain_data = food_data[food_data['category'] == 'Muscle_Gain']

# Print 5 random rows from the filtered data
    musclegainfoods = muscle_gain_data['Descrip'].sample(n=5).to_string(index=False)
    
    
    # Your code to filter and retrieve the data goes here 

    # Render the filtered data on the same page
    return render_template("mainpage.html", musclegainfoods=musclegainfoods)

@app.route("/weightgain", methods=['POST'])
def weightgain():
    vegetarian = request.form.getlist('vegetarian')
    iron = request.form.getlist('iron')
    calcium = request.form.getlist('calcium')
    anyfoods = request.form.getlist('anyfoods')
    if 'iron' in iron:
        weight_gain_data = food_data[(food_data['category'] == 'Weight_Gain') & (food_data['Iron_mg'] > 6)]
    if 'calcium' in calcium:
        weight_gain_data = food_data[(food_data['category'] == 'Weight_Gain') & (food_data['Calcium_mg'] > 150)]
        print(weight_gain_data)
    if 'vegetarian' in vegetarian:
        exclude_keywords = ['Egg','Fish', 'meat', 'beef','Chicken','Beef','Deer','lamb','crab','pork','turkey','flesh']
        weight_gain_data = food_data[(food_data['category'] == 'Weight_Gain') & (~food_data['Descrip'].str.contains('|'.join(exclude_keywords)))]
    if 'anyfoods' in anyfoods:    
        weight_gain_data = food_data[food_data['category'] == 'Weight_Gain']

# Print 5 random rows from the filtered data
    weightgainfoods = weight_gain_data['Descrip'].sample(n=5).to_string(index=False)
    # Your code to filter and retrieve the data goes here 

    # Render the filtered data on the same page
    return render_template("mainpage.html", weightgainfoods=weightgainfoods)

@app.route("/weightloss", methods=['POST'])
def weightloss():
    vegetarian = request.form.getlist('vegetarian')
    iron = request.form.getlist('iron')
    calcium = request.form.getlist('calcium')
    anyfoods = request.form.getlist('anyfoods')
    if 'iron' in iron:
        weight_loss_data = food_data[(food_data['category'] == 'Weight_Loss') & (food_data['Iron_mg'] > 6)]
    if 'calcium' in calcium:
        weight_loss_data = food_data[(food_data['category'] == 'Weight_Loss') & (food_data['Calcium_mg'] > 150)]
    if 'vegetarian' in vegetarian:
        exclude_keywords = ['Egg','Fish', 'meat', 'beef','Chicken','Beef','Deer','lamb','crab','pork','turkey','flesh']
        weight_loss_data = food_data[(food_data['category'] == 'Weight_Loss') & (~food_data['Descrip'].str.contains('|'.join(exclude_keywords)))]
    if 'anyfoods' in anyfoods:    
        weight_loss_data = food_data[food_data['category'] == 'Weight_Loss']

# Print 5 random rows from the filtered data
    weightlossfoods = weight_loss_data['Descrip'].sample(n=5).to_string(index=False)
    # Your code to filter and retrieve the data goes here 

    # Render the filtered data on the same page
    return render_template("mainpage.html", weightlossfoods=weightlossfoods)

@app.route("/search", methods=['POST'])
def search(sort_by='Descrip'):
    vegetarian = request.form.getlist('vegetarian')
    iron = request.form.getlist('iron')
    calcium = request.form.getlist('calcium')
    rows = read_csv('done_food_data.csv', sort_by)
    return render_template('search.html', rows=rows)
if __name__ == "__main__":
    app.run()