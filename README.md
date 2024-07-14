``` My HNG Devops Stage 3 Project ```

HNG TASK 3

............................
sudo apt-get update

```Install Rabbitmq-server```
-touch rabbitmq.sh
-code rabbitmq.sh
-chmod +x rabbitmq.sh
-./rabbitmq.sh
-sudo systemctl start rabbitmq-server -d

```Install Celery```
-pip install celery

```Install Nginx```
-sudo apt install nginx -y

-sudo nano /etc/nginx/sites-available/messaging_system

Add the following configuration:
```
server {
    listen 80;
    server_name localhost;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```
-sudo ln -s /etc/nginx/sites-available/messaging_system /etc/nginx/sites-enabled/
-sudo nginx -t
-sudo systemctl restart nginx

```Install Ngrok via Apt```
curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc \
	| sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null \
	&& echo "deb https://ngrok-agent.s3.amazonaws.com buster main" \
	| sudo tee /etc/apt/sources.list.d/ngrok.list \
	&& sudo apt update \
	&& sudo apt install ngrok

ngrok config add-authtoken 2jBLGgpKIVbjL0GzCVlkMYYfAoC_6GUQ9n2bAKphWC7UaBtqm


```Install python and env variables```
sudo apt-get install python3-venv
python3 -m venv messaging_system
source messaging_system/bin/queue


```pip install Flask```
```pip install python-dotenv```
```pip install celery```
```pip install Flask-mail```


sudo celery -A app.celery worker

nohup python3 app.py > app.log 2>&1 &

ngrok http --domain=midge-neutral-commonly.ngrok-free.app 80


```Send E-Mail```
Go to midge-neutral-commonly.ngrok-free.app//sendmail?=example@gmail.com to send mail
