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
        sleep 0.005
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

print_animated "Checking system and requirements..." "blue"
print_animated "Detected OS: $OS" "yellow"

missing_deps=()
install_commands=()

# Check for pip
if ! command_exists pip; then
    missing_deps+=("pip")
    case "$OS" in
        *Ubuntu*|*Debian*)
            install_commands+=("sudo apt-get update && sudo apt-get install -y python3-pip && pip install python-dotenv")
            ;;
        *Fedora*)
            install_commands+=("sudo dnf install -y python3-pip && pip install python-dotenv")
            ;;
        *CentOS*|*RHEL*)
            install_commands+=("sudo yum install -y python3-pip && pip install python-dotenv")
            ;;
        *)
            print_animated "Error: Unsupported OS. Please install pip manually." "red"
            exit 1
            ;;
    esac
fi

# Check for Python libraries
if ! pip show requests python-dotenv >/dev/null 2>&1; then
    missing_deps+=("Python libraries (requests, python-dotenv)")
    install_commands+=("pip install requests python-dotenv")
fi

if [ ${#missing_deps[@]} -ne 0 ]; then
    print_animated "The following dependencies are missing:" "yellow"
    for dep in "${missing_deps[@]}"; do
        print_animated "- $dep" "yellow"
    done
    print_animated "The following commands will be used to install them:" "blue"
    for cmd in "${install_commands[@]}"; do
        print_animated "$ $cmd" "blue"
    done
    print_animated "Do you want to proceed with the installation? (y/n): " "green"
    read -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        for cmd in "${install_commands[@]}"; do
            eval $cmd
        done
    else
        print_animated "Installation cancelled. Please install the missing dependencies manually." "red"
        exit 1
    fi
else
    print_animated "All required dependencies are already installed." "green"
fi

print_animated "Downloading github_setup.py script..." "blue"
curl -sS -o github_setup.py https://raw.githubusercontent.com/reegen66/gprsa/main/github_setup.py

print_animated "Making github_setup.py script executable..." "yellow"
chmod +x github_setup.py

# Check if .gprsa already exists
if [ -f .gprsa ]; then
    print_animated ".gprsa file already exists. Do you want to overwrite it? (y/n): " "yellow"
    read -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_animated "Existing .gprsa file will be kept. When ready, run: ./github_setup.py" "blue"
        exit 0
    fi
fi

print_animated "Do you want to enter your GitHub token and email now? (y/n): " "blue"
read -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    print_animated "Please enter your GitHub token: " "yellow"
    read -r github_token
    print_animated "Please enter your GitHub email: " "yellow"
    read -r github_email
    
    # Create .gprsa file with the provided information in the current directory
    echo "GITHUB_TOKEN=$github_token" > .gprsa
    echo "GITHUB_EMAIL=$github_email" >> .gprsa
    
    print_animated "GitHub token and email have been saved to .gprsa in the current directory" "green"
    print_animated "Executing github_setup.py script..." "green"
    ./github_setup.py
else
    # Create .gprsa file with placeholders in the current directory
    echo "GITHUB_TOKEN=" > .gprsa
    echo "GITHUB_EMAIL=" >> .gprsa
    print_animated "A .gprsa file with placeholders has been created in the current directory." "yellow"
    print_animated "Please add your GITHUB_TOKEN and GITHUB_EMAIL to .gprsa" "yellow"
    print_animated "Once you've added the information, run: ./github_setup.py" "blue"
fi

print_animated "Setup completed successfully." "green"
