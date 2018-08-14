#!/bin/bash

################################################################################
# variables
################################################################################
PROFILE=1527


################################################################################
# portfolio-dynamodb
################################################################################
TEMPLATE=templates/dynamodb.yaml
STACK=portfolio-dynamodb
PARAMS=ParameterKey=ParamTableName,ParameterValue=portfolio
VERB=update-stack
aws --profile $PROFILE cloudformation $VERB \
--stack-name $STACK \
--template-body file://$TEMPLATE \
--parameters $PARAMS \
--capabilities CAPABILITY_IAM

aws --profile $PROFILE cloudformation describe-stack-resources --stack-name $STACK | jq -c '.["StackResources"][] | {type:.ResourceType, id:.PhysicalResourceId}'
DDBROLE=$(aws --profile $PROFILE cloudformation describe-stacks --stack-name $STACK | jq -c '.["Stacks"][]["Outputs"][]  | select(.OutputKey == "OutDDBRole") | .OutputValue' | tr -d '"')

################################################################################
# portfolio-s3
################################################################################
TEMPLATE=templates/s3.yaml
STACK=portfolio-s3
PARAMS=ParameterKey=ParamBucketName,ParameterValue=higs-portfolio
VERB=create-stack
aws --profile $PROFILE cloudformation $VERB \
--stack-name $STACK \
--template-body file://$TEMPLATE \
--parameters $PARAMS \
--capabilities CAPABILITY_IAM

aws --profile $PROFILE cloudformation describe-stack-resources --stack-name $STACK | jq -c '.["StackResources"][] | select(.ResourceType == "AWS::Cognito::UserPool") '

################################################################################
# portfolio-cognito
################################################################################
TEMPLATE=templates/cognito.yaml
STACK=portfolio-cognito
PARAMS=ParameterKey=ParamUserPoolName,ParameterValue=higs-portfolio
VERB=create-stack
aws --profile $PROFILE cloudformation $VERB \
--stack-name $STACK \
--template-body file://$TEMPLATE \
--parameters $PARAMS \
--capabilities CAPABILITY_IAM

aws --profile $PROFILE cloudformation describe-stack-resources --stack-name $STACK | jq -c '.["StackResources"][]'

USERPOOLID=$(aws --profile $PROFILE cloudformation describe-stack-resources --stack-name $STACK | jq -c '.["StackResources"][] | select(.ResourceType == "AWS::Cognito::UserPool") | .PhysicalResourceId' | tr -d '"')
DOMAIN=higs-portfolio
aws --profile $PROFILE cognito-idp create-user-pool-domain --user-pool-id $USERPOOLID --domain $DOMAIN
aws --profile $PROFILE cognito-idp describe-user-pool-domain --domain $DOMAIN

USERCLIENTID=$(aws --profile $PROFILE cloudformation describe-stack-resources --stack-name $STACK | jq -c '.["StackResources"][] | select(.ResourceType == "AWS::Cognito::UserPoolClient") | .PhysicalResourceId' | tr -d '"')
aws cognito-idp sign-up \
--region us-east-1 \
--client-id $USERCLIENTID \
--username $USERNAME \
--password $PASSWORD

aws cognito-idp admin-confirm-sign-up \
--region us-east-1 \
--user-pool-id $USERPOOLID \
--username $USERNAME

# Notes
# - Seems you cannot add domain name in the app integration section via Cloudformation, must be done via console or cli
# - Seems you cannot setup attributes to specify email address or phone number as the user name, try using UsernameAttributes instead of AliasAttributes
# --> https://forums.aws.amazon.com/thread.jspa?threadID=271949
# - When doing stack update, if it has to delete/replace, be sure to remove the domain name integration


################################################################################
# sam
################################################################################
S3BUCKET=higs-serverless
aws --profile $PROFILE cloudformation package \
--template-file etc/sam-input.yaml \
--output-template-file etc/sam-output.yaml \
--s3-bucket $S3BUCKET

STACK=portfolio-apig
aws --profile $PROFILE cloudformation deploy \
--template-file etc/sam-output.yaml \
--stack-name $STACK \
--capabilities CAPABILITY_IAM \
--parameter-overrides "ParamDDBRole=$DDBROLE"

APIID=$(aws --profile $PROFILE cloudformation describe-stack-resources --stack-name $STACK | jq -c '.["StackResources"][] | select(.ResourceType == "AWS::ApiGateway::RestApi") | .PhysicalResourceId' | tr -d '"')
STAGE=Prod
URL=https://$APIID.execute-api.us-east-1.amazonaws.com/$STAGE
curl "$URL/hello"
curl -X POST -H "Content-Type: application/json" -d '{"user_id": "heeki", "note_id": "n-1011", "content": "testing123"}' "$URL/create"
curl "$URL/get?user_id=test&note_id=n-1011"
curl "$URL/list?user_id=test"
curl -X POST -H "Content-Type: application/json" -d '{"user_id": "heeki", "note_id": "n-1011", "content": "testing1234"}' "$URL/update"


# list and update are failing

################################################################################
# cleanup
################################################################################
aws --profile $PROFILE cloudformation delete-stack \
--stack-name $STACK
