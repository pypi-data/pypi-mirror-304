import json
import os
import shutil
from rich.progress import Progress
from .utils import hash_file, load_ignore_patterns, should_ignore


def add_to_store(app_dir, store_dir, ignore_file=None):
    metadata = {'files': []}

    os.makedirs(store_dir, exist_ok=True)

    if ignore_file is None:
        ignore_file = os.path.join(app_dir, '.titanic-ignore')

    ignore_patterns = load_ignore_patterns(ignore_file)

    all_files = []
    for root, _, files in os.walk(app_dir):
        for file in files:
            filepath = os.path.join(root, file)
            relative_path = os.path.relpath(filepath, app_dir)
            all_files.append((filepath, relative_path))

    with Progress() as progress:
        task = progress.add_task("[green]Adding files to store...", total=len(all_files))

        for filepath, relative_path in all_files:
            if should_ignore(relative_path, ignore_patterns):
                progress.update(task, advance=1)
                continue

            file_hash = hash_file(filepath)
            store_path = os.path.join(store_dir, file_hash)

            if not os.path.exists(store_path):
                shutil.copy(filepath, store_path)

            metadata['files'].append({
                'original_path': relative_path,
                'hash': file_hash
            })

            progress.update(task, advance=1)

    with open('titanic-metadata.json', 'w') as f:
        json.dump(metadata, f, indent=2)


def recreate_from_store(metadata_path, output_dir, store_dir):
    with open(metadata_path, 'r') as f:
        metadata = json.load(f)

    files_to_process = metadata['files']

    os.makedirs(output_dir, exist_ok=True)

    with Progress() as progress:
        task = progress.add_task("[green]Recreating project from store...", total=len(files_to_process))

        for file_info in files_to_process:
            dest_path = os.path.join(output_dir, file_info['original_path'])
            source_path = os.path.join(store_dir, file_info['hash'])

            os.makedirs(os.path.dirname(dest_path), exist_ok=True)

            shutil.copy(source_path, dest_path)

            progress.update(task, advance=1)


def prune_store(metadata_paths, store_dir):
    all_files = set()

    for metadata_path in metadata_paths:
        with open(metadata_path, 'r') as f:
            metadata = json.load(f)
            all_files.update(file_info['hash'] for file_info in metadata['files'])

    store_files = set(os.listdir(store_dir))

    files_to_delete = store_files - all_files

    deleted_size = 0
    with Progress() as progress:
        task = progress.add_task("[red]Deleting files from store...", total=len(files_to_delete))

        for file_hash in files_to_delete:
            deleted_size += os.path.getsize(os.path.join(store_dir, file_hash))
            os.remove(os.path.join(store_dir, file_hash))
            progress.update(task, advance=1)

    return deleted_size
