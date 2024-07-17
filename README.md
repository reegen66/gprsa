# Automated GitHub Private Project/Repository Setup/Creator

This powerful Python script automates the process of setting up a new GitHub repository, making it easier than ever to start a new coding project. Whether you're a seasoned developer or just starting out, this tool streamlines your workflow by handling repository creation, Git initialization, and initial commits all in one go.

## Features

- 🚀 Automatically creates a new private GitHub repository
- 🔧 Initializes Git locally and sets up remote origin
- 📝 Downloads language-specific `.gitignore` files (Python or Node.js)
- 🔒 Securely handles GitHub authentication using personal access tokens
- 🧹 Option to clean existing Git files for a fresh start
- ✏️ Allows adding custom entries to `.gitignore`
- 🔄 Performs initial commit and push to the new repository

## Prerequisites

Before you begin, ensure you have the following installed:
- Python 3.6 or higher
- `pip` (Python package manager)

## Quick Start

To get started with the GitHub Project Setup Script, follow these steps:

1. Download the script using `wget`:

```bash
wget https://raw.githubusercontent.com/reegen66/agprc/main/github_setup.py
```

2. Install the required Python packages:

```bash
pip install requests python-dotenv
```

3. Create a `.env` file in the same directory as the script with the following content:

```
GITHUB_TOKEN=your_personal_access_token_here
GITHUB_EMAIL=your_github_email@example.com
```

Replace `your_personal_access_token_here` with your GitHub personal access token and `your_github_email@example.com` with your GitHub email address.

4. Make the script executable:

```bash
chmod +x github_setup.py
```

5. Run the script:

```bash
./github_setup.py
```

## Usage

When you run the script, it will guide you through the following steps:

1. If an existing Git repository is detected, it will ask if you want to delete it and start fresh.
2. You'll be prompted to choose the project language (Python or Node.js).
3. The script will download the appropriate `.gitignore` file for your chosen language.
4. You'll have the option to add custom lines to the `.gitignore` file.
5. You'll be asked to enter a name for your new GitHub repository.
6. The script will create the repository, initialize Git, and push the initial commit.

## Creating a GitHub Personal Access Token

To use this script, you need to create a GitHub Personal Access Token with the correct permissions. Follow these steps:

1. Log in to your GitHub account.
2. Click on your profile picture in the top-right corner and select "Settings" from the dropdown menu.
3. In the left sidebar, click on "Developer settings".
4. In the new left sidebar, click on "Personal access tokens".
5. Click on "Generate new token" (or "Generate new token (classic)" if you see that option).
6. Give your token a descriptive name, e.g., "GitHub Project Setup Script".
7. Set the expiration as per your preference. For security reasons, it's recommended to set an expiration date.
8. Select the following scopes (permissions):
   - `repo` (Full control of private repositories)
     - This allows the script to create and manage repositories.
   - `admin:public_key` (Manage your public keys)
     - This allows the script to add deploy keys to your repositories if needed.
9. Scroll to the bottom and click "Generate token".
10. **Important:** Copy the generated token immediately and store it securely. You won't be able to see it again!

Once you have your token, add it to your `.env` file like this:

```
GITHUB_TOKEN=your_generated_token_here
GITHUB_EMAIL=your_github_email@example.com
```

Replace `your_generated_token_here` with the actual token you just created, and `your_github_email@example.com` with the email associated with your GitHub account.

**Security Note:** Never share your personal access token or commit it to a repository. The `.env` file is included in the `.gitignore` to prevent accidental exposure of your token.

## Troubleshooting

If you encounter any issues:

- Ensure your GitHub token has the necessary permissions to create repositories.
- Check that your `.env` file is in the correct location and contains the right information.
- Make sure you have a stable internet connection.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Keywords

GitHub automation, repository setup, Git initialization, Python script, Node.js projects, developer workflow, project management, version control, .gitignore management, GitHub API

---
Credits: [https://bizigniter.io](https://bizigniter.io)
Happy coding! 🎉

