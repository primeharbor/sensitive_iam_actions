#!/usr/bin/env python3

import yaml
import io
import json
import sys
import argparse


RISK_TYPES=['PrivEsc', 'ResourceExposure', 'CredentialExposure', 'DataAccess', 'ALL']

def main(args):

    policy = {
        "Version": "2012-10-17",
        "Statement": []
    }

    try:
        with open(args.action_file, "r") as f:
            action_list = yaml.safe_load(f)
    except Exception as e:
        print(f"Error loading {args.action_file}: {e}")
        exit(1)

    if args.risk == "ALL":
        risk_types = RISK_TYPES
    else:
        risk_types = [ args.risk ]

    excluded_actions = []
    if args.exclude_actions:
        excluded_actions = [x.lower() for x in args.exclude_actions]

    for risk_type in risk_types:
        if risk_type == 'ALL':
            continue
        if risk_type not in action_list:
            print(f"Warning: no definition for {risk_type}. Skipping...")
            continue

        print(f"Processing actions of type: {risk_type}")
        statement = {
            "Sid": f"Deny{risk_type}",
            "Effect": "Deny",
            "Action": [],
        }

        if args.exclude_resources:
            statement['NotResource'] = args.exclude_resources
        else:
            statement['Resource'] = "*"

        for action_name in action_list[risk_type]['Actions']:
            if action_name.lower() in excluded_actions:
                continue
            if type(action_name) is str:
                statement['Action'].append(action_name)
            else:
                statement['Action'].append(list(action_name.keys())[0])
                # print(action_name)
                # exit(1)

        policy['Statement'].append(statement)

    try:
        with open(args.policy_file, 'w') as f:
            json.dump(policy, f, indent=2)
    except Exception as e:
        print(f"Error writing {args.policy_file}: {e}")
        exit(1)


def do_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", help="print debugging info", action='store_true')
    parser.add_argument("--risk", help="Risk Categories to generate a policy for", required=True, choices=RISK_TYPES)
    parser.add_argument("--exclude-resources", nargs='+', help="Which Resources to exclude (via NotResource)")
    parser.add_argument("--exclude-actions", nargs='+', help="Which Actions will not be included in the Deny statement")
    parser.add_argument("--action-file", help="Action Database to use", default="actions.yaml")
    parser.add_argument("--policy-file", help="Filename for generated policy", required=True)

    args = parser.parse_args()
    return(args)

if __name__ == '__main__':
    try:
        args = do_args()
        main(args)
        exit(0)
    except KeyboardInterrupt:
        exit(1)