#!/bin/bash

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function for colorful and animated output
print_animated() {
    local text="$1"
    local color="$2"
    case "$color" in
        "red") color_code="\033[0;31m" ;;
        "green") color_code="\033[0;32m" ;;
        "yellow") color_code="\033[0;33m" ;;
        "blue") color_code="\033[0;34m" ;;
        *) color_code="\033[0m" ;;
    esac
    
    echo -ne "${color_code}"
    for (( i=0; i<${#text}; i++ )); do
        echo -n "${text:$i:1}"
        sleep 0.03
    done
    echo -e "\033[0m"
}

# Detect OS
if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS=$NAME
elif type lsb_release >/dev/null 2>&1; then
    OS=$(lsb_release -si)
elif [ -f /etc/lsb-release ]; then
    . /etc/lsb-release
    OS=$DISTRIB_ID
else
    OS=$(uname -s)
fi

# Ask for user confirmation
print_animated "This script will set up your GitHub environment." "blue"
print_animated "Detected OS: $OS" "yellow"
read -p "Do you want to proceed with the installation? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    print_animated "Installation cancelled." "red"
    exit 1
fi

# Check if pip is installed
if ! command_exists pip; then
    print_animated "pip is not installed. Installing..." "yellow"
    case "$OS" in
        *Ubuntu*|*Debian*)
            print_animated "Suggested command: sudo apt-get update && sudo apt-get install -y python3-pip" "blue"
            sudo apt-get install -y python3-pip
            ;;
        *Fedora*)
            print_animated "Suggested command: sudo dnf install -y python3-pip" "blue"
            sudo dnf install -y python3-pip
            ;;
        *CentOS*|*RHEL*)
            print_animated "Suggested command: sudo yum install -y python3-pip" "blue"
            sudo yum install -y python3-pip
            ;;
        *)
            print_animated "Error: Unsupported OS. Please install pip manually." "red"
            exit 1
            ;;
    esac
fi

print_animated "Installing requests and python-dotenv..." "green"
pip install requests python-dotenv

print_animated "Downloading github_setup.py script..." "blue"
curl -O https://raw.githubusercontent.com/reegen66/gprsa/main/github_setup.py

print_animated "Making github_setup.py script executable..." "yellow"
chmod +x github_setup.py

# Ask user if they want to enter GitHub token and email now
print_animated "Do you want to enter your GitHub token and email now? (y/n): " "blue"
read -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    print_animated "Please enter your GitHub token: " "yellow"
    read -r github_token
    print_animated "Please enter your GitHub email: " "yellow"
    read -r github_email
    
    # Create .gprsa file with the provided information
    echo "GITHUB_TOKEN=$github_token" > ~/.gprsa
    echo "GITHUB_EMAIL=$github_email" >> ~/.gprsa
    
    print_animated "GitHub token and email have been saved to ~/.gprsa" "green"
    print_animated "Executing github_setup.py script..." "green"
    ./github_setup.py
else
    # Create empty .gprsa file
    touch ~/.gprsa
    print_animated "An empty ~/.gprsa file has been created." "yellow"
    print_animated "Please add your GITHUB_TOKEN and GITHUB_EMAIL to ~/.gprsa" "yellow"
    print_animated "Once you've added the information, run ./github_setup.py" "blue"
fi

print_animated "Setup completed successfully." "green"
