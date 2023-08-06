import datetime
import tempfile
import json

def set_start(s3client, bucket, prefix, infinstor_time_spec):
    import botocore
    # this is not really a locking mechanism - the prev ddb conditional put based code was
    status_object_name = f"{prefix}/index/{infinstor_time_spec}/names.json.creating"
    try:
        metadata = s3client.head_object(Bucket=bucket, Key=status_object_name)
        creation_time = metadata['LastModified']
        tnow = datetime.datetime.utcnow()
        delta = tnow - creation_time
        if delta.total_seconds() > 900:
            print(f"Status object {creation_time} older than 900 seconds {tnow} for {infinstor_time_spec}. This lambda invocation continuing ..")
            return True
        else:
            print(f"Status object {creation_time} less than 900 seconds old {tnow} for {infinstor_time_spec}. This lambda invocation exiting ..")
            return False
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print(f"{status_object_name} does not exist. This lambda invocation creating status object and continuing..")
        else:
            print(f"Caught {e} while reading {status_object_name}. This lambda invocation exiting..")
            return False

    fd, tfile = tempfile.mkstemp()
    try:
        response = s3client.upload_file(tfile, bucket, status_object_name)
        print(f"{status_object_name} does not exist. This lambda invocation successfully created status object {status_object_name} and continuing..")
        return True
    except botocore.exceptions.ClientError as e:
        print(f"Caught {e} while creating status file {status_object_name}. This lambda invocation exiting..")
        return False

# returns 'NotPresent'|'Creating'|'Ready'|'CreationFailed', names|None
def get_cache_entry(bucket, prefix, infinstor_time_spec, head_only):
    import boto3
    import botocore
    s3client = boto3.client('s3')
    object_name = f"{prefix}/index/{infinstor_time_spec}/names.json"

    if head_only:
        lfn = "/tmp/names.json"
        try:
            metadata = s3client.head_object(Bucket=bucket, Key=object_name)
            return 'Ready', {}
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "404":
                print(f"{object_name} does not exist. Trying status object")
            else:
                print(f"Caught {e} while reading {object_name}. Returning NotPresent")
                return 'NotPresent', None
    else:
        lfn = "/tmp/names.json"
        try:
            s3client.download_file(bucket, object_name, lfn)
            with open(lfn, 'r') as fp:
                dct = json.load(fp)
                print(f"Loaded json file {len(dct)} entries from {object_name}")
            os.remove(lfn)
            if dct:
                return 'Ready', dct
            else:
                return 'Ready', {}
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "404":
                print(f"{object_name} does not exist. Trying status object")
            else:
                print(f"Caught {e} while reading {object_name}. Returning NotPresent")
                return 'NotPresent', None

    status_object_name = f"{prefix}/index/{infinstor_time_spec}/names.json.creating"
    try:
        metadata = s3client.head_object(Bucket=bucket, Key=status_object_name)
        creation_time = metadata['LastModified']
        tnow = datetime.datetime.utcnow()
        delta = creation_time - tnow
        if delta.total_seconds() > 900:
            print(f"Status object {creation_time} older than 900 seconds {tnow} for {infinstor_time_spec}. CreationFailed..")
            return 'CreationFailed', None
        else:
            print(f"Status object {creation_time} less than 900 seconds old {tnow} for {infinstor_time_spec}. waiting..")
            return 'Creating', None
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print(f"{status_object_name} does not exist. Returning NotPresent")
            return 'NotPresent', None
        else:
            print(f"Caught {e} while reading {status_object_name}. Returning CreationFailed")
            return 'CreationFailed', None

