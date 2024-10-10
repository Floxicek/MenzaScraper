import requests
from bs4 import BeautifulSoup

def get_daily_menu(cousines: list = [3]) -> list:
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
