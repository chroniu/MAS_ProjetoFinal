# https://stackoverflow.com/questions/4409502/directory-transfers-on-paramiko
import os
import tarfile
import zipfile
import errno
import stat

def download_files(sftp_client, remote_dir, local_dir):
    if not exists_remote(sftp_client, remote_dir):
        return

    if not os.path.exists(local_dir):
        os.mkdir(local_dir)

    for filename in sftp_client.listdir(remote_dir):
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


def extract_files(path, to_directory='.'):
    if path.endswith('.zip'):
        opener, mode = zipfile.ZipFile, 'r'
    elif path.endswith('.tar.gz') or path.endswith('.tgz'):
        opener, mode = tarfile.open, 'r:gz'
    elif path.endswith('.tar.bz2') or path.endswith('.tbz'):
        opener, mode = tarfile.open, 'r:bz2'
    else:
        raise ValueError, "Could not extract `%s` as no appropriate extractor is found" % path

    cwd = os.getcwd()
    os.chdir(to_directory)

    try:
        file = opener(path, mode)
        try: file.extractall()
        finally: file.close()
    finally:
        os.chdir(cwd)
