# flask_blog
A mini blog built on flask

1. when deploy this application, you need to set the environment variables 
   1. EMAIL_USERNAME
   2. EMAIL_PASSWORD
   3. FLASK_BLOG_APP_SECRET_KEY
   4. FLASK_BLOG_APP_SQLALCHEMY_DATABASE_URI
   5. For windows, you may need to restart the os to make these changes work.

# Deployment app on a linux server(linode) from a Mac
Note: the following commands are for macOS. If you are using a windows, the commands are different but the process is similar.
For flask project, It's recommended to use nginx and gunicorn
1. Set up a linux server for the flask project
   1. Go to the cloud server provider website, and create a linux server in cloud server provider like linode
   2. Record the ssh command (ssh root@45.33.123.214) and run it in your local bash shell, which should connect you to the remote linux system
   3. After connected, upgrade the software of this sever by running "apt update && apt upgrade"
   4. Set up the host name of this server by running "hostnamectl set-hostname flask-server". If you type in "hostname", you should see "flask-server"
   5. Set up the host name and host file by running "nano /etc/hosts". Within the host file, under 127.0.0.1, put the ip address and the name of the server like "45.33.123.214    flask-server".
   6. Add a limited user and password to the machine by running "adduser flaskblog". 
   7. Add the new user to sudo group: "adduser flaskblog sudo"
   8. logout root, and login as flaskblog user by running "exit" and "ssh flaskblog@45.33.123.214".
   9. You should log in as the new user.
   10. In the home folder, make a .ssh director by running "mkdir .ssh"
   11. Switch to your local bash shell, generate an ssh key in your local terminal by running "ssh-keygen -b 4096".
   12. Move the public key to the server by runing "scp ~/.ssh/id_rsa.pub flaskblog@45.33.123.214:~/.ssh/authorized_keys"
   13. Switch to the server bash shell, and run "ls .ssh" to check if the public key is stored successfully.
   14. Set up the permissions for the owner of the .ssh folder by running "sudo chmod 700 ~/.ssh/"
   15. Set up the permissions for the file of the .ssh folder by running "sudo chmod 600 ~/.ssh/*"
   16. Switch to your local machine's terminal and run "ssh root@45.33.123.214", this should ssh into the cloud machine without entering a password
   17. Need to disallow the root login over ssh, which is done by updating the ssh config file. Run "sudo nano /etc/ssh/sshd_config".
   18. Change two values of the ssh config file. Change PermitRootLogin from yes to no. Change PasswordAuthentication from yes to no. These will protect your project from hackers.
   19. Restart the ssh service by running "sudo systemctl restart sshd"
   20. Set up the fairwall by running "sudo apt install ufw"
   21. Set up firewall rules: "sudo ufw default allow outgoing" "sudo ufw default deny incoming" "sudo ufw allow ssh" "sudo ufw allow 5000" "sudo ufw enable"
   22. To see the things you allowed and disallowed, you can run "sudo ufw status"
2. Deploy the flask project to the cloud server
   1. If you are using a git repo, you can simply clone the repo into the home directory of the user you just created by running "git clone repo"
   2. You can also do step 1 if you are using a virtual enviornment.
      1. run "pip freeze > requirements.txt" to put all the dependencies used in the project into the requirements.txt file.
      2. "scp -r D:\xx\github_repos\flask_blog flaskblog@45.33.123.214:~/"
      3. switch to the cloud server bash, run "ls" to check if the flask project directory is copied successfully.
   3. Create a virtual environment on the cloud server to run the app.
      1. "sudo apt install python3-pip"
      2. "sudo apt install python3-venv"
      3. "python3 -m venv flask_blog" to create a new virtual enviornment
      4. cd flask_blog and ls, you should see 5 items: flask_blog directory where the app sits, __pychache__, requirements.txt, run.py and venv
      5. activate the virtual enviroment by running "source venv/bin/activate"
      6. "pip install -r requirements.txt"
   4. Set up the system variables to store the sensitive info of the flask app
      1. Switch to the local machine bash, 
      2. run "os.environ.get('FLASK_BLOG_APP_SECRET_KEY')"
      3. run "os.environ.get('FLASK_BLOG_APP_SQLALCHEMY_DATABASE_URI')"
      4. "os.environ.get('EMAIL_USERNAME')"
      5. "os.environ.get('EMAIL_PASSWORD')"
      6. Switch to the cloud server bash: (venv)flaskblog@flask-server:~/flask_blog$
      7. "sudo touch /etc/flask_blog_config.json" to create a config file
      8. "sudo nano /etc/flask_blog_config.json" to edit the file
      ```json
            {
               "SECRET_KEY":"balabala",
               "SQLALCHEMY_DATABASE_URI":"balabala",
               "MAIL_USERNAME":"balabala",
               "MAIL_PASSWORD":"balabala",
            }
      ```
      9. cd to flask_blog folder, and edit the config.py file
      ```python
         import os
         import json
      
         with open('/etc/flask_blog_config.json') as config_file:
             config = json.load(config_file)
         class Config:
             SECRET_KEY = config.get('FLASK_BLOG_APP_SECRET_KEY')
             SQLALCHEMY_DATABASE_URI = config.get('FLASK_BLOG_APP_SQLALCHEMY_DATABASE_URI') # this is the relevant path from the current file
             MAIL_SERVER = 'smtp.gmail.com'
             MAIL_PORT = 587
             MAIL_USE_TLS = True
             MAIL_USERNAME = config.get('EMAIL_USERNAME')
             MAIL_PASSWORD = config.get('EMAIL_PASSWORD')
      ```
   5. (venv)flaskblog@flask-server:~/flask_blog$ export FLASK_APP=run.py
   6. (venv)flaskblog@flask-server:~/flask_blog$ flask run --host=0.0.0.0, which will expose the app to the whole network
   7. Till now, your app should be running on the ip address 45.33.123.214:5000
3. Use nginx and gunicorn to deploy a production server
   1. cd to the home director: (venv)flaskblog@flask-server:~$ sudo apt install nginx
   2. (venv)flaskblog@flask-server:~$ pip install gunicorn
   3. update the configuration file for nginx
   4. (venv)flaskblog@flask-server:~$ sudo rm /etc/nginx/sites-enabled/default to remove the default file
   5. (venv)flaskblog@flask-server:~$ sudo nano /etc/nginx/sites-enabled/flaskblog to create a new flaskblog file
   6. Inside the flaskblog file, add the following things
   ```
   server{
         listen 80;
         server_name: 45.33.123.214;
   
         location /static {
               alias /home/flaskblog/flask_blog/flask_blog/static; //the static folder path of the flask app
         }
         location / {
               proxy_pass http://localhost:8000; //forward all the traffic to the gunicorn and handle python code
               include /etc/nginx/proxy_params;
               proxy_redirect off;
         }
   }
   ```
   7. (venv)flaskblog@flask-server:~$ sudo ufw allow http/tcp, which will allow the http/tcp traffic
   8. (venv)flaskblog@flask-server:~$ sudo ufw delete allow 500, which forbid the access to port 5000 since its the development server
   9. (venv)flaskblog@flask-server:~$ sudo ufw enable
   10. (venv)flaskblog@flask-server:~$ sudo systemctl restart nginx, which starts the nginx service but it doesn start the gunicorn service
   11. (venv)flaskblog@flask-server:~$ gunicorn -w 3 run:app, which spcifies the number of workers. The number of workser should equal to (2*core)+1
   12. So far, you should be able to open the app with 45.33.123.214, but you need something to constantly monitor the gunicorn and make sure it will auto started and restarted if it crashed
   13. (venv)flaskblog@flask-server:~/flask_blog$ sudo apt install supervisor
   14. set up a config file for supervisor
   15. (venv)flaskblog@flask-server:~/flask_blog$ sudo nano /etc/supervisor/conf.d/flaskblog.conf
   16. inside flaskblog.conf, you need add the following lines
   ```editorconfig
      [program: flaskblog]
      directory=/home/flaskblog/flask_blog
      command=/home/flaskblog/flask_blog/venv/bin/gunicorn -w 3 run:app
      user=flaskblog
      autostart=true
      autorestart=true
      stopasgroup=true
      killasgroup=true
      stderr_logfile=/var/log/flaskblog/falskblog.err.log
      stdout_logfile=/var/log/flaskblog/falskblog.out.log
   ```
   17. (venv)flaskblog@flask-server:~/flask_blog$ sudo mkdir -p /var/log/flaskblog
   18. (venv)flaskblog@flask-server:~/flask_blog$ sudo touch /var/log/flaskblog/falskblog.err.log
   19. (venv)flaskblog@flask-server:~/flask_blog$ sudo touch /var/log/flaskblog/falskblog.out.log
   20. (venv)flaskblog@flask-server:~/flask_blog$ sudo supervisorctl reload, which will start the supervisor
   21. Till now, you should be able to open the app with 45.33.123.214, and it will auto restarted always
   22. (venv)flaskblog@flask-server:~/flask_blog$ sudo nano /etc/nginx/nginx.conf, to change the default size nginx can accept
   23. Inside nginx.conf file, under "type_hash_max_size 2048", add "client_max_body_size 5M"
   24. (venv)flaskblog@flask-server:~/flask_blog$ sudo systemctl restart nginx, which will make the change work
