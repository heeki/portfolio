import json


def apig_hello(event, context):
    print "Received event: {}".format(json.dumps(event, indent=2))
    print "Received context: {}".format(str(context))
    print "Logging information: {}, {}".format(context.log_group_name, context.log_stream_name)
    print "Request id: {}".format(context.aws_request_id)
    print "Memory limit (MB): {}".format(context.memory_limit_in_mb)
    print "Hello world!"

    body = event["requestContext"]["requestId"]

    # direct lambda response
    # response = {
    #     'statusCode': 200,
    #     'headers': {},
    #     'body': json.dumps(body, indent=2)
    # }

    # lambda proxy integration
    response = {
        'isBase64Encoded': False,
        'statusCode': 200,
        'headers': {},
        'body': json.dumps(body, indent=2)
    }

    print "Response object: {}".format(response)
    return response
