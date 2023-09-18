# Sensitive IAM Actions
Crowdsourced list of sensitive IAM Actions


## What is this?

There exists no definitive list of Sensitive IAM Actions that can lead to credential or data access, privilege escalation, or making resources public. Several tools have tried to take an opinion on this issue, but there is no centralized list of these sensitive IAM Actions that tools and IAM policy writers can reference.

This repo contains a [list of IAM Actions](actions.yaml) that fall into one of four risk categories:
* Credential Exposure
* Data Access
* Privilege Escalation
* Resource Exposure

That list is then parsed into these files:
* A list of actions annotated with SAR information in [JSON](annotated.json) and [YAML](annotated.yaml).
* [JSON Policy documents](policies) you can attach to your users and roles to Deny actions in specific risk categories.

The addition of an action to these lists can be subjective. Is a pull request in a CodeCommit repo sensitive? What about the comments in an AWS Support case? It depends on what the person puts in. Others can be more obvious, like the list of users in a Cognito user pool, data in a DynamoDB table, or access to the data in an ElasticSearch cluster.


### Generating your own policies

The script [policy-generation.py](scripts/policy-generation.py) allows you to customize your policies to an extent. If there are specific actions you want to exclude from the explicit deny, you can specify them using `--exclude-actions`. If there are a handful of resource ARNs that you need to access, say a specific S3 Bucket, you can use the `--exclude-resources` flag, and they will be added to the policy using a `NotResource` field.

```bash
usage: policy-generation.py [-h] [--debug] --risk {PrivEsc,ResourceExposure,CredentialExposure,DataAccess,ALL}
                            [--exclude-resources EXCLUDE_RESOURCES [EXCLUDE_RESOURCES ...]]
                            [--exclude-actions EXCLUDE_ACTIONS [EXCLUDE_ACTIONS ...]] [--action-file ACTION_FILE]
                            --policy-file POLICY_FILE

optional arguments:
  -h, --help            show this help message and exit
  --debug               print debugging info
  --risk {PrivEsc,ResourceExposure,CredentialExposure,DataAccess,ALL}
                        Risk Categories to generate a policy for
  --exclude-resources EXCLUDE_RESOURCES [EXCLUDE_RESOURCES ...]
                        Which Resources to exclude (via NotResource)
  --exclude-actions EXCLUDE_ACTIONS [EXCLUDE_ACTIONS ...]
                        Which Actions will not be included in the Deny statement
  --action-file ACTION_FILE
                        Action Database to use
  --policy-file POLICY_FILE
                        Filename for generated policy
```

## How to Contribute

Adding a new sensitive action is as simple as updating the [actions.yaml](actions.yaml) file with the new sensitive action. A GitHub action will run to update the annotated files and the JSON [policies](policies/).

### Future Work
While the data access actions are generally comprehensive, they may not work for all use cases. A FinOps user might not need to run cloudtrail:LookupEvents or lambda:GetFunction and access source code. A security auditor or incident response person would need those permissions. Breaking down the data access into sub-categories like source code, possible PII, etc., may need to be considered.

## Prior Art

Several experts in the cloud security community have built tooling to wrangle the complexity of AWS IAM and to parse AWS's [Service Authorization Reference](https://docs.aws.amazon.com/service-authorization/latest/reference/reference.html). This repo is based on the work from:
* [Scott Piper](https://summitroute.com/)
* [Kinnaird McQuade](https://kmcquade.com/)
* [Ian Mckay](https://onecloudplease.com/)
* [Victor GRENU](https://zoph.me/)

### Related Tools

* [Parliament](https://github.com/duo-labs/parliament/) is an AWS IAM linting library from [Scott Piper](https://github.com/0xdabbad00) and Duo Labs.
* [Cloudsplaining](https://github.com/salesforce/cloudsplaining/) is an AWS IAM Security Assessment tool that identifies violations of least privilege from [Kinnaird McQuade](https://github.com/kmcquade) and Salesforce.
* [Permissions.cloud](https://aws.permissions.cloud/) uses a variety of information gathered within the [IAM Dataset](https://github.com/iann0036/iam-dataset/) and exposes that information in a clean, easy-to-read format. From [Ian Mckay](https://github.com/iann0036).
* [IAM Dataset](https://github.com/iann0036/iam-dataset/) also from [Ian Mckay](https://github.com/iann0036).
	* This repo leverages the [iam_definitions.json](https://github.com/iann0036/iam-dataset/blob/main/iam_definition.json) file to annotate the actions.
	* The initial list of sensitive actions was sourced from [add_managed_policies.py](https://github.com/iann0036/iam-dataset/blob/main/add_managed_policies.py) which was sourced from Cloudsplaining.
* [Monitor AWS Managed IAM Policies](https://github.com/zoph-io/MAMIP/) from [Victor GRENU](https://github.com/z0ph).
* [AWS Service Authorization scrape](https://github.com/fluggo/aws-service-auth-reference) from [Brian Crowell](https://github.com/fluggo) is a JSON-formatted version of the AWS Service Authorization Reference packaged for use in Node.js and for querying directly from raw GitHub.

### Blog Posts & Articles
* [AWS API calls that return credentials](https://gist.github.com/kmcquade/33860a617e651104d243c324ddf7992a) - [Kinnaird McQuade](https://github.com/kmcquade)
* [Resource Exposure Actions](https://gist.github.com/kmcquade/3161a6737285dc0508a9fa3446e22090) - [Kinnaird McQuade](https://github.com/kmcquade)
* [Unwanted Permissions that may impact security when using the ReadOnlyAccess policy in AWS](https://www.sidechannel.blog/en/unwanted-permissions-that-may-impact-security-when-using-the-readonlyaccess-policy-in-aws/) - [Rodrigo Montoro](https://www.linkedin.com/in/spooker/)
* [IAM Dataset's list of PrivEsc, Resource Exposure, and Credential Exposure Actions](https://github.com/iann0036/iam-dataset/blob/main/add_managed_policies.py) - [Ian Mckay](https://github.com/iann0036)
* [Sensitive AWS API Calls That Return Credentials and Data](https://kmcquade.com/sensitive-aws-api-calls/) - [Kinnaird McQuade](https://kmcquade.com/)
