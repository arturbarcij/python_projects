class Contact_book:
    def __init__(self):
        self.contacts = []

    def add_contact(self, name, phone, adress):
        contact = {
            "name": name,
            "phone": phone,
            "adress": adress
        }
        self.contacts.append(contact)
        print(f"Contact {name} added succesfully.")
    
    def remove_contact(self, name):
        for contact in self.contacts:
            if contact["name"] == name:
                self.contacts.remove(contact)
                print(f"Contact {name} removed succesfully.")
            else:
                print(f"Contact {name} not found")

    def update_contact(self, name, phone=None, adress=None):
        for contact in self.contacts:
            if contact["name"] == name:
                if phone:
                    contact["phone"] == phone
                if adress:
                    contact["adress"] == adress
            print(f"Contact {name} updated succesfully.")
            return
        print(f"Contact {name} not found.")
    
    def display_contacts(self):
        if not self.contacts:
            print("No contact found.")
            return
        for contact in self.contacts:
            print(f"Name: {contact['name']}, Phone: {contact['phone']}, Adress: {contact['adress']}")
    

book = Contact_book()

book.add_contact("Alice", "1234567890", "123 Wonderland")
book.add_contact("Bob", "0987654321", "456 Nowhere")

# Display contacts
book.display_contacts()

# Update a contact
book.update_contact("Alice", phone="1111111111")

# Display contacts
book.display_contacts()

# Remove a contact
book.remove_contact("Bob")

# Display contacts
book.display_contacts()