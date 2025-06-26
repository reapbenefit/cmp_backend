import os
from os.path import exists


if exists("/appdata"):
    data_root_dir = "/appdata"
else:
    root_dir = os.path.dirname(os.path.abspath(__file__))
    data_root_dir = f"{root_dir}/db"

if not exists(data_root_dir):
    os.makedirs(data_root_dir)


sqlite_db_path = f"{data_root_dir}/db.sqlite"

chat_history_table_name = "chat_history"
sessions_table_name = "sessions"
users_table_name = "users"
communities_table_name = "communities"
actions_table_name = "actions"
action_categories_table_name = "action_categories"
action_types_table_name = "action_types"
skills_table_name = "skills"
action_skills_table_name = "action_skills"
