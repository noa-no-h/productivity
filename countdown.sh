#!/bin/bash

# Define the target date
target_date="2023-11-18"

# Get the current date in the same format
current_date=$(date +"%Y-%m-%d")

# Convert both dates to Unix timestamps
target_timestamp=$(date -d "$target_date" +%s)
current_timestamp=$(date -d "$current_date" +%s)

# Calculate the number of seconds remaining
seconds_remaining=$((target_timestamp - current_timestamp))

# Calculate the number of days remaining
days_remaining=$((seconds_remaining / 86400))

# Print the result
echo "Number of days until November 18, 2023: $days_remaining days"
