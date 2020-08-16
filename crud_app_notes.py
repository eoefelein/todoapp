# create - C = SQL insert -> SQLAlchemy = db.session.add(user1)
# read - R = SQL select -> SQLAlchemy = User.query.all()
# update - U = SQL update -> SQLAlchemy = user1.foo = 'new value'
# remove - D = SQL delete -> SQLAlchemy = db.session.delete(user1)

# Model View Controller" MVC Pattern
    # most common patterns to know in architecting a full-stack app
# Migrations
    # necessary when we want to change our data schema in the future,
    # when we may already have data in our system, based on an old schema
# Modeling Relationships (in SQLAlchemy ORM) 
    #  in a way that reflects the relationships between objs in our web app
# Implementing Search
    # implementing search in a web app, tying all SQL and SQLAlchemy methods
