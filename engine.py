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


    def initialize(self, daba=None):
        try:
            db.connect()
            db.create_tables([Entry], safe=True)
        except OperationalError:
            print("DB Connection Failed")

    def menu_loop(self, choice=None):
        """Show the menu."""

        while choice != 'q':
            self.clear()
            print("Welcome to the Task Manager")
            print("Enter 'q' to quit.\n")
            for key, value in self.main_menu.items():
                print('{}) {}'.format(key, value.__doc__))
            choice = input('\nAction: ').lower().strip()

            if choice in self.main_menu:
                self.clear()
                self.main_menu[choice]()
            elif choice == 'q':
                self.clear()


    def get_all_entries(self):
        return Entry.select().order_by(Entry.id.desc())


    def get_last_entry(self):
        return Entry.select().order_by(Entry.id.desc()).get()


    def add_simple_entry(self, name, task, minutes, notes):
        Entry.create(
        name=name,
        task=task,
        minutes=minutes,
        notes=notes)


    def add_entry(self, entry=None, finished=False):
        """Add an Entry."""

        if not entry:
            name, task, notes = (None, None, None)
            minutes = 0
        else:
            name = entry.name
            task = entry.task
            minutes = entry.minutes
            notes = entry.notes

        # Declare Errors
        name_error, task_error, minutes_error = (None, None, None)

        # Creation Loop
        while finished == False:

            # Clear
            self.clear()
            if not entry:
                print("Task Creator (Press 'q' to return)\n")
            else:
                print("Edit Task")

            # Check for name
            if not name and not name_error:
                name = input("Please enter your name: ").strip()
            elif name_error:
                name = input(name_error).strip()
            elif entry:
                msg = "Please enter your name[{}]: ".format(entry.name)
                name = input(msg).strip() or entry.name
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
                if not task and not task_error:
                    task = input("Please enter the task you worked on: ").strip()
                elif entry:
                    msg = "Please enter the task you worked on[{}]: ".format(entry.task)
                    task = input(msg).strip() or entry.task
                elif task_error:
                    task = input(task_error).strip()
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

                    # Handle Minute Input
                    if not minutes and not minutes_error:
                        minutes = input("Please enter the number of minutes you took: ").strip()
                    elif entry:
                        msg = "Please enter the number of minutes you took[{}]: ".format(entry.minutes)
                        minutes = input(msg).strip() or entry.minutes
                    elif minutes_error:
                        minutes = input(minutes_error).strip()
                    else:
                        print("Please enter the number of minutes you took: {}".format(minutes))

                    # Check for Quit Option
                    if minutes == 'q':
                        finished = True
                        break

                    if self.validate_input('int', minutes):

                        # Reset Minutes Error
                        if minutes_error:
                            minutes_error = None

                        # Display Current Notes
                        if entry and notes != '':
                            print('Current Notes: {}'.format(entry.notes))
                            notes = input("Edit Notes: ").strip() or entry.notes
                        else:
                            # Asks for Optional Notes
                            notes = input("Enter some notes (Optional): ").strip() or ""

                        # Last check
                        if input('Save entry? [Yn] ').lower() != 'n':

                            # Check if Edit or Add
                            if not entry:
                                # Create Entry in DB
                                Entry.create(
                                name=name,
                                task=task,
                                minutes=minutes,
                                notes=notes)
                            else:
                                Entry.update(
                                    name=name,
                                    task=task,
                                    minutes=minutes,
                                    notes=notes
                                ).where(
                                    Entry.task == task
                                ).execute()

                            # Finish Loop
                            finished = True
                            break
                        # Task Input Error
                    else:
                        minutes_error = 'Please enter a valid integer number: '
                # Task Input Error
                else:
                    task_error = 'Please enter a valid task you worked on: '

            # Name Input Error
            else:
                # Declare Name Error
                name_error = 'Please enter a valid name: '


    def view_entries(self, searched=None, entries=None):
        """View Entries."""
        # Get Entries
        if not searched:
            entries = Entry.select().order_by(Entry.timestamp.desc())
        elif searched and not entries:
            print('No records found with this criteria')
            input('Pres [Enter] to continue: ')
            next_action = 'b'

        # Loop Counter
        count = 0

        next_action = None

        # Check if Entries
        if len(entries) > 0:
            while count < len(entries):

                # Clear
                self.clear()
                # Display Cool Entry
                self.display_entry(entries[count])

                # User options
                if count == 0 and len(entries) == 1:
                    msg = '([D]elete/[E]dit/[B]ack)'
                elif count == 0 and len(entries) > 1:
                    msg = '([N]ext/[D]elete/[E]dit/[B]ack)'
                elif count == (len(entries) - 1):
                    msg = '([P]revious/[D]elete/[E]dit/[B]ack)'
                else:
                    msg = '([P]revious/[N]ext/[D]elete/[E]dit/[B]ack)'


                next_action = input('Action: {}: '.format(msg)).lower().strip()

                if next_action == 'n':
                    if count == 0 and len(entries) == 1:
                        pass
                    else:
                        count += 1
                elif next_action == 'p':
                    if count == 0 and len(entries) > 1:
                        pass
                    else:
                        count -= 1
                elif next_action == 'd':
                    if self.delete_entry(entries[count]):
                        count = len(entries) + 1
                elif next_action == 'e':
                    self.add_entry(entries[count])
                    count = len(entries) + 1
                else:
                    count = len(entries) + 1

        else:
            if not searched:
                # Give the user the option to create a new record
                print('You haven\'t created any records yet...')
                if input('Create Entry? [Yn]: ') != 'n':
                    self.add_entry()


    def search_entries(self):
        """Search Entries."""
        self.clear()

        # Options
        print('Search Entries By:\n')
        print('a) Employee')
        print('b) Date')
        print('c) Time Spent')
        print('d) Search Term')
        print('q) Back to Main Menu\n')

        msg = 'Choose the criteria to search: '
        search_action = input(msg).lower().strip()

        if search_action == 'a':
            search_query = input('Enter Employee Name: ').strip()
            self.view_entries('query', self.search_tasks('name', search_query))
        elif search_action == 'b':
            search_query = input('Enter Date (d/m/Y): ').strip()
            self.view_entries('query', self.search_tasks('timestamp', search_query))
        elif search_action == 'c' or self.validate_input('int', search_action):
            search_query = input('Enter minutes: ').strip()
            self.view_entries('query', self.search_tasks('minutes', search_query))
        elif search_action == 'd':
            search_query = input('Enter Search Term: ').strip()
            self.view_entries('query', self.search_tasks('search_term', search_query))


    def search_tasks(self, search_by, *search_query):
        """Search Tasks with Criteria"""
        # Get Entries
        entries = Entry.select().order_by(Entry.timestamp.desc())

        # Check Criteria
        if search_by == 'name':
            return entries.where(Entry.name==search_query[0])
        elif search_by == 'timestamp':
            return entries.where(Entry.timestamp==search_query[0])
        elif search_by == 'minutes':
            return entries.where(Entry.minutes==search_query[0])
        elif search_by == 'search_term':
            return entries.where(
                Entry.task.contains(search_query[0]) |
                Entry.notes.contains(search_query[0]))


    def validate_input(self, what, value):
        """Validate User Input"""
        if what == 'string':
            if isinstance(value, str):
                return True
            else:
                return False
        elif what == 'int':
            try:
                int(value)
                return True
            except ValueError:
                return False



    def delete_entry(self, entry):
        """Delete an entry."""
        if input('Are you sure? [Yn]: ').lower().strip() == 'y':
            entry.delete_instance()
            print('Entry deleted!')
            input('Go back to main menu [Enter]: ')
            return True
        return False


    def display_entry(self, entry):
        print("Showing all tasks: \n")
        print(entry.timestamp)
        print('='*len(entry.timestamp))
        print('Task Author: {}'.format(entry.name))
        print('Task: {}'.format(entry.task))
        print('Minutes Spent: {}'.format(entry.minutes))
        if entry.notes != "":
            print('Notes (Optional): {}'.format(entry.notes))
        print('')
