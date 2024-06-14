from routes import create_app
from extensions import db, migrate

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        migrate.init_app(app, db)
    app.run(debug=True, ssl_context=('../certificat_dev/cert.pem', '../certificat_dev/key.pem'))
