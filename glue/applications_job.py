import sys
import boto3
from awsglue.utils import getResolvedOptions

# --------------------------------------------------
# 1. Get Arguments
# --------------------------------------------------
args = getResolvedOptions(sys.argv, ['RAW_BASE', 'SILVER_BASE'])
raw_base_path = args['RAW_BASE']

print(f"DEBUG: Checking access to: {raw_base_path}")

# --------------------------------------------------
# 2. Extract Bucket and Prefix
# --------------------------------------------------
# raw_base_path looks like "s3://my-bucket/raw"
# We need to split it into "my-bucket" and "raw"
try:
    path_parts = raw_base_path.replace("s3://", "").split("/", 1)
    bucket_name = path_parts[0]
    prefix = path_parts[1] if len(path_parts) > 1 else ""
    
    print(f"DEBUG: Extracted Bucket: '{bucket_name}'")
    print(f"DEBUG: Extracted Folder: '{prefix}'")
except Exception as e:
    print(f"ERROR: Could not parse path: {raw_base_path}. Error: {str(e)}")
    sys.exit(1)

# --------------------------------------------------
# 3. List Objects (The Connection Test)
# --------------------------------------------------
s3 = boto3.client('s3')

print("-" * 50)
print("ATTEMPTING TO LIST FILES...")
print("-" * 50)

try:
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
    
    if 'Contents' in response:
        print("SUCCESS! Found these files:")
        for obj in response['Contents']:
            print(f" - FOUND FILE: {obj['Key']} (Size: {obj['Size']} bytes)")
    else:
        print("WARNING: Connection successful, but folder is EMPTY.")
        print(f"Ensure your file is inside '{prefix}' folder.")

except Exception as e:
    print("CRITICAL FAILURE: Access Denied or Bucket Not Found.")
    print(f"Error Message: {str(e)}")
    
print("-" * 50)
