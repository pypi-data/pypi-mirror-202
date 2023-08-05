import datetime
import tempfile

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


