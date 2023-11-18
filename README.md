# Django Starter

This is a personal project to help me get started with Django projects. Heavily influenced by [thenewboston](https://www.youtube.com/watch?v=DaxcmbWcdTA&list=PL6gx4Cwl9DGDYbs0jJdGefNN8eZRSwWqy&index=1).

## Requirements

- **Django** - web framework
- **Poetry** - package manager

## Libraries
- **Makefile** - for running commands conveniently
- **pyproject.toml** - for build system requirements

## Installation

Copy dev environment settings to local directory (create it first if it doesn't exist):

```bash
mkdir -p local
cp core/django_starter/settings/templates/settings.dev.py ./local/settings.dev.py
```

## Usage

Start the database:
```bash
docker compose -f docker-compose.dev.yml up db
```

Reinstall psycopg2-binary:
```bash
poetry remove psycopg2-binary
poetry add psycopg2-binary
```

Apply migrations:
```bash
make migrate
```

Create superuser:
```bash
make superuser
```

Run the server:
```bash
make run-server
```
## License

[MIT](https://choosealicense.com/licenses/mit/)
