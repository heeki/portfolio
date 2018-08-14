import json
from scriptlets.scriptlet_dynamodb import ScriptletDynamoDB
from scriptlets.scriptlet_global import Global
from response import success, failure


app_name = "portfolio"
log_file = "{}.log".format(app_name)
log_dir = "/tmp"
log = Global.get_logger(app_name, log_file, log_dir)


def apig_create(event, context):
    log.info("event={}".format(event))
    log.info("context={}".format(str(context)))

    profile = ""
    if 'profile' in event.keys():
        profile = event["profile"]
    ddb = ScriptletDynamoDB(app_name, profile)

    data = json.loads(event["body"])
    user_id = data["user_id"]
    note_id = data["note_id"]
    content = "{}: {}".format(event["requestContext"]["requestId"], data["content"])

    table_name = "portfolio"
    item = {
        "user_id": {"S": user_id},
        "note_id": {"S": note_id},
        "content": {"S": content}
    }

    # should really wrap this is a try/catch block and then use the success/failure methods
    returned = ddb.put_item(table_name, item)
    log.info("returned={}".format(returned))
    if returned["ResponseMetadata"]["HTTPStatusCode"] == 200:
        response = success(returned["ResponseMetadata"]["HTTPStatusCode"])
    else:
        response = failure(returned["ResponseMetadata"]["HTTPStatusCode"])
    log.info("response={}".format(response))

    return response
