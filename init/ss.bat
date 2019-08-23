pip install --upgrade setuptools pip


pip install superset Flask==1.0 pandas==0.23.4


set FLASK_APP=superset
flask fab create-admin

cd venv\Scripts\

python superset db upgrade
python superset init

echo cd ./venv/Scripts/ ^& python superset run -p 8080 --with-threads --reload --debugger > "../../run_superset.bat"

python superset run -p 8080 --with-threads --reload --debugger