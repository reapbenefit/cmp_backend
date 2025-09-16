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

skill_to_microskills = {
    "data_orientation": [
        {
            "level": "L1",
            "microskill": "Using Data Tools",
            "description": "Uses simple forms or tools to collect information.",
        },
        {
            "level": "L2",
            "microskill": "Reading Reports",
            "description": "Understands and learns from existing data and reports.",
        },
        {
            "level": "L3",
            "microskill": "Analyzing Data",
            "description": "Finds patterns or key points in information.",
        },
        {
            "level": "L4",
            "microskill": "Creating Data Tools",
            "description": "Designs ways to collect new information.",
        },
        {
            "level": "L5",
            "microskill": "Insight & Strategy Design",
            "description": "Uses insights from data to plan bigger actions.",
        },
    ],
    "hands_on": [
        {
            "level": "L1",
            "microskill": "Basic Tool Use",
            "description": "Handles everyday tools safely and confidently.",
        },
        {
            "level": "L2",
            "microskill": "Simple Repairs",
            "description": "Fixes or sets up basic items.",
        },
        {
            "level": "L3",
            "microskill": "Solution Installation",
            "description": "Sets up and installs working solutions.",
        },
        {
            "level": "L4",
            "microskill": "Prototype Building",
            "description": "Creates test versions of new ideas.",
        },
        {
            "level": "L5",
            "microskill": "Final Product Design",
            "description": "Builds and completes fully working solutions.",
        },
    ],
    "citizenship": [
        {
            "level": "L1",
            "microskill": "Local Awareness",
            "description": "Knows the area and notices community issues.",
        },
        {
            "level": "L2",
            "microskill": "Regular Reporting",
            "description": "Reports and follows up on problems often.",
        },
        {
            "level": "L3",
            "microskill": "Joining Campaigns",
            "description": "Participates actively in campaigns or projects.",
        },
        {
            "level": "L4",
            "microskill": "Leading Campaigns",
            "description": "Starts and leads new community actions.",
        },
        {
            "level": "L5",
            "microskill": "Policy Engagement",
            "description": "Works with decision-makers to create bigger change.",
        },
    ],
    "problem_solving": [
        {
            "level": "L1",
            "microskill": "Problem Awareness",
            "description": "Notices and understands challenges.",
        },
        {
            "level": "L2",
            "microskill": "Research & Plan",
            "description": "Finds information and makes a plan.",
        },
        {
            "level": "L3",
            "microskill": "Structured Execution",
            "description": "Follows clear steps to solve problems.",
        },
        {
            "level": "L4",
            "microskill": "Trigger Mapping for Solution Design",
            "description": "Understands stakeholders’ behaviour using trigger mapping and designs solutions accordingly.",
        },
        {
            "level": "L5",
            "microskill": "Prototyping & Iterating Solutions",
            "description": "Builds test versions of solutions, gathers feedback, and improves them.",
        },
    ],
    "communication": [
        {
            "level": "L1",
            "microskill": "Clear Instructions",
            "description": "Explains tasks simply and clearly.",
        },
        {
            "level": "L2",
            "microskill": "Group Facilitation",
            "description": "Guides group discussions to make decisions.",
        },
        {
            "level": "L3",
            "microskill": "Compelling Storytelling",
            "description": "Shares stories that inspire and connect.",
        },
        {
            "level": "L4",
            "microskill": "Interactive Facilitation",
            "description": "Runs engaging activities for participation.",
        },
        {
            "level": "L5",
            "microskill": "Mobilizing People",
            "description": "Inspires and organizes large groups to take action.",
        },
    ],
    "critical_thinking": [
        {
            "level": "L1",
            "microskill": "Identifying Issues",
            "description": "Spots problems or gaps.",
        },
        {
            "level": "L2",
            "microskill": "Breaking Down Steps",
            "description": "Splits problems into smaller actions.",
        },
        {
            "level": "L3",
            "microskill": "Contextual Thinking",
            "description": "Adapts ideas to fit the situation.",
        },
        {
            "level": "L4",
            "microskill": "Questioning Assumptions",
            "description": "Challenges ideas to make them stronger.",
        },
        {
            "level": "L5",
            "microskill": "Future Planning",
            "description": "Thinks ahead and prepares for possible outcomes.",
        },
    ],
    "community_collaboration": [
        {
            "level": "L1",
            "microskill": "Knowing Who to Work With",
            "description": "Identifies people or groups who can help.",
        },
        {
            "level": "L2",
            "microskill": "Stakeholder Outreach",
            "description": "Connects with key people for the project.",
        },
        {
            "level": "L3",
            "microskill": "Co-Creation",
            "description": "Works together to make solutions.",
        },
        {
            "level": "L4",
            "microskill": "Coordinating Campaigns",
            "description": "Brings people together for joint action.",
        },
        {
            "level": "L5",
            "microskill": "Designing & Leading Campaigns",
            "description": "Creates and guides large group projects.",
        },
    ],
    "grit": [
        {
            "level": "L1",
            "microskill": "Sustaining Interest",
            "description": "Stays focused on an idea or cause.",
        },
        {
            "level": "L2",
            "microskill": "Committed Execution",
            "description": "Works steadily even on routine tasks.",
        },
        {
            "level": "L3",
            "microskill": "Consistent Follow-up",
            "description": "Checks in regularly to keep progress on track.",
        },
        {
            "level": "L4",
            "microskill": "Working with Multiple Stakeholders",
            "description": "Engages different people to keep things moving.",
        },
        {
            "level": "L5",
            "microskill": "Persistent Leadership",
            "description": "Leads and motivates others over the long term.",
        },
    ],
    "applied_empathy": [
        {
            "level": "L1",
            "microskill": "Respectful Conduct",
            "description": "Treats everyone kindly and fairly.",
        },
        {
            "level": "L2",
            "microskill": "Emotional Awareness",
            "description": "Thinks about how actions make others feel.",
        },
        {
            "level": "L3",
            "microskill": "Active Listening",
            "description": "Makes sure everyone is heard and understood.",
        },
        {
            "level": "L4",
            "microskill": "Conflict Resolution",
            "description": "Helps solve disagreements peacefully.",
        },
        {
            "level": "L5",
            "microskill": "Inclusive Decision-Making",
            "description": "Ensures all voices are part of final choices.",
        },
    ],
    "entrepreneurial": [
        {
            "level": "L1",
            "microskill": "Idea Generation",
            "description": "Comes up with creative ideas.",
        },
        {
            "level": "L2",
            "microskill": "Action Planning",
            "description": "Makes step-by-step plans to act.",
        },
        {
            "level": "L3",
            "microskill": "Feedback Application",
            "description": "Uses feedback to make things better.",
        },
        {
            "level": "L4",
            "microskill": "Team Coordination",
            "description": "Organizes and supports a team’s work.",
        },
        {
            "level": "L5",
            "microskill": "Delivering Outcomes",
            "description": "Finishes projects and achieves goals.",
        },
    ],
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
