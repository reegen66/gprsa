#!/usr/bin/env python3
import os
import subprocess
import requests
import json
from dotenv import load_dotenv
import sys
import shutil
import re
import tempfile

# Load environment variables from .gprsa
def load_gprsa():
    if os.path.exists('.gprsa'):
        with open('.gprsa', 'r') as f:
            for line in f:
                if '=' in line:
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value

# Load environment variables
load_gprsa()

# GitHub API endpoint
GITHUB_API = "https://api.github.com"

def log(message):
    print(f"[LOG] {message}")

def run_command(command, check_error=True, mask_token=False):
    if mask_token:
        logged_command = re.sub(r'(https://)[^@]*(@)', r'\1[TOKEN HIDDEN]\2', command)
    else:
        logged_command = command
    log(f"Executing command: {logged_command}")
    
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    
    output_str = output.decode('utf-8')
    error_str = error.decode('utf-8')
    
    if output_str.strip():
        log(f"Command output: {output_str}")
    if error_str.strip():
        log(f"Command error: {error_str}")
    
    if check_error and process.returncode != 0:
        raise Exception(f"Command failed with return code {process.returncode}")
    
    return output_str, error_str

def clean_git_files():
    log("Cleaning existing Git files...")
    if os.path.exists('.git'):
        shutil.rmtree('.git')
    if os.path.exists('.gitignore'):
        os.remove('.gitignore')
    
    # Remove any existing submodules
    for item in os.listdir('.'):
        if os.path.isdir(item) and os.path.exists(os.path.join(item, '.git')):
            log(f"Removing submodule: {item}")
            shutil.rmtree(item)

def download_gitignore(language):
    log(f"Downloading .gitignore for {language}...")
    url = f"https://raw.githubusercontent.com/github/gitignore/main/{language}.gitignore"
    response = requests.get(url)
    if response.status_code == 200:
        with open('.gitignore', 'w') as f:
            f.write(response.text)
        log(".gitignore downloaded successfully")
        
        # Add github_setup.py and .gprsa to .gitignore
        with open('.gitignore', 'a') as f:
            f.write("\n# Ignore GitHub setup script and auth file\ngithub_setup.py\n.gprsa\n")
        log("Added github_setup.py and .gprsa to .gitignore")
    else:
        log(f"Failed to download .gitignore. Status code: {response.status_code}")
        sys.exit(1)

def add_custom_gitignore():
    log("Add custom lines to .gitignore (type 'imdone' when finished):")
    with open('.gitignore', 'a') as f:
        while True:
            line = input("Enter a line to add to .gitignore (or 'imdone' to finish): ")
            if line.lower() == 'imdone':
                break
            f.write(f"{line}\n")
    log("Custom lines added to .gitignore")

def create_github_repo(token, repo_name):
    log(f"Creating GitHub repository: {repo_name}")
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    data = {
        'name': repo_name,
        'private': True
    }
    response = requests.post(f'{GITHUB_API}/user/repos', headers=headers, json=data)
    if response.status_code == 201:
        log("Repository created successfully")
        return response.json()['clone_url']
    else:
        log(f"Failed to create repository. Status code: {response.status_code}")
        log(f"Response: {response.text}")
        sys.exit(1)

def setup_git(repo_url, github_email, github_token):
    log("Setting up Git...")
    run_command('git init')
    run_command(f'git config user.email "{github_email}"')
    run_command('git config user.name "$(git config user.email)"')
    
    # Use HTTPS URL with embedded token
    repo_url_with_token = repo_url.replace('https://', f'https://{github_token}@')
    run_command(f'git remote add origin {repo_url_with_token}', mask_token=True)
    
    run_command('git add .')
    run_command('git commit -m "Initial commit"')
    run_command('git branch -M main')
    run_command('git push -u origin main')

def clone_private_repo(token, repo_url, github_email):
    log(f"Preparing to clone private repository: {repo_url}")
    
    # Ensure the URL ends with .git
    if not repo_url.endswith('.git'):
        repo_url += '.git'
    
    # Extract the repo name from the URL
    repo_name = repo_url.split('/')[-1].replace('.git', '')
    
    # Use HTTPS URL with embedded token
    repo_url_with_token = repo_url.replace('https://', f'https://{token}@')
    
    # Create a temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        log(f"Created temporary directory for cloning: {temp_dir}")
        
        # Clone the repository into the temporary directory
        run_command(f'git clone {repo_url_with_token} {temp_dir}', mask_token=True)
        
        # Move contents from temp directory to current directory
        for item in os.listdir(temp_dir):
            source = os.path.join(temp_dir, item)
            destination = os.path.join('.', item)
            
            if os.path.exists(destination):
                if item == '.env':
                    # Rename .env to .env_repo to avoid conflicts
                    os.rename(source, os.path.join(temp_dir, '.env_repo'))
                    log(f"Renamed repository's .env to .env_repo")
                    source = os.path.join(temp_dir, '.env_repo')
                elif item == '.git':
                    # Remove existing .git folder
                    shutil.rmtree(destination)
                else:
                    # Remove existing file/folder
                    if os.path.isfile(destination):
                        os.remove(destination)
                    else:
                        shutil.rmtree(destination)
            
            # Move item from temp directory
            shutil.move(source, destination)
    
    log("Repository contents moved to current directory")
    
    # Set up git configuration
    run_command(f'git config user.email "{github_email}"')
    run_command('git config user.name "$(git config user.email)"')
    
    log(f"Repository {repo_name} cloned successfully")
    return repo_url

def main():
    log("Starting GitHub project setup...")
    
    # Get GitHub personal access token and email from .gprsa file
    github_token = os.getenv('GITHUB_TOKEN')
    github_email = os.getenv('GITHUB_EMAIL')

    if not github_token or not github_email:
        log("ERROR: GITHUB_TOKEN or GITHUB_EMAIL not set in .gprsa file.")
        sys.exit(1)

    # Ask user whether to clone an existing repo or create a new one
    while True:
        action = input("Choose an action:\n1. Clone an existing repository\n2. Create a new repository and push existing project files\nEnter 1 or 2: ")
        if action in ['1', '2']:
            break
        log("Invalid choice. Please enter 1 or 2.")

    if action == '1':  # Clone existing repository
        repo_url = input("Enter the URL of the private repository you want to clone: ")
        try:
            # Clone the private repository
            cloned_repo_url = clone_private_repo(github_token, repo_url, github_email)
            log("Private repository cloned successfully.")
            log(f"Repository URL: {cloned_repo_url}")
            
        except Exception as e:
            log(f"An error occurred while cloning: {str(e)}")
            sys.exit(1)

    elif action == '2':  # Create new repository
        # Ask for confirmation before cleaning Git files
        if os.path.exists('.git'):
            confirm = input("Existing Git conifguration detected. Do you want to delete it (only configuration files) and start fresh? (y/n): ").lower()
            if confirm == 'y':
                clean_git_files()
                confirm_continue = input("Existing Git files have been deleted. Do you want to continue with creating a new repository? (y/n): ").lower()
                if confirm_continue != 'y':
                    log("Setup cancelled by user.")
                    sys.exit(0)
            else:
                log("Keeping existing Git files. Proceeding with caution.")
        else:
            log("No existing Git repository detected. Proceeding with setup.")

        # Ask for language choice
        language = input("Enter the project language (python/node): ").lower()
        if language not in ['python', 'node']:
            log("Invalid language choice. Please choose 'python' or 'node'.")
            sys.exit(1)

        # Download appropriate .gitignore
        download_gitignore('Python' if language == 'python' else 'Node')

        # Ask if user wants to add custom lines to .gitignore
        add_custom = input("Do you want to add custom lines to .gitignore? (y/n): ").lower()
        if add_custom == 'y':
            add_custom_gitignore()

        # Ask for project name
        project_name = input("Enter the project name for GitHub: ")

        try:
            # Create GitHub repository
            repo_url = create_github_repo(github_token, project_name)

            # Setup git and push to GitHub
            setup_git(repo_url, github_email, github_token)

            log("GitHub project setup completed successfully.")
            log(f"Repository URL: {repo_url}")

        except Exception as e:
            log(f"An error occurred: {str(e)}")
            sys.exit(1)

if __name__ == "__main__":
    main()
