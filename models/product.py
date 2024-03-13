from myapp import db

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500))
    price = db.Column(db.Float, nullable=False)
    unit = db.Column(df.Integer, nullable=False)
    image = db.Column(db.String(200))
    # user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def repr(self):
        return '<Product >'.format(self.name)