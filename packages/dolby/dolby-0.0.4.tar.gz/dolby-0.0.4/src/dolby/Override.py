import uuid
from icrawler import ImageDownloader


class FileName(ImageDownloader):
    """
    Custom ImageDownloader for icrawler that generates unique filenames for downloaded images.
    """

    def get_filename(self, task, default_ext) -> str:
        """
        Overrides the default get_filename method to generate a unique filename using a UUID and the file extension.

        Args:
            task (dict): A dictionary containing the task information.
            default_ext (str): The default file extension for the downloaded image.

        Returns:
            str: A unique filename for the downloaded image.
        """
        filename = super(FileName, self).get_filename(
            task, default_ext)
        ext = filename.split('.')[-1]
        return f"{str(uuid.uuid4())}.{ext}"
