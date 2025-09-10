#!/bin/bash

# ==============================================
# run_requests.sh
#
# This script runs API request Python scripts
# based on the numeric argument you provide.
#
# Usage:
#   ./api_requests/run_requests.sh 1    # Runs search_request.py
#   ./api_requests/run_requests.sh 2    # Runs upload_request.py
#
# Options:
#   1 -> Search request
#   2 -> Upload request
# ==============================================

# $1 is the first argument passed to the script
case $1 in
    1)
        echo "Running search_request..."
        python api_requests/search_request.py
        ;;
    2)
        echo "Running upload_request..."
        python api_requests/upload_request.py
        ;;
    *)
        echo "Invalid option. Use 1->search, 2->upload"
        ;;
esac