import json
from scriptlets.scriptlet_dynamodb import ScriptletDynamoDB
from scriptlets.scriptlet_global import Global
from response import success, failure


app_name = "portfolio"
log_file = "{}.log".format(app_name)
log_dir = "/tmp"
log = Global.get_logger(app_name, log_file, log_dir)


def apig_update(event, context):
    log.info("event={}".format(event))
    log.info("context={}".format(str(context)))

    profile = ""
    if 'profile' in event.keys():
        profile = event["profile"]
    ddb = ScriptletDynamoDB(app_name, profile)

    data = json.loads(event["body"])
    user_id = data["user_id"]
    note_id = data["note_id"]
    content = data["content"]

    table_name = "portfolio"
    key = {
        "user_id": {"S": user_id},
        "note_id": {"S": note_id}
    }

    # should really wrap this is a try/catch block and then use the success/failure methods
    returned = ddb.update(table_name, key, content)
    log.info("returned={}".format(returned))

    if returned["ResponseMetadata"]["HTTPStatusCode"] == 200:
        response = success(returned["Attributes"])
    else:
        response = failure(returned["Attributes"])
    log.info("response={}".format(response))

    return response
