# Get the list of changed files and calculate the total pylint score for them

# Get the list of changed files
{ # try
changes=$(git diff --name-only HEAD main | grep '\.py$')
} || { # catch
if [ $? -eq 1 ]; then
    echo "No python file changes found in the pull request."
    exit 0
fi
}

echo -e "changes:\n$changes\n"
# Make sure to include only the files that exist
changed_files=""
for file in $changes; do
if [ -f "$file" ]; then
    changed_files="$changed_files $file"
fi
done
echo -e "Changed existing files:\n$changed_files\n"

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