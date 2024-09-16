#!/bin/bash

#Define the google drive file IDs
FILE_ID_1="1-J1uOGCme0NsP7iaylYJHuiomTH76lup"
FILE_ID_2="16G4vzsoJqybIk9I2Mk4Ssp0BX9_3EApq"

# Define the destination filenames
DEST_1="macroscopicModel.bin"
DEST_2="microscopicModel.bin"

# Download files using curl
echo "Downloading model 1..."
curl -L -o $DEST_1 "https://drive.google.com/uc?export=download&id=$FILE_ID_1"

echo "Downloading model 2..."
curl -L -o $DEST_2 "https://drive.google.com/uc?export=download&id=$FILE_ID_2"

echo "Download complete."
