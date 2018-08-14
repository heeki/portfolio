import json
import sys

sys.path.append('src')
from get import apig_get


# note: lambda function takes query string parameters as input
if __name__ == "__main__":
    user_id = sys.argv[1]
    note_id = sys.argv[2]
    req_id = sys.argv[3]
    profile = sys.argv[4]
    event = {
        "queryStringParameters": {
            "user_id": user_id,
            "note_id": note_id},
        "profile": profile,
        "requestContext": {
            "requestId": req_id
        }
    }
    print "event={}".format(event)
    context = {}
    response = apig_get(event, context)
    assert response['statusCode'] == 200, "apig_get() failed!"

