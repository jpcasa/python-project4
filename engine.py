#!/usr/bin/env python3
from collections import OrderedDict
import datetime
import sys
import os

from peewee import *

# Declare DB
db = SqliteDatabase('employees.db')

class Entry(Model):
    name = CharField(max_length=255)
    task = CharField(max_length=535)
    minutes = IntegerField()
    notes = TextField(default="")
    timestamp = CharField(default=datetime.date.today().strftime('%d/%m/%Y'))

    class Meta:
        database = db

class Engine:
    """Main Program Engine."""

    def __init__(self):
        self.main_menu = OrderedDict([
            ('a', self.add_entry),
            ('v', self.view_entries),
            ('s', self.search_entries),
        ])


    def clear(self):
        """Clear Fix."""
        os.system('cls' if os.name == 'nt' else 'clear')


    def initialize(self):
        db.connect()
        db.create_tables([Entry], safe=True)

    def menu_loop(self):
        """Show the menu."""
        choice = None

        while choice != 'q':
            self.clear()
            print("Welcome to the Task Manager")
            print("Enter 'q' to quit.\n")
            for key, value in self.main_menu.items():
                print('{}) {}'.format(key, value.__doc__))
            choice = raw_input('\nAction: ').lower().strip()

            if choice in self.main_menu:
                self.clear()
                self.main_menu[choice]()


    def add_entry(self):
        """Add an Entry."""

        finished = False
        name, task = (None, None)
        name_error, task_error, minutes_error = (None, None, None)
        minutes = 0

        # Creation Loop
        while finished == False:

            # Clear
            self.clear()

            print("Task Creator (Press 'q' to return)\n")

            # Check for name
            if not name and not name_error:
                name = raw_input("Please enter your name: ").strip()
            elif name_error:
                name = raw_input(name_error).strip()
            else:
                print("Please enter your name: {}".format(name))

            # Check for Quit Option
            if name == 'q':
                finished = True
                break

            # Check for valid input
            if self.validate_input('string', name):

                # Reset Name Error
                if name_error:
                    name_error = None

                # Check for task
                if not task:
                    task = raw_input("Please enter the task you worked on: ").strip()
                elif task_error:
                    task = raw_input(task_error).strip()
                else:
                    print("Please enter the task you worked on: {}".format(task))
                # Check for Quit Option
                if task == 'q':
                    finished = True
                    break

                # Check for valid input
                if self.validate_input('string', task):

                    # Reset Task Error
                    if task_error:
                        task_error = None

                    if not minutes:
                        task = raw_input("Please enter the number of minutes you took: ").strip()

                # Task Input Error
                else:
                    task_error = 'Please enter a valid task you worked on: '

            # Name Input Error
            else:
                # Declare Name Error
                name_error = 'Please enter a valid name: '



    def view_entries(self):
        """View Entries."""
        pass


    def search_entries(self):
        """Search Entries."""
        pass


    def validate_input(self, what, value):
        """Validate User Input"""
        if what == 'string':
            if value:
                return True
            else:
                return False
