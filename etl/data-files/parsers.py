import subprocess
import shutil
import os
from urllib.parse import urlparse

class Gitparser:
    @classmethod
    def create(cls):
        # Return an instance of Gitparser (note the parentheses)
        return cls()

    def extract(self, repo_url: str) -> list:
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

class Director:
    def __init__(self):
        # Initialize the parsers dictionary in the instance
        self.parsers = {}
        # Add Gitparser for GitHub
        self.parsers['github.com'] = Gitparser.create()

    def extract(self, link: str):
        # Get the domain from the link
        domain = urlparse(link).netloc
        parser = self.parsers.get(domain)
        if not parser:
            raise ValueError(f"No parser available for domain: {domain}")
        return parser.extract(link)

if __name__ == "__main__":
    link = 'https://github.com/yTKONOSINA/data-pipeline-demo'
    # Create an instance of Director
    director = Director()
    file_contents = director.extract(link)
    for filename, content in file_contents.items():
        print(f"Filename: {filename}\nContent:\n{content}\n{'-'*40}")
