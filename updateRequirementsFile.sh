pipdeptree --warn silence | grep -E '^\S' > requirements.txt
pip-compile --no-annotate --output-file requirements_temp.txt requirements.txt

rm -rf requirements.txt
mv requirements_temp.txt requirements.txt