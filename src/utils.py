from models import ActionType

skill_to_name = {
    "citizenship": "Citizenship",
    "communication": "Communication",
    "community_collaboration": "Community Collaboration",
    "critical_thinking": "Critical Thinking",
    "data_digital_citizenship": "Data Orientation",
    "empathy": "Applied Empathy",
    "grit": "Grit",
    "hands_on": "Hands-On",
    "problem_solving": "Problem Solving",
    "entrepreneurial": "Entrepreneurial",
}


def extract_skill_from_action_type(action_type: ActionType) -> str:
    skills = []

    if action_type in [
        ActionType.MAPPING_ASSET_OR_ISSUE_ALT,
        ActionType.REPORTED_ISSUE,
        ActionType.SOLVED_A_REAL_WORLD_PROBLEM,
        ActionType.SHARED_PUBLIC_OPINION,
        ActionType.SEGREGATE_WASTE_AT_SOURCE,
        ActionType.CARRY_A_CLOTH_BAG,
        ActionType.SWACHHATA_LEAGUE_PARTICIPATION_2023,
        ActionType.OTHER_ACTIVITY,
        ActionType.CROWDSOURCED_DATA,
        ActionType.CHANGEMAKER_ADDA,
        ActionType.SHARING_ADDA,
        ActionType.URBAN_PLANNING,
    ]:
        skills.append("citizenship")

    if action_type in [
        ActionType.ENGAGED_PEOPLE_THROUGH_SESSIONS,
        ActionType.FOLLOWED_UP,
        ActionType.CROWDSOURCED_DATA,
        ActionType.OLD_REPORT_FOLLOWUP,
        ActionType.CREATED_A_CAMPAIGN,
        ActionType.DID_AUDIT_OR_INVESTIGATED,
        ActionType.ATTENDED_AN_OFFLINE_EVENT,
        ActionType.PROTOTYPE,
        ActionType.PROJECT_IDEA,
        ActionType.BUSINESS_PLAN,
    ]:
        skills.append("communication")

    if action_type in [
        ActionType.CREATED_A_CAMPAIGN,
        ActionType.JOINED_A_CAMPAIGN,
        ActionType.CROWDSOURCED_DATA,
        ActionType.ENGAGED_PEOPLE_THROUGH_SESSIONS,
        ActionType.ATTENDED_AN_OFFLINE_EVENT,
    ]:
        skills.append("community_collaboration")

    if action_type in [
        ActionType.TECH_PROTOTYPE,
        ActionType.NON_TECH_PROTOTYPE,
        ActionType.TECH_SOLUTION,
        ActionType.NON_TECH_SOLUTION,
        ActionType.IMPLEMENTED_EXISTING_SOLUTION,
        ActionType.DID_AUDIT_OR_INVESTIGATED,
        ActionType.CREATED_SOLUTION,
        ActionType.SUSTAINABLE_LIFESTYLE,
        ActionType.PROTOTYPE,
        ActionType.PROJECT_IDEA,
        ActionType.BUSINESS_PLAN,
    ]:
        skills.append("critical_thinking")

    if action_type in [
        ActionType.CROWDSOURCED_DATA,
        ActionType.MAPPING_ASSET_OR_ISSUE_ALT,
        ActionType.CREATED_A_CAMPAIGN,
        ActionType.DID_AUDIT_OR_INVESTIGATED,
        ActionType.REPORTED_ISSUE,
        ActionType.AUDIT,
    ]:
        skills.append("data_digital_citizenship")

    if action_type in [
        ActionType.CROWDSOURCED_DATA,
        ActionType.MAPPING_ASSET_OR_ISSUE_ALT,
        ActionType.ENGAGED_PEOPLE_THROUGH_SESSIONS,
        ActionType.SOLVED_A_REAL_WORLD_PROBLEM,
        ActionType.PROJECT_IDEA,
    ]:
        skills.append("empathy")

    if action_type in [
        ActionType.TECH_PROTOTYPE,
        ActionType.NON_TECH_PROTOTYPE,
        ActionType.OLD_REPORT_FOLLOWUP,
        ActionType.CREATED_SOLUTION,
        ActionType.FOLLOWED_UP,
        ActionType.PROTOTYPE,
    ]:
        skills.append("grit")

    if action_type in [
        ActionType.TECH_PROTOTYPE,
        ActionType.NON_TECH_PROTOTYPE,
        ActionType.TECH_SOLUTION,
        ActionType.NON_TECH_SOLUTION,
        ActionType.IMPLEMENTED_EXISTING_SOLUTION,
        ActionType.CREATED_SOLUTION,
        ActionType.SEGREGATE_WASTE_AT_SOURCE,
        ActionType.CARRY_A_CLOTH_BAG,
        ActionType.SWACHHATA_LEAGUE_PARTICIPATION_2023,
        ActionType.OTHER_ACTIVITY,
    ]:
        skills.append("hands_on")

    if action_type in [
        ActionType.CREATED_SOLUTION,
        ActionType.TECH_SOLUTION,
        ActionType.NON_TECH_SOLUTION,
        ActionType.SOLVED_A_REAL_WORLD_PROBLEM,
        ActionType.SEGREGATE_WASTE_AT_SOURCE,
        ActionType.CARRY_A_CLOTH_BAG,
        ActionType.SWACHHATA_LEAGUE_PARTICIPATION_2023,
        ActionType.OTHER_ACTIVITY,
        ActionType.SUSTAINABLE_LIFESTYLE,
        ActionType.PROTOTYPE,
        ActionType.PROJECT_IDEA,
        ActionType.BUSINESS_PLAN,
    ]:
        skills.append("problem_solving")

    if action_type in [
        ActionType.TECH_PROTOTYPE,
        ActionType.NON_TECH_PROTOTYPE,
        ActionType.BUSINESS_PLAN,
    ]:
        skills.append("entrepreneurial")

    return skills
