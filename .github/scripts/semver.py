import subprocess
import os
import uuid


class ReleaseNotes:
    def __init__(self):
        self.breaking = []
        self.features = []
        self.fixes = []
        self.other = []

    def add_breaking(self, commit):
        self.breaking.append(commit.removeprefix("fix!").removeprefix("feat!"))

    def add_features(self, commit):
        self.features.append(commit.removeprefix("feat:"))

    def add_fixes(self, commit):
        self.fixes.append(commit.removeprefix("fix:"))

    def add_other(self, commit):
        self.other.append(commit.removeprefix("chore:"))

    def __repr__(self):
        text = ""
        if self.breaking:
            text += "## Breaking Changes\n* " + "\n* ".join(self.breaking) + "\n\n"
        if self.features:
            text += "## Features\n* " + "\n* ".join(self.features) + "\n\n"
        if self.fixes:
            text += "## Fixes\n* " + "\n* ".join(self.fixes) + "\n\n"
        if self.other:
            text += "## Other\n* " + "\n* ".join(self.other) + "\n\n"
        return text


def get_last_tag() -> str:
    try:
        return (
            subprocess.check_output(
                ["git", "describe", "--tags", "--abbrev=0"], stderr=subprocess.PIPE
            )
            .strip()
            .decode()
        )
    except subprocess.CalledProcessError:
        return ""


def get_commit_messages(since_tag: str):
    command = ["git", "log", "--pretty=format:%s (%h)"]
    if since_tag:
        command.append(f"{since_tag}..HEAD")
    return subprocess.check_output(command).strip().decode().split("\n")


def parse_commits(
    commits: list[str], last_tag: str = "0.0.0"
) -> tuple[ReleaseNotes, str]:
    notes = ReleaseNotes()
    major, minor, patch = [int(v.strip()) for v in last_tag.strip("v").split(".")]

    for commit in commits:
        if commit.startswith("fix!") or commit.startswith("feat!"):
            major += 1
            minor = 0
            patch = 0
            notes.add_breaking(commit)
        elif commit.startswith("fix:"):
            patch += 1
            notes.add_fixes(commit)
        elif commit.startswith("feat:"):
            minor += 1
            patch = 0
            notes.add_features(commit)
        else:
            notes.add_other(commit)

    return notes, f"{major}.{minor}.{patch}"


def set_output(name, value):
    with open(os.environ["GITHUB_OUTPUT"], "a") as fh:
        delimiter = uuid.uuid1()
        print(f"{name}<<{delimiter}", file=fh)
        print(value, file=fh)
        print(delimiter, file=fh)


def main():
    last_tag = get_last_tag()
    commits = get_commit_messages(since_tag=last_tag)
    release_notes, new_version = parse_commits(commits, last_tag)
    if last_tag == new_version:
        print("No new release")
        return
    set_output("tag", f"v{new_version}")
    set_output("version", new_version)
    set_output("release_notes", release_notes)
    print(f"Release {new_version} created with notes: \n{release_notes}")


if __name__ == "__main__":
    main()
