#!/bin/bash
# ==============================================
# run_app.sh
#
# This script either starts the FastAPI server
# or runs the seed_all script based on the numeric
# argument you provide.
#
# Usage:
#   ./start.sh 1    # Start FastAPI server
#   ./start.sh 2    # Run database seed_all script
#
# Options:
#   1 -> Start server
#   2 -> Run seed_all
# ==============================================

case $1 in
    1)
        echo "Starting FastAPI server..."
        uvicorn app.main:app --reload
        ;;
    2)
        echo "Running seed_all script..."
        python -m app.seed.seed_all
        ;;
    *)
        echo "Invalid option. Use 1->start server, 2->run seed_all"
        ;;
esac
