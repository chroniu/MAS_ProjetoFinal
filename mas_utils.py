# https://stackoverflow.com/questions/4409502/directory-transfers-on-paramiko
import os
import tarfile
import zipfile
import errno
import stat
import shutil
import six

def download_files(sftp_client, remote_dir, local_dir, files_download):
    if not exists_remote(sftp_client, remote_dir):
        return

    if not os.path.exists(local_dir):
        os.mkdir(local_dir)

    for filename in files_download:#sftp_client.listdir(remote_dir):
        if stat.S_ISDIR(sftp_client.stat(remote_dir + filename).st_mode):
            # uses '/' path delimiter for remote server
            download_file(sftp_client, remote_dir + filename + '/', os.path.join(local_dir, filename))
        else:
            if not os.path.isfile(os.path.join(local_dir, filename)):
                sftp_client.get(remote_dir + filename, os.path.join(local_dir, filename))

def exists_remote(sftp_client, path):
    try:
        sftp_client.stat(path)
    except (IOError) as  e:
        print(e)
        if e.errno == errno.ENOENT:
            return False
        raise
    else:
        return True

# from keras
def _extract_archive(file_path, path='.', archive_format='auto'):
    """Extracts an archive if it matches tar, tar.gz, tar.bz, or zip formats.
    # Arguments
        file_path: path to the archive file
        path: path to extract the archive file
        archive_format: Archive format to try for extracting the file.
            Options are 'auto', 'tar', 'zip', and None.
            'tar' includes tar, tar.gz, and tar.bz files.
            The default 'auto' is ['tar', 'zip'].
            None or an empty list will return no matches found.
    # Returns
        True if a match was found and an archive extraction was completed,
        False otherwise.
    """
    if archive_format is None:
        return False
    if archive_format is 'auto':
        archive_format = ['tar', 'zip']
    if isinstance(archive_format, six.string_types):
        archive_format = [archive_format]

    for archive_type in archive_format:
        if archive_type is 'tar':
            open_fn = tarfile.open
            is_match_fn = tarfile.is_tarfile
        if archive_type is 'zip':
            open_fn = zipfile.ZipFile
            is_match_fn = zipfile.is_zipfile

        if is_match_fn(file_path):
            with open_fn(file_path) as archive:
                try:
                    archive.extractall(path)
                except (tarfile.TarError, RuntimeError,
                        KeyboardInterrupt):
                    if os.path.exists(path):
                        if os.path.isfile(path):
                            os.remove(path)
                        else:
                            shutil.rmtree(path)
                    raise
            return True
    return False

def extract_files(directory, to_directory, files_set):
    for root, dirs, files in os.walk(directory):
        for file in files_set:
            if file.endswith('.tar.bz'):
                print('extracting file', file)
                _extract_archive(root+'/'+file, path=to_directory)
