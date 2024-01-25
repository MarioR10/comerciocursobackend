from main import createApp, db
import os

app=createApp()


with app.app_context():
        db.create_all()

if __name__ == '__main__':

        app.run(port=os.getenv("PORT"), debug=True)
