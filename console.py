#!/usr/bin/python3
"""Defines the HBNB console."""
import cmd
from shlex import split
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """Command interpreter for HolbertonBnB."""

    prompt = "(hbnb) "
    __classes = {
        "BaseModel",
        "User",
        "State",
        "City",
        "Amenity",
        "Place",
        "Review"
    }

    _class_map = {
        "BaseModel": BaseModel,
        "User": User,
        "State": State,
        "City": City,
        "Amenity": Amenity,
        "Place": Place,
        "Review": Review
    }

    def emptyline(self):
        """Do nothing on empty input line."""
        pass

    def do_quit(self, line):
        """Quit the command interpreter."""
        return True

    def do_EOF(self, line):
        """Exit on EOF (Ctrl+D)."""
        print("")
        return True

    def do_create(self, line):
        """Creates a new instance with parameters:
        create <ClassName> <key=value> ...
        """
        try:
            if not line:
                raise SyntaxError()
            args = split(line)
            class_name = args[0]
            if class_name not in self.__classes:
                raise NameError()
            kwargs = {}
            for pair in args[1:]:
                if "=" not in pair:
                    continue
                key, value = pair.split("=", 1)
                if value.startswith('"') and value.endswith('"'):
                    value = value[1:-1].replace("_", " ")
                else:
                    try:
                        value = eval(value)
                    except Exception:
                        pass
                kwargs[key] = value
            obj = self._class_map[class_name](**kwargs)
            storage.new(obj)
            storage.save()
            print(obj.id)
        except SyntaxError:
            print("** class name missing **")
        except NameError:
            print("** class doesn't exist **")
        except Exception as e:
            print(f"An error occurred: {e}")
            try:
                storage._DBStorage__session.rollback()
            except Exception as rollback_error:
                print(f"Rollback failed: {rollback_error}")

    def do_show(self, line):
        """Shows the string representation of an instance."""
        try:
            if not line:
                raise SyntaxError()
            args = line.split()
            if args[0] not in self.__classes:
                raise NameError()
            if len(args) < 2:
                raise IndexError()
            obj = storage.all().get(f"{args[0]}.{args[1]}")
            if not obj:
                raise KeyError()
            print(obj)
        except SyntaxError:
            print("** class name missing **")
        except NameError:
            print("** class doesn't exist **")
        except IndexError:
            print("** instance id missing **")
        except KeyError:
            print("** no instance found **")

    def do_destroy(self, line):
        """Deletes an instance."""
        try:
            if not line:
                raise SyntaxError()
            args = line.split()
            if args[0] not in self.__classes:
                raise NameError()
            if len(args) < 2:
                raise IndexError()
            key = f"{args[0]}.{args[1]}"
            if key not in storage.all():
                raise KeyError()
            del storage.all()[key]
            storage.save()
        except SyntaxError:
            print("** class name missing **")
        except NameError:
            print("** class doesn't exist **")
        except IndexError:
            print("** instance id missing **")
        except KeyError:
            print("** no instance found **")

    def do_all(self, line):
        """Displays all instances of a class, or all if no class given."""
        args = line.split()
        objects = storage.all()
        if args and args[0] not in self.__classes:
            print("** class doesn't exist **")
            return
        result = [
            str(obj) for key, obj in objects.items()
            if not args or key.startswith(args[0])
        ]
        print(result)

    def do_update(self, line):
        """Updates an instance by setting attributes:
        update <class name> <id> <attribute name> "<attribute value>"
        """
        try:
            if not line:
                raise SyntaxError()
            args = split(line)
            if args[0] not in self.__classes:
                raise NameError()
            if len(args) < 2:
                raise IndexError()
            key = f"{args[0]}.{args[1]}"
            if key not in storage.all():
                raise KeyError()
            if len(args) < 3:
                raise AttributeError()
            if len(args) < 4:
                raise ValueError()
            obj = storage.all()[key]
            attr_name = args[2]
            try:
                attr_value = eval(args[3])
            except Exception:
                attr_value = args[3]
            setattr(obj, attr_name, attr_value)
            obj.save()  # optional if your save() calls storage.save()
            storage.save()  # push to DB
        except SyntaxError:
            print("** class name missing **")
        except NameError:
            print("** class doesn't exist **")
        except IndexError:
            print("** instance id missing **")
        except KeyError:
            print("** no instance found **")
        except AttributeError:
            print("** attribute name missing **")
        except ValueError:
            print("** value missing **")

    def count(self, line):
        """Counts instances of a given class."""
        try:
            args = line.split()
            if not args or args[0] not in self.__classes:
                raise NameError()
            count = sum(1 for k in storage.all() if k.startswith(args[0] + "."))
            print(count)
        except NameError:
            print("** class doesn't exist **")

    def strip_clean(self, args):
        """Helper to clean arguments from dot notation."""
        new_list = [args[0]]
        try:
            dict_repr = eval(args[1][args[1].find('{'):args[1].find('}')+1])
        except Exception:
            dict_repr = None
        if isinstance(dict_repr, dict):
            id_part = args[1][args[1].find('(')+1:args[1].find(')')].split(", ")[0].strip('"')
            new_list.append(id_part)
            new_list.append(dict_repr)
            return new_list
        arg_str = args[1][args[1].find('(')+1:args[1].find(')')]
        new_list.append(" ".join(arg_str.split(", ")))
        return " ".join(i for i in new_list)

    def default(self, line):
        """Handle default dot-notation commands."""
        args = line.split('.')
        if len(args) < 2:
            return cmd.Cmd.default(self, line)
        if args[1] == "all()":
            self.do_all(args[0])
        elif args[1] == "count()":
            self.count(args[0])
        elif args[1].startswith("show"):
            self.do_show(self.strip_clean(args))
        elif args[1].startswith("destroy"):
            self.do_destroy(self.strip_clean(args))
        elif args[1].startswith("update"):
            parts = self.strip_clean(args)
            if isinstance(parts, list):
                for key, value in parts[2].items():
                    self.do_update(f"{parts[0]} {parts[1]} {key} \"{value}\"")
            else:
                self.do_update(parts)


if __name__ == '__main__':
    HBNBCommand().cmdloop()
