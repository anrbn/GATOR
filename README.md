```
GATOR: GCP Attack Toolkit for Offensive Research

Command groups:
    iam                                 IAM Management
        service-accounts list           Lists service accounts for a given project
        service-accounts download       Downloads a service account key
        set-iam-policy                  Sets an IAM policy for a Cloud Function

    auth                                Authentication Management
        list                            Lists all available authentication mechanisms
        activate                        Activates an authentication mechanism
        delete                          Deletes an authentication mechanism

    storage                             Cloud Storage Management
        buckets list                    Lists all storage buckets in a project
        objects list                    Lists all objects in a given bucket

    functions                           Cloud Functions Management
        list                            Lists Cloud Functions for a given project
        deploy                          Deploys a Cloud Function
        check-permissions               Checks permissions for a Cloud Function
        check-env-vars                  Checks environment variables for a Cloud Function
        list-triggers                   Lists triggers for a Cloud Function

    privesc                             Privilege Escalation
        function deploy                 Deploys a Cloud Function with escalated privileges

Options:
  -h, --help                            Shows this help message and exit

For more information on a specific command, type "main.py COMMAND --help/-h".
```
