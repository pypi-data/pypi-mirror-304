import requests
import argparse
from datetime import datetime
from packaging.version import parse
import re
from typing import Union, List, Any


def get_package_versions(package_name: str) -> List[str]:
    url = f"https://pypi.org/pypi/{package_name}/json"
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise ValueError(f"Failed to fetch package versions: {e}")

    data = response.json()
    versions = sorted(data['releases'].keys(), key=parse)
    return versions


def get_github_releases(owner: str, repo: str) -> List[str]:
    url = f"https://api.github.com/repos/{owner}/{repo}/releases"
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise ValueError(f"Failed to fetch GitHub releases: {e}")

    data = response.json()
    versions = sorted([release['tag_name'] for release in data], key=parse)
    return versions


def generate_new_version(versions: List[str]) -> str:
    now = datetime.now()
    first_day_of_month = now.replace(day=1)
    week_number_in_month = (now.day + first_day_of_month.weekday()) // 7 + 1

    version_patterns = [
        f"{now.year}.{now.month}",
        f"{now.year}.{now.month}.{now.day}",
        f"{now.year}.{now.month}.{now.day}.{now.hour}",
        f"{now.year}.{now.month}.{now.day}.{now.hour}.{now.minute}",
        f"{now.year}.{now.month}.{now.day}.{now.hour}.{now.minute}.{now.second}"
    ]

    for pattern in version_patterns:
        if pattern not in versions:
            return pattern

    return version_patterns[-1]


def parse_input(input_str: str) -> Union[
    tuple[str, Union[str, Any], Union[str, Any]], tuple[str, Union[str, Any]], tuple[str, str], None]:
    # Check if it's a valid GitHub or PyPI link first
    if "github.com" in input_str or "pypi.org" in input_str:
        # Detect GitHub URL
        github_pattern = r"github\.com/(?P<owner>[^/]+)/(?P<repo>[^/]+)"
        # Detect PyPI URL
        pypi_pattern = r"pypi\.org/project/(?P<package>[^/]+)"

        if re.search(github_pattern, input_str):
            match = re.search(github_pattern, input_str)
            return "github", match.group("owner"), match.group("repo")
        elif re.search(pypi_pattern, input_str):
            match = re.search(pypi_pattern, input_str)
            return "pypi", match.group("package")
    else:
        # Detect owner/repo format (no URL)
        owner_repo_pattern = r"(?P<owner>[^/]+)/(?P<repo>[^/]+)"
        if re.match(owner_repo_pattern, input_str):
            match = re.search(owner_repo_pattern, input_str)
            return "github", match.group("owner"), match.group("repo")
        else:
            # If it's neither a URL nor an owner/repo format, assume it's a PyPI package name
            return "pypi", input_str

    return None


def main():
    parser = argparse.ArgumentParser(
        description="Version Hawk: Generate new version tags.",
        epilog=("Input formats:\n"
                "1. GitHub URL: https://github.com/<owner>/<repo> or\n"
                "   https://github.com/<owner>/<repo>/tree/<branch>\n"
                "2. PyPI URL: https://pypi.org/project/<package_name>/\n"
                "3. Owner/Repo format: <owner>/<repo>\n"
                "4. Package name for PyPI: <package_name>")
    )
    parser.add_argument("package", help="The name of the package on PyPI or GitHub.")
    parser.add_argument("--versions", action="store_true", help="List all versions of the package.")

    args = parser.parse_args()
    input_str = args.package

    parsed_result = parse_input(input_str)

    if parsed_result is None:
        return  # Invalid input; exit silently

    input_type, *parsed_data = parsed_result
    versions = []
    try:
        if input_type == "pypi":
            package_name = parsed_data[0]
            versions = get_package_versions(package_name)
        elif input_type == "github":
            owner, repo = parsed_data
            versions = get_github_releases(owner, repo)
    except ValueError as e:
        return  # Error fetching versions; exit silently

    if not versions:
        return  # No versions found; exit silently

    new_version = generate_new_version(versions)
    print(new_version)


if __name__ == "__main__":
    main()
