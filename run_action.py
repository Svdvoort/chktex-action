"""Find all *tex files and run chktex on them"""

import os
import subprocess
import sys

SKIP_DIRS = set(["venv", ".git", "__pycache__"])
chktexrc_file = sys.argv[1]
additional_args = sys.argv[2]
warnings_as_errors = sys.argv[3]


GITHUB_WORKSPACE = os.environ.get("GITHUB_WORKSPACE")
if not GITHUB_WORKSPACE:
    print("No GITHUB_WORKSPACE environment variable set.")
    sys.exit(1)

os.chdir(GITHUB_WORKSPACE)

CHKTEX_COMMAND = CHKTEX_COMMAND = ["chktex", "-q", "-b=0"]
if os.path.exists(chktexrc_file):
    chktexrc_file = os.path.abspath(chktexrc_file)
    print("found local chktexrc")
    CHKTEX_COMMAND.extend(["-l", chktexrc_file])

if additional_args is not "NONE":
    additional_args = additional_args.split(' ')
    CHKTEX_COMMAND.extend(additional_args)

CHKTEX_COMMAND.append('filename')


def main():
    """main function"""

    all_files_in_tree = []
    for root, dirs, files in os.walk(".", topdown=True):
        for skip_dir in SKIP_DIRS:
            if skip_dir in dirs:
                dirs.remove(skip_dir)

        for file in files:
            all_files_in_tree.append(os.path.join(root, file))

    files_to_process = [file for file in all_files_in_tree if file.endswith(".tex")]

    if not files_to_process:
        print("Found no .tex files to process")
        print("Complete tree found:")
        for file in all_files_in_tree:
            print(file)
        sys.exit(0)

    files_with_errors = 0

    for file in files_to_process:
        print(f"Linting {file}")

        directory = os.path.dirname(file)
        relative_file = os.path.basename(file)
        CHKTEX_COMMAND[-1] = relative_file

        # run process inside the file's folder
        completed_process = subprocess.run(
            CHKTEX_COMMAND,
            cwd=directory,
            capture_output=True,
            text=True,
            check=False,
        )
        stdout = completed_process.stdout
        stderr = completed_process.stderr

        if stdout:
            files_with_errors += 1
            print(
                "----------------------------------------",
                stdout,
                "----------------------------------------",
                sep="\n",
            )

        if stderr:
            print("chktex run into errors:", stderr, sep="\n")

    print(f"found {files_with_errors} files with errors")
    if warnings_as_errors == "1":
        sys.exit(files_with_errors)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
