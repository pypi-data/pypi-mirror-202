import argparse
import os
import boto3
import json
import hashlib


class Puploader:
    def __init__(self, study=None, client=None):
        self.study = study
        self.client = client
        self.bucket_name = "polarplot-data"
        self.meta_file = "puploader_meta.json"
        self.s3 = boto3.resource('s3')
        self.bucket = self.s3.Bucket(self.bucket_name)

    def list_files(self):
        with self.bucket.Object(self.meta_file).get()['Body'] as f:
            file_content = f.read().decode('utf-8')
            meta_data = json.loads(file_content)
        return meta_data

    def get_file_hashes(self):
        hashes = []

        # get all objects with .nc extension in bucket
        objects = self.bucket.objects.all()
        files = [obj.key for obj in objects if obj.key.endswith('.nc')]

        # calculate hash for each file and add to hashes list
        for file in files:
            response = self.bucket.Object(file).get()
            hasher = hashlib.sha256()
            hasher.update(response['Body'].read())
            hashes.append(hasher.hexdigest())
        return hashes

    def _get_metadata(self):
        try:
            with self.bucket.Object(self.meta_file).get() as f:
                metadata = json.loads(f.read().decode('utf-8'))
                return metadata
        except Exception:
            return {}

    def _generate_hash(self, file):
        hasher = hashlib.sha256()
        with open(file, 'rb') as f:
            buf = f.read()
            hasher.update(buf)
        return hasher.hexdigest()

    def upload(self, file_path):
        # generate unique hash for file
        file_hash = self._generate_hash(file_path)

        # get file name from path
        file_name = os.path.basename(file_path)

        # check if file with same hash already exists
        for f in self.get_file_hashes():
            if f == file_hash:
                print(f"The file {file_name} already exists with the same hash {file_hash}.")
                list_of_files = json.dumps(self.list_files())
                print(list_of_files)
                return

        # upload file to bucket with client and project metadata
        metadata_tags = {'client': self.client, 'study': self.study}
        with open(file_path, 'rb') as f:
            self.bucket.put_object(Body=f, Key=file_hash + '.nc', Metadata=metadata_tags)

        # add file metadata to metadata file with hash as key
        metadata = self._get_metadata()
        metadata[file_hash] = {'client': self.client, 'study': self.study}

        # write updated metadata file
        upload_response = self.bucket.put_object(Body=json.dumps(metadata), Key=self.meta_file)
        print(f"{file_name} uploaded successfully. File hash {file_hash} ")


def main():
    parser = argparse.ArgumentParser(
        prog="Puploader",
        description='A command line tool to upload .nc files to the Polarplot dedicated S3 bucket',
        epilog="Copyright: D-ICE ENGINEERING"
    )

    parser.add_argument('--study', type=str, help='Study name')
    parser.add_argument('--client', type=str, help='Client name')
    parser.add_argument('--list', action='store_true', help='List all uploaded files')
    parser.add_argument('--json', action='store_true', help='Output list as JSON')
    parser.add_argument('file', nargs='?', help='File to upload')

    args = parser.parse_args()
    print(args)

    puploader = Puploader(args.study, args.client)

    if args.list:
        files = puploader.list_files()
        if args.json:
            print(json.dumps(files))
        else:
            for hash, meta in files.items():
                # f = json.loads(f)
                print("Key : {}".format(hash))
                print(f"hash={hash} (study={meta['study']}, client={meta['client']})")
    elif args.file:
        puploader.upload(args.file)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
