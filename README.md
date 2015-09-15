# Linux-Server-Configuration

IP ADDRESS: 52.10.220.44

SSH PORT: 2200

FULL URL: ec2-52-10-220-44.us-west-2.compute.amazonaws.com

- use 'nslookup <ipaddress>' in bash shell 


SUMMARY:

This project is to configure a Linux Server to host a Flask Application

0. Initial setup
	a. get pip installed, to simplify package downloads
		- "$ sudo apt-get install python-pip"
		https://pip.pypa.io/en/latest/installing/

	b. Install Flask (0.10.1)
		- "$ pip install Flask" 
		http://flask.pocoo.org/docs/0.10/installation/

	c. Install SQLAlchemy (0.8.4 or greater)
		- "$ pip install SQLAlchemy"
		http://docs.sqlalchemy.org/en/rel_1_0/intro.html

	d. Install OAuth2 client (1.4.11)
		- "$ pip install --upgrade oauth2client"
		https://github.com/google/oauth2client

	e. Flask-SeaSurf (0.2.0) for CSRF protection
		- "$ pip install flask-seasurf"
		https://flask-seasurf.readthedocs.org/en/latest/

	f. Install git
		- "$ sudo apt-get install git"
		https://git-scm.com/book/en/v2/Getting-Started-Installing-Git

	g. Clone the RestaurantApp from https://github.com/pshevade/RestaurantApp
		- "$ git clone https://github.com/pshevade/RestaurantApp.git"

	h. Install PostgreSQL
		- "$ sudo apt-get install postgresql-9.4"
		http://www.postgresql.org/download/linux/ubuntu/

	i. Update the Flask application to run with a PostgreSQL database instead of the SQLite database. 


1. & 2. SSH into the web server using the RSA key given by Udacity.

3. & 4. Create user 'grader' and give 'grader' persmissions to sudo:
	- "$ sudo adduser"
	- create file in /etc/sudoers.d called 'grader'
	- "$ sudo nano /etc/sudoers.d/grader" 
	- Add the line to the file 
		"grader ALL=(ALL) NOPASSWD:ALL"

5. Update all currently installed packages. 
	- "$ sudo apt-get update" (to update package source list)
	- "$ sudo apt-get upgrade"

6. Change SSH port:
	- "$ sudo nano /etc/ssh/sshd_config" - change Port from 22 to 2200

7. Setup Firewall:
	- "$ sudo ufw allow 2200" (for our updated ssh port)
	- "$ sudo ufw deny 22" (to block port 22 for ssh)
	- "$ sudo ufw allow www" (to allow port 80)
	- "$ sudo ufw allow ntp" (to allow NTP on port 123)
	- "$ sudo ufw enable" (to enable firewall)

	Status: active

	To                         Action      From
	--                         ------      ----
	2200/tcp                   ALLOW       Anywhere
	22                         DENY        Anywhere
	80/tcp                     ALLOW       Anywhere
	123                        ALLOW       Anywhere
	2200/tcp (v6)              ALLOW       Anywhere (v6)
	22 (v6)                    DENY        Anywhere (v6)
	80/tcp (v6)                ALLOW       Anywhere (v6)
	123 (v6)                   ALLOW       Anywhere (v6)

8. Set timezone to UTC.
	- "$ sudo dpkg-reconfigure tzdata" and follow on screen prompt to set timzeone to UTC

9. Install & Configure Apache.
	- "$ sudo apt-get install apache2"
	- "$ sudo apt-get install libapache2-mod-wsgi" to host python web applications
	- create the directory 'RestaurantApp' in /var/www
	- create the restaurantapp.wsgi script here (see 4. below)
	- Folder structure
		var
			www
				RestaurantApp
					RestaurantApp
						__init__.py (to start the Flask App)
						(All Other Flask Application File)
						client_secrets.json (see 4. below)
 						templates (html files)
						static (all javascript, css, and folder for uploaded images)
					restaurantapp.wsgi
	- Permissions: change all permissions for RestaurantApp to www-data, which is a user created for Apache. This will allow Apache to serve the Flask Application
	"$ sudo chown -R www-data:www-data /var/www/RestaurantApp"

   Configuration Files.
	- change the /etc/apache2/sites-enabled/000-default.conf 
		- change document root to /var/www/RestaurantApp 
	- create a restaurantapp.wsgi in /var/www/RestaurantApp (see attached file)
		- this script will initiate the Flask Application
	- download the client_secrets.json file from console.developers.google.com
		- make sure that "Authorized JavaScipt origins" includes the IP address of the server before downloading.

   Restart Apache.
	- "$ sudo service apache2 restart"

10. Create a user 'catalog' for PostgreSQL
	- "$ sudo -i -u postgres" to switch into posgres user
	- "postgres@<ipaddress>$ createuser --interactive -P" 
	The '--interactive' will ask you options about the user (is it a super user, can they create databases, etc) in the prompt, and '-P' will prompt the user for a password for this new user.
	- make sure that remote connections to the database are disabled. Change the pg_hba.conf file.

	# Change the authentication method for postgres to 'trust' so once the postgres # user is activated, you don't need further authentication
	local   all             postgres                                trust

	# TYPE  DATABASE        USER            ADDRESS                 METHOD

	# "local" is for Unix domain socket connections only
	local   all             all                                     md5
	# IPv4 local connections: DISABLED
	#host    all             all             127.0.0.1/32            md5
	# IPv6 local connections: DISABLED
	#host    all             all             ::1/128                 md5
	# Allow replication connections from localhost, by a user with the
	# replication privilege.
	#local   replication     postgres                                peer
	#host    replication     postgres        127.0.0.1/32            md5
	#host    replication     postgres        ::1/128                 md5

11. Clone the RestaurantApp from https://github.com/pshevade/RestaurantApp
	- "$ git clone https://github.com/pshevade/RestaurantApp.git"
	- Move files to var/www/Restaurant, without the .git folder (make sure the client_secret.json file still exists)
	- you might need to reset the permissions to www-data:www-data 

12. Configure firewall to monitor repeat unsuccessful login attempts:
	- install fail2ban
	- "$ sudo apt-get install fail2ban"
	- configure as per (https://www.digitalocean.com/community/tutorials/how-to-protect-ssh-with-fail2ban-on-ubuntu-14-04)

13. Auto updates:
	- create a file 'autoupdt' to include :
		#!/bin/bash
		apt-get update
		apt-get upgrade -y
		apt-get autoclean
	- move this file to /etc/cron.weekly
	  https://help.ubuntu.com/community/AutoWeeklyUpdateHowTo

14. Monitoring application:
	- use the application "Glances" 
	- "$ pip install glances"
	https://pypi.python.org/pypi/Glances/
	- "$ glances" to view system status locally.

