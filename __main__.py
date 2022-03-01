from getopt import getopt
import boto3
import sys
import re
import pandas as pd
from getpass import getpass

filter_tags = {}


def checkTags(tags: list) -> bool:
    next(
        item for item in tags
        if item['Key'] in filter_tags.keys() and item['Value'] == filter_tags[item['Key']]
    )
    return True


statuses = ['ROLLBACK_COMPLETE', 'CREATE_COMPLETE', 'UPDATE_COMPLETE']


def main():

    aws_access_key_id = None
    region = None

    argv = sys.argv[1:]

    try:
        opts, args = getopt(
            argv,
            shortopts='',
            longopts=[
                "tags=",
                # "stack-pattern",
                "aws-access-key-id=",
                "region="
            ]
        )
    except Exception as e:
        print('An exception ocurred: ' + str(e))
        sys.exit(2)

    for opt, arg in opts:
        # Mandatorio y transversal a parametros y tablas
        if opt in ['--tags']:
            print(f'valor: {arg}')
            regex = re.search(r"([A-Za-z0-9]+):([A-Za-z0-9]+)", arg)
            try:
                tag_name = regex.group(1).strip()
                tag_value = regex.group(2).strip()
            except AttributeError:
                print(
                    '''
                        Tags must be specified in the following way: "Key=value"
                    ''')
            filter_tags[tag_name] = tag_value
        elif opt in ['--region']:
            region = arg
        elif opt in ['--aws-access-key-id']:
            aws_access_key_id = arg
    
    aws_secret_acces_key = getpass('aws-secret-access-key: ')

    cfn_client = boto3.client(
        'cloudformation',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_acces_key,
        region_name=region
    )

    stacks = cfn_client.list_stacks(StackStatusFilter=statuses)[
        'StackSummaries']

    filtered_stacks = list(
        filter(
            lambda stack: checkTags(
                cfn_client.describe_stacks(
                    StackName=stack['StackName']
                )['Stacks'][0]['Tags']
            ) == True, stacks
        )
    )

    df = pd.DataFrame(
        columns=[
            'StackName', 'LastUpdatedTimestamp',
            'LogicalResourceId', 'PhysicalResourceId', 'ResourceType'
        ]
    )

    for stack in (filtered_stacks):

        resources = cfn_client.list_stack_resources(
            StackName=stack['StackName'],
            # NextToken='string'
        )['StackResourceSummaries']

        for resource in resources:

            row = {
                'StackName':  stack['StackName'],
                'LastUpdatedTimestamp': resource['LastUpdatedTimestamp'],
                'LogicalResourceId': resource['LogicalResourceId'],
                'PhysicalResourceId': resource['LogicalResourceId'],
                'ResourceType': resource['ResourceType'],
            }

            df = df.append(row, ignore_index=True)

    if len(df) > 0:
        df.to_csv('stack_inventory.csv')
        print('Inventory generated succesfully')
    else:
        print('Nothing to show in csv')


if __name__ == "__main__":
    main()
