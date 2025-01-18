import os
import mmap
import re

# searchterms.txt is to be newline sparated #

def parse_file_with_pattern(filename, pattern):
    """
    Parses a file for lines matching a regex pattern.

    Args:
        filename (str): The file to parse.
        pattern (str): Regex pattern to match.

    Returns:
        list: A list of matched lines.
    """
    compiled_pattern = re.compile(pattern)
    results = []

    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            if compiled_pattern.match(line):
                results.append(line.strip())

    return results

def search_with_mmap(filename, search_term, output_file):
    """
    Searches for a term in a file using mmap and appends matches to an output file.

    Args:
        filename (str): The file to search.
        search_term (str): The term to search for.
        output_file (str): The file to write matches to.
    """
    with open(filename, 'r', encoding='utf-8') as file:
        with mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ) as mm:
            for line in mm.read().decode('utf-8').splitlines():
                if search_term in line:
                    with open(output_file, 'a', encoding='utf-8') as matches:
                        matches.write(f'File: {filename} | Matched Term: {line}\n')

def check_creds(cred_file, search_terms_file, output_file, matched_creds_file):
    """
    Searches for terms in a credentials file and writes matches to an output file and a separate matched credentials file.

    Args:
        cred_file (str): The file containing credentials.
        search_terms_file (str): The file containing search terms.
        output_file (str): The file to write all matches to.
        matched_creds_file (str): The file to write only matched credentials to.
    """
    with open(search_terms_file, 'r', encoding='utf-8') as searchterms:
        for term in searchterms:
            term = term.strip()
            with open(cred_file, 'r', encoding='utf-8') as file:
                for line in file:
                    if term in line:
                        with open(output_file, 'a', encoding='utf-8') as matches:
                            matches.write(f'Matched Term: {term} | Line: {line.strip()}\n')
                        with open(matched_creds_file, 'a', encoding='utf-8') as matched_creds:
                            matched_creds.write(f'{line.strip()}\n')

def process_folder(base_folder, search_terms_file, conf_output_file, creds_output_file):
    """
    Processes files in a folder, searching for terms and parsing credentials.

    Args:
        base_folder (str): The base folder containing subfolders to process.
        search_terms_file (str): The file containing search terms.
        conf_output_file (str): The file to write config matches to.
        creds_output_file (str): The file to write credential matches to.
    """
    for folder in os.listdir(base_folder):
        folder_path = os.path.join(base_folder, folder)
        if not os.path.isdir(folder_path):
            continue

        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)

            if file_name.endswith("conf"):
                with open(search_terms_file, 'r', encoding='utf-8') as searchterms:
                    for term in searchterms:
                        search_with_mmap(file_path, term.strip(), conf_output_file)

            elif file_name.endswith("txt"):
                pattern = r".+:.*"
                creds = parse_file_with_pattern(file_path, pattern)

                with open(creds_output_file, 'a', encoding='utf-8') as creds_file:
                    for match in creds:
                        creds_file.write(f'{match}\n')

# Main script
if __name__ == "__main__":
    BASE_FOLDER = 'data'
    SEARCH_TERMS_FILE = 'searchterms.txt'
    CONF_OUTPUT_FILE = 'configMatches.txt'
    CREDS_OUTPUT_FILE = 'creds.txt'
    MATCHED_CREDS_FILE = 'matchedCreds.txt'

    # Clear output files before processing
    open(CONF_OUTPUT_FILE, 'w').close()
    open(CREDS_OUTPUT_FILE, 'w').close()
    open(MATCHED_CREDS_FILE, 'w').close()

    process_folder(BASE_FOLDER, SEARCH_TERMS_FILE, CONF_OUTPUT_FILE, CREDS_OUTPUT_FILE)
    check_creds(CREDS_OUTPUT_FILE, SEARCH_TERMS_FILE, CONF_OUTPUT_FILE, MATCHED_CREDS_FILE)
