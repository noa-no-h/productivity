#!/bin/bash

# Function to calculate the end time
calculate_end_time() {
    start_time=$1
    duration=$2
    end_time=$((start_time + duration))
    echo $end_time
}

# Function to calculate the time remaining
calculate_time_remaining() {
    end_time=$1
    current_time=$(date +%s)
    time_remaining=$((end_time - current_time))
    echo $time_remaining
}

# Function to format time as HH:MM:SS
format_time() {
    seconds=$1
    hours=$((seconds / 3600))
    seconds=$((seconds % 3600))
    minutes=$((seconds / 60))
    seconds=$((seconds % 60))
    printf "%02d:%02d:%02d" $hours $minutes $seconds
}

# Function to display a red circle
display_red_circle() {
    echo -n -e "\033[31m⭕\033[0m"
}

# Main function to manage multiple tasks
main() {
    while true; do
        read -p $'\nEnter task name (or press Enter to finish): ' task_name

        if [ -z "$task_name" ]; then
            break
        fi

        read -p "Enter expected duration in minutes: " duration_minutes

        start_time=$(date +%s)
        end_time=$(calculate_end_time $start_time $((duration_minutes * 60)))

        while true; do
            current_time=$(date +%s)
            time_remaining=$(calculate_time_remaining $end_time)


            if [ $time_remaining -le 0 ]; then
                display_red_circle
            fi

            elapsed_time=$(format_time $((current_time - start_time)))
            remaining_time=$(format_time $time_remaining)

            echo -ne "\r\033[1m$task_name | $(date -r $start_time '+%H:%M') | $(date -r $end_time '+%H:%M') | $(format_time $((current_time - start_time))) | $(format_time $time_remaining)\033[0m "


            # Check for user input (Enter key) to proceed to the next task
            read -t 1 -n 1 key
            #echo "Debug: key pressed is '$key'"  # Debug line
            if [[ $key == $'a' ]]; then
                read -r -t 0.1 -n 10000 discard  # Clear input buffer
                break  # Break the inner loop to ask for new task
            fi

            sleep 1  # Update every second
        done
    done
}

main
