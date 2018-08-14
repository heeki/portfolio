from scriptlets.scriptlet_dynamodb import ScriptletDynamoDB
from scriptlets.scriptlet_global import Global
from response import success, failure


app_name = "portfolio"
log_file = "{}.log".format(app_name)
log_dir = "/tmp"
log = Global.get_logger(app_name, log_file, log_dir)


def apig_list(event, context):
    log.info("event={}".format(event))
    log.info("context={}".format(str(context)))

    profile = ""
    if 'profile' in event.keys():
        profile = event["profile"]
    ddb = ScriptletDynamoDB(app_name, profile)

    data = event["queryStringParameters"]
    user_id = data["user_id"]
    # user_id = data["requestContext"]["identity"]["cognitoIdentityId"]

    table_name = "portfolio"
    key = "user_id"
    value = user_id
    returned = ddb.query(table_name, key, value)
    log.info("returned['Count']={}".format(returned['Count']))
    for item in returned['Items']:
        log.info("item={}".format(item))

    if returned['Count'] > 0:
        response = success(returned['Items'])
    else:
        response = failure(returned['Items'])
    log.info("response={}".format(response))

    return response
