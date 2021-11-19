from flask_sqlalchemy import SQLAlchemy

# Initialise the ORM.
db = SQLAlchemy()


"""
    From here onwards you will find the entities for various tables used in this application.
"""
class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, db.Identity(always=False, start=1, cycle=False), primary_key=True)
    user_name = db.Column(db.String(50), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email_id = db.Column(db.String(120), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    #last_loggedin = db.Column(db.String)

    def __repr__(self):
        return f"User(id={self.id!r}, user_name={self.user_name!r}, first_name={self.first_name!r}, last_name={self.last_name!r}, email_id={self.email_id!r}, is_active={self.is_active!r})"

class Page(db.Model):
    __tablename__ = 'page'
    
    id = db.Column(db.Integer, db.Identity(always=False, start=1, cycle=False), primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    sections = db.relationship('Section', backref='page', lazy=True)

    def __repr__(self):
        return super().__repr__()

class SectionType(db.Model):
    __tablename__ = 'section_type'
    
    id = db.Column(db.Integer, db.Identity(always=False, start=1, cycle=False), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(120), nullable=False)

class Section(db.Model):
    __tablename__ = 'section'
    
    id = db.Column(db.Integer, db.Identity(always=False, start=1, cycle=False), primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    section_type = db.Column(db.Integer, db.ForeignKey('section_type.id'), nullable=False)
    page_id = db.Column(db.Integer, db.ForeignKey('page.id'), nullable=True)
    contents = db.relationship('Content', backref='section', lazy=True)

class ContentType(db.Model):
    __tablename__ = 'content_type'
    
    id = db.Column(db.Integer, db.Identity(always=False, start=1, cycle=False), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return super().__repr__()

class Content(db.Model):
    __tablename__ = 'content'

    id = db.Column(db.Integer, db.Identity(always=False, start=1, cycle=False), primary_key=True)
    name = db.Column(db.String(80), nullable=False)  
    content_type = db.Column(db.Integer, db.ForeignKey('content_type.id'), nullable=False)
    data = db.Column(db.Text, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    section_id = db.Column(db.Integer, db.ForeignKey('section.id'), nullable=True)

    def __repr__(self):
        return super().__repr__()