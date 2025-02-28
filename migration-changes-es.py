import requests
import re
import sys

# List of URLs to fetch additional content for version 8.0
additional_urls_8_0 = [
    "https://raw.githubusercontent.com/elastic/elasticsearch/refs/heads/8.17/docs/reference/migration/migrate_8_0/cluster-node-setting-changes.asciidoc",
    "https://raw.githubusercontent.com/elastic/elasticsearch/refs/heads/8.17/docs/reference/migration/migrate_8_0/command-line-tool-changes.asciidoc",
    "https://raw.githubusercontent.com/elastic/elasticsearch/refs/heads/8.17/docs/reference/migration/migrate_8_0/index-setting-changes.asciidoc",
    "https://raw.githubusercontent.com/elastic/elasticsearch/refs/heads/8.17/docs/reference/migration/migrate_8_0/java-api-changes.asciidoc",
    "https://raw.githubusercontent.com/elastic/elasticsearch/refs/heads/8.17/docs/reference/migration/migrate_8_0/jvm-option-changes.asciidoc",
    "https://raw.githubusercontent.com/elastic/elasticsearch/refs/heads/8.17/docs/reference/migration/migrate_8_0/logging-changes.asciidoc",
    "https://raw.githubusercontent.com/elastic/elasticsearch/refs/heads/8.17/docs/reference/migration/migrate_8_0/mapping-changes.asciidoc",
    "https://raw.githubusercontent.com/elastic/elasticsearch/refs/heads/8.17/docs/reference/migration/migrate_8_0/packaging-changes.asciidoc",
    "https://raw.githubusercontent.com/elastic/elasticsearch/refs/heads/8.17/docs/reference/migration/migrate_8_0/painless-changes.asciidoc",
    "https://raw.githubusercontent.com/elastic/elasticsearch/refs/heads/8.17/docs/reference/migration/migrate_8_0/plugin-changes.asciidoc",
    "https://raw.githubusercontent.com/elastic/elasticsearch/refs/heads/8.17/docs/reference/migration/migrate_8_0/rest-api-changes.asciidoc",
    "https://raw.githubusercontent.com/elastic/elasticsearch/refs/heads/8.17/docs/reference/migration/migrate_8_0/sql-jdbc-changes.asciidoc",
    "https://raw.githubusercontent.com/elastic/elasticsearch/refs/heads/8.17/docs/reference/migration/migrate_8_0/system-req-changes.asciidoc",
    "https://raw.githubusercontent.com/elastic/elasticsearch/refs/heads/8.17/docs/reference/migration/migrate_8_0/transform.asciidoc"
]

# Function to fetch and clean content from the URL based on version
def fetch_and_clean_content(version, sections_to_include):
    # Replace dots with underscores in the version number
    version = version.replace('.', '_')
    url = f"https://raw.githubusercontent.com/elastic/elasticsearch/8.17/docs/reference/migration/migrate_{version}.asciidoc"
    #print(f"Fetching content from: {url}")  # Debugging: Print the URL being accessed
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Failed to fetch content from {url}. HTTP Status: {response.status_code}")
        return ""

    # Remove unwanted metadata
    cleaned_content = response.text.replace("[discrete]", "").replace("[%collapsible]", "")

    # Replace {es} with Elasticsearch
    cleaned_content = cleaned_content.replace("{es}", "Elasticsearch")

    # Debugging: Print a snippet of the fetched content
    #print(f"Fetched content for version {version}:\n", cleaned_content[:500])

    # Check for the presence of Deprecations and Notable changes
    has_deprecations = "=== Deprecations" in cleaned_content
    has_notable_changes = "=== Notable changes" in cleaned_content

    # Adjust breaking changes pattern based on the presence of Deprecations and Notable changes
    if has_deprecations:
        breaking_changes_pattern = r"=== Breaking changes.*?(?=== Deprecations)"
    elif has_notable_changes:
        breaking_changes_pattern = r"=== Breaking changes.*?(?=== Notable changes)"
    else:
        breaking_changes_pattern = r"=== Breaking changes.*"

    # Regular expression patterns to match the relevant sections
    migrating_pattern = r"== Migrating to [^\n]+"
    deprecations_pattern = r"=== Deprecations.*"
    notable_changes_pattern = r"=== Notable changes.*"


    # Extract the relevant sections using regex
    migrating_section = re.search(migrating_pattern, cleaned_content, re.DOTALL)
    breaking_changes_section = re.search(breaking_changes_pattern, cleaned_content, re.DOTALL)
    deprecations_section = re.search(deprecations_pattern, cleaned_content, re.DOTALL)
    notable_changes_section = re.search(notable_changes_pattern, cleaned_content, re.DOTALL)

    # Collect the content of each section, if they are found
    migrating_content = migrating_section.group(0) if migrating_section else ""
    breaking_changes_content = breaking_changes_section.group(0) if breaking_changes_section else ""
    deprecations_content = deprecations_section.group(0) if deprecations_section else ""
    notable_changes_content = notable_changes_section.group(0) if notable_changes_section else ""

    # Filter out unwanted deprecation entries (like [[deprecations_815_rest_api]], etc.)
    deprecations_content = re.sub(r"\[\[deprecations_.*?\]\]", "", deprecations_content)
    deprecations_content = re.sub(r"\[\[deprecate_.*?\]\]", "", deprecations_content)

    # Formatting Breaking Changes section
    breaking_changes_content = re.sub(r"=== Breaking changes.*?\n+", "=== Breaking changes\n\n", breaking_changes_content, flags=re.DOTALL)
    breaking_changes_content = re.sub(r"\n\[\[.*?\]\]\n", "\n", breaking_changes_content)  # Remove [[anchors]]
    #breaking_changes_content = re.sub(r"\n\..*?\n", "\n", breaking_changes_content)  # Remove explicit anchors from titles

    # Formatar a seção de Notable Changes
    notable_changes_content = re.sub(r"=== Notable changes.*?\n+", "=== Notable changes\n\n", notable_changes_content, flags=re.DOTALL)
    notable_changes_content = re.sub(r"\n\[\[.*?\]\]\n", "\n", notable_changes_content)  # Remover [[anchors]]
    notable_changes_content = re.sub(r"\n\..*?\n", "\n", notable_changes_content)  # Remover âncoras explícitas dos títulos


    # Formatting each section
    breaking_changes_content = re.sub(r"==== (.*?)\n+", r"==== \1\n\n", breaking_changes_content)  # Ensure spacing
    breaking_changes_content = re.sub(r"(\*Details\* \+)", r"\n\1", breaking_changes_content)  # Ensure spacing before details

    def clean_content(content):
        # Remove unwanted metadata and clean the content
        content = content.replace("[discrete]", "").replace("[%collapsible]", "")
        return content

    # If the version is 8.0, add additional data
    if version == "8_0":
        print("Fetching additional content for version 8.0...")
        additional_content = ""
        for url in additional_urls_8_0:
            print(f"Fetching additional content from: {url}")
            additional_response = requests.get(url)
            if additional_response.status_code == 200:
                additional_cleaned_content = clean_content(additional_response.text)  # Clean the additional content
                additional_content += additional_cleaned_content  # Add the cleaned content to the result
            else:
                print(f"Failed to fetch additional content from {url}. HTTP Status: {additional_response.status_code}")

        breaking_changes_content += "\n\n" + additional_content  # Add the cleaned additional content to Breaking Changes


    # Combine the relevant sections into one string
    #return migrating_content + "\n" + breaking_changes_content + "\n" + notable_changes_content + "\n" + "\n" + deprecations_content

    # Select sections to include based on user's choice
    content_to_return = ""
    if 'All' in sections_to_include:
        content_to_return = migrating_content + "\n" + breaking_changes_content + "\n" + notable_changes_content + "\n" + "\n" + deprecations_content
    if 'Breaking Changes' in sections_to_include:
        content_to_return += breaking_changes_content
    if 'Notable Changes' in sections_to_include:
        content_to_return += notable_changes_content
    if 'Deprecations' in sections_to_include:
        content_to_return += deprecations_content

    # If 'Migrating to' section exists, prepend it to the content
    if migrating_content and 'All' not in sections_to_include:
        content_to_return = migrating_content + "\n" + content_to_return

    return content_to_return


# Main script to handle arguments and save the output
def main():
    # Ask the user if they want to fetch one version or a range
    while True:
        version_input = input("Do you want to fetch content for a single version or a range? (single/range): ").strip().lower()

        if version_input in ['single', 'range']:
            break  # Exit the loop if valid input is given
        else:
            print("Invalid input. Please enter 'single' or 'range'.")

    def is_valid_version(version):
        # Ensure the version is between 8.0 and 8.19
        try:
            major, minor = map(int, version.split('.'))
            return 8 <= major <= 8 and 0 <= minor <= 19
        except ValueError:
            return False

    if version_input == 'single':
        while True:
            version = input("Enter the version you want to fetch from 8.0-latest version (e.g., 8.5): ").strip()
            if is_valid_version(version):
                break
            else:
                print("Invalid version. Please enter a version between 8.0 and 8.19.")

        print(f"Fetching content for version {version}...")
        # Ask for section selection with a while loop to validate input
        while True:
            sections_input = input("Which section do you want to include (Select only one option)? (1 - All, 2 - Breaking Changes, 3 - Notable Changes, 4 - Deprecations): ").strip()
            if sections_input in ['1', '2', '3', '4']:
                break  # Exit the loop if valid input is given
            else:
                print("Invalid input. Please enter a number between 1 and 4.")
        # Map the input to the corresponding sections
        sections_map = {
            '1': ['All'],
            '2': ['Breaking Changes'],
            '3': ['Notable Changes'],
            '4': ['Deprecations']
        }
        sections_to_include = sections_map.get(sections_input, ['All'])  # Default to 'All' if invalid input
        final_content = fetch_and_clean_content(version, sections_to_include)
        output_file = f"migration_{version}_formatted.txt"
    
    elif version_input == 'range':
        while True:
            from_version = input("Enter the 'from' version from 8.0-latest version (e.g., 8.5): ").strip()
            if is_valid_version(from_version):
                break
            else:
                print("Invalid version. Please enter versions between 8.0 and 8.19.")
        while True:
            to_version = input("Enter the 'to' version from 8.0-latest version (e.g., 8.5): ").strip()
            if is_valid_version(to_version):
                break
            else:
                print("Invalid version. Please enter versions between 8.0 and 8.19.")

        # Ask for section selection with a while loop to validate input
        while True:
            sections_input = input("WWhich section do you want to include (Select only one option)? (1 - All, 2 - Breaking Changes, 3 - Notable Changes, 4 - Deprecations): ").strip()
            if sections_input in ['1', '2', '3', '4']:
                break  # Exit the loop if valid input is given
            else:
                print("Invalid input. Please enter a number between 1 and 4.")
        # Map the input to the corresponding sections
        sections_map = {
            '1': ['All'],
            '2': ['Breaking Changes'],
            '3': ['Notable Changes'],
            '4': ['Deprecations']
        }
        sections_to_include = sections_map.get(sections_input, ['All'])  # Default to 'All' if invalid input
                     
        # Split the version string into major and minor parts
        start_major, start_minor = map(int, from_version.split('.'))
        end_major, end_minor = map(int, to_version.split('.'))

        all_content = ""
        current_major = start_major
        current_minor = start_minor

        # Loop through versions from start_version to end_version
        while (current_major < end_major) or (current_major == end_major and current_minor <= end_minor):
            # Format version to match the URL pattern
            current_version = f"{current_major}.{current_minor}"
            #print(f"Debug: Current version: {current_version}")  # Debugging print statement
            version_content = fetch_and_clean_content(current_version, sections_to_include)
            if version_content:
                all_content += version_content + "\n\n"  # Combine the content
            
            # Increment the version
            if current_minor < 10:
                current_minor += 1  # Increment by 1 for versions like 8.8 to 8.9
            else:
                current_minor += 1  # Increment minor for versions like 8.10 to 8.11
                if current_minor == 100:  # Special case for 8.99 -> 9.0
                    current_major += 1
                    current_minor = 0

        final_content = all_content
        output_file = f"migration_{from_version}_to_{to_version}_formatted.txt"
    # If no content fetched, exit
    if not final_content:
        print("No content was fetched or formatted. Exiting.")
        sys.exit(1)

    # Save the combined content to a text file
    with open(output_file, "w") as file:
        file.write(final_content)

    print(f"Formatted migration guide saved to {output_file}")

if __name__ == "__main__":
    main()
