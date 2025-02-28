# Elasticsearch Migration Changes Script

This script fetches Elasticsearch migration content for different versions and sections, cleans it, and allows you to save it for future reference. The script supports two modes: single version or a range of versions. You can choose which sections to include (such as Deprecations, Breaking changes, etc.).

## Features

- Fetch migration content from Elasticsearch documentation for specific versions.
- Includes options to select specific sections of migration changes.
- Supports both single and range versions.
- Can be executed via the terminal/command line.

## Installation Requirements for macOS (you can do similar for other OS's)

Before you run the script, ensure that the following dependencies are installed:

### 1. **Homebrew**
Homebrew is a package manager for macOS. If you don't have it installed, you can install it by running the following command:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Then, you can check the version:
```bash
brew --version
```

### 2. **Python**
You can check if Python is installed with:
```bash
python3 --version
```

If it is not installed:
```bash
brew install python
```

### 3. **Running the script**
Clone the repository or download the ```migration-changes-es.py``` then run it:
```bash
python3 migration-changes-es.py
```

The script will prompt you to choose whether you want to fetch content for a single version or a range of versions.
You can then select the version or range and decide which sections to include in the output.
Follow the prompts to generate the output content.

### Usage Example:
```bash
script % python3 migration-changes-es.py
Do you want to fetch content for a single version or a range? (single/range): single
Enter the version you want to fetch from 8.0-latest version (e.g., 8.5): 8.11
Fetching content for version 8.11...
Which section do you want to include (Select only one option)? (1 - All, 2 - Breaking Changes, 3 - Notable Changes, 4 - Deprecations): 1
Formatted migration guide saved to migration_8.11_formatted.txt
```

Then, you can do a simple grep to find the wanted changes.

