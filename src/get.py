from scriptlets.scriptlet_dynamodb import ScriptletDynamoDB
from scriptlets.scriptlet_global import Global
from response import success, failure


app_name = "portfolio"
log_file = "{}.log".format(app_name)
log_dir = "/tmp"
log = Global.get_logger(app_name, log_file, log_dir)


def apig_get(event, context):
    log.info("event={}".format(event))
    log.info("context={}".format(str(context)))

    profile = ""
    if 'profile' in event.keys():
        profile = event["profile"]
    ddb = ScriptletDynamoDB(app_name, profile)

    data = event["queryStringParameters"]
    user_id = data["user_id"]
    note_id = data["note_id"]

    table_name = "portfolio"
    key = {
        "user_id": {"S": user_id},
        "note_id": {"S": note_id}
    }

    returned = ddb.get_item(table_name, key)
    item = returned["Item"]["content"]
    log.info("returned={}".format(item))
    if len(returned.keys()) > 0:
        response = success(item)
    else:
        response = failure(item)
    log.info("response={}".format(response))

    return response
