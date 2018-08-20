from flask import Flask, render_template, request, redirect, url_for, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)

# create sqlite database
engine = create_engine('sqlite:///restaurantmenu.db',connect_args={'check_same_thread': False})
Base.metadata.bind = engine

# bind DBSession to Sqlite Engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Show all restaurants
@app.route('/')
@app.route('/restaurants/')
def restaurantsIndex():
    try:
        restaurants = session.query(Restaurant).all()
        return render_template('index.html',restaurants=restaurants)
    except Exception as e: 
        print(e)
        return("hello")

# Create a New Restaurant
@app.route('/restaurant/new', methods=['GET', 'POST'])
def newRestaurantItem():
    if request.method == 'POST':
        newRestaurantItem = Restaurant(name=request.form['name'])
        session.add(newRestaurantItem)
        session.commit()
        return redirect(url_for('restaurantsIndex'))
    else:
        return render_template('newrestaurantitem.html')

# Edit a restaurant 
@app.route('/restaurants/<int:restaurant_id>/edit',   methods=['GET', 'POST'])
def editRestaurantItem(restaurant_id):
    editRestaurantItem = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method =='POST':
        if request.form['name']:
            editRestaurantItem.name = request.form['name']
        session.add(editRestaurantItem)
        session.commit()
        return redirect(url_for('restaurantsIndex'))
    else:
        return render_template('editrestaurantitem.html', restaurant_id=restaurant_id, item=editRestaurantItem)

# Delete a restaurant 
@app.route('/restaurants/<int:restaurant_id>/delete',   methods=['GET', 'POST'])
def deleteRestaurantItem(restaurant_id):
    deleteRestaurantItem = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method =='POST':
        items = session.query(MenuItem).filter_by(id=restaurant_id).all()
        for item in items:
            session.delete(item)
        session.delete(deleteRestaurantItem)
        session.commit()
        return redirect(url_for('restaurantsIndex'))
    else:
        return render_template('deleteRestaurantItem.html', restaurant_id=restaurant_id, item=deleteRestaurantItem)

# Show a restaurant menu
@app.route('/restaurants/<int:restaurant_id>/menu')
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id)
    return render_template(
        'menu.html', restaurant=restaurant, items=items, restaurant_id=restaurant_id)

# Create a new menu item 
@app.route('/restaurants/<int:restaurant_id>/new', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):

    if request.method == 'POST':
        newItem = MenuItem(name=request.form['name'], description=request.form[
                           'description'], price=request.form['price'], course=request.form['course'], restaurant_id=restaurant_id)
        session.add(newItem)
        session.commit()
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('newmenuitem.html', restaurant_id=restaurant_id)


# Edit a restaurant menu 
@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit',
           methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    editedItem = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['description']
        if request.form['price']:
            editedItem.price = request.form['price']
        if request.form['course']:
            editedItem.course = request.form['course']
        session.add(editedItem)
        session.commit()
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template(
            'editmenuitem.html', restaurant_id=restaurant_id, menu_id=menu_id, item=editedItem)



# delete a menu item
@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete',
           methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    itemToDelete = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('deletemenuitem.html', item=itemToDelete)


# API calls to return Json Data

# Return Json of all restaurants
@app.route('/restaurants/JSON')
def restaurantsJson():
    restaurants = session.query(Restaurant).all()
    return jsonify(Restaurants=[i.serialize for i in restaurants])


# Return all menu times in Json format
@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
    return jsonify(MenuItems=[i.serialize for i in items])


# Return Json data of one menu item
@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def menuItemJSON(restaurant_id, menu_id):
    menuItem = session.query(MenuItem).filter_by(id=menu_id).one()
    return jsonify(MenuItem=menuItem.serialize)

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)