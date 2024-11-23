import os


def upload_csv_path(instance, filename):
    return os.path.join('uploads/', f"user_{instance.user.id}/{filename}")
