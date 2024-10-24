import os
import boto3
import json
import pandas as pd
import awswrangler as wr
from pathlib import Path
from botocore.exceptions import ClientError

class AWSStorage:
    """
    A class to interact with AWS S3 storage.

    This class provides methods to initialize an AWS S3 client and fetch details of documents
    stored in an S3 bucket. It uses the Boto3 library to interface with AWS services.

    Attributes:
        s3_client (boto3.client): The S3 client instance for performing S3 operations.
    """
    def __init__(self):
        """
        Initialize AWS S3 client for interacting with S3 storage.
        
        This method creates an S3 client instance using Boto3, which allows for various
        operations on S3 buckets and objects.
        """
        self.s3_client = boto3.client('s3')
        print("Initialized AWS S3 client for interacting with S3 storage.")

    def get_document_details(self, bucket_name, prefix='', file_type=None):
        """
        Fetches details of documents from an AWS S3 bucket with a specific prefix and file type.

        This method retrieves the names, hashes, and sizes of documents in the specified
        S3 bucket, filtering by optional prefix and file type.

        Parameters:
            bucket_name (str): The name of the S3 bucket from which to retrieve documents.
            prefix (str, optional): The folder prefix within the S3 bucket to filter results. 
                                    Defaults to '' (all objects in the bucket).
            file_type (str, optional): The file extension (e.g., '.csv') to filter files. 
                                        Defaults to None (no filtering by file type).

        Returns:
            dict: A dictionary with document details including:
                  - document_name (str): The name of the document without extension.
                  - document_hash (str): The MD5 hash of the document (ETag).
                  - document_size (int): The size of the document in bytes.
                  - file_type (str or None): The file type used for filtering (if provided).

        Raises:
            Exception: If the S3 request fails or if the bucket does not exist.

        Examples:
            aws_service = AWSStorage()
            documents = aws_service.get_document_details('my-bucket', prefix='data/', file_type='.csv')
            print(documents)

        Notes:
            - The method excludes files containing 'fhir_data' in their name.
            - To use this class, ensure you have the Boto3 library installed and configured.
        """
        if not bucket_name:
            raise ValueError("Bucket name must not be empty.")

        print(f"Fetching document details from AWS S3: bucket={bucket_name}, prefix={prefix}, file_type={file_type}")
        
        # Initialize paginator for listing large sets of objects
        paginator = self.s3_client.get_paginator('list_objects_v2')
        document_details = {}

        try:
            # Paginate through all objects in the bucket with the specified prefix
            for page in paginator.paginate(Bucket=bucket_name, Prefix=prefix):
                if 'Contents' in page:
                    for obj in page['Contents']:
                        full_document_name = obj['Key']
                        
                        # Filter by file type and exclude unwanted files
                        if (file_type is None or full_document_name.endswith(file_type)) and 'fhir_data' not in full_document_name:
                            base_document_name = os.path.splitext(os.path.basename(full_document_name))[0]
                            document_size = obj['Size']
                            document_hash = obj['ETag'].strip('"')  # MD5 hash from S3 metadata

                            # Store document details
                            document_details[base_document_name] = {
                                'document_name': base_document_name,
                                'document_hash': document_hash,
                                'document_size': document_size,  
                                'file_type': file_type
                            }

        except ClientError as e:
            # Handle specific errors related to S3
            print(f"An error occurred: {e}")
            raise Exception(f"Failed to fetch documents from bucket '{bucket_name}': {e}")

        except Exception as e:
            # Handle any other exceptions
            print(f"An unexpected error occurred: {e}")
            raise Exception(f"An unexpected error occurred: {e}")

        return document_details
    
    def count_documents_in_storage(self, bucket_name, prefix='', file_extension=None):
        """
        Counts total and unique documents of a specific type in an S3 bucket or within a specific prefix (folder).

        This method also returns a list of document names that match the specified criteria.

        Args:
            s3_bucket_name (str): Name of the S3 bucket.
            s3_prefix (str, optional): Prefix to list objects within a specific folder. 
                                        Defaults to '' (all objects).
            file_extension (str, optional): File extension to filter by (e.g., 'xml' for XML files).

        Returns:
            tuple: A tuple containing:
                - total_count (int): The total number of documents found.
                - unique_count (int): The count of unique documents based on ETags.
                - document_names (list): A list of document names that match the criteria.

        Raises:
            Exception: If there is an error accessing S3 or if the bucket does not exist.

        Examples:
            total, unique, documents = aws_service.count_documents_in_s3_bucket('my-bucket', prefix='data/', file_extension='csv')
            print(total, unique, documents)
        """
        etags = set()
        total_count = 0
        document_names = []

        try:
            # Initialize paginator for handling more than 1000 objects
            paginator = self.s3_client.get_paginator('list_objects_v2')

            # Ensure the file extension starts with a dot
            if file_extension and not file_extension.startswith('.'):
                file_extension = '.' + file_extension

            # Create a PageIterator from the paginator
            page_iterator = paginator.paginate(Bucket=bucket_name, Prefix=prefix)

            # Loop through each page of results
            for page in page_iterator:
                if 'Contents' in page:
                    for obj in page['Contents']:
                        # Filter objects by file extension and exclude unwanted files
                        if (file_extension is None or obj['Key'].endswith(file_extension)) and 'fhir_data' not in obj['Key']:
                            total_count += 1
                            etags.add(obj['ETag'])
                            document_names.append(obj['Key'])  # Collect document names

        except ClientError as e:
            raise Exception(f"Error accessing S3: {str(e)}")
        except Exception as e:
            raise Exception(f"An unexpected error occurred: {str(e)}")

        # Unique count is the size of the set of ETags
        unique_count = len(etags)
        return total_count, unique_count, document_names
    
    def key_exists_in_storage(self, bucket_name, object_key, processing_info=None, key_to_set=None):
        """
        Check if an object exists in an S3 bucket.

        This method checks for the existence of an object in the specified S3 bucket by
        attempting to retrieve its metadata. If the object exists, it can optionally store
        the object's ETag in a provided dictionary.

        Args:
            bucket_name (str): The name of the S3 bucket to check.
            object_key (str): The key (name) of the object to check for existence.
            processing_info (dict, optional): A dictionary to store additional processing
                                            information. If provided, the ETag of the
                                            object will be stored under `key_to_set`.
                                            Defaults to None.
            key_to_set (str, optional): The key under which to store the ETag in
                                        `processing_info`. Defaults to None.

        Returns:
            bool: True if the object exists, False otherwise.

        Raises:
            Exception: If an error occurs during the request to S3.

        Examples:
            exists = key_exists_in_storage('my-bucket', 'path/to/my/object.txt')
            print(exists)  # True or False

            processing_info = {}
            exists = key_exists_in_storage('my-bucket', 'path/to/my/object.txt', processing_info, 'etag_key')
            if exists:
                print(processing_info['etag_key'])  # Prints the ETag of the object if it exists
        """
        try:
            response = self.s3_client.head_object(Bucket=bucket_name, Key=object_key)
            etag = response['ETag']
            if processing_info and key_to_set:
                processing_info[key_to_set] = etag.strip('"')
            return True
        except self.s3_client.exceptions.NoSuchKey:
            print(f"Object with key '{object_key}' does not exist in bucket '{bucket_name}'.")
            return False
        except Exception as e:
            print(f"Error checking for object '{object_key}' in bucket '{bucket_name}': {e}")
            return False

    def parquet_existence_check(self, bucket_name, patient_id, versions):
        """
        Check for the existence of a Parquet file in an S3 bucket for a given patient ID across specified versions.

        This function checks if the Parquet file associated with the specified patient ID 
        exists for any of the provided version numbers. It returns the highest version number 
        where the file is found.

        Args:
            bucket_name (str): The name of the S3 bucket where the Parquet files are stored.
            patient_id (str): The patient ID used to construct the S3 key for the file.
            versions (list): A list of version numbers (integers) to check for the existence of the file.

        Returns:
            int or None: The version number where the Parquet file exists, or None if no file is found.

        Raises:
            ValueError: If `versions` is empty or contains non-integer values.
            Exception: For any other errors encountered during S3 access.

        Examples:
            bucket = 'my-bucket'
            patient = 'patient_123'
            available_versions = [1, 2, 3]
            version_found = parquet_existence_check(bucket, patient, available_versions)
            if version_found is not None:
                print(f'File found for version: {version_found}')
            else:
                print('No file found for any version.')
        """
        # Validate input versions
        if not versions:
            raise ValueError("The 'versions' list must not be empty.")

        if not all(isinstance(v, int) for v in versions):
            raise ValueError("All elements in 'versions' must be integers.")

        # Sort the versions in descending order to check the latest versions first
        versions = sorted(versions, reverse=True)
        
        for version in versions:
            object_key = f"{patient_id}/v{version}/addr.parquet"  # Generate the S3 key for the file
            
            try:
                if self.key_exists_in_storage(bucket_name, object_key):
                    print(f'Parquet exists for Version: {version}')
                    return version  # Return the first version where the file exists
            except Exception as e:
                print(f"Error checking for file existence in bucket '{bucket_name}' for key '{object_key}': {e}")

        return None

    def load_parquet_file(self, bucket_name, object_key, environment, project_root):
        """
        Load a Parquet file from S3 or a local path into a Pandas DataFrame.

        This function attempts to load a Parquet file from an S3 bucket or from a local
        directory, depending on the specified environment. If the loading fails, it returns an empty
        DataFrame with default columns.

        Args:
            bucket_name (str): The name of the S3 bucket.
            object_key (str): The S3 key (path) of the Parquet file to load.
            environment (str): The current environment ('local' or 'production').
            project_root (str): The root path of the project for local file access.

        Returns:
            pd.DataFrame: A DataFrame containing the data from the Parquet file, or an empty
                        DataFrame with default columns if loading fails.

        Raises:
            ValueError: If the object_key is invalid.
            Exception: For any other errors encountered during file loading.

        Examples:
            df = load_parquet_file('my-bucket', 'path/to/file.parquet', 'production', '/path/to/project')
        """
        default_columns = ['section_name', 'document_id']
        s3_path = f's3://{bucket_name}/{object_key}'

        # Validate the object key
        if not object_key:
            print("Error: The 'object_key' must not be empty.")
            raise ValueError("The 'object_key' must not be empty.")

        try:
            if environment == "local":
                file_path = f'{project_root}/data/{object_key}'
                print(f"Loading Parquet file from local path: {file_path}")
                df = pd.read_parquet(path=file_path)
            else:
                print(f"Loading Parquet file from S3: {s3_path}")
                df = wr.s3.read_parquet(path=s3_path)
            return df

        except FileNotFoundError as e:
            print(f"Error: File not found: {e}")
            return pd.DataFrame(columns=default_columns)
        
        except Exception as e:
            print("Error: An unexpected error occurred while loading the Parquet file.")
            print(e)
            return pd.DataFrame(columns=default_columns)
        
    def load_json_from_storage(self, bucket_name, file_key):
        """
        Load a JSON file from S3 and return the parsed JSON object.

        This function retrieves a JSON file from the specified S3 bucket and parses its
        content into a Python dictionary. If the file does not exist or an error occurs,
        an empty dictionary is returned.

        Args:
            bucket_name (str): The name of the S3 bucket.
            file_key (str): The key (path) to the JSON file in S3.

        Returns:
            dict: The parsed JSON object, or an empty dictionary if an error occurs.

        Raises:
            ValueError: If the file_key is empty.

        Examples:
            json_data = load_json_from_s3('my-bucket', 'path/to/file.json')
        """
        # Validate the file key
        if not file_key:
            print("Error: The 'file_key' must not be empty.")
            raise ValueError("The 'file_key' must not be empty.")

        try:
            response = self.s3_client.get_object(Bucket=bucket_name, Key=file_key)

            # Read the content of the file and parse it as JSON
            json_content = response['Body'].read().decode('utf-8')
            json_data = json.loads(json_content)
            return json_data

        except self.s3_client.exceptions.NoSuchKey:
            print(f"The specified key '{file_key}' does not exist in the bucket '{bucket_name}'.")
            return {}
        
        except Exception as e:
            print(f"An unexpected error occurred while loading the JSON file: {e}")
            return {}
        
    def download_folder_from_storage(self, bucket_name, folder_prefix, local_folder):
        """
        Download all files from a specified S3 folder to a local directory.

        This function retrieves all objects in the specified S3 folder (prefix) and
        downloads them to the given local folder. If the local folder does not exist,
        it will be created.

        Args:
            bucket_name (str): The name of the S3 bucket.
            folder_prefix (str): The prefix (folder path) in S3 from which to download files.
            local_folder (str): The local directory to which files will be downloaded.

        Raises:
            ValueError: If the bucket_name or folder_prefix is empty.
            Exception: If any unexpected error occurs during the download process.

        Examples:
            download_s3_folder('my-bucket', 'path/to/folder/', '/local/path/')
        """
        # Validate input parameters
        if not bucket_name:
            raise ValueError("Bucket name must not be empty.")
        if not folder_prefix:
            raise ValueError("Folder prefix must not be empty.")

        print(f"Starting download from S3 bucket '{bucket_name}' with prefix '{folder_prefix}' to local folder '{local_folder}'.")

        # Ensure the local folder exists
        os.makedirs(local_folder, exist_ok=True)

        try:
            # List objects in the specified S3 folder
            response = self.s3_client.list_objects_v2(Bucket=bucket_name, Prefix=folder_prefix)
            
            if 'Contents' in response:
                total_files = len(response['Contents'])
                print(f"Found {total_files} files in S3 folder '{folder_prefix}'. Beginning download...")

                # Loop through all objects in the S3 folder
                for idx, obj in enumerate(response['Contents'], start=1):
                    key = obj['Key']
                    file_name = os.path.basename(key)  # Get the file name from the S3 object key
                    local_file_path = os.path.join(local_folder, file_name)  # Create the local file path

                    # Download the file from S3 to the local folder
                    print(f"Downloading file {idx}/{total_files}: '{file_name}' to '{local_file_path}'...")
                    self.s3_client.download_file(bucket_name, key, local_file_path)

                print(f"Download completed. {total_files} files downloaded to '{local_folder}'.")

            else:
                print(f"No files found in the specified S3 folder '{folder_prefix}'.")

        except Exception as e:
            print(f"An error occurred during the download process: {e}")

    def generate_signed_url(self, bucket_name, object_key, expiration_time=3600):
        """
        Generate a presigned URL to retrieve an object from an S3 bucket.

        This function creates a presigned URL that allows users to retrieve a specific 
        object from an S3 bucket without requiring direct access to the AWS credentials.
        
        Parameters:
        - bucket_name (str): The name of the S3 bucket.
        - object_key (str): The key (file path) of the object in the S3 bucket.
        - expiration_time (int, optional): The time in seconds for the presigned URL 
        to remain valid (default is 3600 seconds = 1 hour).

        Returns:
        - str: A presigned URL for accessing the specified S3 object.

        Raises:
        - ValueError: If either bucket_name or object_key is not provided.
        - botocore.exceptions.ClientError: If an error occurs when generating the presigned URL.

        Example:
            url = generate_signed_url('my-bucket', 'folder/myfile.txt', expiration_time=1800)
            print(url)

        Notes:
        - Ensure that the AWS credentials used have sufficient permissions to generate
        presigned URLs for S3 objects.
        """
        
        # Ensure bucket_name and object_key are provided
        if not bucket_name:
            raise ValueError("Bucket name is required.")
        if not object_key:
            raise ValueError("Object key is required.")

        try:
            # Generate the presigned URL for the specified object
            pre_signed_url = self.s3_client.generate_presigned_url(
                ClientMethod="get_object",
                Params={
                    "Bucket": bucket_name,
                    "Key": object_key
                },
                ExpiresIn=expiration_time  # URL expiration time in seconds (default 1 hour)
            )
            return pre_signed_url

        except self.s3_client.exceptions.NoSuchBucket:
            print(f"Error: The bucket '{bucket_name}' does not exist.")
            return None
        except self.s3_client.exceptions.NoSuchKey:
            print(f"Error: The object '{object_key}' does not exist in the bucket '{bucket_name}'.")
            return None
        except Exception as e:
            print(f"An error occurred while generating the presigned URL: {e}")
            return None

    def save_data_and_get_signed_url(self, bucket_name, file_name, result, environment, local_dir_path):
        """
        Save a JSON object either locally or to S3, and generate a presigned URL for the S3 object.

        Parameters:
        - bucket_name (str): The name of the S3 bucket where the file will be stored.
        - file_name (str): The name (key) of the file to save in S3 or locally.
        - result (dict): The JSON object to save.
        - environment (str): The current environment ('local' or 's3').
        - local_dir_path (str): The local directory path to save the file if the environment is 'local'.

        Returns:
        - tuple:
            - If environment is 'local':
            ('local', None)
            - If environment is 's3':
            - str: Presigned URL for accessing the file in S3.
            - str: The file's ETag (hash) from S3.
            - int: The file's size in bytes.
        
        Raises:
        - ValueError: If required parameters are missing or invalid.
        - botocore.exceptions.ClientError: If an error occurs while uploading to or retrieving from S3.

        Example:
            result_data = {"key": "value"}
            url, file_hash, file_size = save_data_and_get_signed_url(
                'my-bucket', 'data/result.json', result_data, environment='s3', local_dir_path='/tmp')
        """
        
        # Handle local environment
        if environment == 'local':
            try:
                local_path = f"{local_dir_path}/output/{'/'.join(file_name.split('/')[:-1])}"
                Path(local_path).mkdir(parents=True, exist_ok=True)
                with open(f'{local_dir_path}/output/{file_name}', 'w', encoding='utf-8') as f:
                    json.dump(result, f, ensure_ascii=False)
                return 'local', None
            except Exception as e:
                print(f"Error saving file locally: {e}")
                return None, None
        try:
            response = self.s3_client.put_object(
                Bucket=bucket_name,
                Body=json.dumps(result),
                Key=file_name
            )
            file_hash = response.get('ETag').strip('"')

            # Get the file size from the S3 object metadata
            file_info = self.s3_client.head_object(Bucket=bucket_name, Key=file_name)
            file_size = file_info['ContentLength']

            # Get a presigned URL for the uploaded file
            url = self.generate_signed_url(bucket_name, file_name)

            # Return the presigned URL, file hash, and file size
            return url, file_hash, file_size

        except self.s3_client.exceptions.NoSuchBucket:
            print(f"Error: The bucket '{bucket_name}' does not exist.")
            return None, None, None
        except self.s3_client.exceptions.ClientError as e:
            print(f"S3 ClientError: {e}")
            return None, None, None
        except Exception as e:
            print(f"An error occurred while saving to S3: {e}")
            return None, None, None

    def download_ml_models(self, processing_info, bucket_name, s3_dir_path, local_dir_path):
        """
        Downloads all model files for a specific version from an S3 bucket.

        Args:
        - processing_info (dict): Dictionary containing processing metadata, including model version.
        - bucket_name (str): Name of the S3 bucket.
        - s3_dir_path (str): Path in the S3 bucket where models are stored (e.g., 'Summary_Models/').
        - local_dir_path (str): Local directory where the files will be downloaded.

        Returns:
        - bool: True if any model files were downloaded, False if no download was required.
        """
        model_download_required = False

        # Ensure the local directory exists
        try:
            os.makedirs(local_dir_path, exist_ok=True)
        except Exception as e:
            print(f"Error creating local directory '{local_dir_path}': {e}")
            return False

        # List objects in the specified S3 directory
        paginator = self.s3_client.get_paginator('list_objects_v2')
        pages = paginator.paginate(Bucket=bucket_name, Prefix=s3_dir_path)

        # Loop through the S3 objects and download relevant files
        for page in pages:
            for obj in page.get('Contents', []):
                key = obj['Key']
                
                # Check if the key matches the specified version
                if f"/{processing_info['summary_version']}/" in key:
                    filename = os.path.basename(key)  # Extract filename from key
                    local_file_path = os.path.join(local_dir_path, filename)
                    
                    # Ensure local directories exist
                    try:
                        os.makedirs(os.path.dirname(local_file_path), exist_ok=True)
                    except Exception as e:
                        print(f"Error creating directories for '{local_file_path}': {e}")
                        continue
                    
                    # Check if the file already exists locally
                    if not os.path.exists(local_file_path):
                        try:
                            # Download the file from S3
                            print(f"Downloading {filename} from S3 bucket {bucket_name}...")
                            self.s3_client.download_file(bucket_name, key, local_file_path)
                            print(f"Downloaded '{filename}' to '{local_file_path}'.")
                            model_download_required = True
                        except Exception as e:
                            print(f"Error downloading '{filename}': {e}")
                    else:
                        print(f"File '{filename}' already exists locally, skipping download.")
        
        return model_download_required
    
    def load_json_metadata(self, person_id, version, json_metadata_path):
        """
        Loads metadata for a person from three parquet files: trident changes, MR metadata, and HR metadata.

        Args:
            person_id (str): The ID of the person.
            version (str): The version of the metadata.
            json_metadata_path (str): The base S3 path where JSON metadata is stored.

        Returns:
            tuple: Three DataFrames (trident_changes_metadata_df, hr_metadata_df, mr_metadata_df)
        """
        # Define S3 object keys
        trident_changes_metadata_object_key = f"{version}/trident_changes/{person_id}_trident-changes.parquet"
        mr_object_key = f"{version}/mr_metadata_info/{person_id}_mr-metadata.parquet"
        hr_object_key = f"{version}/hr_metadata_info/{person_id}_hr-metadata.parquet"
        
        # Define expected columns for each DataFrame
        trident_changes_columns = ['person_id', 'document_id', 'org_id', 'org_name', 'section_name', 'section_code', 
                                'original_column', 'destination_column', 'changes_type', 'overlapping_count', 
                                'predicted_scores', 'row_count', 'rows_below_95', 'top_5_predictions', 
                                'merge_status', 'is_unknown', 'create_date']
        mr_metadata_columns = ['document_id', 'section_name', 'row_count', 'create_date']
        hr_metadata_columns = ['document_id', 'section_name', 'row_count', 'unknown_section', 'create_date']
        
        # Helper function to load a parquet file or return an empty DataFrame
        def load_parquet_or_empty(s3_path, columns):
            if self.key_exists_in_storage(json_metadata_path, s3_path):
                try:
                    return pd.read_parquet(f"s3://{json_metadata_path}/{s3_path}")
                except Exception as e:
                    print(f"Error loading parquet file '{s3_path}': {e}")
                    return pd.DataFrame(columns=columns)
            else:
                return pd.DataFrame(columns=columns)

        # Load metadata
        trident_changes_metadata_df = load_parquet_or_empty(trident_changes_metadata_object_key, trident_changes_columns)
        mr_metadata_df = load_parquet_or_empty(mr_object_key, mr_metadata_columns)
        hr_metadata_df = load_parquet_or_empty(hr_object_key, hr_metadata_columns)

        return trident_changes_metadata_df, hr_metadata_df, mr_metadata_df

    def save_json_metadata(self, processing_info, trident_changes_metadata_df, hr_metadata_df, mr_metadata_df, json_metadata_path):
        """
        Save metadata DataFrames to S3 as parquet files.

        This method takes three metadata DataFrames and stores them as parquet files
        in the specified S3 location. Each file is saved under a directory structure
        that includes the summary version and person ID to uniquely identify the data.

        Args:
            processing_info (dict): A dictionary containing information about the processing.
                Expected keys:
                    - 'summary_version' (str): The version of the summary.
                    - 'person_id' (str): The ID of the person whose metadata is being saved.
            trident_changes_metadata_df (pd.DataFrame): DataFrame containing metadata for trident changes.
            hr_metadata_df (pd.DataFrame): DataFrame containing HR metadata information.
            mr_metadata_df (pd.DataFrame): DataFrame containing MR metadata information.
            json_metadata_path (str): The base S3 path where JSON metadata files will be stored.

        Example:
            processing_info = {'summary_version': 'v1', 'person_id': '12345'}
            json_metadata_path = "my-s3-bucket/metadata"
            save_json_metadata(processing_info, trident_df, hr_df, mr_df, json_metadata_path)

        Raises:
            Exception: If an error occurs during the saving process to S3.
        """
        summary_version = processing_info['summary_version']
        person_id = processing_info['person_id']

        try:
            trident_changes_metadata_df.to_parquet(
                f"s3://{json_metadata_path}/{summary_version}/trident_changes/{person_id}_trident-changes.parquet")
            print(f"Trident changes metadata saved for {person_id} in version {summary_version}.")

            hr_metadata_df.to_parquet(
                f"s3://{json_metadata_path}/{summary_version}/hr_metadata_info/{person_id}_hr-metadata.parquet")
            print(f"HR metadata saved for {person_id} in version {summary_version}.")

            mr_metadata_df.to_parquet(
                f"s3://{json_metadata_path}/{summary_version}/mr_metadata_info/{person_id}_mr-metadata.parquet")
            print(f"MR metadata saved for {person_id} in version {summary_version}.")
            
        except Exception as e:
            print(f"An error occurred while saving metadata for {person_id}: {e}")

    def add_unknown_sections(self, bucket_name, prefix, section_column_df):
        """
        Add unknown sections from S3 parquet files to the section_column_df DataFrame.

        This function checks for parquet files in the specified S3 bucket and prefix.
        It identifies any unknown sections (i.e., sections not already present in the
        provided DataFrame `section_column_df`) and adds them. Section names are extracted
        from the parquet filenames that end with '_text.parquet', and the corresponding
        section codes are also parsed where available.

        Args:
            bucket_name (str): The name of the S3 bucket containing the parquet files.
            prefix (str): The S3 prefix used to filter relevant parquet files.
            section_column_df (pd.DataFrame): A DataFrame with existing section names and codes.

        Returns:
            pd.DataFrame: Updated DataFrame with added unknown sections (if found).

        Raises:
            Exception: If there is any error while interacting with S3 or processing the files.
        """
        try:
            response = self.s3_client.list_objects_v2(Bucket=bucket_name, Prefix=prefix)

            for obj in response.get('Contents', []):
                if obj['Key'].endswith('_text.parquet'):
                    section_file = obj['Key'].split('/')[-1].replace('.parquet', '')

                    # Check if the section file is already in the DataFrame
                    if section_file not in section_column_df['hr_table_name'].values:
                        try:
                            section_name, codes = section_file.split('_(')
                            codes = codes.split(')_text')[0]
                        except ValueError:
                            section_name = section_file.replace('_text', '')
                            codes = ''

                        # Add the unknown section to the DataFrame
                        new_entry = {
                            'section_name': f"unknown {section_name}",
                            'hr_table_name': section_file,
                            'codes': json.dumps([codes])
                        }
                        section_column_df.loc[len(section_column_df)] = new_entry

                        print(f"Added new unknown section: {new_entry}")

            print("All objects processed.")
            return section_column_df

        except Exception as e:
            print(f"An error occurred while adding unknown sections: {e}")
            return section_column_df