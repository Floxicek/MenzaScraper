import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re

class Food:
    translation = {
        "Hlavní jídla": "Main",
        "Polévky": "Soup",
        "Vegetariánská jídla": "Vegetarian",
        "Minutky": "Quick",
        "Minutka": "Quick",
        "Moučníky": "Dessert",
        "Studená jídla": "Cold",
        "Specialita dne": "Special",
        "Bezmasá jídla": "Vegetarian",
        "Saláty a talíře": "Salad",
    }
    
    
    def __init__(self, name, type, place, last_seen_now=True):
        self.name = name
        self.type = Food.translation.get(type, type)
        self.place = place
        self.key = re.split("/|,|-", name)[0] # Key to merge food with different side dishes
        
        if self.key == "CHLAZENÝ PULT ":
            self.key = re.split("/|,|-", name)[1]
    
        if last_seen_now:
            self.last_seen = datetime.now().date()
        else:
            self.last_seen = None

    def __repr__(self):
        return f"Food(name={self.name}, type={self.type}, place={self.place}, key={self.key})"


def get_from_weekly_menu(cousines: list = [3]) -> list:
    foods = []
    for i in cousines:
        url = f"https://agata.suz.cvut.cz/jidelnicky/indexTyden.php?lang=cs&clPodsystem={i}"

        response = requests.get(url)
        html_content = response.text

        soup = BeautifulSoup(html_content, "html.parser")
        curr_cous_food = []
        current_day = -1
        table_rows = soup.find_all('tr')
        for row in table_rows:
            cols = row.find_all('td')
            
            if len(cols) == 1:
                # Day
                if current_day >= 0:
                    break
                curr_cous_food.append([])
                current_day += 1
            
            if len(cols) == 2:
                # soup
                # typ = cols[0].get_text(strip=True)
                food = cols[1].get_text(strip=True)
                
                if food:
                    curr_cous_food[current_day].append(food)
            elif len(cols) == 3:
                # main course
                # typ = cols[0].get_text(strip=True)
                # amount = cols[1].get_text(strip=True).replace('\xa0', ' ')
                food = cols[2].get_text(strip=True)
                if food:
                    curr_cous_food[current_day].append(food)
        
        foods.append(curr_cous_food)
    return foods


def get_from_daily_menu(cantine_id = 3) -> list:
    menu = []
    url = f"https://agata.suz.cvut.cz/jidelnicky/index.php?clPodsystem={cantine_id}&lang=cs"

    response = requests.get(url)
    html_content = response.text
    # with open('save_websites/technicka.html', 'r', encoding='utf-8') as file:
    #     html_content = file.read()

    soup = BeautifulSoup(html_content, "html.parser")
    
    cantine_name = soup.find('div', class_='col-5').find('b').get_text(strip=True).split(',')[0]

    category = None
    tbody = soup.find('tbody')
    for row in tbody.find_all('tr'):
        header = row.find('th', colspan=True)
        if header:
            category = header.text.strip()
            continue

        food_cell = row.find_all('td')[2]
        if food_cell:
            food_name = food_cell.text.strip()

            food_instance = Food(name=food_name, type=category, place=cantine_name)
            menu.append(food_instance)

    return menu
        

get_from_daily_menu()