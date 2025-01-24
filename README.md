# Belsen File Processing and Search Tool

## This tool is designed strictly for rapid assessment of structured data. Any misuse of this tool for illegal purposes is not condoned.

## Overview
This Python script processes structured folders and files to extract and organize critical data such as credentials, IP addresses, and ports. It provides functionality to:
- Parse `.txt` files for credentials matching custom regex patterns.
- Search for specific terms in files and log matches.
- Organize and export data based on folder structure and country codes.

---

## Possible Future features
- **ETL Option**: Dump data directly into a mysql database for further analysis.
---

## Prerequisites
- Python 3.7 or higher
- Required Python library:
  ```bash
  pip install pycountry


---

## File Structure

- **`BelsenLeak/`**: Base folder containing country subfolders named by ISO Alpha-2 codes.
- Each country folder contains subfolders named with IP and port details in the format `IP_PORT` (e.g., `192.168.0.1_8080`).
The script assumes the following structure:
```
BelsenLeak/
├── US/
│   ├── 192.168.0.1_8080/
│   │   ├── credentials.txt
│   │   ├── config.txt
│   └── 192.168.0.2_9090/
│       └── data.txt
├── DE/
│   └── 10.0.0.1_80/
│       ├── logs.txt
│       └── other_data.txt
KeywordSearchTerms.txt
Config_Matches.txt
All Credentials.txt
Credential_Matches.txt
All_IPs_by_Country.txt

```

---

### Input:

- **`KeywordSearchTerms.txt`**: An input file for you to list search terms, one per line.

---

### Outputs

The script generates the following output files:

- **`Config_Matches.txt`**: Matches based on `KeywordSearchTerms.txt` in processed files.
- **`All Credentials.txt`**: A consolidated list of credentials from all `.txt` files, organized by country.
- **`Credential_Matches.txt`**: Credentials matching specific search terms.
- **`All_IPs_by_Country.txt`**: IP addresses and ports organized by country.

---

### Usage

#### 1. Prepare Input Files

- Organize your data inside the `BelsenLeak/` folder as described in the file structure.
- Add search terms to `KeywordSearchTerms.txt`, one term per line.

  Example 'KeywordSearchTerms.txt':
  company1
  company2
  knowncompanyuseraccount
  knowncredential
  etc...


#### 2. Run the Script

Execute the script using Python:

```bash
python script_name.py
```

### 3. Review Outputs
- Open `Config_Matches.txt`, `All_IPs_by_Country`, `All Credentials.txt`, and `Credential_Matches.txt` to review results.

---

## Code Details

### Main Workflow
1. Clears the contents of all output files to avoid duplicates.
2. Processes country subfolders by expanding ISO Alpha-2 country codes.
3. Extracts and logs credentials from .txt files using a regex pattern.
4. Searches for terms in files based on the provided KeywordSearchTerms.txt.
5. Organizes and outputs data into the corresponding files.

---

## Customization
- **Regex Pattern**: Update the regex pattern in parse_file_with_pattern() to match your desired format. The default matches `username:password`.
- **Search Terms**: Add or modify terms in `KeywordSearchTerms.txt` to adjust the scope of your search.
- **File Structure**: Change the `BASE_FOLDER` variable in the script if your folder structure differs.

---

## License
This script is provided under the MIT License. Feel free to use and modify it.
