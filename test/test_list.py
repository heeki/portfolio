import sys

sys.path.append('src')
from list import apig_list


if __name__ == "__main__":
    user_id = sys.argv[1]
    req_id = sys.argv[2]
    profile = sys.argv[3]
    event = {
        "queryStringParameters": {
            "user_id": user_id
        },
        "requestContext": {
            "requestId": req_id
        }
    }
    context = {}
    apig_list(event, context)
