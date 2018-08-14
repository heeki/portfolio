import json
import sys

sys.path.append('src')
from update import apig_update

# note: intentionally converting body to a string, as the function expects that body to be a full string
# this is because that comes in as a json payload via the body of a post request
# in other cases, the input parameters come in as query string parameters
if __name__ == "__main__":
    user_id = sys.argv[1]
    note_id = sys.argv[2]
    content = sys.argv[3]
    req_id = sys.argv[4]
    profile = sys.argv[5]
    event = {
        "body": json.dumps({
            "user_id": user_id,
            "note_id": note_id,
            "content": content
        }),
        "profile": profile,
        "requestContext": {
            "requestId": req_id
        }
    }
    print "event={}".format(event)
    context = {}
    response = apig_update(event, context)
    assert response['statusCode'] == 200, "apig_update() failed!"

