import boto3
import botocore
import pprint
from boto3.dynamodb.conditions import Key
from scriptlets.scriptlet_global import Global

pp = pprint.PrettyPrinter(indent=4)


class ScriptletDynamoDB:
    def __init__(self, app_name, profile=""):
        log_file = "{}.log".format(app_name)
        log_dir = "/tmp"
        self.log = Global.get_logger(app_name, log_file, log_dir)
        self.profile = profile
        if profile == "":
            self.ddb_client = boto3.client('dynamodb')
            self.ddb_resource = boto3.resource('dynamodb')
        else:
            self.ddb_client = boto3.Session(profile_name=self.profile).client('dynamodb')
            self.ddb_resource = boto3.Session(profile_name=self.profile).resource('dynamodb')

    def table_exists(self, table_name):
        """ Check if a DynamoDB table exists

        :param table_name: name of the DynamoDB table to check
        :return: True|False
        """
        try:
            response = self.ddb_client.describe_table(TableName=table_name)
            pp.pprint(response)
            return True
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == 'ResourceNotFoundException':
                self.log.info("table_exists(): {} not found".format(table_name))
            else:
                self.log.error("table_exists(): undefined error checking for {}".format(table_name))
            return False

    def create_table(self, table_name):
        """ Create a table and return the Table object

        :param table_name: name of the DynamoDB table to check
        :return: Table object
        """
        self.log.info("create_table(): {}".format(table_name))
        if self.table_exists(table_name):
            return self.ddb_resource.Table(table_name)
        else:
            table = self.ddb_resource.create_table(
                TableName=table_name,
                KeySchema=[
                    {
                        'AttributeName': 'id',
                        'KeyType': 'HASH'
                    },
                    {
                        'AttributeName': 'timestamp',
                        'KeyType': 'RANGE'
                    }
                ],
                AttributeDefinitions=[
                    {
                        'AttributeName': 'id',
                        'AttributeType': 'S'
                    },
                    {
                        'AttributeName': 'timestamp',
                        'AttributeType': 'S'
                    }
                ],
                ProvisionedThroughput={
                    'ReadCapacityUnits': 5,
                    'WriteCapacityUnits': 5
                }
            )
            table.meta.client.get_waiter('table_exists').wait(TableName=table_name)
            self.log.info("create_table(): table created, {} items".format(table.item_count))
            return table

    def put_item(self, table_name, item):
        """ Put an item into a DynamoDB table

        :param table_name: table_name
        :param item: item to be inserted
        :return:
        """
        self.log.info("put_item(): putting item {}".format(item))
        response = self.ddb_client.put_item(
            TableName=table_name,
            Item=item
        )
        return response

    def get_item(self, table_name, key):
        """ Get an item from a DynamoDB table

        :param table_name: DynamoDB table from which the item will retrieved
        :param key: key of the item to be retrieved
        :return:
        """
        self.log.info("get_item(): getting item with key {}".format(key))
        response = self.ddb_client.get_item(
            TableName=table_name,
            Key=key
        )
        if response['ResponseMetadata']['HTTPStatusCode'] == 200 and 'Item' in response.keys():
            self.log.info("get_item(): retrieved item {}".format(response['Item']))
        else:
            self.log.info("get_item(): no items found with that key")
        return response

    def query(self, table_name, key, value):
        """ Query for a list of items from a DynamoDB table

        :param table_name: DynamoDB table from which the items will retrieved
        :param key: parameters for the query
        :param value: parameters for the query
        :return:
        """
        self.log.info("query(): querying with key={}, value={}".format(key, value))
        fexp = Key(key).eq(value)
        table = self.ddb_resource.Table(table_name)
        response = table.query(
            KeyConditionExpression=fexp
        )
        # TODO: Need to figure out how to do client-based query()
        # response = self.ddb_client.query(
        #     TableName=table_name,
        #     KeyConditionExpression="user_id = :user",
        #     ExpressionAttributeValues={
        #         ':user': {
        #             'S': key
        #         }
        #     }
        # )
        return response

    def update(self, table_name, key, value):
        self.log.info("update(): updating {} with {}".format(key, value))
        response = self.ddb_client.update_item(
            TableName=table_name,
            Key=key,
            ReturnValues="UPDATED_NEW",
            UpdateExpression="SET content = :content",
            ExpressionAttributeValues={
                ':content': {
                    'S': value
                }
            }
        )
        return response

