from app import app
# from db import db

from config import ProductionConfig

app.config.from_object(ProductionConfig)

# db.init_app(app)
#
#
# @app.before_first_request
# def create_tables():
#     db.create_all()

if __name__ == '__main__':
    app.run()
