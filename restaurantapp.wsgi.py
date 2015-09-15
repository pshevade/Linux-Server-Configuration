
#!/usr/bin/python
import sys
import logging
# Set path for logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/RestaurantApp/")

# Import the Flask App from Restaurant App
from RestaurantApp import app as application
# Key must be set here.
application.secret_key = 'super_secret_key'