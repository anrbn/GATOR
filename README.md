
<div align="center">

<p><img src="https://drive.google.com/uc?id=16Bs9-czIY7Huz2AIluTRtZrotQuXBu1F"></p>

</div>

# 
![](https://img.shields.io/badge/Python-3.11-%14354C.svg?style=flat-square&logo=python&logoColor=yellow&color=blue) ![](https://img.shields.io/github/release/anrbn/GATOR?style=flat-square&color=blueviolet) 

**GATOR** - **GCP Attack Toolkit for Offensive Research**, a tool designed to aid in research and exploiting Google Cloud Environments. It offers a comprehensive range of modules tailored to support users in various attack stages, spanning from Reconnaissance to Impact.  

<p float="left">
<img src="https://drive.google.com/uc?id=1iTXAtF2MKAX-suOKeIIRTixtGk4UV9lj" width="400" />
<img src="https://drive.google.com/uc?id=1nQzkdCYh8_8rxVC7zvn6MJrs5wqTzhGV" width="400" />
</p>

### Modules Implemented
<div>
<table>
  <tr>
   <td><strong>Tactic</strong></td>
   <td><strong>Resource</strong></td>
   <td><strong>Modules</strong></td>
   <td><strong>Description</strong></td>
  </tr>
  <tr>
   <td>Recon</td>
   <td>Cloud Functions</td>
   <td>list-function</td>
  <td>List Functions.</td>
  </tr>
  <tr>
   <td></td>
   <td>Cloud IAM</td>
   <td>custom-roles</td>
      <td>List Custom Roles.</td>
  </tr>
  <tr>
   <td></td>
   <td>Cloud Storage</td>
   <td>storage-tree</td>
      <td>List Storage Buckets & Object (Tree).</td>
  </tr>
  <tr>
   <td></td>
   <td>Cloud SQL</td>
   <td>cloudsql-list</td>
   <td>List Cloud SQL Instances.</td>

  </tr>
  <tr>
   <td>Privilege Escalation</td>
   <td>Cloud Functions</td>
   <td>function-deploy</td>
   <td>PrivEsc via Deploying Cloud Function.</td>
  </tr>
    <tr>
   <td>Persistence</td>
   <td>Cloud IAM</td>
   <td>service-account-keys</td>
   <td>Persistence via Downloading Service Account Key(s).</td>
  </tr>
      <tr>
   <td>Other</td>
   <td>Cloud IAM</td>
   <td>createroles</td>
   <td>Create Custom Roles.</td>
  </tr>
  <tr>
  <td></td>
     <td>Cloud IAM</td>
   <td>createsa</td>
   <td>Create Service Accounts.</td>
   </tr>
</table>
</div>

# Documentation

Have a look at the GATOR [Gitbook](https://anrbn.gitbook.io/gator/) for documentation and guide on using GATOR and it's module!

# Prerequisites

### Windows / Unix
* Python 3.11 or newer should be installed. You can verify your Python version with the following command:
```shell
python --version
```
### Docker
* Latest version of Docker should be installed.
* It is recommended to mount only the /tmp directory to the Docker container, and place the Service Account JSON file etc., inside the /tmp directory. 
```shell
sudo docker run -v /tmp:/tmp -it anrbn/gator:latest
```
* To be better organized create a dedicated directory called GATOR inside the /tmp directory.
```shell
mkdir /tmp/GATOR
```
* If you're running GATOR in Docker, by default the files downloaded by GATOR, will be available in your host's /tmp/GATOR directory.

# Installation

## Windows / Unix

```shell
git clone https://github.com/anrbn/GATOR.git
cd GATOR/
pip3 install -r requirements.txt
python3 gator.py
```

## Docker
```shell
sudo docker pull anrbn/gator:latest
sudo docker run -v /tmp:/tmp -it anrbn/gator:latest
```

# Issues
## Reporting an Issue
If you encounter any problems with this tool, I encourage you to let me know. Here are the steps to report an issue:

1. **Check Existing Issues**: Before reporting a new issue, please check the existing issues in this repository. Your issue might have already been reported and possibly even resolved.

2. **Create a New Issue**: If your problem hasn't been reported, please create a new issue in the GitHub repository. Click the Issues tab and then click New Issue.

3. **Describe the Issue**: When creating a new issue, please provide as much information as possible. Include a clear and descriptive title, explain the problem in detail, and provide steps to reproduce the issue if possible. Including the version of the tool you're using and your operating system can also be helpful.

4. **Submit the Issue**: After you've filled out all the necessary information, click Submit new issue.

Your feedback is important, and will help improve the tool. I appreciate your contribution!

## Resolving an Issue
I'll be reviewing reported issues on a regular basis and try to reproduce the issue based on your description and will communicate with you for further information if necessary. Once I understand the issue, I'll work on a fix.

Please note that resolving an issue may take some time depending on its complexity. I appreciate your patience and understanding.

# Contributing
I warmly welcome and appreciate contributions from the community! If you're interested in contributing on any existing or new modules, feel free to submit a pull request (PR) with any new/existing modules or features you'd like to add.

Once you've submitted a PR, I'll review it as soon as I can. I might request some changes or improvements before merging your PR. Your contributions play a crucial role in making the tool better, and I'm excited to see what you'll bring to the project!

Thank you for considering contributing to the project!


# Questions and Issues
If you have any questions regarding the tool or any of its modules, please check out the [documentation](https://anrbn.gitbook.io/gator/) first. I've tried to provide clear, comprehensive information related to the tools and all of its modules. If however your query is not yet solved or you have a different question altogether please don't hesitate to reach out to me via [Twitter](https://twitter.com/corvuscr0w) or [LinkedIn](https://www.linkedin.com/in/anrbnds/). I'm always happy to help and provide support. :)



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
