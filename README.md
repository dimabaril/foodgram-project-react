### praktikum_new_diplom

## Setup

git clone git@github.com:dimabaril/foodgram-project-react.git
cd foodgram-project-react/backend
python3 -m venv venv
source venv/bin/activate
pip3 install -r requarements.txt
cd foodgram_back
python3 manage.py importcsv
python3 manage.py runserver
