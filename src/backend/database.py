"""
MongoDB database configuration and setup for Mergington High School API
"""

try:
    from pymongo import MongoClient
    from argon2 import PasswordHasher

    # Try to connect to MongoDB
    client = MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=1000)
    client.server_info()  # Test connection
    db = client['mergington_high']
    activities_collection = db['activities']
    teachers_collection = db['teachers']
    
except Exception:
    # Fallback to mock database for development/testing
    print("MongoDB not available, using mock database")
    
    from argon2 import PasswordHasher
    
    # Mock collections using dictionaries
    activities_collection_data = {}
    teachers_collection_data = {}

    # Mock collection class
    class MockCollection:
        def __init__(self, data):
            self.data = data
        
        def count_documents(self, filter_dict):
            return len(self.data)
        
        def insert_one(self, document):
            id_field = document.get("_id")
            self.data[id_field] = {k: v for k, v in document.items() if k != "_id"}
            return type('MockResult', (), {'inserted_id': id_field})()
        
        def find(self, filter_dict=None):
            if filter_dict is None:
                filter_dict = {}
            
            results = []
            for id_val, doc in self.data.items():
                doc_copy = {"_id": id_val, **doc}
                
                # Simple filter matching - this is a basic implementation
                match = True
                for key, value in filter_dict.items():
                    if key not in doc_copy:
                        match = False
                        break
                    # Handle MongoDB operators
                    if isinstance(value, dict):
                        if "$in" in value:
                            if key not in doc_copy or not any(item in doc_copy[key] for item in value["$in"]):
                                match = False
                                break
                        elif "$gte" in value:
                            if key not in doc_copy or doc_copy[key] < value["$gte"]:
                                match = False
                                break
                        elif "$lte" in value:
                            if key not in doc_copy or doc_copy[key] > value["$lte"]:
                                match = False
                                break
                    else:
                        if doc_copy[key] != value:
                            match = False
                            break
                
                if match:
                    results.append(doc_copy)
            
            return results
        
        def find_one(self, filter_dict):
            results = self.find(filter_dict)
            return results[0] if results else None
        
        def update_one(self, filter_dict, update_dict):
            # Find matching document
            for id_val, doc in self.data.items():
                doc_copy = {"_id": id_val, **doc}
                
                match = True
                for key, value in filter_dict.items():
                    if key not in doc_copy or doc_copy[key] != value:
                        match = False
                        break
                
                if match:
                    # Apply updates
                    for op, updates in update_dict.items():
                        if op == "$push":
                            for field, value in updates.items():
                                if field not in self.data[id_val]:
                                    self.data[id_val][field] = []
                                self.data[id_val][field].append(value)
                        elif op == "$pull":
                            for field, value in updates.items():
                                if field in self.data[id_val] and isinstance(self.data[id_val][field], list):
                                    self.data[id_val][field] = [item for item in self.data[id_val][field] if item != value]
                    
                    return type('MockResult', (), {'modified_count': 1})()
            
            return type('MockResult', (), {'modified_count': 0})()
        
        def aggregate(self, pipeline):
            # Basic aggregation support for getting unique days
            results = []
            if len(pipeline) >= 2 and pipeline[0].get("$unwind") == "$schedule_details.days":
                # Get all unique days
                days = set()
                for doc in self.data.values():
                    if "schedule_details" in doc and "days" in doc["schedule_details"]:
                        for day in doc["schedule_details"]["days"]:
                            days.add(day)
                
                for day in sorted(days):
                    results.append({"_id": day})
            
            return results

    # Mock collections
    activities_collection = MockCollection(activities_collection_data)
    teachers_collection = MockCollection(teachers_collection_data)

# Methods
def hash_password(password):
    """Hash password using Argon2"""
    ph = PasswordHasher()
    return ph.hash(password)

def init_database():
    """Initialize database if empty"""

    # Initialize activities if empty
    if activities_collection.count_documents({}) == 0:
        for name, details in initial_activities.items():
            activities_collection.insert_one({"_id": name, **details})
            
    # Initialize teacher accounts if empty
    if teachers_collection.count_documents({}) == 0:
        for teacher in initial_teachers:
            teachers_collection.insert_one({"_id": teacher["username"], **teacher})

# Initial database if empty
initial_activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Mondays and Fridays, 3:15 PM - 4:45 PM",
        "schedule_details": {
            "days": ["Monday", "Friday"],
            "start_time": "15:15",
            "end_time": "16:45"
        },
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 7:00 AM - 8:00 AM",
        "schedule_details": {
            "days": ["Tuesday", "Thursday"],
            "start_time": "07:00",
            "end_time": "08:00"
        },
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Morning Fitness": {
        "description": "Early morning physical training and exercises",
        "schedule": "Mondays, Wednesdays, Fridays, 6:30 AM - 7:45 AM",
        "schedule_details": {
            "days": ["Monday", "Wednesday", "Friday"],
            "start_time": "06:30",
            "end_time": "07:45"
        },
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Soccer Team": {
        "description": "Join the school soccer team and compete in matches",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 5:30 PM",
        "schedule_details": {
            "days": ["Tuesday", "Thursday"],
            "start_time": "15:30",
            "end_time": "17:30"
        },
        "max_participants": 22,
        "participants": ["liam@mergington.edu", "noah@mergington.edu"]
    },
    "Basketball Team": {
        "description": "Practice and compete in basketball tournaments",
        "schedule": "Wednesdays and Fridays, 3:15 PM - 5:00 PM",
        "schedule_details": {
            "days": ["Wednesday", "Friday"],
            "start_time": "15:15",
            "end_time": "17:00"
        },
        "max_participants": 15,
        "participants": ["ava@mergington.edu", "mia@mergington.edu"]
    },
    "Art Club": {
        "description": "Explore various art techniques and create masterpieces",
        "schedule": "Thursdays, 3:15 PM - 5:00 PM",
        "schedule_details": {
            "days": ["Thursday"],
            "start_time": "15:15",
            "end_time": "17:00"
        },
        "max_participants": 15,
        "participants": ["amelia@mergington.edu", "harper@mergington.edu"]
    },
    "Drama Club": {
        "description": "Act, direct, and produce plays and performances",
        "schedule": "Mondays and Wednesdays, 3:30 PM - 5:30 PM",
        "schedule_details": {
            "days": ["Monday", "Wednesday"],
            "start_time": "15:30",
            "end_time": "17:30"
        },
        "max_participants": 20,
        "participants": ["ella@mergington.edu", "scarlett@mergington.edu"]
    },
    "Math Club": {
        "description": "Solve challenging problems and prepare for math competitions",
        "schedule": "Tuesdays, 7:15 AM - 8:00 AM",
        "schedule_details": {
            "days": ["Tuesday"],
            "start_time": "07:15",
            "end_time": "08:00"
        },
        "max_participants": 10,
        "participants": ["james@mergington.edu", "benjamin@mergington.edu"]
    },
    "Debate Team": {
        "description": "Develop public speaking and argumentation skills",
        "schedule": "Fridays, 3:30 PM - 5:30 PM",
        "schedule_details": {
            "days": ["Friday"],
            "start_time": "15:30",
            "end_time": "17:30"
        },
        "max_participants": 12,
        "participants": ["charlotte@mergington.edu", "amelia@mergington.edu"]
    },
    "Weekend Robotics Workshop": {
        "description": "Build and program robots in our state-of-the-art workshop",
        "schedule": "Saturdays, 10:00 AM - 2:00 PM",
        "schedule_details": {
            "days": ["Saturday"],
            "start_time": "10:00",
            "end_time": "14:00"
        },
        "max_participants": 15,
        "participants": ["ethan@mergington.edu", "oliver@mergington.edu"]
    },
    "Science Olympiad": {
        "description": "Weekend science competition preparation for regional and state events",
        "schedule": "Saturdays, 1:00 PM - 4:00 PM",
        "schedule_details": {
            "days": ["Saturday"],
            "start_time": "13:00",
            "end_time": "16:00"
        },
        "max_participants": 18,
        "participants": ["isabella@mergington.edu", "lucas@mergington.edu"]
    },
    "Sunday Chess Tournament": {
        "description": "Weekly tournament for serious chess players with rankings",
        "schedule": "Sundays, 2:00 PM - 5:00 PM",
        "schedule_details": {
            "days": ["Sunday"],
            "start_time": "14:00",
            "end_time": "17:00"
        },
        "max_participants": 16,
        "participants": ["william@mergington.edu", "jacob@mergington.edu"]
    },
    "Manga Maniacs": {
        "description": "Dive into epic adventures, legendary heroes, and incredible worlds through Japanese manga - discuss your favorite series and discover new ones!",
        "schedule": "Tuesdays, 7:00 PM - 8:00 PM",
        "schedule_details": {
            "days": ["Tuesday"],
            "start_time": "19:00",
            "end_time": "20:00"
        },
        "max_participants": 15,
        "participants": []
    }
}

initial_teachers = [
    {
        "username": "mrodriguez",
        "display_name": "Ms. Rodriguez",
        "password": hash_password("art123"),
        "role": "teacher"
     },
    {
        "username": "mchen",
        "display_name": "Mr. Chen",
        "password": hash_password("chess456"),
        "role": "teacher"
    },
    {
        "username": "principal",
        "display_name": "Principal Martinez",
        "password": hash_password("admin789"),
        "role": "admin"
    }
]

