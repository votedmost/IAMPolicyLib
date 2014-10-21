============
IAMPolicyLib
============

Quick library to easily and interactively generate IAM policies.

The `Actions` class is automatically parsed from the boto JSON definitions and
turned into a `namedtuple` for easy tab completion.

Example::

    In [1]: from IAMPolicyLib import Policy, PolicyStatement, Actions

    In [2]: access_bucket = PolicyStatement("arn:aws:s3:::my_cool_bucket",[Actions.s3.GetBucketLocation,Actions.s3.ListBuckets])

    In [3]: access_bucket_contents = PolicyStatement("arn:aws:s3:::my_cool_bucket/*",[Actions.s3.GetObject])

    In [4]: new_policy = Policy(access_bucket, access_bucket_contents)

    In [5]: print new_policy
    {
      "Statements": [
        "{
        "Resource": "arn:aws:s3:::my_cool_bucket", 
        "Effect": "Allow", 
        "Actions": [
            "s3:GetBucketLocation", 
            "s3:ListBuckets"
        ]
    },{
        "Resource": "arn:aws:s3:::my_cool_bucket/*", 
        "Effect": "Allow", 
        "Actions": [
            "s3:GetObject"
        ]
    }"
      ]
    }


TODO
====

- generate `Actions` in a better way (currently assumes you've parked your boto
  library in the same place that I have because I was too impatient to dig through
  the API to see where this data was exposed)

- Allow `PolicyStatement` constructor to take boto buckets, queues, etc as `Resource`
  and autogenerate the ARN
