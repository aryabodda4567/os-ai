#!/bin/bash
echo "Configuring..."

CURRENT_PATH=$(pwd)
TARGET="$HOME/.local/bin"

echo "Target path: $TARGET"

# Ensure the local bin directory exists
mkdir -p "$TARGET"

# Create venv (assuming createvenv.sh is valid and in the same directory)
chmod +x createvenv.sh
sudo ./createvenv.sh

# Get venv Python path
VENV_PYTHON="$CURRENT_PATH/.venv/bin/python3.12"

# Create the launcher script
cat <<EOF > myai
#!/bin/bash
input="\$1"
echo $input
$VENV_PYTHON  $CURRENT_PATH/main.py  "$input"
EOF

# Make it executable
chmod +x myai

# Move to user's local bin
cp myai "$TARGET"

# Ensure the bin path is in user's PATH
if [[ ":$PATH:" != *":$TARGET:"* ]]; then
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.bashrc"
    source "$HOME/.bashrc"
fi

echo "Done! Run using: myai 'your input'"
