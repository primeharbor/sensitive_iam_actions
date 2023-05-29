#!/usr/bin/env python3

import yaml
import io
import json
import sys
import argparse

def main(args):
    try:
        with open(args.action_file, "r") as f:
            action_list = yaml.safe_load(f)
    except Exception as e:
        print(f"Error loading {args.action_file}: {e}")
        exit(1)

    try:
        with open(args.definition_file, "r") as f:
            iam_definition = json.loads(f.read())
    except Exception as e:
        print(f"Error loading {args.definition_file}: {e}")
        exit(1)

    # Convert to a lookup of actions
    iam_map = {}
    for service in iam_definition:
        for p in service['privileges']:
            action = f"{service['prefix']}:{p['privilege']}".lower()
            iam_map[action] = p
            iam_map[action]['service_name'] = service['service_name']
            iam_map[action]['action'] = f"{service['prefix']}:{p['privilege']}"

    # Now process our action list.
    output = {}
    new_yaml = {}
    for risk_type, risk_data in action_list.items():
        new_yaml[risk_type] = { 'Actions': [] }
        for a in risk_data['Actions']:
            if '*' in a:
                prefix = a.replace('*', '').lower()
                for w in filter(lambda x: x.startswith(prefix), iam_map.keys()):
                    # print(f"found wildcard action {w} for prefix {prefix}")
                    output, action_name = process_action(output, w, iam_map, risk_type)
                    if args.no_annotation:
                        new_yaml[risk_type]['Actions'].append(action_name)
                    else:
                        new_yaml[risk_type]['Actions'].append({action_name: output[action_name]})
            else:
                if a.lower() not in iam_map:
                    print(f"Warning. No definition for {a}")
                    continue
                output, action_name = process_action(output, a, iam_map, risk_type)
                if args.no_annotation:
                    new_yaml[risk_type]['Actions'].append(action_name)
                else:
                    new_yaml[risk_type]['Actions'].append({action_name: output[action_name]})

    with io.open(args.output_yaml, 'w', encoding='utf8') as outfile:
        if args.no_annotation:
            yaml.dump(new_yaml, outfile, width=1000, allow_unicode=True)
        else:
            yaml.dump(new_yaml, outfile, width=1000, allow_unicode=True, Dumper=NoAliasDumper)
    with open(args.output_json, 'w') as f:
        json.dump(output, f, indent=2)

    exit(0)

class NoAliasDumper(yaml.SafeDumper):
    def ignore_aliases(self, data):
        return True

    def write_line_break(self, data=None):
        super().write_line_break(data)

        if len(self.indents) == 1:
            super().write_line_break()

        if len(self.indents) == 3:
            super().write_line_break()


def process_action(output, action_name, iam_map, risk_type):
    lc_action_name = action_name.lower()
    cc_action_name = iam_map[lc_action_name]['action']
    if cc_action_name in output:
        output[cc_action_name]['risk_category'].append(risk_type)
        return(output, cc_action_name)
    else:
        output[cc_action_name] = {
            'access_level': iam_map[lc_action_name]['access_level'],
            'description': iam_map[lc_action_name]['description'],
            'service_name': iam_map[lc_action_name]['service_name'],
            'risk_category': [risk_type]
        }
        return(output, cc_action_name)


def do_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", help="print debugging info", action='store_true')
    parser.add_argument("--action-file", help="List of actions to use", default="actions.yaml")
    parser.add_argument("--definition-file", help="IAM Definition file to use", default="iam_definition.json")
    parser.add_argument("--output-yaml", help="Filename for annotated output in Yaml", required=True)
    parser.add_argument("--output-json", help="Filename for annotated output in JSON", required=True)
    parser.add_argument("--no-annotation", help="Just print the list of actions without annotations", action='store_true')

    args = parser.parse_args()
    return(args)

if __name__ == '__main__':
    try:
        args = do_args()
        main(args)
        exit(0)
    except KeyboardInterrupt:
        exit(1)