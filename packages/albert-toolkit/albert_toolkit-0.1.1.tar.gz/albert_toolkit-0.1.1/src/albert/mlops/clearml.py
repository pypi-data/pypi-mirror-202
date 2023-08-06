from clearml import Task, Dataset, StorageManager


class ClearML:
    def __init__(self, task_name, project_name=None, task_type=None):
        """
        Initialize a new ClearML task with the given task name, project name, and task type.

        :param task_name: str, the name of the task.
        :param project_name: str, the name of the project (default: None).
        :param task_type: str, the type of the task (default: None).
        """
        self.task = Task.init(task_name=task_name, project_name=project_name, task_type=task_type)

    def create_dataset(self, dataset_name):
        """
        Create a new ClearML dataset with the given name.

        :param dataset_name: str, the name of the dataset.
        :return: Dataset, the newly created dataset.
        """
        return Dataset.create(dataset_name)

    def get_dataset(self, dataset_id):
        """
        Retrieve a ClearML dataset by its ID.

        :param dataset_id: str, the ID of the dataset.
        :return: Dataset, the retrieved dataset.
        """
        return Dataset.get(dataset_id)

    def upload_file(self, local_path, remote_path):
        """
        Upload a file from the local file system to the remote storage.

        :param local_path: str, the path to the local file.
        :param remote_path: str, the path to the remote file.
        :return: str, the URL of the uploaded file.
        """
        return StorageManager.upload(local_path=local_path, remote_path=remote_path)

    def download_file(self, remote_path, local_path):
        """
        Download a file from the remote storage to the local file system.

        :param remote_path: str, the path to the remote file.
        :param local_path: str, the path to the local file.
        """
        return StorageManager.download(remote_path=remote_path, local_path=local_path)

# clearml = ClearML(task_name='my_task', project_name='my_project', task_type='training')
#
# dataset = clearml.create_dataset('my_dataset')
# file_path = clearml.upload_file('local_path', 'remote_path')
