virtualenv -q ve
source ./ve/bin/activate
pip install -E ./ve -r requirements/project.txt
cd $WORKSPACE
#python manage.py migrate
python manage.py jenkins fusion
