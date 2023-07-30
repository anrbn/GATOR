# gator/services/functions/triggers.py

from googleapiclient.discovery import build
from gator.auth.credentials import load_credentials

import gator.helpers.print_helper as ph

def list_triggers(args):
    creds = load_credentials(args)
    service = build('cloudfunctions', 'v2', credentials=creds)
    parent = f'projects/{args.project_id}/locations/-'
    response = service.projects().locations().functions().list(parent=parent).execute()
    functions = response.get('functions', [])

    if not functions:
        ph.yellow(f"\n[!] No Cloud Functions found in the project {args.project_id}!.\n")
    else:
        if args.function_name:
            function = next((f for f in functions if f['name'].split('/')[-1] == args.function_name), None)
            if function:
                ph.green(f"\n[+] Listing triggers for Function {args.function_name} in Project {args.project_id} ...\n")
                print_function_triggers(function)
            else:
                ph.red(f"\n[-] Function {args.function_name} not found in project {args.project_id}.\n")
        else:
            ph.green(f"\n[+] Listing triggers for all functions in project {args.project_id} ...\n")
            for function in functions:
                print_function_triggers(function)


def print_function_triggers(function):
    ph.green(f"Function: {function['name'].split('/')[-1]}")
        
    trigger = function.get('eventTrigger', {})
    print((f"   - Trigger: {trigger.get('trigger', 'Null')}"))
    print((f"   - Trigger Region: {trigger.get('triggerRegion', 'Null')}"))
    print((f"   - Event Type: {trigger.get('eventType', 'Null')}"))
    print((f"   - Pubsub Topic: {trigger.get('pubsubTopic', 'Null')}"))
    print((f"   - Service Account Email: {trigger.get('serviceAccountEmail', 'Null')}"))
    print((f"   - Retry Policy: {trigger.get('retryPolicy', 'Null')}"))

    event_filters = trigger.get('eventFilters', [])
    for i, event_filter in enumerate(event_filters):
        print((f"   - Event Filter {i+1}:"))
        print((f"     - Attribute: {event_filter.get('attribute', 'Null')}"))
        print((f"     - Value: {event_filter.get('value', 'Null')}"))

    print((f"   - Channel: {trigger.get('channel', 'Null')}"))
    print()
