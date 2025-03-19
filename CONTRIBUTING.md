# Contributing to the Voice-Assisted Desktop Assistant

Welcome to the open-source Voice-Assisted Desktop Assistant project! Contributions are always appreciated, and it's a breeze to get involved. Here's how you can contribute:

## How to Contribute

1. **_Fork the Project:_** Click the "Fork" button at the top-right to create your copy of the project.

2. **_Clone Your Fork:_** Copy the URL from the address bar and run the following command in your terminal.

    ```bash
    git clone <your-fork-url>
    cd Desktop-Assistant
    ```
3. **_Set Up the Project:_** Run the following script to create a virtual environment, install the necessary libraries and pre-commit hooks to set up the project. 

    ```bash
    bash setupProject.sh
    ```

4. **_Create a New Branch:_** Create a new branch from the `main` branch to work on your changes.

    ```bash
    git switch -c <new-branch-name>
    ```

5. **_Make Changes:_** Work on the issue you're assigned to or the feature you want to add. Make sure to test your changes.
   - Any new command added should be implemented via a class defined in the `commands` directory.
   - Any additional generic utility should be added in the `infra.py` file.
   - DO NOT DEFINE ANY GLOBAL VARIABLES IN THE `infra.py`. Define a class variable inside `__init__(self)` method of `Assistant` class if you have to.
     - All the functions implemented in the `infra.py` file should be python equivalent of _static_ methods.

    ```
    # class structure
    - static methods
        - commandName
            - No arguements
            - the `__name__` field of class as return value
        - validate_query
            - Single argument - query
            - Validates query and returns true if query is a match for the action
        - execute_query
            - Two arguments - query and voice-interface instance
            - executes the query and announces the result via the voice interface instance
    ```

6. **_Registering Command:_** Once the command is implemented, register the command in the `command_registery.py` file via the `register_command(command_name, validate_query, execute_query)` method of the `CommandRegistery` class.

7. **_Requirements:_** If you are adding any new libraries or dependencies, make sure to update the `requirements.txt` file. To generate the updated `requirements.txt` file, run the following command:

    ```bash
    pipdeptree --warn silence | grep -E '^[a-zA-Z0-9]' | sed 's/==/~=/g' > requirements.txt
    ```
    - The above command will generate the `requirements.txt` file with the appropriate versions of the libraries used in the project without the nested depedencies and metadata.

8. **_Run the Pre-commit hooks:_** The pre-commit hooks are set up to ensure that the code is formatted correctly and passes the linting checks. They are already set up in the project and configured via the `.pre-commit-config.yaml` file. To run the pre-commit hooks, use the following command:
     ```bash
     pre-commit run --all-files
     ```
   - The hooks automatically resolve any issues occuring in the code. So, in the case hook fails, run them again to ensure that the issues are resolved in the previous run.

7. **_Commit Changes:_** Use clear and simple commit messages. For example:
    - "Added a weather command"
    - "Fixed voice recognition bug"
        ```bash
        git commit -m "<mandatory commit message here>" -m "<optional commit description here>"
        ```

8. **_Push to Your Fork:_** Send your changes back to your forked repository.

    ```bash
    git push origin <branch-name>
    ```

9. **_Create a Pull Request (PR):_** Open a PR to the `main` branch of `vihar-s1/Desktop-Assistant`. Describe your changes briefly and why they're awesome. MAKE SURE TO FOLLOW THE PREDEFINED PULL REQUEST TEMPLATE.

10. **_Workflow Checks and PR Review:_** Note that the PR will have to successfully pass all the workflows setup via GitHub action. A successfully checked PR
    will be then reviewed and then merged. Any changes suggested must be met before PR can be merged.

## Additional Notes

- If you are adding any new features, make sure to update the `README.md` file with the new feature details.
- If you are adding a new pre-commit hook, make sure to use the appropriate latest version of the hook when updating the `.pre-commit-config.yaml` file.

## Guidelines

- Have fun! This is an open-source project, and we're all here to learn and enjoy coding together.
- Keep it simple. Make sure your code is easy for others (and your future self) to understand.
- Make sure to use comments wherever needed and update the `README.md` file if necessary.
- Test your changes. Ensure things work as expected.
- Share your thoughts. If you have ideas or questions, open an issue to discuss them.

That's it! Thanks for being part of this project. Every contribution, big or small, makes a difference.

---
