# Amazon Scraper

# Steps to configure and run this project

1. Clone repository: git clone [https://github.com/shahid/lincoln.git](https://github.com/ShahidZia/amazon_scraper.git)
2. Install virtualenv. `pip install virtualenv``
3. Create virtualenv. `virtualenv env`
4. Start your virtualenv. `.\env\scripts/activate` (windows) `source env/bin/activate` (linux)
5. Install pip-tools by `pip install pip-tools`
```
6. Install requirements.
```
cd requirements  
pip-sync dev.txt
```
7. Install `sudo apt install redis-server` and then run `redis-cli ping` get response `PONG` for successfully installed.

8. Start redis server
```
redis-server
```
9. Migrate DB
```
python manage.py migrate
```
10. Command will create superuser and a Nike brand
```
python manage.py create_user_and_brand
```
11. Run celery and celery-beat using following commands where celery-beat will run 4 times a day every 6 hours(Can be changed in the settings.py)
```
celery -A amazon_scraper worker --loglevel=info

celery -A amazon_scraper beat --loglevel=info
```
12. There is a setting var in project setting.py name SCRAPER_RETRIES(default set to 10) which can be set
 to any number of retries we want to make until we declare the request as bad request.

13. Done! Run the development server
`python manage.py runserver 0.0.0.0:8000`

14. Open your browser and navigate to http://localhost:8000

# Admin access
After running series of setup which includes migrations, you will have a default admin access as follows:
```
username: admin
email: admin@admin.com
password: adminpassword
```

# Overview and Implementation
The site consist of two models. Brand and Product.

## Models
* Whereas Brand model contains two fields name and website_url which will be used in fetching/scrapping the data from amazon brand pages.
* Another model name Product contains multiple fields such as name, sku, image, asin and brand(FK) to store the information fetched from the amazon pages using scrapping.

## Logic
* We are using celery-beat which is set to run 4 times a day to fetch data from the amazon pages and store them into the database.
* We have retrying mechanism which makes the scraper more powerful by retrying for a certain time until it get the data.
* We are using user-agent rotation in headers to deal with anti-scraping measures.
* We are using the logging mechanism which store the success and failure logs.
* Logs are stored in general.log file.
* Pagination and search using jquery datatable are implemented on the Frontend.
