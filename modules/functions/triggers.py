# modules/functions/triggers.py

from googleapiclient.discovery import build

from auth.credentials import load_credentials
from utils import print_helpers as ph

def functions_list_triggers(project_id, function_name):

    def print_function_triggers(function):
        ph.green(f"Function: {function['name'].split('/')[-1]}")
        
        trigger = function.get('eventTrigger', None)
        if not trigger:
            print("   - No Trigger Found.")
            print()
            return

        print(f"   - Trigger: {trigger.get('trigger', 'Null')}")
        print(f"   - Trigger Region: {trigger.get('triggerRegion', 'Null')}")
        print(f"   - Event Type: {trigger.get('eventType', 'Null')}")
        print(f"   - Pubsub Topic: {trigger.get('pubsubTopic', 'Null')}")
        print(f"   - Service Account Email: {trigger.get('serviceAccountEmail', 'Null')}")
        print(f"   - Retry Policy: {trigger.get('retryPolicy', 'Null')}")

        event_filters = trigger.get('eventFilters', [])
        for i, event_filter in enumerate(event_filters):
            print(f"   - Event Filter {i+1}:")
            print(f"     - Attribute: {event_filter.get('attribute', 'Null')}")
            print(f"     - Value: {event_filter.get('value', 'Null')}")

        print(f"   - Channel: {trigger.get('channel', 'Null')}")
        print()

    try: 
        creds = load_credentials()
        if creds is None:
            # ph.print_error("Failed to load credentials. Exiting.")
            return        
        service = build('cloudfunctions', 'v2', credentials=creds)
        parent = f'projects/{project_id}/locations/-'
        response = service.projects().locations().functions().list(parent=parent).execute()
        functions = response.get('functions', [])

        if not functions:
            ph.print_info(f"No Cloud Functions found in the project {project_id}!.\n")
        else:
            if function_name:
                function = next((f for f in functions if f['name'].split('/')[-1] == function_name), None)
                if function:
                    print(f"\n(+) Listing triggers for Function {function_name} in Project {project_id}\n")
                    print_function_triggers(function)
                else:
                    ph.print_info(f"Function {function_name} not found in project {project_id}.\n")
            else:
                print(f"\n(+) Listing triggers for all Functions in Project {project_id}\n")
                for function in functions:
                    print_function_triggers(function)
    except Exception as ex:
        ph.print_error("{}".format(ex))
        print()