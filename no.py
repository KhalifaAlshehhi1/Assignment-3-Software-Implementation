# -*- coding: utf-8 -*-
"""No.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1wKQ4GEpupEQjvZfwemnAPyroEdB5Rlto
"""

import tkinter as tk
from tkinter import messagebox
import pickle
import os

# Entity classes definitions
class Employee:
    def __init__(self, employee_id, name, department, job_title, basic_salary, age, date_of_birth, passport_details):
        self.employee_id = int(employee_id)
        self.name = name
        self.department = department
        self.job_title = job_title
        self.basic_salary = basic_salary
        self.age = age
        self.date_of_birth = date_of_birth
        self.passport_details = passport_details

class Event:
    def __init__(self, event_id, event_type, theme, date, time, duration, venue_id, client_id, budget):
        self.event_id = int(event_id)
        self.event_type = event_type
        self.theme = theme
        self.date = date
        self.time = time
        self.duration = duration
        self.venue_id = venue_id
        self.client_id = client_id
        self.budget = budget

class Client:
    def __init__(self, client_id, name, contact_details, address, budget):
        self.client_id = int(client_id)
        self.name = name
        self.contact_details = contact_details
        self.address = address
        self.budget = budget

class Guest:
    def __init__(self, guest_id, name, contact_details, address, special_requirements, event_id):
        self.guest_id = int(guest_id)
        self.name = name
        self.contact_details = contact_details
        self.address = address
        self.special_requirements = special_requirements
        self.event_id = event_id

class Supplier:
    def __init__(self, supplier_id, name, service_type, contact_details, address):
        self.supplier_id = int(supplier_id)
        self.name = name
        self.service_type = service_type
        self.contact_details = contact_details
        self.address = address

class Venue:
    def __init__(self, venue_id, name, address, capacity, booking_status):
        self.venue_id = int(venue_id)
        self.name = name
        self.address = address
        self.capacity = capacity
        self.booking_status = booking_status

# GUI class for event management system
class EventManagementSystemGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Event Management System")
        self.entities = {
            'employee': [], 'event': [], 'client': [], 'guest': [], 'supplier': [], 'venue': []
        }
        self.create_widgets()
        self.load_data()

    def create_widgets(self):
        buttons = ['Add', 'Delete', 'Modify', 'Display']
        for index, name in enumerate(buttons):
            button = tk.Button(self.master, text=name, command=lambda n=name: getattr(self, f"{n.lower()}_entity")())
            button.grid(row=0, column=index, padx=10, pady=5)

    def add_entity(self):
        entity_type = self.ask_entity_type()
        if entity_type and entity_type in self.entities:
            entity_class = globals()[entity_type.capitalize()]
            entity_details = self.get_entity_details(entity_class)
            if entity_details is not None:
                entity = entity_class(*entity_details)
                self.entities[entity_type].append(entity)
                self.save_data()
                messagebox.showinfo("Success", f"{entity_type.capitalize()} added successfully!")
        else:
            messagebox.showerror("Error", "Invalid entity type!")

    def delete_entity(self):
        entity_type = self.ask_entity_type()
        if entity_type and entity_type in self.entities:
            try:
                entity_id = int(input(f"Enter ID of the {entity_type} to delete: "))
                initial_count = len(self.entities[entity_type])
                self.entities[entity_type] = [e for e in self.entities[entity_type] if getattr(e, f"{entity_type}_id") != entity_id]
                if len(self.entities[entity_type]) < initial_count:
                    self.save_data()
                    messagebox.showinfo("Success", f"{entity_type.capitalize()} deleted successfully!")
                else:
                    raise ValueError(f"{entity_type.capitalize()} with ID {entity_id} not found!")
            except ValueError as e:
                messagebox.showerror("Error", str(e))
            except Exception as e:
                messagebox.showerror("Unexpected Error", str(e))

    def modify_entity(self):
        entity_type = self.ask_entity_type()
        if entity_type and entity_type in self.entities:
            try:
                entity_id = int(input(f"Enter ID of the {entity_type} to modify: "))
                entity = next((e for e in self.entities[entity_type] if getattr(e, f"{entity_type}_id") == entity_id),
                              None)
                if entity:
                    changes_made = False
                    for key, value in vars(entity).items():
                        if key != f"{entity_type}_id":  # Prevent modifying the ID
                            new_val = input(f"Enter new {key} (current: {value}): ")
                            if new_val:  # Only update if a new value is provided
                                setattr(entity, key, new_val)
                                changes_made = True
                    if changes_made:
                        self.save_data()
                        messagebox.showinfo("Success", f"{entity_type.capitalize()} modified successfully!")
                    else:
                        messagebox.showinfo("Info", "No changes made.")
                else:
                    raise ValueError(f"{entity_type.capitalize()} with ID {entity_id} not found!")
            except ValueError as e:
                messagebox.showerror("Error", str(e))
            except Exception as e:
                messagebox.showerror("Unexpected Error", str(e))

    def display_entity(self):
        entity_type = self.ask_entity_type()
        if entity_type and entity_type in self.entities:
            try:
                entity_id = int(input(f"Enter ID of the {entity_type} to display: "))
                entity = next((e for e in self.entities[entity_type] if getattr(e, f"{entity_type}_id") == entity_id), None)
                if entity:
                    details = '\n'.join([f"{key}: {value}" for key, value in vars(entity).items()])
                    messagebox.showinfo(f"{entity_type.capitalize()} Details", details)
                else:
                    raise ValueError(f"{entity_type.capitalize()} with ID {entity_id} not found!")
            except ValueError as e:
                messagebox.showerror("Error", str(e))
            except Exception as e:
                messagebox.showerror("Unexpected Error", str(e))

    def get_entity_details(self, entity_class):
        try:
            return [input(f"Enter {arg}: ") for arg in entity_class.__init__.__code__.co_varnames[1:]]
        except Exception as e:
            messagebox.showerror("Error", f"Invalid input: {e}")
            return None

    def ask_entity_type(self):
        types = ', '.join([key for key in self.entities.keys()])
        entity_type = input(f"Enter entity type ({types}): ").lower()
        if entity_type not in self.entities:
            messagebox.showerror("Error", "Invalid entity type specified!")
            return None
        return entity_type

    def load_data(self):
        for entity_type in self.entities:
            filename = f"{entity_type}.pkl"
            try:
                with open(filename, "rb") as f:
                    self.entities[entity_type] = pickle.load(f)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load data for {entity_type}: {e}")
                self.entities[entity_type] = []  # Initialize with an empty list if load fails

    def save_data(self):
        for entity_type, data in self.entities.items():
            try:
                with open(f"{entity_type}.pkl", "wb") as f:
                    pickle.dump(data, f)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save data for {entity_type}: {e}")

    def run(self):
        self.master.mainloop()

def main():
    root = tk.Tk()
    app = EventManagementSystemGUI(root)
    app.run()

if __name__ == "__main__":
    main()