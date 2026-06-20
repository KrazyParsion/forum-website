from blog import app
from blog import db
# Main Driver Function

if __name__ == "__main__":
    with app.app_context():
        # db.drop_all()
        db.create_all()
    app.run(debug = True, port = 5022, host = "0.0.0.0")