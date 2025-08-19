#!/usr/bin/env python3
"""
🛹 Skate Park & Shop - Version Simple
"""

import os
import re

os.environ['HF_MODEL_ID'] = 'HuggingFaceH4/zephyr-7b-beta'

# Modèle 
class HfApiModel:
    def __init__(self, model_id):
        self.model_id = model_id
    
    def generate(self, prompt, max_tokens=100):
        if 'classify' in prompt.lower():
            if 'book' in prompt or 'reserve' in prompt:
                return "BOOKING"
            elif 'buy' in prompt or 'stock' in prompt:
                return "INVENTORY"
            else:
                return "GENERAL"
        return "Réponse générée par Zephyr-7B"

# État global simple
inventory = {'skateboard': 10, 'helmet': 5, 'wheels': 8}
bookings = []

# Outils
def get_inventory_level(item):
    return inventory.get(item.lower(), 0)

def sell_inventory_item(item, quantity):
    if inventory.get(item.lower(), 0) >= quantity:
        inventory[item.lower()] -= quantity
        return True, f"Vendu {quantity}x {item}"
    return False, "Stock insuffisant"

def check_booking_availability(date, time):
    return (date, time) not in bookings

def add_new_booking(date, time, customer):
    if check_booking_availability(date, time):
        bookings.append((date, time, customer))
        return True, f"Réservé pour {customer}"
    return False, "Créneau occupé"

# Agents
class CustomerSupportAgent:
    def __init__(self, model):
        self.model = model
    
    def diagnose_issue(self, request):
        return self.model.generate(f"classify: {request}")

class InventoryAgent:
    def check_stock(self, item):
        level = get_inventory_level(item)
        return f"{item}: {level} en stock"
    
    def process_purchase(self, item, qty):
        success, msg = sell_inventory_item(item, qty)
        return f"✅ {msg}" if success else f"❌ {msg}"

class ParkManagementAgent:
    def check_availability(self, date, time):
        available = check_booking_availability(date, time)
        return "Disponible" if available else "Occupé"
    
    def make_booking(self, date, time, customer):
        success, msg = add_new_booking(date, time, customer)
        return f"✅ {msg}" if success else f"❌ {msg}"

# Orchestrateur
class Orchestrator:
    def __init__(self, model):
        self.support = CustomerSupportAgent(model)
        self.inventory = InventoryAgent()
        self.park = ParkManagementAgent()
    
    def handle_request(self, request):
        print(f"🎯 Demande: {request}")
        
        # Classification
        category = self.support.diagnose_issue(request)
        print(f"📂 Catégorie: {category}")
        
        # Parsing simple
        date = re.search(r'\d{4}-\d{2}-\d{2}', request)
        time = re.search(r'\d{2}:\d{2}', request)
        buy_match = re.search(r'(\d+)\s+(\w+)', request)
        
        # Routage
        if category == "BOOKING" and date and time:
            availability = self.park.check_availability(date.group(), time.group())
            if "Disponible" in availability:
                booking = self.park.make_booking(date.group(), time.group(), "Client")
                return f"🏄 {booking}"
            else:
                return "❌ Créneau occupé, essayez un autre horaire"
        
        elif category == "INVENTORY":
            if buy_match:
                qty, item = int(buy_match.group(1)), buy_match.group(2)
                return f"🛒 {self.inventory.process_purchase(item, qty)}"
            else:
                # Recherche d'article dans la demande
                for item in inventory:
                    if item in request.lower():
                        return f"📦 {self.inventory.check_stock(item)}"
                return "📋 Stock: skateboard(10), helmet(5), wheels(8)"
        
        else:
            return "👋 Bonjour ! Skate Park & Shop Nairobi. Réservations ou achats ?"

# Demo
def main():
    print("🛹 Skate Park & Shop - Version Simple\n")
    
    model = HfApiModel("HuggingFaceH4/zephyr-7b-beta")
    orchestrator = Orchestrator(model)
    
    # 3 tests rapides
    tests = [
        "réserver 2024-03-15 14:00",
        "acheter 2 skateboard", 
        "bonjour, quels sont vos services ?"
    ]
    
    for test in tests:
        response = orchestrator.handle_request(test)
        print(f"💬 {response}\n")

if __name__ == "__main__":
    main()