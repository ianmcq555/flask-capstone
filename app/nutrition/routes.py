from flask import Blueprint, render_template, request, url_for, redirect, flash
from flask_login import login_required, current_user
from app.models  import Nutrition, Diary
from .forms import CreatePostForm
import requests, json

nutrition = Blueprint('nutrition', __name__, template_folder='nutrition_templates')

@nutrition.route('/nutrition/search', methods=["GET", "POST"])
@login_required
def searchNutrition():
    form = CreatePostForm()
    if request.method == "POST":
        if form.validate():
            name = form.name.data

            url = f'https://api.api-ninjas.com/v1/nutrition?query={name}'
            requests.get(url, headers={'X-Api-Key':'OVILOs9grpcPa7FuOTfl9A==oIp3y6ykbbLgTvcF'})
            response = requests.get(url)
            if response.ok:
                nutrition_dict = {}
                data =  response.json()
                nutrition_dict[name.title()] = {
                    'Serving_Size' : data["serving_size_g"],
                    'Calories' : data["calories"],
                    'Protein' : data["protein_g"],
                    'Carbs' : data["carbohydrates_total_g"],
                    'Fat' : data["fat_total_g"]
            }

                serving_size = nutrition_dict[name.title()]['Serving_Size']
                calories = nutrition_dict[name.title()]['Calories']
                protein = nutrition_dict[name.title()]['Protein']
                carbs = nutrition_dict[name.title()]['Carbs']
                fat = nutrition_dict[name.title()]['Fat']

            else:
                flash('That food does not exist', 'danger')
                return redirect(url_for('nutrition.searchNutrition'))
            
            u1 = Nutrition.query.filter_by(name=name).first()
            if u1:
                flash('Label already exists in Diary', 'danger')
            else:
                flash(f'Succesfully added {name} to Diary!', 'success')
                nutrition = Nutrition(name, serving_size, calories, protein, carbs, fat, current_user.id)
                nutrition.saveToDB()
                

    return render_template('search.html', form=form)

@nutrition.route('/nutrition')
def viewFood():
    nutritions = Nutrition.query.order_by(Nutrition.food_name).all()[::-1]
    return render_template('nutrition.html', nutritions=nutritions)

@nutrition.route('/add_to_diary/<int:nutrition_id>')
@login_required
def addFood(nutrition_id):
    nutrition = Nutrition.query.get(nutrition_id)
    if nutrition:
        # print(current_user.pokemon_team.count())
        if current_user.my_diary.count() == 100:
            flash('diary full')
        else:
            current_user.addToDiary(nutrition)
            flash(f'Successfully added {nutrition.name} to {current_user.username}\'s diary', 'success')
    else:
        flash(f'Cannot add nutrition that does not exist...', 'danger')
    return redirect(url_for('homePage'))

@nutrition.route('/remove_from_diary/<int:pokemon_id>')
@login_required
def removeFood(nutrition_id):
    nutrition = Nutrition.query.get(nutrition_id)
    if nutrition:
        n = Nutrition.query.filter_by(nutrition_id=nutrition.id).first()
        current_user.removeFromDiary(n)
        flash(f'Successfully removed {nutrition.name} from {current_user.username}\'s diary', 'success')
    else:
        flash(f'Cannot remove nutrition that does not exist...', 'danger')

    return redirect(url_for('homePage'))