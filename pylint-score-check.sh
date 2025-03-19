# Get the list of changed files and calculate the total pylint score for them

# # Setup the project and activate the virtual environment
# bash setupProject.sh
# source .venv/bin/activate
# echo "Active Virtual Environment: ${VIRTUAL_ENV}"

# # get the list of installed python modules
# pip freeze

# Get the list of changed files
changes=""

# Make sure to include only the files that exist
changed_files=""
for file in $changes; do
    if [ -f "$file" ]; then
        changed_files="$changed_files $file"
    fi
done
echo "Changed existing files: $changed_files"

# Check if there are any changed Python files
if [ -z "$changed_files" ]; then
    echo "No Python files changed."
    exit 0
fi

# Run pylint on the changed files and capture the score
{ # try
    pylint_score=$(pylint $changed_files | grep 'Your code has been rated at' | awk '{print $7}' | cut -d '/' -f 1)
} || { # catch
    echo "Pylint failed to run with exit code: $?"
}
# Check if the score is below 9
if (( $(echo "$pylint_score < 9" | bc -l) )); then
    echo "Pylint score is below 9: $pylint_score"
    exit 1
else
    echo "Pylint score is acceptable: $pylint_score"
fi