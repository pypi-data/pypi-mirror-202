# Puploader
Puploader is a command line tool for uploading .nc files to the Polarplot dedicated S3 bucket.

## Requirements
- Python 3
- boto3 library
## Installation
You can either install the tool from pip using ``` pip install puploader``` or by following the steps below : 

- Clone the repository: git clone https://github.com/YOUR_USERNAME/puploader.git
- Change into the directory: cd puploader
- Install the required libraries: pip install -r requirements.txt
- Add your AWS credentials to your environment variables or to your ~/.aws/credentials file. For example:


``` shell
aws_access_key_id = YOUR_ACCESS_KEY_ID
aws_secret_access_key = YOUR_SECRET_ACCESS_KEY
```

## Usage
### Upload a file
To upload a file, use the following command:


```shell
puploader /path/to/file.nc --study STUDY_NAME --client CLIENT_NAME 
```
Replace STUDY_NAME, CLIENT_NAME, and /path/to/file.nc with the appropriate values for your file.

### List uploaded files
To list all uploaded files and their metadata, use the following command:


```shell
puploader --list
```
This will display a list of all files that have been uploaded to the bucket, along with their metadata.

You can also output the list as JSON by using the --json option:

```shell
puploader --list --json
```

License
This tool is licensed under the MIT License. See the LICENSE file for details.