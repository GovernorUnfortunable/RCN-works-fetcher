This repository includes scripts for retrieving information from Open Alex to map the work of a Research Coordination Network. So far, these are the scripts included: 

## 1. ´RCN-works-fetcher´
This Python script retrieves and analyzes academic works from the OpenAlex database for a predefined list of authors (in this case, the NSF-SEEKCommons research project). It provides  data extraction and includes author information and some publication details.

### Features
1. Fetches academic works for multiple authors (i.e., [people who create works]([url](https://docs.openalex.org/api-entities/authors))) 
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
   git clone https://github.com/yourusername/openalex-works-retrieval.git
   cd openalex-works-retrieval
   ```
   
2. Run the script:
   ```bash
   python openalex_works_retrieval.py
   ```

3. Follow the prompts:
   - Enter your email address (this optional, but recommended to work with OpenAlex API recommendations)
   - Specify start and end dates for work retrieval (format YYYY-MM-DD)

### Provided outputs
The script generates three output files in the `openalex_outputs` directory:

1. `openalex_works_{start_date}_{end_date}.csv`
   - Columns: author_id, openalex_author_id, orcid, author_name, title, publication_year, openalex_url

2. `top_10_authors_{start_date}_{end_date}.csv`
   - Lists top 10 authors by publication count

3. `works_citations_{start_date}_{end_date}.txt`
   - Detailed citations including:
     * Author name
     * OpenAlex ID
     * ORCID
     * Last known institution
     * Publication details

### Customization
To modify the list of authors, edit the `author_ids` list in the script. The current list includes 70+ author IDs.

### API Considerations
- The script implements a 1-second delay between API requests to be API-friendly
- Requires an email address for API courtesy
- Handles potential API request errors gracefully

### Limitations
- Limited to the OpenAlex database
- Rate-limited by OpenAlex API guidelines
- Requires manual updates to the author list

## License
Distributed under the MIT License. See `LICENSE` for more information.

## Contact
M. Milia <mmilia@nd.edu>

## Acknowledgments
- [OpenAlex](https://openalex.org/) for providing the academic works database
- [Requests](https://docs.python-requests.org/en/master/) library
- [Pandas](https://pandas.pydata.org/) for data manipulation
