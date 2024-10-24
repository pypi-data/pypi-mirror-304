

# 🦅 Version Hawk

Version Hawk is a command-line tool for managing and generating version tags for Python packages on PyPI and GitHub repositories. It allows you to retrieve existing version tags from both platforms and generate new version numbers based on your project's release history.

## Features

- **Retrieve Versions from PyPI**: Get all version tags for a specified PyPI package.
- **Retrieve Releases from GitHub**: Fetch release tags from a GitHub repository.
- **Generate New Version Tags**: Automatically generate a new version tag based on existing versions.
- **Flexible Input**: Accepts various input formats including:
  - URLs for GitHub repositories (e.g., `https://github.com/username/repo`)
  - URLs for PyPI packages (e.g., `https://pypi.org/project/package`)
  - GitHub owner/repo format (e.g., `username/repo`)
  - Direct package names (e.g., `package`)

## Installation

To use Version Hawk, you need to have Python 3.6 or higher. You can clone the repository and install the required dependencies using `pip`:

```bash
git clone https://github.com/yourusername/versionhawk.git
cd versionhawk
pip install -r requirements.txt
```


## Usage

Run the tool from the command line:

```bash
python version_hawk.py <input>
```


Input Options

	•	GitHub Repository URL:
	•	Example: https://github.com/psf/requests
	•	PyPI Package URL:
	•	Example: https://pypi.org/project/requests/
	•	Owner/Repo Format:
	•	Example: psf/requests
	•	Direct Package Name:
	•	Example: requests

Listing Versions

To list all versions of a package or releases of a repository, use the --versions flag:

```bash
python version_hawk.py <input> --versions
```

## Example

```bash
# Get all versions from PyPI for the 'requests' package
python version_hawk.py requests --versions

# Get all releases from GitHub for the 'psf/requests' repository
python version_hawk.py psf/requests --versions

# Generate a new version based on existing tags
python version_hawk.py https://github.com/psf/requests
```

## Testing

You can run the unit tests to ensure that everything is working correctly. Make sure you have unittest available, then execute:


```bash
python -m unittest discover tests
```

### Contributing

Contributions are welcome! If you have suggestions for improvements or new features, please open an issue or submit a pull request.

### License

This project is licensed under the MIT License. See the LICENSE file for details.

### Acknowledgements

	•	Requests for HTTP requests.
	•	argparse for command-line argument parsing.
	•	packaging for version parsing.


### Key Sections Explained

1. **Features**: Outlines what the tool can do.
2. **Installation**: Provides steps to set up the project.
3. **Usage**: Explains how to run the tool and its input options.
4. **Example**: Shows practical usage examples.
5. **Testing**: Instructions for running unit tests.
6. **Contributing**: Encourages community contributions.
7. **License**: Mentions the license type.

Feel free to modify any part of the README to better fit your project! If you have additional features or sections to add, let me know!





VersionHawk is a tool for managing the versions of Python packages based on semantic versioning and the current date. It automatically suggests a new version tag if previous ones are already taken and allows you to fetch a list of all existing versions of a package.

## ✨ Features

	•	Generate a new version: Suggests a unique version tag based on the current date and time.
	•	View all versions: Optionally fetches a list of all existing versions of a package on PyPI.
	•	User-friendly command-line interface: Easily run it from the terminal.

## 🔧 Installation

You can install VersionHawk using pip:


pip install versionhawk

## 🚀 Usage

Once installed, you can run VersionHawk through the versionhawk command in your terminal.

## 🆕 Generate a New Version

To generate a new version for a package on PyPI, use the following command:


versionhawk <package_name>

Example:

versionhawk requests

## 📄 View All Versions

To fetch a list of all existing versions of a package on PyPI, use the --versions flag:

versionhawk <package_name> --versions

Example:

versionhawk requests --versions

## ⚙️ How It Works

VersionHawk uses the current date and time to suggest a new version. It checks the following patterns in order:

	•	Year.Month (e.g., 2024.10)
	•	Year.Month.Week Number in Month (e.g., 2024.10.3)
	•	Year.Month.Day (e.g., 2024.10.22)
	•	Year.Month.Day.Hour (e.g., 2024.10.22.20)
	•	Year.Month.Day.Hour.Minutes (e.g., 2024.10.22.20.01)
	•	Year.Month.Day.Hour.Minutes.Seconds (e.g., 2024.10.22.20.01.30)

VersionHawk checks these patterns against existing versions and suggests the first available unique tag.

## 💡 Example Usage

Let’s say the current date is 2024-10-22 20:01, and the requests package already has versions up to 2024.10.22.20.01. VersionHawk will suggest the next available version, such as 2024.10.22.20.01.30, if earlier versions are taken.

## 📦 Dependencies

VersionHawk requires the following dependencies to work:

	•	requests — to fetch version information from PyPI.
	•	packaging — to correctly sort versions.

These dependencies are automatically installed when you install VersionHawk.

## 📜 License

This project is licensed under the MIT License. See the LICENSE file for more details.
