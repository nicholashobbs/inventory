from flask import Flask, render_template, request, jsonify, redirect, url_for
import json
from datetime import datetime

app = Flask(__name__)

# Define hardcoded list of stores
stores = ['Store 1', 'Store 2', 'Store 3']
names = ['a','b','c']

# Define path to the JSON data file
data_file = 'data.json'

# Load inventory data from the JSON file
with open(data_file, 'r') as f:
    data = json.load(f)

# Define route for the index page
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        selected_store = request.form.get('store')
        return render_template('index.html', stores=stores, selected_store=selected_store, data=data)
    else:
        return render_template('index.html', stores=stores)

# Define route for adding a new inventory item
@app.route('/add_item', methods=['POST'])
def add_item():
    store = request.form['store']
    product = request.form['product']
    stock = int(request.form['stock'])
    min_level = int(request.form['min_level'])
    
    # Update the data dictionary
    if store not in data:
        data[store] = {}
    data[store][product] = {"stock": stock, "min_level": min_level}
    
    # Write the updated data to the JSON file
    with open(data_file, 'w') as f:
        json.dump(data, f)
    
    return jsonify(success=True)

@app.route('/update_stock', methods=['GET', 'POST'])
def update_stock():
    if request.method == 'POST':
        selected_name = request.form.get('name')
        selected_store = request.form.get('store')
        inventory = data[selected_store]
        if request.form.get('submit') == 'Add to Stock':
            update_type = 'add'
        else:
            update_type = 'subtract'
        update_data = {'name': selected_name, 'store': selected_store, 'products': {}}
        for product in inventory:
            quantity = request.form.get(product)
            if quantity is not None and quantity != '':
                if update_type == 'add':
                    inventory[product]['stock'] += int(quantity)
                else:
                    inventory[product]['stock'] -= int(quantity)
                update_data['products'][product] = int(quantity)
        update_data['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open('updates.json', 'a') as f:
            f.write(json.dumps(update_data) + '\n')
        with open('data.json', 'w') as f:
            json.dump(data, f)
        return redirect(url_for('update_stock'))
    else:
        return render_template('update_stock.html', names=names, stores=stores, inventory=None)

if __name__ == '__main__':
    app.run()
