# sensitive_iam_actions
Crowdsourced list of sensitive IAM Actions


## What is this?

### Why?


## How to Contribute

Adding a new sensitive action is as simple as updating the [actions.yaml](actions.yaml) file with the new sensitive action. A GitHub action will run to update the annotated files and the JSON [policies](policies/).


## Prior Art

A number of folks have built tooling to wrangle the complexity of AWS IAM and to parse AWS's [Service Authorization Reference](https://docs.aws.amazon.com/service-authorization/latest/reference/reference.html). This repo is based on the work from:
* [Scott Piper](https://summitroute.com/)
* [Kinnaird McQuade](https://kmcquade.com/)
* [Ian Mckay](https://onecloudplease.com/)
* [Victor GRENU](https://zoph.me/)

### Related Tools

* [Parliament](https://github.com/duo-labs/parliament/) is an AWS IAM linting library, from [Scott Piper](https://github.com/0xdabbad00) and Duo Labs.
* [Cloudsplaining](https://github.com/salesforce/cloudsplaining/) is an AWS IAM Security Assessment tool that identifies violations of least privilege, from [Kinnaird McQuade](https://github.com/kmcquade) and Salesforce
* [Permissions.cloud](https://aws.permissions.cloud/) uses a variety of information gathered within the [IAM Dataset](https://github.com/iann0036/iam-dataset/) and exposes that information in a clean, easy-to-read format. From [Ian Mckay](https://github.com/iann0036).
* [IAM Dataset](https://github.com/iann0036/iam-dataset/) also from [Ian Mckay](https://github.com/iann0036).
* [Monitor AWS Managed IAM Policies](https://github.com/zoph-io/MAMIP/) from [Victor GRENU](https://github.com/z0ph).


### Blog Posts & Articles
* [AWS API calls that return credentials](https://gist.github.com/kmcquade/33860a617e651104d243c324ddf7992a) - [Kinnaird McQuade](https://github.com/kmcquade)
* [Resource Exposure Actions](https://gist.github.com/kmcquade/3161a6737285dc0508a9fa3446e22090) - [Kinnaird McQuade](https://github.com/kmcquade)
* [Unwanted Permissions that may impact security when using the ReadOnlyAccess policy in AWS](https://www.sidechannel.blog/en/unwanted-permissions-that-may-impact-security-when-using-the-readonlyaccess-policy-in-aws/) - [Rodrigo Montoro](https://www.linkedin.com/in/spooker/)
* [IAM Dataset's list of PrivEsc, Resource Exposure, and Credential Exposure Actions](https://github.com/iann0036/iam-dataset/blob/main/add_managed_policies.py) - [Ian Mckay](https://github.com/iann0036)
* [Sensitive AWS API Calls That Return Credentials and Data](https://kmcquade.com/sensitive-aws-api-calls/) - [Kinnaird McQuade](https://kmcquade.com/)