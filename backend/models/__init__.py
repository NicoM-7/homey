from .user import User
from .property import Property
from .property_image import PropertyImage
from .group import Group
from .group_participant import GroupParticipant
from .conversation import Conversation
from .participant import Participant
from .message import Message
from .profile import Profile
from .expense import Expense
from .calendar_event import CalendarEvent
from .chore import Chore
from .review import Review
from .list import List
from .item import Item
from .inventory import Inventory
from .store import Store
from db import db

# === Set up relationships ===

# User - Property
User.properties = db.relationship("Property", back_populates="landlord", cascade="all, delete-orphan")
Property.landlord = db.relationship("User", back_populates="properties")

# Property - PropertyImage
Property.images = db.relationship("PropertyImage", back_populates="property", cascade="all, delete-orphan")
PropertyImage.property = db.relationship("Property", back_populates="images")

# User - Group (as landlord)
User.groups = db.relationship("Group", back_populates="landlord", cascade="all, delete-orphan")
Group.landlord = db.relationship("User", back_populates="groups")

# Property - Group
Property.groups = db.relationship("Group", back_populates="property", cascade="all, delete-orphan")
Group.property = db.relationship("Property", back_populates="groups")

# Group <-> User many-to-many
Group.participants = db.relationship("User", secondary="group_participant", back_populates="joined_groups")
User.joined_groups = db.relationship("Group", secondary="group_participant", back_populates="participants")

# User - Message
User.messages = db.relationship("Message", back_populates="user", cascade="all, delete-orphan")
Message.user = db.relationship("User", back_populates="messages")

# Group - Conversation
Group.conversations = db.relationship("Conversation", back_populates="group", cascade="all, delete-orphan")
Conversation.group = db.relationship("Group", back_populates="conversations")

# Conversation - Message
Conversation.messages = db.relationship("Message", back_populates="conversation", cascade="all, delete-orphan")
Message.conversation = db.relationship("Conversation", back_populates="messages")

# Conversation - Participant
Conversation.participants = db.relationship("Participant", back_populates="conversation", cascade="all, delete-orphan")
Participant.conversation = db.relationship("Conversation", back_populates="participants")

# User - Participant
User.participants = db.relationship("Participant", back_populates="user", cascade="all, delete-orphan")
Participant.user = db.relationship("User", back_populates="participants")

# Group - Expense
Group.expenses = db.relationship("Expense", back_populates="group", cascade="all, delete-orphan")
Expense.group = db.relationship("Group", back_populates="expenses")

# User - Expense (paidBy / owedTo)
User.expenses_paid_by = db.relationship("Expense", foreign_keys="[Expense.paid_by]", back_populates="paid_by_user")
User.expenses_owed_to = db.relationship("Expense", foreign_keys="[Expense.owed_to]", back_populates="owed_to_user")
Expense.paid_by_user = db.relationship("User", foreign_keys="[Expense.paid_by]", back_populates="expenses_paid_by")
Expense.owed_to_user = db.relationship("User", foreign_keys="[Expense.owed_to]", back_populates="expenses_owed_to")

# User - Chore
User.assigned_chores = db.relationship("Chore", back_populates="assignee", cascade="all, delete-orphan")
Chore.assignee = db.relationship("User", back_populates="assigned_chores")

# Group - Chore
Group.chores = db.relationship("Chore", back_populates="group", cascade="all, delete-orphan")
Chore.group = db.relationship("Group", back_populates="chores")

Group.events = db.relationship("CalendarEvent", back_populates="group", cascade="all, delete-orphan")
CalendarEvent.group = db.relationship("Group", back_populates="events")

# Group - Profile
Group.profiles = db.relationship("Profile", back_populates="group", cascade="all, delete-orphan")
Profile.group = db.relationship("Group", back_populates="profiles")

# Group - List
Group.lists = db.relationship("List", back_populates="group", cascade="all, delete-orphan")
List.group = db.relationship("Group", back_populates="lists")

# Group - Inventory
Group.inventories = db.relationship("Inventory", back_populates="group", cascade="all, delete-orphan")
Inventory.group = db.relationship("Group", back_populates="inventories")

__all__ = [
    "User", "Property", "PropertyImage", "Group", "GroupParticipant", "Conversation", "Participant", "Message",
    "Profile", "Expense", "CalendarEvent", "Chore", "Review", "List", "Item", "Inventory", "Store"
]