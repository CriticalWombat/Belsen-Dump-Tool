import os
import mmap
import re
import pycountry
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Only log high-level progress
    format="%(asctime)s - %(message)s",
    handlers=[logging.StreamHandler()],  # Only log to console
)

def expand_country_code(code):
    """
    Expands a country code (ISO Alpha-2) to its full name.
    """
    try:
        country = pycountry.countries.get(alpha_2=code.upper())
        return country.name if country else "Unknown Country Code"
    except AttributeError:
        return "Unknown Country Code"


def parse_file_with_pattern(filename, pattern):
    """
    Parses a file for lines matching a regex pattern.
    """
    compiled_pattern = re.compile(pattern)
    with open(filename, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file if compiled_pattern.match(line)]


def append_to_file(filepath, lines):
    """
    Appends a list of lines to a file.
    """
    with open(filepath, 'a', encoding='utf-8') as file:
        file.writelines(f"{line}\n" for line in lines)


def search_with_mmap(filename, search_terms, output_file):
    """
    Searches for terms in a file using mmap and writes matches to an output file.
    """
    if os.path.getsize(filename) == 0:
        return  # Skip empty files

    with open(filename, 'r', encoding='utf-8') as file, \
         mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ) as mm:
        content = mm.read().decode('utf-8')
        matched_lines = [
            f"File: {filename} | Matched Term: {line.strip()}"
            for line in content.splitlines()
            for term in search_terms
            if term in line
        ]
    append_to_file(output_file, matched_lines)


def check_creds(cred_file, search_terms, output_file, matched_creds_file):
    """
    Searches credentials for matching terms and writes results to output files.
    """
    matched_lines = []
    matched_creds = []
    with open(cred_file, 'r', encoding='utf-8') as file:
        for line in file:
            if any(term in line for term in search_terms):
                matched_lines.append(f"Matched Term: {line.strip()}")
                matched_creds.append(line.strip())
    append_to_file(output_file, matched_lines)
    append_to_file(matched_creds_file, matched_creds)


def process_folder(base_folder, search_terms_file, conf_output_file, creds_output_file, ip_port_output_file):
    """
    Processes all files in the folder, searching for matches based on file type,
    and logs the IP addresses and ports along with credentials, organized by country.
    """
    # Load search terms once
    with open(search_terms_file, 'r', encoding='utf-8') as file:
        search_terms = [term.strip() for term in file]

    # Get the total number of countries for progress tracking
    countries = [d for d in os.listdir(base_folder) if os.path.isdir(os.path.join(base_folder, d))]
    total_countries = len(countries)

    # Traverse the directory structure with progress tracking
    with open(ip_port_output_file, 'w', encoding='utf-8') as ip_file, \
         open(creds_output_file, 'w', encoding='utf-8') as creds_file:  # Open credentials output file once
        for idx, country_code in enumerate(countries, start=1):
            country_folder = os.path.join(base_folder, country_code)
            country = expand_country_code(country_code)

            # Log progress
            progress = (idx / total_countries) * 100
            logging.info(f"Processing {country} ({country_code}) - {progress:.1f}% complete")

            # Add a header for the country in the IP-port output file
            ip_file.write(f"== {country} ({country_code}) ==\n")
            creds_file.write(f"== {country} ({country_code}) ==\n")

            for target_ip in os.listdir(country_folder):
                target_folder = os.path.join(country_folder, target_ip)
                if not os.path.isdir(target_folder):
                    continue

                # Extract IP and port information
                if "_" in target_ip:  # Assuming target_ip is in the format x.x.x.x_portnumber
                    ip, port = target_ip.split("_")
                    formatted_entry = f"{ip}:{port}"
                    ip_file.write(f"{formatted_entry}\n")  # Write IP and port to the IP output file
                    creds_file.write(f"{formatted_entry}\n")  # Write IP and port to the credentials output file

                credentials = []
                for file_name in os.listdir(target_folder):
                    file_path = os.path.join(target_folder, file_name)

                    # Process .txt files for credentials
                    if file_name.endswith(".txt"):
                        pattern = r".+:.*"  # Regex pattern to extract credentials (username:password)
                        matches = parse_file_with_pattern(file_path, pattern)
                        credentials.extend(matches)

                # Write credentials under the corresponding IP and port
                for cred in credentials:
                    creds_file.write(f" \t{cred}\n")

            # Add a blank line between countries for readability
            ip_file.write("\n")
            creds_file.write("\n")



def clear_files(*files):
    """
    Clears the contents of the given files.
    """
    for file in files:
        open(file, 'w').close()


# Main script
if __name__ == "__main__":
    BASE_FOLDER = 'BelsenLeak'
    SEARCH_TERMS_FILE = 'KeywordSearchTerms.txt'
    CONF_OUTPUT_FILE = 'Config_Matches.txt'
    CREDS_OUTPUT_FILE = 'All Credentials.txt'
    MATCHED_CREDS_FILE = 'Credential_Matches.txt'
    IP_PORT_OUTPUT_FILE = 'All_IPs_by_Country.txt'  # File for IP and port output

    # Clear output files before processing
    clear_files(CONF_OUTPUT_FILE, CREDS_OUTPUT_FILE, MATCHED_CREDS_FILE, IP_PORT_OUTPUT_FILE)

    # Start processing
    logging.info("Starting the processing of folders and files.")
    process_folder(BASE_FOLDER, SEARCH_TERMS_FILE, CONF_OUTPUT_FILE, CREDS_OUTPUT_FILE, IP_PORT_OUTPUT_FILE)

    with open(SEARCH_TERMS_FILE, 'r', encoding='utf-8') as st_file:
        search_terms = [line.strip() for line in st_file]
    check_creds(CREDS_OUTPUT_FILE, search_terms, CONF_OUTPUT_FILE, MATCHED_CREDS_FILE)
    logging.info("Processing completed.")
