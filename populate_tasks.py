"""
Script to populate todos.json with sample tasks
Run this once to load the sample data into your app
"""
import json
from datetime import datetime

sample_tasks = [
  {"title":"Replace car windshield wipers","dueDate":"2026-04-03","description":"Improve visibility before spring rains."},
  {"title":"Organize bedroom closet","dueDate":"2026-02-20","description":"Sort clothes and remove clutter."},
  {"title":"Pay electric bill","dueDate":"2026-02-10","description":"Avoid late fees by paying on time."},
  {"title":"Research weekend getaway spots","dueDate":"2026-05-01","description":"Explore options for a short trip."},
  {"title":"Clean out email inbox","dueDate":"2026-02-15","description":"Delete junk and archive important messages."},
  {"title":"Update résumé","dueDate":"2026-06-10","description":"Refresh job history and skills."},
  {"title":"Call insurance company","dueDate":"2026-02-18","description":"Clarify coverage questions."},
  {"title":"Meal-prep lunches for the week","dueDate":"2026-02-09","description":"Cook and portion meals."},
  {"title":"Wash and fold laundry","dueDate":"2026-02-09","description":"Clean clothes and bedding."},
  {"title":"Refill prescription","dueDate":"2026-02-12","description":"Ensure medication supply doesn't run out."},
  {"title":"Vacuum living room","dueDate":"2026-02-11","description":"Remove dust and debris."},
  {"title":"Back up phone photos","dueDate":"2026-03-05","description":"Save memories to cloud or drive."},
  {"title":"Plan birthday gift for a friend","dueDate":"2026-04-15","description":"Choose and order a thoughtful gift."},
  {"title":"Fix squeaky door hinge","dueDate":"2026-02-22","description":"Lubricate or tighten hardware."},
  {"title":"Review monthly budget","dueDate":"2026-03-01","description":"Adjust spending categories."},
  {"title":"Water houseplants","dueDate":"2026-02-08","description":"Keep plants healthy and hydrated."},
  {"title":"Order new running shoes","dueDate":"2026-03-20","description":"Replace worn-out footwear."},
  {"title":"Declutter kitchen drawers","dueDate":"2026-03-02","description":"Remove unused utensils."},
  {"title":"Schedule dentist appointment","dueDate":"2026-04-08","description":"Book cleaning and exam."},
  {"title":"Take recycling out","dueDate":"2026-02-09","description":"Clear bins before pickup."},
  {"title":"Update software on laptop","dueDate":"2026-02-14","description":"Install security patches."},
  {"title":"Buy dog food","dueDate":"2026-02-10","description":"Restock pet supplies."},
  {"title":"Research new hobby ideas","dueDate":"2026-06-01","description":"Explore creative activities."},
  {"title":"Clean out car interior","dueDate":"2026-02-25","description":"Remove trash and vacuum seats."},
  {"title":"Renew driver's license","dueDate":"2026-09-15","description":"Complete renewal before expiration."},
  {"title":"Replace air filters at home","dueDate":"2026-04-01","description":"Improve air quality."},
  {"title":"Prep tax documents","dueDate":"2026-03-20","description":"Gather forms and receipts."},
  {"title":"Write thank-you notes","dueDate":"2026-03-05","description":"Send appreciation messages."},
  {"title":"Organize bookshelf","dueDate":"2026-03-10","description":"Sort books by category."},
  {"title":"Donate old clothes","dueDate":"2026-04-02","description":"Drop off items at donation center."},
  {"title":"Check tire pressure","dueDate":"2026-02-16","description":"Ensure safe driving conditions."},
  {"title":"Plan weekly workout routine","dueDate":"2026-02-13","description":"Set fitness schedule."},
  {"title":"Review credit report","dueDate":"2026-05-15","description":"Check for errors or fraud."},
  {"title":"Buy birthday card","dueDate":"2026-03-18","description":"Pick a card for upcoming event."},
  {"title":"Clean bathroom sink","dueDate":"2026-02-10","description":"Remove stains and buildup."},
  {"title":"Update phone contacts","dueDate":"2026-04-12","description":"Remove duplicates and old numbers."},
  {"title":"Create backup of important files","dueDate":"2026-03-25","description":"Store copies securely."},
  {"title":"Schedule haircut","dueDate":"2026-02-28","description":"Book appointment before growth gets wild."},
  {"title":"Wash dishes","dueDate":"2026-02-08","description":"Clean sink and counters."},
  {"title":"Organize digital files","dueDate":"2026-04-20","description":"Sort documents and photos."},
  {"title":"Buy printer ink","dueDate":"2026-03-07","description":"Restock before running out."},
  {"title":"Research investment options","dueDate":"2026-07-01","description":"Explore long-term financial strategies."},
  {"title":"Plan grocery list","dueDate":"2026-02-09","description":"Prepare items for next trip."},
  {"title":"Clean microwave","dueDate":"2026-02-12","description":"Remove food splatters."},
  {"title":"Replace light bulbs","dueDate":"2026-02-17","description":"Fix dim or dead bulbs."},
  {"title":"Check smoke detector batteries","dueDate":"2026-03-30","description":"Ensure safety devices work."},
  {"title":"Plan date night","dueDate":"2026-04-22","description":"Choose activity and location."},
  {"title":"Review subscription services","dueDate":"2026-05-10","description":"Cancel unused ones."},
  {"title":"Organize pantry","dueDate":"2026-03-12","description":"Sort food items and toss expired goods."},
  {"title":"Buy new bedsheets","dueDate":"2026-04-05","description":"Replace worn linens."},
  {"title":"Clean fridge shelves","dueDate":"2026-02-18","description":"Remove spills and expired items."},
  {"title":"Update emergency contact list","dueDate":"2026-05-25","description":"Add new numbers."},
  {"title":"Plan weekend meal menu","dueDate":"2026-02-14","description":"Decide meals ahead of time."},
  {"title":"Sweep front porch","dueDate":"2026-02-11","description":"Clear dirt and leaves."},
  {"title":"Research new TV options","dueDate":"2026-08-01","description":"Compare models and prices."},
  {"title":"Create packing list for trip","dueDate":"2026-06-15","description":"Prepare essentials."},
  {"title":"Clean shower tiles","dueDate":"2026-02-19","description":"Scrub grout and soap scum."},
  {"title":"Buy vitamins","dueDate":"2026-02-13","description":"Restock supplements."},
  {"title":"Organize receipts","dueDate":"2026-03-18","description":"Sort for budgeting or taxes."},
  {"title":"Check bank statements","dueDate":"2026-03-02","description":"Review transactions."},
  {"title":"Reorganize workspace","dueDate":"2026-03-22","description":"Improve productivity layout."},
  {"title":"Water outdoor plants","dueDate":"2026-02-09","description":"Keep garden hydrated."},
  {"title":"Replace toothbrush","dueDate":"2026-02-15","description":"Swap for a fresh one."},
  {"title":"Clean keyboard","dueDate":"2026-02-12","description":"Remove dust and crumbs."},
  {"title":"Plan monthly goals","dueDate":"2026-03-01","description":"Set targets for next month."},
  {"title":"Buy stamps","dueDate":"2026-04-10","description":"Restock for mailing."},
  {"title":"Review insurance policy","dueDate":"2026-06-20","description":"Check coverage details."},
  {"title":"Clean windows","dueDate":"2026-04-25","description":"Improve natural light."},
  {"title":"Order groceries online","dueDate":"2026-02-09","description":"Schedule delivery."},
  {"title":"Update passwords","dueDate":"2026-05-05","description":"Improve account security."},
  {"title":"Organize cables","dueDate":"2026-03-28","description":"Label and bundle cords."},
  {"title":"Buy new pillow","dueDate":"2026-04-18","description":"Replace old pillow."},
  {"title":"Clean coffee maker","dueDate":"2026-02-16","description":"Remove mineral buildup."},
  {"title":"Plan movie night","dueDate":"2026-03-08","description":"Pick films and snacks."},
  {"title":"Check freezer inventory","dueDate":"2026-02-14","description":"See what needs restocking."},
  {"title":"Clean out junk drawer","dueDate":"2026-03-06","description":"Toss useless items."},
  {"title":"Review retirement account","dueDate":"2026-07-15","description":"Check contributions."},
  {"title":"Buy snacks for work","dueDate":"2026-02-10","description":"Stock up for the week."},
  {"title":"Organize garage tools","dueDate":"2026-04-30","description":"Sort and store equipment."},
  {"title":"Clean stovetop","dueDate":"2026-02-13","description":"Remove grease and stains."},
  {"title":"Replace shower curtain liner","dueDate":"2026-03-04","description":"Prevent mildew."},
  {"title":"Plan social media detox","dueDate":"2026-05-12","description":"Set boundaries and schedule."},
  {"title":"Check for software updates","dueDate":"2026-02-15","description":"Keep devices secure."},
  {"title":"Buy new notebook","dueDate":"2026-03-14","description":"Replace old one."},
  {"title":"Clean car exterior","dueDate":"2026-02-20","description":"Wash and wax vehicle."},
  {"title":"Review phone storage","dueDate":"2026-03-09","description":"Delete unused apps."},
  {"title":"Organize travel documents","dueDate":"2026-06-10","description":"Prepare for upcoming trip."},
  {"title":"Buy batteries","dueDate":"2026-02-12","description":"Restock household supply."},
  {"title":"Clean baseboards","dueDate":"2026-03-16","description":"Dust and wipe edges."},
  {"title":"Plan reading list","dueDate":"2026-04-28","description":"Choose books for the season."},
  {"title":"Check weather for the week","dueDate":"2026-02-08","description":"Prepare clothing and plans."},
  {"title":"Organize medicine cabinet","dueDate":"2026-03-11","description":"Toss expired meds."},
  {"title":"Buy dish soap","dueDate":"2026-02-09","description":"Restock cleaning supplies."},
  {"title":"Clean out old text messages","dueDate":"2026-04-03","description":"Free up storage."},
  {"title":"Plan monthly budget","dueDate":"2026-03-01","description":"Allocate spending."},
  {"title":"Replace kitchen sponge","dueDate":"2026-02-08","description":"Swap for a clean one."},
  {"title":"Review calendar for upcoming events","dueDate":"2026-02-14","description":"Prepare for deadlines."},
  {"title":"Declutter old cables and chargers","dueDate":"2026-04-07","description":"Remove unused electronics."}
]

def convert_date_format(date_str):
    """Convert from YYYY-MM-DD to MM/DD/YYYY"""
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    return date_obj.strftime("%m/%d/%Y")

def populate_tasks():
    """Convert sample tasks to app format and save to todos.json"""
    todos = []
    
    for task_data in sample_tasks:
        todo = {
            "task": task_data["title"],
            "due": convert_date_format(task_data["dueDate"]),
            "description": task_data["description"],
            "completed": False,
            "completed_at": None,
            "deleted": False,
            "deleted_at": None,
            "saved": False,
            "saved_at": None
        }
        todos.append(todo)
    
    # Save to todos.json
    with open("todos.json", "w") as f:
        json.dump(todos, f, indent=2)
    
    print(f"✅ Successfully loaded {len(todos)} tasks into todos.json!")
    print("Refresh your app in the browser to see all the new tasks.")

if __name__ == "__main__":
    populate_tasks()
