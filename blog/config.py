# Add a DevelopmentConfig class to contain the configuration variables for
# the project. 
# Set location of the database, set the debug mode to track errors, and
# set the 'secret_key' variable to secure the calls to database
# note that key is not stored in DevConfig but in os.environ variable

import os
class DevelopmentConfig(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "postgresql://dennell:thinkful@localhost:5432/blogful")
    DEBUG = True
    SECRET_KEY = os.environ.get("BLOGFUL_SECRET_KEY", os.urandom(12))

class TestingConfig(object):
	# Set up a separate database for testing
	SQLALCHEMY_DATABASE_URI = "postgresql://dennell:thinkful@localhost:5432/blogful-test"
	# Disable Debug mode 
	DEBUG = True
	# And use a different secret key than Development Config
	SECRET_KEY = "Not secret"


class TravisConfig(object):
    # Set up a separate database for testing
    SQLALCHEMY_DATABASE_URI = "postgresql://dennell:thinkful@localhost:5432/blogful-test"
    # Disable Debug mode 
    DEBUG = True
    # And use a different secret key than Development Config
    SECRET_KEY = "Not secret"    