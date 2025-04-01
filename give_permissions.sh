#!/bin/bash

echo "Giving permissions to all python scripts of this project..."
find . -type f -name "*.sh" -exec chmod +x {} \;
echo "Permissions given permenantly"