import asana
import sys
import os

token = os.environ.get("ASANA_TOKEN")
client = asana.Client.access_token(token)

ws_id = sys.argv[1]
project_id = sys.argv[2]
task = sys.argv[3]
user_id = client.users.me()['id']

client.tasks.create_in_workspace(int(ws_id), {
    "name": task,
    "assignee": int(user_id),
    "projects": [int(project_id)]
})

print("Asana task added.")
