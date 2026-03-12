import argparse
import importlib
import inspect
import os
import sys
from .models import Model, TimestampedModel
from .db import Database

def migrate(modules):
    """
    Looks for all subclasses of Model in the given modules and creates the
    corresponding tables in CouchDB if they don't exist.
    """
    print("Starting migration...")
    db_server = Database()  # This will use env vars
    Model.set_server(db_server) # Set the server for all models

    for module_name in modules:
        try:
            # Add the current directory to the path to help with module discovery
            sys.path.insert(0, os.getcwd())
            module = importlib.import_module(module_name)
            print(f"Inspecting module: {module_name}")
            for name, obj in inspect.getmembers(module):
                if inspect.isclass(obj) and issubclass(obj, Model) and obj not in [Model, TimestampedModel]:
                    if hasattr(obj, '_table_name') and obj._table_name:
                        print(f"Found model {obj.__name__} with table_name: {obj._table_name}")
                        # The get_db method on the model will now work
                        obj.get_db()
                        print(f"Ensured database '{obj._table_name}' exists.")
                    else:
                        print(f"Warning: Model {obj.__name__} has no Meta class with table_name.")
        except ImportError as e:
            print(f"Error: Could not import module {module_name}. {e}")
        finally:
            # Clean up path
            if os.getcwd() in sys.path:
                sys.path.remove(os.getcwd())

def main():
    parser = argparse.ArgumentParser(description="TMTVR command-line utility.")
    subparsers = parser.add_subparsers(dest='command', required=True)

    # Migrate command
    migrate_parser = subparsers.add_parser('migrate', help='Run database migrations.')
    migrate_parser.add_argument('modules', nargs='*', default=['models'], help='List of modules containing models to migrate (e.g., myapp.models). Defaults to "models".')

    args = parser.parse_args()

    if args.command == 'migrate':
        migrate(args.modules)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
