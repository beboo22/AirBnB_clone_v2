#!/usr/bin/python3
"""command interpreter."""

import re
import cmd
import json
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
from models import storage


class HBNBCommand(cmd.Cmd):
    __models = ["User", "BaseModel", "Place", "State", "City",
                "Amenity", "Review"]
    prompt = "(hbnb) "

    def do_quit(self, line):
        """Quit command to exit the program
        """
        return True

    def do_EOF(self, line):
        """EOF command to exit the program
        """
        print()
        return True

    def emptyline(self):
        """don't execute anything
        """
        pass

    def do_create(self, arg):
        """Creates a new instance of BaseModel"""
        if arg in self.__models:
            obj = eval(arg)()
            obj.save()
            print(obj.id)
        elif len(arg) == 0:
            print("** class name missing **")
        else:
            print("** class doesn't exist **")

    def do_show(self, args):
        """
        Prints the string representation of an instance
        based on the class name and
        """
        splits = args.split()
        if len(splits) == 0:
            print("** class name missing **")
            return None

        if splits[0] not in self.__models:
            print("** class doesn't exist **")
            return None

        elif len(splits) == 1:
            if splits[0] in self.__models:
                print("** instance id missing **")
                return None

        all_objs = storage.all()
        if f"{splits[0]}.{splits[1]}" in all_objs:
            print("{}".format(all_objs[f"{splits[0]}.{splits[1]}"]))
            return None

        print("** no instance found **")

    def do_destroy(self, args):
        """Deletes an instance based on the class name and id"""
        splits = args.split()
        if len(splits) == 0:
            print("** class name missing **")
            return None

        if splits[0] not in self.__models:
            print("** class doesn't exist **")
            return None

        elif len(splits) == 1:
            if splits[0] in self.__models:
                print("** instance id missing **")
                return None

        all_objs = storage.all()
        if f"{splits[0]}.{splits[1]}" in all_objs:
            del all_objs[f"{splits[0]}.{splits[1]}"]
            storage.save()
        else:
            print("** no instance found **")
            return None

    def do_all(self, args):
        """
        Prints all string representation
        of all instances based or not on the class name
        """
        all_objs = storage.all()
        if not args:
            print([str(all_objs) for obj in all_objs.values()])
            return
        splits = args.split()
        if splits[0] not in self.__models:
            print("** class doesn't exist **")
        else:
            li = []
            for obj in all_objs.values():
                if obj.__class__.__name__ == splits[0]:
                    li.append(str(obj))
            print(li)

    def do_update(self, args):
        """
        Updates an instance based on the class name and
        id by adding or updating attribute
        """
        splits = args.split()
        if len(splits) == 0:
            print("** class name missing **")
            return None

        if splits[0] not in self.__models:
            print("** class doesn't exist **")
            return None

        elif len(splits) == 1:
            if splits[0] not in self.__models:
                print("** class doesn't exist **")
                return None
            else:
                print("** instance id missing **")
                return None

        all_objs = storage.all()
        if f"{splits[0]}.{splits[1]}" in all_objs:
            if len(splits) == 2:
                print("** attribute name missing **")
                return None
            elif len(splits) == 3:
                print("** value missing **")
                return None
        else:
            print("** no instance found **")
            return None
        if splits[3].isdigit():
            attr_value = int(splits[3])
        else:
            try:
                attr_value = float(splits[3])
            except ValueError:
                attr_value = splits[3].replace('"', "")
        for key, obj in all_objs.items():
            if f"{splits[0]}.{splits[1]}" == key:
                setattr(obj, splits[2], attr_value)
                storage.save()
                return None

    def default(self, line):
        """
        Update your command interpreter (console.py) to retrieve
        all instances of a class by using: <class name>.all()
        """
        if '.' in line:
            tokens = re.split(r'[().]', line)
            try:
                dictionary = tokens[2].split(", ", 1)[1]
            except IndexError:
                pass
            tokens = [item.replace('"', '') for item in tokens]
            tokens.pop()
            class_name = tokens[0]
            function_name = tokens[1]
            instance_id = tokens[2]
            if class_name in self.__models:
                # <class name>.all()
                if function_name == "all":
                    self.do_all(class_name)
                    return None

                # <class name>.count()
                if function_name == "count":
                    count = 0
                    all_objs = storage.all()
                    for key, value in all_objs.items():
                        if class_name == key.split('.')[0]:
                            count += 1
                    print(count)
                    return None

                # <class name>.show(<id>)
                if function_name == "show":
                    self.do_show(class_name + " " + instance_id)
                    return None

                # <class name>.destroy(<id>)
                if function_name == "destroy":
                    self.do_destroy(class_name + " " + instance_id)
                    return None

                if function_name == "update":
                    # <class name>.update(<id>, <dictionary representation>)
                    args = tokens[2].split(", ")
                    instance_id = args[0]

                    if '{' in dictionary:
                        att = json.loads(dictionary.replace("'", '"'))
                        for key, value in att.items():
                            self.do_update(class_name + " " +
                                           instance_id + " " +
                                           key + " " + str(value))

                    else:
                        # <class name>.update
                        # (<id>, <attribute name>, <attribute value>)
                        attr_name = args[1]
                        attr_value = args[2]
                        self.do_update(class_name + " " +
                                       instance_id + " " +
                                       attr_name + " " + attr_value)


if __name__ == '__main__':
    HBNBCommand().cmdloop()
