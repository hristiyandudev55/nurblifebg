План за разработка на приложение за Driving Experience на Нюрбургринг (само за български клиенти)
1. Инсталация и подготовка
Инсталиране на Poetry
Създаване на виртуална среда и инсталиране на зависимости
2. База данни и връзка с нея (SQLAlchemy)
Създаване на таблици за:

2.1. Коли
ID
Изображение
Марка и модел
Тип двигател (пример: 2.0-4cyl turbo)
Конски сили (hp) и въртящ момент (NM)
Ускорение до 100 км/ч
Тип скоростна кутия
Задвижване (предно, задно, 4х4)
Тегло
Окачване
Спирачки (ендурънс, рейсинг)
Гуми и джанти
Седалки, колани, ролкейдж
Цена за 2 обиколки (BGN)
2.2. Хотели
ID
Снимки
Линк за резервация
2.3. Подаръчни ваучери
ID
Стойност
2.4. Плащания
Пълно име
Имейл
Телефонен код на държавата
Телефон
Купон код (не е задължителен)
Интеграция с API за плащания
2.5. Календар на пистата
Извличане на данни чрез API (ако е налично)
2.6. Контакти
Информация за фирмата (държава, телефон, Viber/WhatsApp, имейл)
Форма за запитвания (ID, име, имейл, държава, съобщение)
2.7. Резервации (Booking)
Връзка с календара и наличните коли
2.8. Ресторанти
ID
Снимка
Линк към местоположение
2.9. Допълнителни активности (Things to do)
ID
Наименование
Изображение/Линк
2.10. Информация за пистата
"About Nürburgring"
"All You Need to Know" (FAQ - ID, въпрос, отговор)
2.11. Fast Lap Experience (Taxi Lap)
Брой пътници
Конски сили / NM
Задвижване
Опция за запис на видео
2.12. Опционални екстри
ID
Име
Цена
3. Основни функционалности
3.1. Таб "Коли и цени"
Списък с коли и цени + бутон за резервация
Изображения:
Ценови листи (BASIC/PREMIUM)
Важна информация
Щети и застраховки
Заснемане на обиколката, Guidance Lap, Telemetry Video
Обобщена информация за коли и спецификации
Банер с QR код за връзка
Subscribe бутон (Mailjet API за нови абонати)
Footer с информация
3.2. Таб "Book a Car"
Стъпка 1: Избор на кола
ID + изображение
Брой пътници
Марка и модел
Стъпка 2: Избор на трасе
Public session + мин. обиколки
Trackday + мин. обиколки
GP-Track + мин. км
Spa-Francorchamps (от 300 км)
Стъпка 3: Избор на дата
Календар с работно време и наличност на колите
Стъпка 4: Избор на час за каране
Списък с наличните времеви диапазони
Стъпка 5: Информация за клиента
Име, имейл, държава, телефонен код, телефон
Съгласие за контакт
Стъпка 6: Избор на пакет
Basic / Premium (автоматично добавяне на цена)
Стъпка 7: Избор на брой обиколки
Добавяне на цена според броя обиколки
Стъпка 8: Допълнителни екстри
Guidance Lap за шофьори 18-23 г.
Видео запис
Damage Excess Reduction (изисква поне 1 Guidance Lap)
Extra Driver:
До 3-ма допълнителни
Вторият е безплатен
Третият – 50€
Стъпка 9: Финализиране на резервацията
Прочитане и приемане на Terms & Conditions
Опции за плащане:
30% предварително, останалото на място
Използване на ваучер/код за отстъпка
4. Backend API методи
4.1. Коли
CREATE_CAR
EDIT_CAR
VIEW_CAR
DELETE_CAR
4.2. Информация за пистата
GET_ABOUT
CREATE_ABOUT
EDIT_ABOUT
DELETE_ABOUT
4.3. Календар на пистата
GET_OFFICIAL_CALENDAR (връзка с API)
4.4. Контакти
POST_CONTACT_FORM
GET_CONTACT_FORM
EDIT_CONTACT_FORM
DELETE_CONTACT_FORM
POST_COMPANY_INFO
GET_COMPANY_INFO
EDIT_COMPANY_INFO
DELETE_COMPANY_INFO
4.5. Ваучери
POST_VOUCHER
GET_VOUCHER
UPDATE_VOUCHER
DELETE_VOUCHER
4.6. Резервации
BOOK_NOW
4.7. Смяна на език
Опция за превключване между BG / ENG
4.8. Поддръжка (опционално)
Вграден чат за поддръжка
4.9. Абонаменти
SUBSCRIBE_USER (интеграция с Mailjet API)


installing -
poetry env use python + add pyproject.toml + poetry env activate + source venv path.



1. Инсталиране на Vite
npm create vite@latest

cd your-project-name
npm install

npm install eslint --save-dev
npx eslint --init
npm install eslint-plugin-vue @vue/eslint-config-prettier --save-dev

Добавете ESLint скриптове: Актуализирайте вашия package.json, за да включите ESLint скриптове:

Инсталирайте Cypress:
npm install cypress --save-dev
npx cypress open
Добавете Cypress скриптове: Актуализирайте вашия package.json, за да включите Cypress скриптове:
// filepath: /Users/a516095/Documents/GitHub/nurblifebg/nurblifebg/frontend/package.json
{
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview",
    "lint": "eslint --ext .js,.vue src",
    "lint:fix": "eslint --fix --ext .js,.vue src",
    "cypress:open": "cypress open",
    "cypress:run": "cypress run"
  }
}

Стартирайте ESLint:
npm run lint
Стартирайте Cypress:
npm run cypress:open