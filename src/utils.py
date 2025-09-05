from models import ActionType

skill_to_name = {
    "citizenship": "Citizenship",
    "communication": "Communication",
    "community_collaboration": "Community Collaboration",
    "critical_thinking": "Critical Thinking",
    "data_orientation": "Data Orientation",
    "applied_empathy": "Applied Empathy",
    "grit": "Grit",
    "hands_on": "Hands on",
    "problem_solving": "Problem Solving",
    "entrepreneurial": "Entrepreneurial",
    "try_new_things": "Try New Things",
}


def extract_skill_from_action_type(action_type: ActionType) -> str:
    skills = []

    # Attended an offline event
    if action_type == ActionType.ATTENDED_AN_OFFLINE_EVENT:
        skills.extend(["communication", "community_collaboration"])

    # Business plan
    elif action_type == ActionType.BUSINESS_PLAN:
        skills.extend(
            [
                "communication",
                "critical_thinking",
                "problem_solving",
                "entrepreneurial",
                "try_new_things",
            ]
        )

    # Carry a cloth bag
    elif action_type == ActionType.CARRY_A_CLOTH_BAG:
        skills.extend(["problem_solving", "citizenship", "hands_on"])

    # Created a Campaign
    elif action_type == ActionType.CREATED_A_CAMPAIGN:
        skills.extend(["communication", "data_orientation", "community_collaboration"])

    elif action_type == "Campaign":
        skills.extend(["communication", "community_collaboration"])

    # Created solution
    elif action_type == ActionType.CREATED_SOLUTION:
        skills.extend(["critical_thinking", "problem_solving", "grit", "hands_on"])

    # Crowdsourced data
    elif action_type == ActionType.CROWDSOURCED_DATA:
        skills.extend(
            [
                "communication",
                "applied_empathy",
                "citizenship",
                "data_orientation",
                "community_collaboration",
            ]
        )

    # Did audit or investigated
    elif action_type == ActionType.DID_AUDIT_OR_INVESTIGATED:
        skills.extend(["communication", "critical_thinking", "data_orientation"])

    # Engaged people through sessions
    elif action_type == ActionType.ENGAGED_PEOPLE_THROUGH_SESSIONS:
        skills.extend(["communication", "applied_empathy", "community_collaboration"])

    # Followed up
    elif action_type == ActionType.FOLLOWED_UP:
        skills.extend(["communication", "grit"])

    # Implemented existing solution
    elif action_type == ActionType.IMPLEMENTED_EXISTING_SOLUTION:
        skills.extend(["critical_thinking", "hands_on"])

    # Joined a Campaign
    elif action_type == ActionType.JOINED_A_CAMPAIGN:
        skills.extend(["community_collaboration"])

    # Non tech prototype
    elif action_type == ActionType.NON_TECH_PROTOTYPE:
        skills.extend(["critical_thinking", "entrepreneurial", "hands_on"])

    # Non tech solution
    elif action_type == ActionType.NON_TECH_SOLUTION:
        skills.extend(["critical_thinking", "problem_solving", "hands_on"])

    # Old report followup
    elif action_type == ActionType.OLD_REPORT_FOLLOWUP:
        skills.extend(["communication", "grit"])

    # Project idea
    elif action_type == ActionType.PROJECT_IDEA:
        skills.extend(
            ["communication", "problem_solving", "try_new_things", "applied_empathy"]
        )

    # Prototype
    elif action_type == ActionType.PROTOTYPE:
        skills.extend(
            [
                "communication",
                "critical_thinking",
                "problem_solving",
                "try_new_things",
                "grit",
            ]
        )

    # Reported issue
    elif action_type == ActionType.REPORTED_ISSUE:
        skills.extend(["citizenship", "data_orientation"])

    elif action_type == "Report":
        skills.extend(["citizenship", "data_orientation"])

    # Segregate waste at source
    elif action_type == ActionType.SEGREGATE_WASTE_AT_SOURCE:
        skills.extend(["problem_solving", "citizenship", "hands_on"])

    # Shared Public Opinion
    elif action_type == ActionType.SHARED_PUBLIC_OPINION:
        skills.extend(["citizenship"])

    # Solved a real world problem
    elif action_type == ActionType.SOLVED_A_REAL_WORLD_PROBLEM:
        skills.extend(["problem_solving", "applied_empathy", "citizenship"])

    # Sustainable Lifestyle
    elif action_type == ActionType.SUSTAINABLE_LIFESTYLE:
        skills.extend(["critical_thinking", "problem_solving"])

    # Swachhata League Participation 2023
    elif action_type == ActionType.SWACHHATA_LEAGUE_PARTICIPATION_2023:
        skills.extend(["problem_solving", "citizenship", "hands_on"])

    # Tech prototype
    elif action_type == ActionType.TECH_PROTOTYPE:
        skills.extend(["critical_thinking", "entrepreneurial", "grit", "hands_on"])

    # Tech solution
    elif action_type == ActionType.TECH_SOLUTION:
        skills.extend(["critical_thinking", "problem_solving", "hands_on"])

    # Mapping asset or issue
    elif action_type == ActionType.MAPPING_ASSET_OR_ISSUE:
        skills.extend(["problem_solving", "data_orientation"])

    # Investigation/Audit
    elif action_type == ActionType.INVESTIGATION_AUDIT:
        skills.extend(["critical_thinking", "data_orientation"])

    # Session Taken
    elif action_type == ActionType.SESSION_TAKEN:
        skills.extend(["communication", "citizenship", "community_collaboration"])

    # Street Cleanliness check
    elif action_type == ActionType.STREET_CLEANLINESS_CHECK:
        skills.extend(["citizenship", "hands_on"])

    # Regular waste pick up
    elif action_type == ActionType.REGULAR_WASTE_PICK_UP:
        skills.extend(["hands_on", "citizenship"])

    # Meet your Safai Karamchari
    elif action_type == ActionType.MEET_YOUR_SAFAI_KARAMCHARI:
        skills.extend(["applied_empathy", "communication"])

    # Community engagement
    elif action_type == ActionType.COMMUNITY_ENGAGEMENT:
        skills.extend(["community_collaboration", "communication", "citizenship"])

    # Conducted a Survey on Water Supply Scheme
    elif action_type == ActionType.CONDUCTED_A_SURVEY_ON_WATER_SUPPLY_SCHEME:
        skills.extend(["data_orientation", "communication", "critical_thinking"])

    # Cloth Collection
    elif action_type == ActionType.CLOTH_COLLECTION:
        skills.extend(["hands_on", "applied_empathy"])

    # Hands on (this is an ActionType, not just a skill)
    elif action_type == ActionType.HANDS_ON:
        skills.extend(["hands_on", "problem_solving"])

    # Urban Flooding (mapped to URBAN_FLOODING instead of URBAN_PLANNING)
    elif action_type == ActionType.URBAN_FLOODING:
        skills.extend(["data_orientation", "problem_solving"])

    # Keep URBAN_PLANNING separate if it exists
    elif action_type == ActionType.URBAN_PLANNING:
        skills.extend(["data_orientation", "problem_solving"])

    # Investigation/Audit - keep the old AUDIT mapping for backwards compatibility
    elif action_type == ActionType.AUDIT:
        skills.extend(["critical_thinking", "data_orientation"])

    # For events not directly mapped in CSV, map to OTHER_ACTIVITY with general skills
    elif action_type == ActionType.OTHER_ACTIVITY:
        # This could be Session Taken, Street Cleanliness check, Regular waste pick up,
        # Meet your Safai Karamchari, Community engagement, Conducted a Survey, Cloth Collection, etc.
        # Using a general mapping for hands_on activities
        skills.extend(["hands_on", "problem_solving"])

    # For CHANGEMAKER_ADDA and SHARING_ADDA (not in CSV, keeping original logic)
    elif action_type in [ActionType.CHANGEMAKER_ADDA, ActionType.SHARING_ADDA]:
        skills.extend(["citizenship"])

    return skills
