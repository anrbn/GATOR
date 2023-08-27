"""
import json
from googleapiclient.discovery import build

from gator.auth.credentials import load_credentials
from gator.utils import print_helpers as ph

def compute_firewall(project_id):
    try:

    except Exception as ex:
        ph.print_error("{}".format(ex))
        print()


import json
from google.cloud import compute_v1

def compute_firewall(project_id, verbose, json_output):
    firewall_rules = fetch_firewall_rules(project_id)
    
    potentially_weak_rules = []
    for rule in firewall_rules:
        if rule["direction"] == "INGRESS" and "0.0.0.0/0" in rule["sourceRanges"]:
            potentially_weak_rules.append(rule["name"])
            if verbose:
                print(f"Warning: Ingress rule {rule['name']} is allowing all traffic from any source!")
        
    if json_output:
        print(json.dumps(potentially_weak_rules))
    else:
        print(f"{len(potentially_weak_rules)} potentially weak firewall rules found.")

def fetch_firewall_rules(project_id):

    client = compute_v1.FirewallsClient()
    firewall_rules_list = list(client.list(project=project_id))

    return firewall_rules_list

"""