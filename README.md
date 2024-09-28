# h-t-handcraft




## Installation
    
1. Create a virtual environment
2. Install the requirements

    `    pip install -r requirements.txt
    `
3. Update requirements.txt
    
    `    pip freeze > requirements.txt
    `
4. Setup database configuration in .env file
5. Apply migrations
    
    `    python manage.py migrate
    `

6. Export data
      
      
      python manage.py dumpdata [app_name] --output fixtures_[app_name].json

7. Import data


      python manage.py loaddata fixtures_[app_name].json