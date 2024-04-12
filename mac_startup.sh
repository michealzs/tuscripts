#!/bin/bash

# Install Homebrew if not installed
if ! command -v brew &>/dev/null; then
    echo "Homebrew is not installed. Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    if [[ $? -ne 0 ]]; then
        echo "Failed to install Homebrew."
        exit 1
    fi
    echo "################################"
    echo "Homebrew installed successfully."
    echo "################################"
else
    echo "##############################"
    echo "Homebrew is already installed."
    echo "################################"
fi

# Update Homebrew
echo "Updating Homebrew..."
brew update
if [[ $? -ne 0 ]]; then
    echo "Failed to update Homebrew."
    exit 1
fi

# Install applications with Homebrew
applications=("tmux" "virtualbox" "vagrant" "firefox" "google-chrome" "sublime-text" "wireshark" "--cask burp-suite" "--cask pycharm")
for app in "${applications[@]}"; do
    echo "Installing $app..."
    brew install $app
    if [[ $? -ne 0 ]]; then
        echo "Failed to install $app."
        exit 1
    fi
    echo "################################"
    echo "$app installed successfully."
    echo "################################"
done
echo "##################################################"
echo "All applications have been installed successfully."
echo "##################################################"
