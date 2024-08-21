# Hermes (Backend)

Real-Time Chat Application. Created to improve my backend development skills with Python using Django.


## Features

- Register user and Login (Simple JWT)
- Edit user
- Send, Accept or Reject friend requests
- Start chat or Delete friends
- Non read messages
- Online or Offline state update
- Send and Get messages in real-time (Django Channels and Redis)
## Installation

Django

```bash
git clone https://github.com/luispacheco-dev/hermes-backend.git
```

```bash
cd hermes-backend
```

```bash
python -m venv .env
```

```bash
source .env/bin/active
```

```bash
pip install -r .requirements.txt
```

```bash
python manage.py migrate
```

```bash
python manage.py runserver
```

Redis

```bash
podman pull docker.io/redis 
```

```bash
podman run -d --name redis_server -p 6379:6379 redis
```
