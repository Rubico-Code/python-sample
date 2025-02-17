# rubico API

Rubico API: Scalable Django REST Backend for Procurement

## Tech Stack

- Python 3.13+
- Django 5.1+
- Django REST Framework
- mySQL 8
- Docker & Docker Compose
- Redis (for caching)
## Use command to genteate secrets 
   ```bash
    python -c "import secrets; print(secrets.token_urlsafe(38))"
    cat /path/to/your/file.sql | docker exec -i <container_name> mysql -u username -p'password' db_name
```
### Prerequisites

- Docker
- Docker Compose
- Make (optional, for using Makefile commands)

### VS Code settings are pre-configured in `.vscode/settings.json`:
    ```jsonc
    {
        "type": "setting",
        "settings": {
            "python.formatting.provider": "none",
            "editor.formatOnSave": true,
            "[python]": {
                "editor.defaultFormatter": "charliermarsh.ruff"
            }
        }
    } 

```

## Prerequisites
## Quick Start

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/django-dockyard.git
    cd django-dockyard
    ```
2. Set up environment variables:
    ```bash
    cp .envs/.env.example .envs/.env.local
    ```

3. Build and start services:
    ```bash
    make build
    make up
    ```

## Development Commands
### Start services
    ```bash
    make up
    ```
### Stop services
    ```bash
    make down
    ```
### View logs
    ```bash
    make show-logs
    ```
### Create migrations
    ```bash
    make makemigrations
    ```
### Apply migrations
    ```bash
    make migrate
    ```



### Django
DJANGO_SETTINGS_MODULE=config.settings.local
DJANGO_SECRET_KEY=your-secret-key


### Redis
REDIS_URL=redis://redis:6379/0

### API Documentation
##### API docs: 
http://localhost:8000/api/docs/

#### API Root: 
http://localhost:8000/api/v1/

