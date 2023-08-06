#!/usr/bin/env python

import argparse, os, tempfile, getpass, yaml
from subprocess import call
from datetime import datetime
from schema import Schema, SchemaError
import git
from pathlib import Path

config_schema = Schema({
    object: list,
    })

def handle_add(args):
    initial_message = '''New:
    -
Bugfix:
    -
# Uses YAML format. You can use as many categories as you wish, for example:
# New:
#  - Amazing feature added
#  - Another amazing feature added
# Bugfix:
#  - Fixed bug in previous amazing feature
# Other:
#  - Some other entry in changelog
# You can leave also empty categories or add comments. They will be ignored.
# Leave this file unchanged to abort adding entry.
'''
    tf = tempfile.NamedTemporaryFile(mode='w+', suffix=".yaml", encoding='utf-8', delete=False)
    tf_name = tf.name
    tf.write(initial_message)
    tf.flush()
    tf.close()
    print("Running editor", args.editor)
    call([args.editor, tf_name])
    
    with open(tf_name, mode='r', encoding='utf-8') as f:
        edited_message = f.read()
    if edited_message == initial_message:
        print("Aborted")
        return False
    if not os.path.isdir(args.source_directory):
        os.makedirs(args.source_directory)
    filename = os.path.join(args.source_directory, getpass.getuser() + '_' + datetime.now(tz=None).strftime("%y-%m-%d_%H-%M-%S") + '.yaml')
    print("Creating source file", filename)
    yaml_content = yaml.load(edited_message, Loader=yaml.Loader)
    try:
        config_schema.validate(yaml_content)
    except SchemaError as se:
        raise se
    with open(filename, mode='w+') as f:
        f.write(edited_message)
    
def handle_release(args):
    source_files = [f for f in os.listdir(args.source_directory) if os.path.isfile(os.path.join(args.source_directory, f))]
    if not source_files:
        print("No source files to process changelog.")
        return False
    print("Got source files", source_files)
    new_entries = {}
    for source_file in source_files:
        with open(os.path.join(args.source_directory, source_file), mode='r', encoding='utf-8') as f:
            yaml_content = f.read()
        yml = yaml.load(yaml_content, Loader=yaml.Loader)
        try:
            config_schema.validate(yml)
        except SchemaError as se:
            raise se
        for key, values in yml.items():
            if not values:
                continue
            if key not in new_entries:
                new_entries[key] = []
            new_entries[key] += values

    print("Got new entries", new_entries)
    new_changelog_content = "# " + args.version
    for key, values in new_entries.items():
        new_changelog_content += "\n"
        new_changelog_content += "## " + key + '\n'
        for value  in values:
            if not value:
                continue
            new_changelog_content += "- " + value + '\n'
    new_changelog_content += "\n"
    changelog_content = ""
    if os.path.isfile(args.changelog_file):
        with open(args.changelog_file, mode='r', encoding='utf-8') as f:
            changelog_content = f.read()
    changelog_content = new_changelog_content + changelog_content
    with open(args.changelog_file, mode='w+', encoding='utf-8') as f:
        f.write(changelog_content)
    print("Added to changelog:\n")
    print(new_changelog_content)
    g = git.cmd.Git(args.repository_root)
    g.add(args.source_directory)
    target_archive_directory = os.path.join(args.archive_directory, args.version)
    if not os.path.exists(target_archive_directory):
        os.makedirs(target_archive_directory)
    g.add(target_archive_directory)
    for source_file in source_files:
        full_source_path = Path(args.source_directory) / Path(source_file)
        full_archive_path = Path(target_archive_directory) / Path(source_file)
        print(f"Moving {full_source_path} to {full_archive_path}")
        g.mv(str(full_source_path), str(full_archive_path))


EDITOR = os.environ.get('EDITOR', 'notepad')  # that easy!

parser = argparse.ArgumentParser(description='Handles changelog entries without conflicts')
parser.add_argument('--source_directory', type=str, nargs=1, 
                    help='directory where developers entries will be stored. You should keep it in the repository together with your code',
                    default="changelog/sources")
parser.add_argument('--archive_directory', type=str, nargs=1, 
                    help='directory where developers entries will be moved after releasing final changelog. You should keep it in the repository together with your code',
                    default="changelog/archives")
parser.add_argument('--changelog_file', type=str, nargs=1, 
                    help='Changelog.md file location. You should keep it in the repository together with your code',
                    default="Changelog.md")
parser.add_argument('--editor', type=str, nargs=1,
                    help='Text editor used to create entry in changelog', default=EDITOR)
parser.add_argument('--repository_root', type=str, nargs=1,
                    help='Path to root of git repository', default='.')
parser.add_argument('action', type=str, nargs=1,  metavar='action', help='add new changelog entry or release previously stored entries. Choices are: add, release', choices=['add', 'release'])
parser.add_argument('version', type=str, nargs='?', help='version of release to store in changelog. Required if action==release')

# group = parser.add_mutually_exclusive_group(required=True)

# subgroup = group.add_argument_group()
# subgroup.add_argument('release', metavar='release', type=str, nargs=1, help='prepare changelog to release')
# subgroup.add_argument('version', metavar='version', type=str, nargs=1, help='String with version of release to add to changelog')


args = parser.parse_args()
if args.action == ['release'] and not args.version:
    parser.error("version is required for action==release")
print(args)

if args.action == ['add']:
    handle_add(args)
elif args.action == ['release']:
    handle_release(args)
else:
    raise Exception("Unknown action " + str(args.action))