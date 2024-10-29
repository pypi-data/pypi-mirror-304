"""Module to handle dataset-related operations within a project."""
import os
import sys

import requests
from matrice.utils import handle_response
from datetime import datetime, timedelta


def get_dataset_size(session, url, project_id):
    """
    Fetch the size of the dataset from the given URL.

    Parameters
    ----------
    url : str
        The URL of the dataset to fetch the size for.

    Returns
    -------
    tuple
        A tuple containing three elements:
        - API response (dict): The raw response from the API.
        - error_message (str or None): Error message if an error occurred, None otherwise.
        - status_message (str): A status message indicating success or failure.

    Example
    -------
    >>> size, err, msg = dataset.get_dataset_size(url="")
    >>> if err:
    >>>     print(f"Error: {err}")
    >>> else:
    >>>     print(f"Dataset size: {size} MB")
    """
    path = f"/v1/dataset/get_dataset_size_in_mb_from_url?projectId={project_id}"
    requested_payload = {"datasetUrl": url}
    headers = {"Content-Type": "application/json"}
    resp = session.rpc.post(path=path, headers=headers, payload=requested_payload)

    return handle_response(
        resp, f"Dataset size fetched successfully", "Could not fetch dataset size"
    )


def upload_file(session, file_path):
    """
    Upload a file to the dataset. Only Zip files are supported for upload.

    Parameters
    ----------
    file_path : str
        The local file path of the file to upload.

    Returns
    -------
    dict
    A dictionary containing three elements:
    - API response (data): The URL of the uploaded file if successful, otherwise an empty string.
    - error_message (str or None): Error message if an error occurred, None otherwise.
    - status_message (str): A status message indicating success or failure.

    Example
    -------
    >>> result = dataset.upload_file(file_path="path/to/data.zip")
    >>> if result['success']:
    >>>     print(f"File uploaded successfully: {result['data']}")
    >>> else:
    >>>     print(f"Error: {result['message']}")
    """
    file_name = os.path.basename(file_path)
    upload_url, error, message = _get_upload_path(session, file_name)

    if error is not None:
        return {"success": False, "data": "", "message": message}

    with open(file_path, "rb") as file:
        response = requests.put(upload_url, data=file)

    if response.status_code == 200:
        return {
            "success": True,
            "data": upload_url.split("?")[0],
            "message": "File uploaded successfully",
        }
    else:
        return {
            "success": False,
            "data": "",
            "message": response.json().get("message", "Network Error"),
        }


def _get_upload_path(session, file_name):
    """
    Get the upload path for a given file name.

    Parameters
    ----------
    file_name : str
        The name of the file to get the upload path for.

    Returns
    -------
    tuple
        A tuple containing three elements:
        - API response (dict): The raw response from the API.
        - error_message (str or None): Error message if an error occurred, None otherwise.
        - status_message (str): A status message indicating success or failure.

    Example
    -------
    >>> resp, err, msg = dataset._get_upload_path(file_name="data.zip")
    >>> if err:
    >>>     print(f"Error: {err}")
    >>> else:
    >>>     print(f"Upload Path: {resp}")
    """
    path = f"/v1/dataset/upload-path?fileName={file_name}"
    resp = session.rpc.get(path=path)
    return handle_response(
        resp, "Upload Path fetched successfully", "Could not fetch upload path"
    )


class Dataset:
    """Class to handle dataset-related operations within a project.

    Please provide either of dataset name or dataset id during class initialization.


    Parameters
    ----------
    session : Session
        The session object that manages the connection to the server.
    dataset_id : str, optional
        The ID of the dataset (default is None).
    dataset_name : str
        The name of the dataset (default is an empty string).

    Example
    -------
    >>> session = Session(account_number="account_number")
    >>> dataset = Dataset(session=session_object,dataset_id=dataset_id,dataset_name=dataset_name)
    """

    def __init__(self, session, dataset_id=None, dataset_name=""):
        self.session = session
        self.project_id = session.project_id
        self.last_refresh_time = datetime.now()
        self.dataset_id = dataset_id
        self.dataset_name = dataset_name
        self.rpc = session.rpc
        assert dataset_id or dataset_name, "Either dataset_id or dataset_name must be provided"
            
        # Fetch dataset by name only if dataset_name is provided
        dataset_by_name = None
        if self.dataset_name is not None:
            dataset_by_name, err, msg = self._get_dataset_by_name()

            if dataset_by_name is None:
                raise ValueError(f"Annotation with name '{self.dataset_name}' not found.")

        # If both dataset_id and dataset_name are provided, check for mismatch
        if self.dataset_id is not None and self.dataset_name is not None:
            fetched_dataset_id = dataset_by_name['_id']
            
            if fetched_dataset_id != self.dataset_id:
                raise ValueError("Provided dataset_id does not match the dataset id of the provided dataset_name.")

        # If only dataset_name is provided, set dataset_id based on fetched dataset
        elif self.dataset_name is not None:
            self.dataset_id = dataset_by_name['_id']
        
        self.dataset_details, error, message = self._get_details()
        self.dataset_id = self.dataset_details['_id']
        self.dataset_name = self.dataset_details['name']
        self.version_status = self.dataset_details.get("stats", [{}])[0].get("versionStatus")
        self.latest_version = self.dataset_details['latestVersion']
        self.no_of_samples = sum(version['versionStats']['total'] for version in self.dataset_details.get('stats', []))
        self.no_of_classes = len(self.dataset_details.get('stats', [{}])[0].get('classStat', {}))
        self.no_of_versions = len(self.dataset_details.get('allVersions', []))
        self.last_updated_at = self.dataset_details.get('updatedAt')
        self.summary , err , message = self._get_summary(self.dataset_details['latestVersion'])


    def refresh(self):
        """
        Refresh the instance by reinstantiating it with the previous values.
        """
        # Check if two minutes have passed since the last refresh
        if datetime.now() - self.last_refresh_time < timedelta(minutes=2):
            raise Exception("Refresh can only be called after two minutes since the last refresh.")

        # Capture the current state
        state = self.__dict__.copy()

        init_params = {
        'session': self.session,
        'dataset_id': self.dataset_id,
    }

        # Reinitialize the instance
        self.__init__(**init_params)
        

        # Update the last refresh time
        self.last_refresh_time = datetime.now()
        
    def _get_details(self):
        """
        Retrieve dataset details based on the dataset ID or name set during class initialization.

        This method first attempts to fetch the dataset details using the dataset ID, if available.
        If the dataset ID is not provided, it will attempt to retrieve the details by the dataset name.
        If neither the dataset ID nor the dataset name is available, a ValueError is raised.

        Returns
        -------
        dict
            The detailed information of the dataset if found, either by ID or name.

        Raises
        ------
        ValueError
            If neither 'dataset_id' nor 'dataset_name' is provided.

        Examples
        --------
        >>> dataset_details = dataset.get_details()
        >>> if isinstance(dataset_details, dict):
        >>>     print("Dataset Details:", dataset_details)
        >>> else:
        >>>     print("Failed to retrieve dataset details.")

        Notes
        -----
        - `_get_dataset()` is called if 'dataset_id' is set and retrieves the dataset by its ID.
        - `_get_dataset_by_name()` is used if 'dataset_name' is set and fetches the dataset by its name.
        """
        id = self.dataset_id
        name = self.dataset_name

        if id:
            try:
                return self._get_dataset()
            except Exception as e:
                print(f"Error retrieving dataset by id: {e}")
        elif name:
            try:
                return self._get_dataset_by_name()
            except Exception as e:
                print(f"Error retrieving dataset by name: {e}")
        else:
            raise ValueError(
                "At least one of 'dataset_id' or 'dataset_name' must be provided."
            )

    def _get_summary(self, dataset_version):
        """
        Retrieve a summary for a specific dataset version.

        The user only needs to provide the dataset version, as the dataset ID and project ID are already set during initialization.

        Parameters
        ----------
        dataset_version : str
            The version of the dataset to fetch the summary for.

        Returns
        -------
        tuple
            A tuple containing three elements:
            - API response (dict): The raw response from the API.
            - error_message (str or None): Error message if an error occurred, None otherwise.
            - status_message (str): A status message indicating success or failure.

        Example
        -------
        >>> resp, err, msg = dataset._get_summary(dataset_version="v1.0")
        >>> if err:
        >>>     print(f"Error: {err}")
        >>> else:
        >>>     print(f"Dataset summary: {resp}")
        """
        if self.dataset_id is None:
            print(
                "Dataset id not set for this dataset. Cannot perform the operation for dataset without dataset id"
            )
            sys.exit(0)

        path = f"/v1/dataset/{self.dataset_id}/version/{dataset_version}/summary?projectId={self.project_id}"
        resp = self.rpc.get(path=path)

        return handle_response(
            resp,
            "Dataset summary fetched successfully",
            "Could not fetch dataset summary",
        )

    def _get_dataset(self):
        """
        Fetch the details of the dataset using dataset id. 

        Returns
        -------
        tuple
            A tuple containing three elements:
            - API response (dict): The raw response from the API.
            - error_message (str or None): Error message if an error occurred, None otherwise.
            - status_message (str): A status message indicating success or failure.

        Example
        -------
        >>> resp, err, msg = dataset._get_dataset()
        >>> if err:
        >>>     print(f"Error: {err}")
        >>> else:
        >>>     print(f"Dataset details: {resp}")
        """
        if self.dataset_id is None:
            print(
                "Dataset id not set for this dataset. Cannot perform the operation for dataset without dataset id"
            )
            sys.exit(0)

        path = f"/v1/dataset/{self.dataset_id}?projectId={self.project_id}"
        resp = self.rpc.get(path=path)

        return handle_response(
            resp, "Dataset fetched successfully", "Could not fetch dataset"
        )

    def get_categories(self, dataset_version):
        """
        Get the dataset categories details for a specific dataset version.

        Parameters
        ----------
        dataset_version : str
            The version of the dataset for which to fetch categories.

        Returns
        -------
        tuple
            A tuple containing three elements:
            - API response (dict): The raw response from the API.
            - error_message (str or None): Error message if an error occurred, None otherwise.
            - status_message (str): A status message indicating success or failure.

        Example
        -------
        >>> resp, err, msg = dataset.get_categories(dataset_version="v1.0")
        >>> if err:
        >>>     print(f"Error: {err}")
        >>> else:
        >>>     print(f"Categories: {resp}")
        """
        if self.dataset_id is None:
            print(
                "Dataset id not set for this dataset. Cannot perform the operation for dataset without dataset id"
            )
            sys.exit(0)

        path = f"/v1/dataset/{self.dataset_id}/version/{dataset_version}/categories?projectId={self.project_id}"
        resp = self.rpc.get(path=path)

        return handle_response(
            resp,
            f"Dataset categories for version - {dataset_version} fetched successfully",
            "Could not fetch dataset categories",
        )

    def _list_items_V2(self, dataset_version, page_size = 10, page_number = 0):
        """
        List all items for a specific version of the dataset.

        Parameters
        ----------
        dataset_version : str
            The version of the dataset for which to list items.

        Returns
        -------
        tuple
            A tuple containing three elements:
            - API response (dict): The raw response from the API.
            - error_message (str or None): Error message if an error occurred, None otherwise.
            - status_message (str): A status message indicating success or failure.

        Example
        -------
        >>> resp, err, msg = dataset._list_items_V2(dataset_version="v2.0", page_size = 10, page_number = 0)
        >>> if err:
        >>>     print(f"Error: {err}")
        >>> else:
        >>>     print(f"Dataset items: {resp}")
        """
        if self.dataset_id is None:
            print(
                "Dataset id not set for this dataset. Cannot perform the operation for dataset without dataset id"
            )
            sys.exit(0)

        path = f"v1/dataset/{self.dataset_id}/version/{dataset_version}/v2/item?Size={page_size}&pageNumber={page_number}&projectId={self.project_id}"
        resp = self.rpc.get(path=path)

        return handle_response(
            resp,
            f"Dataset items for version - {dataset_version} fetched successfully",
            "Could not fetch dataset items",
        )

    def list_items(self, dataset_version, page_size = 10, page_number = 0):
        """
        List all items for a specific version of the dataset. 

        Parameters
        ----------
        dataset_version : str
            The version of the dataset for which to list items.

        Returns
        -------
        tuple
            A tuple containing three elements:
            - API response (dict): The raw response from the API.
            - error_message (str or None): Error message if an error occurred, None otherwise.
            - status_message (str): A status message indicating success or failure.

        Example
        -------
        >>> resp, err, msg = dataset.list_items(dataset_version="v1.0",page_size = 10, page_number = 0)
        >>> if err:
        >>>     print(f"Error: {err}")
        >>> else:
        >>>     print(f"Items: {resp}")
        """
        if self.dataset_id is None:
            print(
                "Dataset id not set for this dataset. Cannot perform the operation for dataset without dataset id"
            )
            sys.exit(0)

        path = f"v1/dataset/{self.dataset_id}/version/{dataset_version}/v2/item?Size={page_size}&pageNumber={page_number}&projectId={self.project_id}"
        resp = self.rpc.get(path=path)

        return handle_response(
            resp,
            f"Dataset items for version - {dataset_version} fetched successfully",
            "Could not fetch dataset items",
        )

    def get_processed_versions(self):
        """
        Get all processed versions of the dataset. 

        Returns
        -------
        tuple
            A tuple containing three elements:
            - API response (dict): The raw response from the API.
            - error_message (str or None): Error message if an error occurred, None otherwise.
            - status_message (str): A status message indicating success or failure.

        Example
        -------
        >>> resp, err, msg = dataset.get_processed_versions()
        >>> if err:
        >>>     print(f"Error: {err}")
        >>> else:
        >>>     print(f"Processed Versions: {resp}")
        """
        if self.dataset_id is None:
            print(
                "Dataset id not set for this dataset. Cannot perform the operation for dataset without dataset id"
            )
            sys.exit(0)

        path = f"/v1/dataset/get_processed_versions?projectId={self.project_id}"
        resp = self.rpc.get(path=path)

        return handle_response(
            resp,
            f"Processed versions fetched successfully",
            "Could not fetch processed versions",
        )

    def check_valid_spilts(self, dataset_version):
        """
        Check whether the dataset version contains valid splits. The valid splits include train, test, and validation.

        Parameters
        ----------
        dataset_version : str
            The version of the dataset to check for valid splits.

        Returns
        -------
        tuple
            A tuple containing three elements:
            - API response (dict): The raw response from the API.
            - error_message (str or None): Error message if an error occurred, None otherwise.
            - status_message (str): A status message indicating success or failure.

        Example
        -------
        >>> resp, err, msg = dataset.check_valid_splits(dataset_version="v1.0")
        >>> if err:
        >>>     print(f"Error: {err}")
        >>> else:
        >>>     print(f"Splits Valid: {resp}")
        """
        if self.dataset_id is None:
            print(
                "Dataset id not set for this dataset. Cannot perform the operation for dataset without dataset id"
            )
            sys.exit(0)

        path = f"/v1/dataset/check_valid_spilts/{self.dataset_id}/{dataset_version}?projectId={self.project_id}"
        resp = self.rpc.get(path=path)

        return handle_response(resp, f"Splits are valid", "Splits are invalid")


    def _get_dataset_by_name(self):
        """
        Fetch the dataset details by using dataset name. 

        Returns
        -------
        tuple
            A tuple containing three elements:
            - API response (dict): The raw response from the API.
            - error_message (str or None): Error message if an error occurred, None otherwise.
            - status_message (str): A status message indicating success or failure.

        Example
        -------
        >>> resp, err, msg = dataset._get_dataset_by_name()
        >>> if err:
        >>>     print(f"Error: {err}")
        >>> else:
        >>>     print(f"Dataset Details: {resp}")
        """
        if self.dataset_name == "":
            print(
                "Dataset name not set for this dataset. Cannot perform the operation for dataset without dataset name"
            )
            sys.exit(0)

        path = f"/v1/dataset/get_dataset_by_name?datasetName={self.dataset_name}&projectId={self.project_id}"
        resp = self.rpc.get(path=path)
        return handle_response(
            resp,
            f"Dataset Details Fetched successfully",
            "Could not fetch dataset details",
        )

    
    # PUT REQUESTS

    def rename(self, updated_name):
        """
        Update the dataset name. 

        Parameters
        ----------
        updated_name : str
            The new name of the dataset.

        Returns
        -------
        tuple
            A tuple containing three elements:
            - API response (dict): The raw response from the API.
            - error_message (str or None): Error message if an error occurred, None otherwise.
            - status_message (str): A status message indicating success or failure.

        Example
        -------
        >>> resp, err, msg = dataset.update_name(updated_name="Updated Dataset Name")
        >>> if err:
        >>>     print(f"Error: {err}")
        >>> else:
        >>>     print(f"Dataset updated successfully: {resp}")
        """
        if self.dataset_id is None:
            print(
                "Dataset id not set for this dataset. Cannot perform the operation for dataset without dataset id"
            )
            sys.exit(0)

        path = f"/v1/dataset/{self.dataset_id}?projectId={self.project_id}"
        headers = {"Content-Type": "application/json"}
        body = {"name": updated_name}
        resp = self.rpc.put(path=path, headers=headers, payload=body)

        return handle_response(
            resp,
            f"Successfully updated dataset name to {updated_name}",
            "Could not update datename",
        )

    def update_item_label(self, dataset_version, item_id, label_id):
        """
        Update the label of a specific dataset item. 

        Parameters
        ----------
        dataset_version : str
            The version of the dataset.
        item_id : str
            The ID of the dataset item.
        label_id : str
            The ID of the new label to assign to the dataset item.

        Returns
        -------
        tuple
            A tuple containing three elements:
            - API response (dict): The raw response from the API.
            - error_message (str or None): Error message if an error occurred, None otherwise.
            - status_message (str): A status message indicating success or failure.

        Example
        -------
        >>> resp, err, msg = dataset.update_item_label(dataset_version="v1.0", item_id="12345", label_id="67890")
        >>> if err:
        >>>     print(f"Error: {err}")
        >>> else:
        >>>     print(f"Label updated successfully: {resp}")
        """
        if self.dataset_id is None:
            print(
                "Dataset id not set for this dataset. Cannot perform the operation for dataset without dataset id"
            )
            sys.exit(0)

        path = f"/v1/dataset/{self.dataset_id}/version/{dataset_version}/item/{item_id}/label?projectId={self.project_id}"
        headers = {"Content-Type": "application/json"}
        body = {"labelId": label_id}
        resp = self.rpc.put(path=path, headers=headers, payload=body)

        return handle_response(
            resp,
            "Update data item label in progress",
            "Could not update the date item label",
        )

    # POST REQUESTS
    def add_data(
        self,
        source,
        source_url,
        new_dataset_version,
        old_dataset_version,
        dataset_description="",
        version_description="",
        compute_alias="",
    ):
        """
        Import a new version of the dataset from an external source. Only Zip files are supported for upload.

        Parameters
        ----------
        source : str
            The source of the dataset.
        source_url : str
            The URL of the dataset to import.
        new_dataset_version : str
            The version number for the new dataset.
        old_dataset_version : str
            The version number of the existing dataset.
        dataset_description : str, optional
            The description of the dataset (default is an empty string).
        version_description : str, optional
            The description of the new dataset version (default is an empty string).
        compute_alias : str, optional
            The alias for the compute instance to be used (default is an empty string).

        Returns
        -------
        tuple
            A tuple containing three elements:
            - API response (dict): The raw response from the API.
            - error_message (str or None): Error message if an error occurred, None otherwise.
            - status_message (str): A status message indicating success or failure.

        Example
        -------
        >>> resp, err, msg = dataset.add_data(source="url", source_url="https://example.com/dataset.zip", new_dataset_version="v2.0", old_dataset_version="v1.0")
        >>> if err:
        >>>     print(f"Error: {err}")
        >>> else:
        >>>     print(f"Dataset import in progress: {resp}")
        """
        if self.dataset_id is None:
            print(
                "Dataset id not set for this dataset. Cannot perform the operation for dataset without dataset id"
            )
            sys.exit(0)

        dataset_resp, err, message = self._get_dataset()
        if err is not None:
            return dataset_resp, err, message

        stats = dataset_resp["stats"]
        if dataset_description == "":
            dataset_description = dataset_resp["datasetDesc"]

        for stat in stats:
            if stat["version"] != old_dataset_version:
                continue
            if stat["versionStatus"] != "processed":
                resp = {}
                err = None
                message = f"Only the dataset versions with complete status can be updated.Version {old_dataset_version} of the dataset doesn't have status complete."
                return resp, err, message

            if version_description == "" and old_dataset_version == new_dataset_version:
                version_description = stat["versionDescription"]
            break

        is_created_new = new_dataset_version == old_dataset_version
        path = f"v1/dataset/{self.dataset_id}/import?project={self.project_id}"
        headers = {"Content-Type": "application/json"}
        body = {
            "source": source,
            "sourceUrl": source_url,
            "isCreateNew": is_created_new,
            "isUnlabeled": False,
            "newDatasetVersion": new_dataset_version,
            "oldDatasetVersion": old_dataset_version,
            "newVersionDescription": version_description,
            "datasetDesc": dataset_description,
            "computeAlias": compute_alias,
        }
        resp = self.rpc.post(path=path, headers=headers, payload=body)

        return handle_response(
            resp,
            "New data item addition in progress",
            "An error occured while trying to add new data item.",
        )

    def split_data(
        self,
        old_dataset_version,
        new_dataset_version,
        is_random_split,
        train_num=0,
        val_num=0,
        test_num=0,
        transfers=[{"source": "", "destination": "", "transferAmount": 1}],
        dataset_description="",
        version_description="",
        new_version_description="",
        compute_alias="",
    ):
        """
        Split or transfer images between training, validation, and test sets in the datasets.

        Parameters
        ----------
        old_dataset_version : str
            The version of the existing dataset.
        new_dataset_version : str
            The version of the new dataset.
        is_random_split : bool
            Whether to perform a random split.
        train_num : int, optional
            Number of training samples (default is 0).
        val_num : int, optional
            Number of validation samples (default is 0).
        test_num : int, optional
            Number of test samples (default is 0).
        transfers : list,
            A list of transfer details .
        dataset_description : str, optional
            Description of the dataset (default is an empty string).
        version_description : str, optional
            Description of the dataset version (default is an empty string).
        new_version_description : str, optional
            Description of the new dataset version (default is an empty string).
        compute_alias : str, optional
            Compute instance alias (default is an empty string).

        Returns
        -------
        tuple
            A tuple containing three elements:
            - API response (dict): The raw response from the API.
            - error_message (str or None): Error message if an error occurred, None otherwise.
            - status_message (str): A status message indicating success or failure.

        Example
        -------
        >>> resp, err, msg = dataset.split_data(
                old_dataset_version="v1.0", new_dataset_version="v2.0",
                is_random_split=True, train_num=100, val_num=20, test_num=30, transfers=[{"source": "train", "destination": "test", "transferAmount": 100}] )
        >>> if err:
        >>>     print(f"Error: {err}")
        >>> else:
        >>>     print(f"Data split in progress: {resp}")
        """
        if self.dataset_id is None:
            print(
                "Dataset id not set for this dataset. Cannot perform the operation for dataset without dataset id"
            )
            sys.exit(0)

        dataset_resp, err, message = self._get_dataset()
        if err is not None:
            return dataset_resp, err, message

        stats = dataset_resp["stats"]
        if dataset_description == "":
            dataset_description = dataset_resp["datasetDesc"]

        for stat in stats:
            if stat["version"] != old_dataset_version:
                continue
            if stat["versionStatus"] != "processed":
                resp = {}
                err = None
                message = f"Only the dataset versions with complete status can be updated.Version {old_dataset_version} of the dataset doesn't have status complete."
                return resp, err, message

            if version_description == "" and old_dataset_version == new_dataset_version:
                version_description = stat["versionDescription"]
            break

        path = f"/v1/dataset/{self.dataset_id}/split_data?projectId={self.project_id}"
        headers = {"Content-Type": "application/json"}
        body = {
            "trainNum": train_num,
            "testNum": test_num,
            "valNum": val_num,
            "unassignedNum": 0,
            "oldDatasetVersion": old_dataset_version,
            "newDatasetVersion": new_dataset_version,
            "isRandomSplit": is_random_split,
            "datasetDesc": dataset_description,
            "newVersionDescription": new_version_description,
            "transfers": transfers,
            "computeAlias": compute_alias,
        }
        resp = self.rpc.post(path=path, headers=headers, payload=body)

        return handle_response(
            resp,
            "Dataset spliting in progress",
            "An error occured while trying to split the data.",
        )

    # DELETE REQUESTS
    def delete_item(self, dataset_version, dataset_item_ids):
        """
        Wrapper function to delete dataset items based on the dataset type detected from the dataset details.

        Parameters
        ----------
        dataset_version : str
            The version of the dataset from which to delete items.
        dataset_item_ids : list
            A list of dataset item IDs to delete.

        Returns
        -------
        tuple
            A tuple containing three elements:
            - API response (dict): The raw response from the API.
            - error_message (str or None): Error message if an error occurred, None otherwise.
            - status_message (str): A status message indicating success or failure.

        Example
        -------
        >>> resp, err, msg = dataset.delete_item(
                dataset_version="v1.0", dataset_item_ids=["123", "456"])
        >>> if err:
        >>>     print(f"Error: {err}")
        >>> else:
        >>>     print(f"Items deleted successfully: {resp}")
        """
        # Retrieve the dataset details to get the type
        resp, error, message = self._get_details()
        if error:
            return resp, error, message

        dataset_type = resp.get('type')
        
        # Check dataset type and call the respective delete function
        if dataset_type == "classification":
            return self._delete_item_classification(dataset_version, dataset_item_ids)
        elif dataset_type == "detection":
            return self._delete_item_detection(dataset_version, dataset_item_ids)
        else:
            return {}, f"Unsupported dataset type: {dataset_type}.", "Failed to delete dataset items"


    def _delete_item_classification(self, dataset_version, dataset_item_ids):
        """
        Delete classification dataset items.

        Parameters
        ----------
        dataset_version : str
            The version of the dataset from which to delete items.
        dataset_item_ids : list
            A list of dataset item IDs to delete.

        Returns
        -------
        tuple
            A tuple containing three elements:
            - API response (dict): The raw response from the API.
            - error_message (str or None): Error message if an error occurred, None otherwise.
            - status_message (str): A status message indicating success or failure.

        Example
        -------
        >>> resp, err, msg = dataset.delete_item_classification(
                dataset_version="v1.0", dataset_item_ids=["123", "456"])
        >>> if err:
        >>>     print(f"Error: {err}")
        >>> else:
        >>>     print(f"Items deleted successfully: {resp}")
        """
        if self.dataset_id is None:
            print(
                "Dataset id not set for this dataset. Cannot perform the operation for dataset without dataset id"
            )
            sys.exit(0)

        path = f"/v1/dataset/version/{dataset_version}/dataset_item_classification?projectId={self.project_id}&datasetId={self.dataset_id}"
        requested_payload = {"datasetItemIds": dataset_item_ids}
        headers = {"Content-Type": "application/json"}
        resp = self.rpc.delete(path=path, headers=headers, payload=requested_payload)

        return handle_response(
            resp,
            f"Given dataset items deleted successfully",
            "Could not delete the given dataset items",
        )

    def _delete_item_detection(self, dataset_version, dataset_item_ids):
        """
        Delete detection dataset items.

        Parameters
        ----------
        dataset_version : str
            The version of the dataset from which to delete items.
        dataset_item_ids : list
            A list of dataset item IDs to delete.

        Returns
        -------
        tuple
            A tuple containing three elements:
            - API response (dict): The raw response from the API.
            - error_message (str or None): Error message if an error occurred, None otherwise.
            - status_message (str): A status message indicating success or failure.

        Example
        -------
        >>> resp, err, msg = dataset.delete_item_detection(
                dataset_version="v1.0", dataset_item_ids=["123", "456"])
        >>> if err:
        >>>     print(f"Error: {err}")
        >>> else:
        >>>     print(f"Items deleted successfully: {resp}")
        """
        if self.dataset_id is None:
            print(
                "Dataset id not set for this dataset. Cannot perform the operation for dataset without dataset id"
            )
            sys.exit(0)

        path = f"/v1/dataset/version/{dataset_version}/dataset_item_detection?projectId={self.project_id}&datasetId={self.dataset_id}"
        requested_payload = {"datasetItemIds": dataset_item_ids}
        headers = {"Content-Type": "application/json"}
        resp = self.rpc.delete(path=path, headers=headers, payload=requested_payload)

        return handle_response(
            resp,
            f"Given dataset items deleted successfully",
            "Could not delete the given dataset items",
        )

    def delete_version(self, dataset_version):
        """
        Delete a specific version of the dataset. 

        Parameters
        ----------
        dataset_version : str
            The version of the dataset to delete.

        Returns
        -------
        tuple
            A tuple containing three elements:
            - API response (dict): The raw response from the API.
            - error_message (str or None): Error message if an error occurred, None otherwise.
            - status_message (str): A status message indicating success or failure.

        Example
        -------
        >>> resp, err, msg = dataset.delete_version(dataset_version="v1.0")
        >>> if err:
        >>>     print(f"Error: {err}")
        >>> else:
        >>>     print(f"Version deleted successfully: {resp}")
        """
        if self.dataset_id is None:
            print(
                "Dataset id not set for this dataset. Cannot perform the operation for dataset without dataset id"
            )
            sys.exit(0)

        path = f"/v1/dataset/{self.dataset_id}/version/{dataset_version}?projectId={self.project_id}"
        resp = self.rpc.delete(path=path)

        return handle_response(
            resp,
            f"Successfully deleted version - {dataset_version}",
            "Could not delete the said version",
        )

    def delete(self):
        """
        Delete the entire dataset. 

        Returns
        -------
        tuple
            A tuple containing three elements:
            - API response (dict): The raw response from the API.
            - error_message (str or None): Error message if an error occurred, None otherwise.
            - status_message (str): A status message indicating success or failure.

        Example
        -------
        >>> resp, err, msg = dataset.delete_dataset()
        >>> if err:
        >>>     print(f"Error: {err}")
        >>> else:
        >>>     print(f"Dataset deleted successfully: {resp}")
        """
        if self.dataset_id is None:
            print(
                "Dataset id not set for this dataset. Cannot perform the operation for dataset without dataset id"
            )
            sys.exit(0)

        path = f"/v1/dataset/{self.dataset_id}?projectId={self.project_id}"
        resp = self.rpc.delete(path=path)

        return handle_response(
            resp, f"Successfully deleted the dataset", "Could not delete the dataset"
        )


