from datetime import datetime
from enum import Enum
from pydantic import BaseModel
from typing import List, Optional


class ChatRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    ANALYSIS = "analysis"


class ChatResponse(BaseModel):
    content: str
    role: ChatRole


class ActionType(str, Enum):
    MAPPING_ASSET_OR_ISSUE = "Mapping asset or issue"
    JOINED_A_CAMPAIGN = "Joined a Campaign"
    OTHER_ACTIVITY = "Other Activity"
    REPORTED_ISSUE = "reported issue"
    OLD_REPORT_FOLLOWUP = "Old report followup"
    CAMPAIGN = "Campaign"
    CREATED_A_CAMPAIGN = "Created a Campaign"
    HANDS_ON = "Hands on"
    TECH_PROTOTYPE = "Tech prototype"
    NON_TECH_PROTOTYPE = "Non tech prototype"
    TECH_SOLUTION = "Tech solution"
    URBAN_PLANNING = "Urban Planning"
    NON_TECH_SOLUTION = "Non tech solution"
    MAPPING_ASSET_OR_ISSUE_ALT = "Mapping assest or issue"
    CROWDSOURCED_DATA = "Crowdsourced data"
    SESSION_TAKEN = "Session Taken"
    STREET_CLEANLINESS_CHECK = "Street Cleanliness check"
    REGULAR_WASTE_PICK_UP = "Regular waste pick up"
    MEET_YOUR_SAFAI_KARAMCHARI = "Meet your Safai Karamchari"
    SHARING_ADDA = "Sharing Adda"
    CHANGEMAKER_ADDA = "Changemaker Adda"
    COMMUNITY_ENGAGEMENT = "Community engagement"
    PROJECT_IDEA = "Project idea"
    BUSINESS_PLAN = "Business plan"
    PROTOTYPE = "Prototype"
    AUDIT = "Audit"
    SUSTAINABLE_LIFESTYLE = "Sustainable Lifestyle"
    CONDUCTED_A_SURVEY_ION_WATER_SUPPLY_SCHEME = (
        "Conducted a Survey ion Water Supply Scheme"
    )
    URBAN_FLOODING = "Urban Flooding"
    CLOTH_COLLECTION = "Cloth Collection"
    SWACHHATA_LEAGUE_PARTICIPATION_2023 = "Swachhata League Participation 2023"
    CARRY_A_CLOTH_BAG = "Carry a cloth bag"
    SEGREGATE_WASTE_AT_SOURCE = "Segregate waste at source"
    ATTENDED_AN_OFFLINE_EVENT = "Attended an offline event"
    SHARED_PUBLIC_OPINION = "Shared Public Opinion"
    FOLLOWED_UP = "followed up"
    IMPLEMENTED_EXISTING_SOLUTION = "implemented existing solution"
    CREATED_SOLUTION = "created solution"
    SOLVED_A_REAL_WORLD_PROBLEM = "solved a real world problem"
    ENGAGED_PEOPLE_THROUGH_SESSIONS = "engaged people through sessions"
    INVESTIGATION_AUDIT = "Investigation/Audit"
    DID_AUDIT_OR_INVESTIGATED = "did audit or investigated"

    def __str__(self):
        return self.value

    def __eq__(self, other):
        if isinstance(other, ActionType):
            return self.value == other.value

        if isinstance(other, str):
            return self.value == other

        return False


class ActionCategory(str, Enum):
    CIVIC = "Civic"
    RELIEF_CENTERS = "Relief Centers"
    HEALTH = "Health"
    AUDIT = "Audit"
    STREET_LIGHTS = "Street Lights"
    WATER_RESOURCES = "Water Resources"
    FLOODS = "Floods"
    TREE_TRACKING = "Tree Tracking"
    STUBBLE_BURNING = "Stubble Burning"
    RAINFALL = "Rainfall"
    BOREWELL = "Borewell"
    PUBLIC_PARK = "Public Park"
    SOLID_WASTE_MANAGEMENT = "Solid Waste Management"
    RECYCLING = "Recycling"
    GARBAGE_DUMPS = "Garbage Dumps"
    HAZARDOUS_WASTE = "Hazardous Waste"
    SOLID_WASTE_COLLECTION = "Solid Waste Collection"
    ANGANWADI_CENTRE = "Anganwadi centre"
    SOLID_WASTE_DISPOSAL = "Solid Waste Disposal"
    HARASSMENT_ZONE = "Harassment Zone"
    POLICY = "Policy"
    PUBLIC_INSTITUTIONS = "Public Institutions"
    GOVERNMENT_INFRASTRUCTURE = "Government Infrastructure"
    CIVIC_ENVIRONMENTAL_DATA = "Civic-Environmental Data"
    CITIZEN_INITIATIVES = "Citizen Initiatives"
    STREET_AUDIT = "Street audit"
    AIR_QUALITY = "Air Quality"
    COMMUNITY_BUILDING = "Community Building"
    SCHEMES = "Schemes"
    PUBLIC_ASSET = "Public asset"
    CROWDSOURCED_DATA = "Crowdsourced Data"
    WATER = "Water"
    WASTE = "Waste"
    TRAFFIC_ROAD = "Traffic/road"
    SANITATION = "Sanitation"
    ELECTRICITY = "Electricity"
    AIR = "Air"
    OTHER = "Other"
    LIVELIHOOD = "Livelihood"

    def __str__(self):
        return self.value

    def __eq__(self, other):
        if isinstance(other, ActionCategory):
            return self.value == other.value

        if isinstance(other, str):
            return self.value == other

        return False


class LoginRequest(BaseModel):
    email: str
    password: str


class BaseUser(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: str


class SignupUserRequest(BaseUser):
    password: str


class User(BaseUser):
    id: int


class UserCommunity(BaseModel):
    id: int
    name: str
    description: str
    link: str | None = None


class CreateCommunityRequest(BaseModel):
    name: str
    description: str
    link: str | None = None
    user_id: int


class UpdateUserProfileRequest(BaseModel):
    bio: str | None = None
    location_state: str | None = None
    location_city: str | None = None


class CreateActionRequest(BaseModel):
    user_id: int
    title: str | None = None
    user_message: str | None = None


class AddChatMessageRequest(BaseModel):
    role: ChatRole
    content: str
    response_type: str


class ChatMessage(AddChatMessageRequest):
    id: int
    created_at: datetime


class ChatSession(BaseModel):
    uuid: str
    title: str
    last_message_time: datetime


class Skill(BaseModel):
    id: int
    name: str
    label: str


class SkillHistoryEvent(BaseModel):
    action_title: str
    summary: str


class SkillHistory(Skill):
    history: List[SkillHistoryEvent]


class ActionSkill(Skill):
    relevance: str
    response: Optional[str] = None


class Action(BaseModel):
    id: int
    uuid: str
    title: str | None = None
    description: str | None = None
    status: Optional[str] = None
    is_verified: bool
    is_pinned: Optional[bool] = None
    category: Optional[str] = None
    type: Optional[str] = None
    created_at: datetime
    skills: Optional[List[ActionSkill]] = None
    chat_history: Optional[List[ChatMessage]] = None


class Portfolio(User):
    is_verified: bool
    bio: str | None = None
    location_state: str | None = None
    location_city: str | None = None
    location_country: str | None = None
    highlight: str | None = None
    communities: List[UserCommunity] | None = None
    actions: List[Action] | None = None
    skills: List[SkillHistory] | None = None


class UpdateActionRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    status: Optional[str] = None
    category: Optional[str] = None
    type: Optional[str] = None
    skills: Optional[List[ActionSkill]] = None


class AIActionMetadataResponse(BaseModel):
    action_title: str
    action_description: str
    action_type: str
    action_category: str
    skills: List[ActionSkill]


class AIChatResponse(BaseModel):
    response: str
    is_done: bool
