from calendar import c
from datetime import datetime
from enum import Enum
from pydantic import BaseModel
from typing import List, Optional


class ChatRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    ANALYSIS = "analysis"


class ChatMode(str, Enum):
    BASIC = "basic"
    DETAIL = "reflection"


class ChatHistoryMessage(BaseModel):
    content: str
    role: ChatRole


class ActionType(str, Enum):
    MAPPING_ASSET_OR_ISSUE = "Mapping asset or issue"
    JOINED_A_CAMPAIGN = "Joined a Campaign"
    OTHER_ACTIVITY = "Other Activity"
    REPORTED_ISSUE = "reported issue"
    OLD_REPORT_FOLLOWUP = "Old report followup"
    CREATED_A_CAMPAIGN = "Created a Campaign"
    HANDS_ON = "Hands on"
    TECH_PROTOTYPE = "Tech prototype"
    NON_TECH_PROTOTYPE = "Non tech prototype"
    TECH_SOLUTION = "Tech solution"
    URBAN_PLANNING = "Urban Planning"
    NON_TECH_SOLUTION = "Non tech solution"
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
    CONDUCTED_A_SURVEY_ON_WATER_SUPPLY_SCHEME = (
        "Conducted a Survey on Water Supply Scheme"
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


class ActionSubCategory(str, Enum):
    CIVIC = "Civic"
    PUBLIC_TOILETS = "Public Toilets"
    PUBLIC_ASSET = "Public asset"
    SMART_CITIES = "Smart Cities"
    GOVERNMENT_SCHEMES = "Government Schemes"
    WATER_EFFICIENT_ZONE = "Water efficient zone"
    NOT_APPLICABLE = "Not Applicable"
    PICK_UP_BY_VEHICLE = "Pick up by vehicle"
    PICK_UP_BY_KARAMCHARI = "Pick up by karamchari"
    RELIEF_CENTERS = "Relief Centers"
    HEALTH = "Health"
    DENGUE_HOTSPOT = "Dengue Hotspot"
    WATER_RESOURCES = "Water Resources"
    AUDIT = "Audit"
    NAGARIKA_SAKHI_RURAL_WOMEN_LEADERS_INITIATIVE = (
        "Nagarika Sakhi - Rural Women Leaders Initiative"
    )
    WATER_SOURCES = "Water Sources"
    STREET_LIGHTS = "Street Lights"
    WATER_QUALITY = "Water Quality"
    WATER_TANKERS = "Water Tankers"
    WATERBODY = "Waterbody"
    RECYCLING = "Recycling"
    SOLID_WASTE_MANAGEMENT = "Solid Waste Management"
    GOVERNMENT_INFRASTRUCTURE = "Government Infrastructure"
    RECYCLE_CENTERS = "Recycle Centers"
    GARBAGE_DUMPS = "Garbage Dumps"
    HAZARDOUS_WASTE = "Hazardous Waste"
    SOLID_WASTE_COLLECTION = "Solid Waste Collection"
    SOLID_WASTE_DISPOSAL = "Solid Waste Disposal"
    TREES = "Trees"
    HARASSMENT_ZONE = "Harassment Zone"
    PUBLIC_INSTITUTIONS = "Public Institutions"
    PUBLIC_TRANSPORT = "Public Transport"
    SANITATION_AUDIT = "Sanitation Audit"
    FIREWORKS = "Fireworks"
    CITIZEN_INITIATIVES = "Citizen Initiatives"
    AIR_QUALITY = "Air Quality"
    CIVIC_ENVIRONMENTAL_DATA = "Civic-Environmental Data"
    SANITATION = "Sanitation"
    ELECTRICITY = "Electricity"
    CROWDSOURCED_DATA = "Crowdsourced Data"
    COMMUNITY_BUILDING = "Community Building"
    TRAFFIC_ROAD = "Traffic/road"
    POLICY = "Policy"
    TRAFFIC_AND_MOBILITY = "Traffic & Mobility"
    CAUVERY_WATER_POLICY = "Cauvery Water Policy"
    WATER_SUPPLY_SCHEME_AUDIT = "Water Supply Scheme Audit"
    GARBAGE_BIN = "Garbage Bin"
    BOREWELL = "Borewell"
    BLACK_SPOT_FIXED_AND_MAINTAINED = "Black Spot Fixed and Maintained"
    RAINFALL = "Rainfall"
    STREET_AUDIT = "Street audit"
    FLOOD_MAP = "Flood map"
    UPCYCLE = "Upcycle"
    PUBLIC_PARK = "Public Park"
    WASTE = "Waste"
    URBAN_FLOODING = "Urban Flooding"
    STUBBLE_BURNING = "Stubble Burning"
    ANGANWADI_CENTRE = "Anganwadi centre"
    POTHOLE_LOWER = "pothole"
    LIVELIHOOD = "Livelihood"
    HEALTHCARE = "healthcare"
    POTHOLE = "Pothole"
    URBAN_GREENERY = "Urban Greenery"
    SCHEMES = "Schemes"
    AIR = "Air"
    TREE_TRACKING = "Tree Tracking"
    ALL_IN_ONE_SERVICE_CENTRE = "All in One Service Centre"
    COVID = "COVID"
    MALARIA_HOTSPOT = "Malaria Hotspot"
    WATER = "Water"
    OTHER = "Other"

    def __str__(self):
        return self.value

    def __eq__(self, other):
        if isinstance(other, ActionSubCategory):
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
    user_message: str


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
    relevance: Optional[str] = None
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
    subcategory: Optional[str] = None
    subtype: Optional[str] = None
    type: Optional[str] = None
    skills: Optional[List[ActionSkill]] = None


class AIActionMetadataResponse(BaseModel):
    action_title: str
    action_description: str
    action_type: str
    action_category: str
    action_subcategory: str
    action_subtype: str
    skills: List[ActionSkill]


class AIUpdateActionMetadataResponse(AIActionMetadataResponse):
    has_changed: bool


class BasicActionChatRequest(BaseModel):
    action_uuid: str
    last_user_message: str


class DetailActionChatRequest(BaseModel):
    action_uuid: str
    last_user_message: str


class AIChatResponse(BaseModel):
    chain_of_thought: str
    response: str
    is_done: bool


class CreateActionResponse(BaseModel):
    ai_response: AIChatResponse
    action: Action
