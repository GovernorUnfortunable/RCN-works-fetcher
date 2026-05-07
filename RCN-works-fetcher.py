import os
import requests
from datetime import datetime, date
import json
import time
import re
import csv
import pandas as pd

def validate_email(email):
    """Validate email address format."""
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email) is not None

def get_user_email():
    """Prompt user for a valid email address."""
    while True:
        email = input("Please enter your email address (used for OpenAlex API courtesy): ").strip()
        if validate_email(email):
            return email
        print("Invalid email address. Please try again.")

def get_date_range():
    """Prompt user for start and end dates."""
    while True:
        try:
            start_input = input("Enter start date (YYYY-MM-DD) or press Enter for no start date: ").strip()
            end_input = input("Enter end date (YYYY-MM-DD) or press Enter for today's date: ").strip()

            start_date = datetime.strptime(start_input, "%Y-%m-%d").date() if start_input else None
            end_date = datetime.strptime(end_input, "%Y-%m-%d").date() if end_input else date.today()

            return start_date, end_date
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")

def load_author_ids(filepath):
    """Load author IDs from a plain text file (one ID per line)."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Author IDs file not found: '{filepath}'")

    with open(filepath, 'r', encoding='utf-8') as f:
        ids = [line.strip() for line in f if line.strip() and not line.startswith('#')]

    if not ids:
        raise ValueError(f"No author IDs found in '{filepath}'. Make sure the file has one ID per line.")

    print(f"Loaded {len(ids)} author ID(s) from '{filepath}'.")
    return ids

def get_author_ids_file():
    """Prompt user for the path to the author IDs file."""
    while True:
        filepath = input("Enter the path to your author IDs file (e.g., authors.txt): ").strip()
        try:
            return load_author_ids(filepath)
        except (FileNotFoundError, ValueError) as e:
            print(f"Error: {e}")
            print("Please try again.\n")

def fetch_author_details(author_id, email):
    """Fetch detailed information for a specific author from OpenAlex."""
    base_url = f"https://api.openalex.org/authors/{author_id}"
    
    params = {
        "mailto": email
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        author_data = response.json()
        
        return {
            'openalex_id': author_data.get('id', 'Unknown'),
            'orcid': author_data.get('orcid', 'Unknown'),
            'display_name': author_data.get('display_name', 'Unknown'),
            'works_count': author_data.get('works_count', 0),
            'last_known_institution': author_data.get('last_known_institution', {}).get('display_name', 'Unknown')
        }
    except requests.RequestException as e:
        print(f"Error fetching author details for {author_id}: {e}")
        return None

def fetch_author_works(author_id, email, start_date=None, end_date=None):
    """Fetch works for a specific author from OpenAlex."""
    base_url = "https://api.openalex.org/works"
    
    filters = [f"author.id:{author_id}"]
    
    if start_date:
        filters.append(f"from_publication_date:{start_date}")
    if end_date:
        filters.append(f"to_publication_date:{end_date}")
    
    filter_param = ",".join(filters)
    
    params = {
        "filter": filter_param,
        "mailto": email,
        "per_page": 200
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching works for author {author_id}: {e}")
        return None

def format_citation(work, author_details=None):
    """Create a formatted citation for a work."""
    title = work.get('title', 'No Title')
    
    authors = work.get('authorships', [])
    author_names = [a.get('author', {}).get('display_name', 'Unknown') for a in authors[:3]]
    author_str = ', '.join(author_names) + (', et al.' if len(authors) > 3 else '')
    
    publication_year = work.get('publication_year', 'N/A')
    
    venue = 'Unknown Venue'
    primary_location = work.get('primary_location', {}) or {}
    if primary_location:
        source = primary_location.get('source', {}) or {}
        venue = source.get('display_name', 'Unknown Venue')
    
    openalex_url = work.get('id', 'No URL')
    
    author_info = ""
    if author_details:
        author_info = f" | OpenAlex: {author_details.get('openalex_id', 'N/A')}"
        author_info += f" | ORCID: {author_details.get('orcid', 'N/A')}"
    
    citation = f"{author_str}. ({publication_year}). {title}. {venue}. OpenAlex: {openalex_url}{author_info}"
    
    return citation

def main():
    print("=== OpenAlex Works Fetcher ===\n")

    # Load author IDs from file
    author_ids = get_author_ids_file()

    # Get user email for API courtesy
    email = get_user_email()

    # Get date range for works
    start_date, end_date = get_date_range()

    # Collect works for all authors
    all_works = {}
    works_data = []
    author_details_dict = {}

    for author_id in author_ids:
        author_details = fetch_author_details(author_id, email)
        if author_details:
            author_details_dict[author_id] = author_details

        print(f"\nFetching works for author {author_id}...")
        works = fetch_author_works(author_id, email, start_date, end_date)
        
        if works:
            results = works.get('results', works)
            if results:
                all_works[author_id] = results
                print(f"Retrieved {len(results)} works for author {author_id}")
                
                for work in results:
                    works_data.append({
                        'author_id': author_id,
                        'openalex_author_id': author_details.get('openalex_id', 'N/A') if author_details else 'N/A',
                        'orcid': author_details.get('orcid', 'N/A') if author_details else 'N/A',
                        'author_name': author_details.get('display_name', 'N/A') if author_details else 'N/A',
                        'title': work.get('title', 'No Title'),
                        'publication_year': work.get('publication_year', 'N/A'),
                        'openalex_url': work.get('id', 'No URL')
                    })
            else:
                print(f"No works found for author {author_id}")
        else:
            print(f"No works retrieved for author {author_id}")
        
        time.sleep(1)

    # Create output directory
    output_dir = 'openalex_outputs'
    os.makedirs(output_dir, exist_ok=True)

    df = pd.DataFrame(works_data)
    date_str = f"{start_date or 'all_time'}_{end_date}"

    author_publication_counts = df.groupby('author_id').size().sort_values(ascending=False)
    top_10_authors = author_publication_counts.head(10)

    works_csv_path = os.path.join(output_dir, f"openalex_works_{date_str}.csv")
    df.to_csv(works_csv_path, index=False)

    top_authors_csv_path = os.path.join(output_dir, f"top_10_authors_{date_str}.csv")
    top_10_authors.to_frame('publication_count').to_csv(top_authors_csv_path)

    citations_path = os.path.join(output_dir, f"works_citations_{date_str}.txt")
    with open(citations_path, 'w', encoding='utf-8') as f:
        for author_id, works in all_works.items():
            author_details = author_details_dict.get(author_id)
            
            if author_details:
                f.write(f"Author: {author_details.get('display_name', 'Unknown')}\n")
                f.write(f"OpenAlex ID: {author_details.get('openalex_id', 'N/A')}\n")
                f.write(f"ORCID: {author_details.get('orcid', 'N/A')}\n")
                f.write(f"Last Known Institution: {author_details.get('last_known_institution', 'N/A')}\n")
            else:
                f.write(f"Author ID: {author_id}\n")
            
            f.write("-" * 50 + "\n")
            
            for work in works:
                try:
                    f.write(format_citation(work, author_details) + "\n")
                except Exception as e:
                    f.write(f"Error formatting citation: {e}\n")
                    f.write(f"Problematic work: {work}\n")
            f.write("\n\n")

    print(f"\nTotal works retrieved: {len(df)}")
    print(f"Top 10 authors by publication count:\n{top_10_authors}")
    print(f"\nOutputs saved:")
    print(f"1. Works CSV: {works_csv_path}")
    print(f"2. Top 10 Authors CSV: {top_authors_csv_path}")
    print(f"3. Works Citations: {citations_path}")

if __name__ == "__main__":
    main()
