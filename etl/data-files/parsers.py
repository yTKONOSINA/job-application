from typing import Annotated
from loguru import logger
import subprocess
import shutil
import os
import requests
import fitz  # PyMuPDF's module name is 'fitz'
from urllib.parse import urlparse
from bs4 import BeautifulSoup

class Gitparser:
    @classmethod
    def create(cls):
        # Return an instance of Gitparser (note the parentheses)
        return cls()

    def extract(self, repo_url: str) -> Annotated[list, "Repo's code"]:
        # Automatically determine the clone directory from the repo_url.
        # It takes the last part of the URL, and if it ends with '.git', removes it.
        repo_name = repo_url.rstrip('/').split('/')[-1]
        if repo_name.endswith('.git'):
            repo_name = repo_name[:-4]
        clone_dir = repo_name

        # Clone the repository into clone_dir
        subprocess.run(['git', 'clone', repo_url], check=True)

        # Define exclusion criteria
        exclude_extensions = {'.txt', '.log'}  # Add any extensions you want to exclude
        exclude_filenames = {'__init__.py', '.gitignore'} 

        file_content_dict = {}
        # Traverse the cloned repository
        for root, _, files in os.walk(clone_dir):
            for file in files:
                if (file not in exclude_filenames and
                    not any(file.lower().endswith(ext.lower()) for ext in exclude_extensions)):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            file_content_dict[file] = f.read()
                    except Exception as e:
                        print(f"Error reading {file_path}: {e}")
        
        # Delete the cloned repository after processing
        shutil.rmtree(clone_dir)

        return [file_content_dict]

class PDFparser:
    @classmethod
    def create(cls):
        return cls()
    
    def extract(self, url : str) -> Annotated[list | None, "Content's of pdf"]:
        # Step 1: Download the PDF
        pdf_path = "temp.pdf"  # Temporary file name

        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(pdf_path, "wb") as f:
                f.write(response.content)
            logger.info(f"Downloaded PDF : {url} to {pdf_path}")
        else:
            print(f"Failed to download PDF: {response.status_code}")
            return None

        # Step 2: Extract text from all pages
        doc = fitz.open(pdf_path)
        full_text = ""
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            full_text += page.get_text()  # Append text from each page
        
        # Close the document
        doc.close()

        # Step 3: Delete the PDF
        os.remove(pdf_path)
        logger.info(f"Deleted file s{url}")

        return [full_text]

class DefaultParser:
    @classmethod
    def create(cls):
        return cls()
    
    def extract(self, url : str) -> Annotated[list | None, "Content's of url"]:
        # Send an HTTP request
        response = requests.get(url)

        # Check if request was successful
        if response.status_code != 200:
            logger.info("Failed to retrieve the page")
            return None
        # Parse the HTML content
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Extract specific text (Example: All paragraph texts)
        paragraphs = [p.get_text() for p in soup.find_all("p")]

        return paragraphs

class Director:
    def __init__(self):
        # Initialize the parsers dictionary in the instance
        self.parsers = {}
        # Add Gitparser for GitHub
        self.parsers['.git'] = Gitparser.create()
        self.parsers['.pdf'] = PDFparser.create()
        self.parsers['.'] = DefaultParser.create()

    def extract(self, link: str):
        # Get the domain from the link
        path = urlparse(link).path
        extention = '.' + path.split('.')[-1].lower()
        parser = self.parsers.get(extention, self.parsers['.'])
        if not parser:
            raise ValueError(f"No parser available for domain: {extention}")
        return parser.extract(link)

if __name__ == "__main__":
    link = 'https://github.com/yTKONOSINA/data-pipeline-demo'
    # Create an instance of Director
    director = Director()
    file_contents = director.extract(link)
    for filename, content in file_contents.items():
        print(f"Filename: {filename}\nContent:\n{content}\n{'-'*40}")
