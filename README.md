# API for Asset Portfolio Management
This project is the start of a portfolio manager for cryptocurrency assets. The goal is to create a way to have users
create a list of cryptocurrency assets that they are interested in following and dynamically updating prices and
granting a view into overall portfolio value.

## Implementation
Test scripts require updates to the initial variables in the script.

```
USERID=test         # user id
NOTEID=n-1010       # note identifier
CONTENT=testing123  # text body
REQID=r-1010        # request identifier
PROFILE=1527        # aws cli profile
```

Deploy scripts require initial variables to be updated along with two environment variables.

```
# initial variable
PROFILE=1527        # aws cli profile

# environment variables
USERNAME=testuser
PASSWORD=password
```