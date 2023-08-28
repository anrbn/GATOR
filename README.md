<div align="center">

<p><img src="https://drive.google.com/uc?id=1BahpF3-BGMCqUAQCIBczLqW6jFcJAJ_Q" width="500"></p>

## GCP ATTACK TOOLKIT FOR OFFENSIVE RESEARCH

</div>

![](https://img.shields.io/badge/Python-3.11-%14354C.svg?style=flat-square&logo=python&logoColor=yellow&color=blue) ![](https://img.shields.io/github/release/anrbn/GATOR?style=flat-square&color=blueviolet) 

**GATOR** - **GCP Attack Toolkit for Offensive Research**, a tool designed to aid in research and exploiting Google Cloud Environments. It offers a comprehensive range of modules tailored to support users in various attack stages, spanning from Reconnaissance to Impact.  

# Modules
<table>
  <thead>
    <tr>
      <th>Resource Category</th>
      <th>Primary Module</th>
      <th>Command Group</th>
      <th>Operation</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td rowspan="4">User Authentication</td>
      <td rowspan="4">auth</td>
      <td>-</td>
      <td>activate</td>
      <td>Activate a Specific Authentication Method</td>
    </tr>
    <tr>
      <td>-</td>
      <td>add</td>
      <td>Add a New Authentication Method</td>
    </tr>
    <tr>
      <td>-</td>
      <td>delete</td>
      <td>Remove a Specific Authentication Method</td>
    </tr>
    <tr>
      <td>-</td>
      <td>list</td>
      <td>List All Available Authentication Methods</td>
    </tr>
    <tr>
      <td rowspan="3">Cloud Functions</td>
      <td rowspan="3">functions</td>
      <td>-</td>
      <td>list</td>
      <td>List All Deployed Cloud Functions</td>
    </tr>
    <tr>
      <td>-</td>
      <td>permissions</td>
      <td>Display Permissions for a Specific Cloud Function</td>
    </tr>
    <tr>
      <td>-</td>
      <td>triggers</td>
      <td>List All Triggers for a Specific Cloud Function</td>
    </tr>
    <tr>
      <td rowspan="2">Cloud Storage</td>
      <td rowspan="2">storage</td>
      <td>buckets</td>
      <td>list</td>
      <td>List All Storage Buckets</td>
    </tr>
    <tr>
      <td>buckets</td>
      <td>permissions</td>
      <td>Display Permissions for Storage Buckets</td>
    </tr>
    <tr>
      <td>Compute Engine</td>
      <td>compute</td>
      <td>instances</td>
      <td>add-ssh-key</td>
      <td>Add SSH Key to Compute Instances</td>
    </tr>
  </tbody>
</table>

# Installation

Python 3.11 or newer should be installed. You can verify your Python version with the following command:

```shell
python --version
```

### Manual Installation via setup.py

```shell
git clone https://github.com/anrbn/GATOR.git
cd GATOR
python setup.py install
```

### Automated Installation via pip

```shell
pip install gator-red
```

# Documentation

Have a look at the GATOR [Documentation](https://github.com/anrbn/GATOR/tree/main/docs#readme) for an explained guide on using GATOR and it's module!

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
If you have any questions regarding the tool or any of its modules, please check out the [documentation](https://github.com/anrbn/GATOR/tree/main/docs#readme) first. I've tried to provide clear, comprehensive information related to all of its modules. If however your query is not yet solved or you have a different question altogether please don't hesitate to reach out to me via [Twitter](https://twitter.com/corvuscr0w) or [LinkedIn](https://www.linkedin.com/in/anrbn/). I'm always happy to help and provide support. :)
