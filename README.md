Find below scripts for retrieving information from Open Alex to map the work of a Research Coordination Network. 

## 1. The RCN-works-fetcher
RCN-works-fetcher is a Python-based tool designed to retrieve and systematize the academic and technical output of a Research Coordination Network (RCN) from the OpenAlex open database. It automates the collection of works, author metadata (including ORCID identifiers and institutional affiliations), and publication details for a predefined list of authors and developers (in our original use case, network members), filtering results by date range. Output files support downstream use in knowledge infrastructure projects — e.g., the SEEKCommons Resource Hub — where making the collective work of researchers, activists, and technologists credited, discoverable, reusable, and actionable is central to supporting research oriented to address socio-environmental challenges and document environmental harm.

### Features
1. Loads author IDs from a plain text file (one ID per line), making it easy to update your list without editing the script (i.e., [people who create works]([url](https://docs.openalex.org/api-entities/authors))) 
2. Retrieves detailed author information, including:
  - OpenAlex ID
  - ORCID
  - Display Name
  - Last Known Institution
3. Filters [works]([url](https://docs.openalex.org/api-entities/works/)) (i.e., journal articles, books, datasets, and theses) by date range (asked to the user as YYYY-MM-DD)
4. Generate multiple output formats:
  - CSV with works details
  - CSV with top 10 authors by publication count
  - Text file with formatted citations
5. Takes into account OpenAlex API guidelines for respectful data extraction. 

### Required Libraries
Runs on Python 3.7+ and requires to install the necessary libraries using pip:

```bash
pip install requests pandas
```

### How to use

1. Clone the repository:
```bash
   git clone https://github.com/GovernorUnfortunable/RCN-works-fetcher.git
   cd RCN-works-fetcher
```

2. Prepare your author IDs file by creating a plain text file (e.g., `authors.txt`) with one OpenAlex author ID per line. Lines starting with `#` are treated as comments and ignored:
```
   # Add your target group/network members' OpenAlex IDs here
   a0000000001
   a0000000002
```

3. Run the script:
   ```bash
   python RCN-works-fetcher.py
   ```
   
4. Follow the prompts:
   - Enter the path to your author IDs file (e.g., `authors.txt`)
   - Enter your email address (this is optional, but recommended as a courtesy to the OpenAlex API)
   - Specify start and end dates for work retrieval (format `YYYY-MM-DD`). Press Enter to skip either date.

### Provided outputs
The script generates three output files in the `openalex_outputs` directory:

1. `openalex_works_{start_date}_{end_date}.csv`
   - Columns: author_id, openalex_author_id, orcid, author_name, title, publication_year, openalex_url

2. `top_10_authors_{start_date}_{end_date}.csv`
   - Lists top 10 authors by publication count

3. `works_citations_{start_date}_{end_date}.txt`
   - A detailed list of citations including:
     * Author name
     * OpenAlex ID
     * ORCID
     * Last known institution
     * Publication details

### Customization
To modify the list of authors, edit your authors.txt file. Add or remove one OpenAlex author ID per line. No changes to the script itself are needed.

### API Considerations
- The script implements a 1-second delay between API requests to be API-friendly
- Requires an email address for API courtesy
- Handles potential API request errors gracefully

### Limitations
- Limited to the OpenAlex database
- Rate-limited by OpenAlex API guidelines (see also new guidelines for credit use in OpenAlex)
- Requires manual updates to the author list
- Authors with very large publication records may have results truncated

## License
Distributed under the MIT License. See `LICENSE` for more information.

## Contact
M. Milia <mmilia@nd.edu>

## Acknowledgments
- [OpenAlex](https://openalex.org/) for providing the academic works database
- [Requests](https://docs.python-requests.org/en/master/) library
- [Pandas](https://pandas.pydata.org/) for data manipulation
