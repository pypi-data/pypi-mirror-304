import subprocess
import json


def rsync_with_includes(remote_server, source, destination, includes):
    with open('/tmp/includes.txt', 'w') as f:
        f.write("\n".join(includes))

    include_opt = ["--include-from=/tmp/includes.txt"]
    exclude_opt = ["--exclude=*"]

    rsync_command = ["rsync", "-avz"] + include_opt + exclude_opt + [f"{remote_server}:{source}/", destination]

    result = subprocess.run(rsync_command)
    if result.returncode != 0:
        raise Exception("rsync failed")


def sync_metadata_and_files(remote_server, project_name, remote_metadata_path, store_dir, remote_store_dir):
    local_metadata_path = 'titanic-metadata.json'

    subprocess.run(["rsync", "-avz", f"{remote_server}:{remote_metadata_path}", local_metadata_path])

    with open(local_metadata_path, 'r') as f:
        metadata = json.load(f)

    includes = [file_info['hash'] for file_info in metadata['files']]

    rsync_with_includes(remote_server, remote_store_dir, store_dir, includes)
