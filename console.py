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

classes = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}

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

    def do_update(self, arg):
        """Update an instance based on the class name, id, attribute & value"""
        args = shlex.split(arg)
        integers = ["number_rooms", "number_bathrooms", "max_guest",
                    "price_by_night"]
        floats = ["latitude", "longitude"]
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] in classes:
            if len(args) > 1:
                k = args[0] + "." + args[1]
                if k in models.storage.all():
                    if len(args) > 2:
                        if len(args) > 3:
                            if args[0] == "Place":
                                if args[2] in integers:
                                    try:
                                        args[3] = int(args[3])
                                    except:
                                        args[3] = 0
                                elif args[2] in floats:
                                    try:
                                        args[3] = float(args[3])
                                    except:
                                        args[3] = 0.0
                            setattr(models.storage.all()[k], args[2], args[3])
                            models.storage.all()[k].save()
                        else:
                            print("** value missing **")
                    else:
                        print("** attribute name missing **")
                else:
                    print("** no instance found **")
            else:
                print("** instance id missing **")
        else:
            print("** class doesn't exist **")


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

    def do_create(self, arg):
        """Creates a new instance of a class"""
        args = arg.split()
        if len(args) == 0:
            print("** class name missing **")
            return False
        if args[0] in classes:
            new_dict = self._key_value_parser(args[1:])
            instance = classes[args[0]](**new_dict)
        else:
            print("** class doesn't exist **")
            return False
        print(instance.id)
        instance.save()

if __name__ == '__main__':
    HBNBCommand().cmdloop()
