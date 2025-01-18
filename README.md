# Belson File Processing and Search Tool

## This tool is designed strictly for rapid assessment of compromise status. Any misuse of this tool for illegal purposes is not condoned.

## Overview
This Python script is designed to search for specific patterns and terms in files located within a folder structure. It provides functionality to:
- Parse files with regex patterns.
- Search for terms in configuration and text files.
- Output results to specific files for detailed analysis.

---

## Features
- **Regex-based Parsing**: Identify lines in files matching custom regex patterns.
- **Memory-mapped Search**: Efficiently search large files using `mmap`.
- **Credential Matching**: Search for specific terms in credential files and generate separate reports for all matches and credential-specific matches.
- **Folder Processing**: Automatically processes all `conf` and `txt` files in a folder hierarchy.

---

## Prerequisites
- Python 3.6 or higher
- A `data/` directory containing subdirectories with `.conf` and `.txt` files.
- A `searchterms.txt` file containing newline-separated search terms.

---

## File Structure
The script assumes the following structure:
```
project/
├── data/
│   ├── folder1/
│   │   ├── example1.conf
│   │   ├── example2.txt
│   ├── folder2/
│       ├── example3.conf
│       ├── example4.txt
├── searchterms.txt
├── configMatches.txt
├── creds.txt
├── matchedCreds.txt
```

---

## Outputs
- **`configMatches.txt`**: Contains lines from `.conf` files matching search terms.
- **`creds.txt`**: Contains all parsed lines from `.txt` files matching the regex pattern. [Default is '.+:.*']
- **`matchedCreds.txt`**: Contains only the lines from `.txt` files that match the search terms.

---

## Usage

### 1. Place Input Files
- Place your files in the `data/` folder.
- Add search terms to `searchterms.txt`, each term on a new line.

### 2. Run the Script
```bash
python script_name.py
```

### 3. Review Outputs
- Open `configMatches.txt`, `creds.txt`, and `matchedCreds.txt` to review results.

---

## Code Details

### Main Workflow
1. Clears the output files.
2. Processes `.conf` and `.txt` files for matches.
3. Logs results to designated output files.

---

## Customization
- **Regex Pattern**: Modify the regex pattern in `process_folder()` to customize line parsing.
- **Search Terms**: Add or modify terms in `searchterms.txt` to adjust the scope of your search.
- **File Structure**: Update `BASE_FOLDER` if your folder structure differs.

---

## License
This script is provided under the MIT License. Feel free to use and modify it.
