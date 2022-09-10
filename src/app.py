"""
Flask, by default, run in production mode without debug.
In order to run flask in debug mode we can set some configurations for it:
 --debug option or app.run(debug=True)

The RECOMMENDED way is:
flask --app app --debug run
(we can ommit "app" because is the same name of the command)
flask --debug run

After move the app to init we need to specify the folder of the app:
flask --app src --debug run

If we put export FLASK_APP=src as an environment variable, in this case in .flasenv, we can run the program with:
flask --debug run
This way it runs with debug, without debug mode just use
flask run

Access to the flask shell
flask --app src shell
Then, in order to create the models put in the shell:
from src.database import db
from src.models.patient import Patient
from src.models.prescription import Prescription
db.create_all()


"""