# gator/services/iam/iam.py

from googleapiclient import discovery
from googleapiclient.errors import HttpError
from gator.auth.credentials import load_credentials

def create_policy(args):
    if args.member.endswith(".gserviceaccount.com"):
        member = f"serviceAccount:{args.member}"
    elif "@" in args.member:
        member = f"user:{args.member}"
    else:
        member = args.member

    policy = {
        "bindings": [
            {
                "role": args.role,
                "members": [member]
            }
        ]
    }

    return policy


def set_iam_policy(args):
    creds = load_credentials(args)

    if args.function_name:
        service = discovery.build('cloudfunctions', 'v1', credentials=creds)
        name = f"projects/{args.project_id}/locations/{args.region}/functions/{args.function_name}"

        policy = create_policy(args)

        try:
            request = service.projects().locations().functions().setIamPolicy(
                resource=name,
                body={
                    'policy': policy,
                }
            )
            request.execute()
            print(f"[+] IAM policy set for function {args.function_name}.")
        except HttpError as error:
            print(f"[-] Error: {error}")

