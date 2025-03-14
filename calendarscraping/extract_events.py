from bs4 import BeautifulSoup
from ics import Calendar, Event
from datetime import datetime, timedelta
import re
import pytz  # За по-добра работа с часови зони

# Зареждане на HTML файла
with open('calendar.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

soup = BeautifulSoup(html_content, 'html.parser')

# Намиране на всички таблици, които съдържат информация за събития
all_tables = soup.find_all('table')

print(f"Намерени са {len(all_tables)} таблици.")

# Създаване на календар
calendar = Calendar()

# Брой на намерените събития
event_count = 0
closed_count = 0

# Задаване на часовата зона на Nürburg (същата като Berlin)
nurburg_tz = pytz.timezone('Europe/Berlin')

# Търсене на дати - обработва и отворени, и затворени дни
for table in all_tables:
    # Намиране на td елемент с данните
    td_element = table.find('td')
    if not td_element:
        continue
        
    # Намиране на div елемент с клас text3
    div_element = td_element.find('div', class_='text3')
    if not div_element:
        continue
        
    # Намиране на strong елемент с датата
    strong_element = div_element.find('strong')
    if not strong_element:
        continue
        
    # Извличане на текста на датата
    date_text = strong_element.text.strip()
    
    # Проверка дали текстът съдържа дата във формат DD.MM.YYYY
    date_match = re.search(r'(\d{2}\.\d{2}\.\d{4})', date_text)
    if not date_match:
        continue
        
    date_str = date_match.group(1)
    
    # Проверка дали е затворен ден
    closed_img = div_element.find('img', src=re.compile(r'closed\.png'))
    
    if closed_img:
        # Създаване на събитие за затворен ден
        event = Event()
        event.name = "Nürburgring Closed"
        
        # Създаване на целодневно събитие с правилна часова зона
        event_date = datetime.strptime(date_str, "%d.%m.%Y")
        event.begin = event_date
        event.make_all_day()
        
        event.location = "Nürburgring Nordschleife"
        event.description = "Nürburgring Nordschleife is closed on this day."
        
        # Добавяне на събитието към календара
        calendar.events.add(event)
        closed_count += 1
        print(f"Добавен затворен ден: {date_str}")
    else:
        # Проверка за отворен ден с работно време
        time_span = div_element.find('span', class_='text10')
        if time_span:
            # Извличане на чист текст от HTML елемент
            time_text = time_span.get_text(strip=True)
            
            print(f"Дата: {date_str}, Намерен текст за време: '{time_text}'")
            
            # Директно извличане на часовете чрез разделяне на стринга
            # Това работи с всички възможни видове тирета
            if '–' in time_text:
                time_parts = time_text.split('–')
                start_time_str = time_parts[0].strip()
                end_time_str = time_parts[1].strip()
            elif '-' in time_text:
                time_parts = time_text.split('-')
                start_time_str = time_parts[0].strip()
                end_time_str = time_parts[1].strip()
            elif '—' in time_text:
                time_parts = time_text.split('—')
                start_time_str = time_parts[0].strip()
                end_time_str = time_parts[1].strip()
            else:
                # Опит да извлече часовете чрез регулярен израз като резервен вариант
                match = re.search(r'(\d{2}:\d{2}).*?(\d{2}:\d{2})', time_text)
                if match:
                    start_time_str = match.group(1)
                    end_time_str = match.group(2)
                else:
                    print(f"Не е намерен валиден формат на време за дата {date_str}, текст: '{time_text}'")
                    continue
            
            try:
                # Изчистване от всички непечатни символи
                start_time_str = ''.join(c for c in start_time_str if c.isdigit() or c == ':')
                end_time_str = ''.join(c for c in end_time_str if c.isdigit() or c == ':')
                
                # Създаване на datetime обекти в часовата зона на Nürburg
                naive_start = datetime.strptime(f"{date_str} {start_time_str}", "%d.%m.%Y %H:%M")
                naive_end = datetime.strptime(f"{date_str} {end_time_str}", "%d.%m.%Y %H:%M")
                
                # Прилагане на часовата зона
                start_datetime = nurburg_tz.localize(naive_start)
                end_datetime = nurburg_tz.localize(naive_end)
                
                # Създаване на събитие
                event = Event()
                event.name = "Tourist Drives Days - Nürburgring"
                event.begin = start_datetime
                event.end = end_datetime
                
                event.location = "Nürburgring Nordschleife"
                event.description = f"Tourist Drives at Nürburgring on {date_str}"
                
                # Добавяне на събитието към календара
                calendar.events.add(event)
                event_count += 1
                print(f"Добавено събитие: {date_str} | {start_time_str}-{end_time_str}")
                
            except ValueError as e:
                print(f"Грешка при обработка на дата/час: {date_str} {start_time_str}-{end_time_str}, Грешка: {e}")

# Записване на календара в .ics файл
with open("nurburgring_schedule.ics", "w") as f:
    f.write(calendar.serialize())

print(f"\nГотово! Създадени са {event_count} събития за отворени дни.")
print(f"Добавени са {closed_count} затворени дни.")
print("Файлът nurburgring_schedule.ics е създаден!")