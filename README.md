### praktikum_new_diplom

Доступен по адресу: http://51.250.2.201/
Админ панель: http://51.250.2.201/admin/
Спицификация API: http://51.250.2.201/api/docs/

## Setup

git clone git@github.com:dimabaril/foodgram-project-react.git
cd foodgram-project-react/backend
python3 -m venv venv
source venv/bin/activate
pip3 install -r requarements.txt
cd foodgram_back
python3 manage.py collectstatic
python3 manage.py migrate
python3 manage.py createsuperuser
python3 manage.py importcsv
python3 manage.py runserver
