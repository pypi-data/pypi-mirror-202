#  Copyright (c) 2023 Macrometa Corp All rights reserved.
import json
import os
import threading
import time

from util.db_util import DB

uuid = os.getenv("WORKFLOW_UUID")
state_save_interval = os.getenv("STATE_SAVE_INTERVAL", 60)
state_file_dir = os.getenv("PROJECT_DIR", "/project/eltworkflow")

db = DB(
    user=os.getenv("RDS_USER"),
    password=os.getenv("RDS_PASSWORD"),
    host=os.getenv("RDS_HOST"),
    port=os.getenv("RDS_PORT"),
    database=os.getenv("RDS_DATABASE", "c8cws")
)


def load_state():
    # Read from the db and write the state into state.json file.
    print(f"Loading the state of workflow {uuid} from the database.")
    state_content = db.get_state(uuid)
    if state_content:
        with open(f"{state_file_dir}/state.json", "w") as state_file:
            json.dump(state_content, state_file)


def save_state():
    # Read the state.json file and write the state to the DB.
    print(f"Saving the state of workflow {uuid} to the database.")
    with open(f"{state_file_dir}/state.json", "r") as state_file:
        state_content = json.load(state_file)
        if state_content:
            db.update_state(uuid, state_content)


def start_periodic_save():
    # Save the state periodically
    save_thread = threading.Thread(target=periodic_save_state, args=(state_save_interval,))
    save_thread.daemon = True  # Set as a daemon thread to exit when the main program exits
    save_thread.start()


def periodic_save_state(save_interval_seconds):
    while True:
        save_state()
        time.sleep(save_interval_seconds)
