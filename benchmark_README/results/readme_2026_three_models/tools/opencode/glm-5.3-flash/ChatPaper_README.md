# ChatPaper

ChatPaper is a research automation toolset for academic papers. It combines PDF parsing, arXiv search, and OpenAI GPT models to help researchers quickly read, translate, review, and survey scientific literature.

## Features

- **Paper Summarization**: Extracts sections, metadata, and figures from local PDFs and generates structured summaries using OpenAI models (`chat_paper.py`).
- **arXiv Search**: Queries arXiv for recent papers matching keywords and automatically summarizes the results (`chat_arxiv.py`).
- **Paper Translation**: Uses GPT-3.5-turbo (switching to the 16k-token variant for long text) to translate scientific PDFs, powered by the bundled GROBID-based `scipdf` parser (`chat_translate.py`).
- **Automated Literature Review**: The `auto_survey/` sub-project automatically searches for related papers, provides sourced citations, and generates survey documents in both LaTeX and Markdown.
- **Reviewer & Response Generation**: The `ChatReviewerAndResponse/` sub-project simulates peer-review comments on a paper and generates point-by-point responses to reviewer feedback.
- **Hugging Face Deployment**: `HuggingFaceDeploy/` contains app files for deploying ChatPaper interfaces on Hugging Face Spaces.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/kaixindelele/ChatPaper.git
   cd ChatPaper
   ```

2. Install the required Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. For `chat_translate.py`, a GROBID service must be running. Use the bundled script:
   ```bash
   bash scipdf_parser-master/serve_grobid.sh
   ```

## Usage

### Summarize a Local PDF

Run the summarization script against a local PDF (defaults to `demo.pdf`):
```bash
python chat_paper.py --pdf_path demo.pdf
```

### Summarize Papers from arXiv

Query arXiv, filter results, and summarize the matching papers:
```bash
python chat_arxiv.py --query "traffic flow prediction" --key_word "GPT robot" --max_results 3 --days 10
```

### Translate a Paper

Ensure the GROBID service is running, then translate a PDF:
```bash
python chat_translate.py
```

### Automated Survey

Navigate into the sub-project folder (it is an independent project):
```bash
cd auto_survey
pip install -r requirements.txt
export OPENAI_API_KEY="your-api-key"
# Edit main.py to set your survey topic
python main.py
```
Results are saved in `auto_survey/outputs/<timestamp>/`, including `survey.md` and `main.tex`.

### Reviewer & Response

Navigate into the sub-project folder and follow the scripts there:
```bash
cd ChatReviewerAndResponse
```
Note that this folder is an independent project and must be opened/run on its own.

## Configuration

- **OpenAI API Key**: Must be set in the environment or directly in the scripts (depending on which module is used).
- **Language**: Output language can be switched between English (`en`) and Chinese (`zh`) using the `--language` flag.
- **File Format**: Output format can be toggled between Markdown (`md`) and plain text (`txt`) using the `--file_format` flag.

## Project Structure

- `chat_paper.py` / `chat_arxiv.py`: Core scripts for PDF parsing, summarization, and arXiv integration.
- `chat_translate.py`: Script for translating scientific PDFs.
- `auto_survey/`: Sub-project for generating automated literature surveys.
- `ChatReviewerAndResponse/`: Sub-project for simulating paper reviews and generating responses.
- `HuggingFaceDeploy/`: Files for deploying on Hugging Face Spaces.
- `scipdf_parser-master/`: Bundled copy of the GROBID-based scientific PDF parser.
- `docker/`: Docker-related build and configuration files.
- `source/`: Sphinx documentation source files.
- `others/`: Auxiliary notebooks and scripts (e.g., Google Scholar scraping).
- `demo.pdf`: Sample PDF for testing.

## Dependencies

Key dependencies listed in `requirements.txt` include:
- `arxiv`
- `PyMuPDF`
- `requests`
- `tiktoken`
- `tenacity`
- `openai`
- `gradio`
- `flask`

## License

This project is licensed under the [Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License](http://creativecommons.org/licenses/by-nc-nd/4.0/).
