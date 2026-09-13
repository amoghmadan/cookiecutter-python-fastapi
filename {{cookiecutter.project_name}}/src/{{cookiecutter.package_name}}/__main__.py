import os


def main():
    """Run administrative tasks."""
    os.environ.setdefault("FASTAPI_SETTINGS_MODULE", "{{cookiecutter.package_name}}.settings")
    try:
        from {{cookiecutter.package_name}}.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import {{cookiecutter.package_name}}. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line()


if __name__ == "__main__":
    main()
