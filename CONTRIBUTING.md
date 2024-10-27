# Contributing to the Voice-Assisted Desktop Assistant

Welcome to the open-source Voice-Assisted Desktop Assistant project! Contributions are always appreciated, and it's a breeze to get involved. Here's how you can contribute:

## How to Contribute

1. **Fork the Project:** Click the "Fork" button at the top-right to create your copy of the project.

2. **Clone Your Fork:** Copy the URL from the address bar and run the following command in your terminal.

    ```bash
    git clone <your-fork-url>
    cd Desktop-Assistant
    ```
3. **Set Up the Project:** Run the following script to create a virtual environment, install the necessary libraries and pre-commit hooks, and set up the project. 

    ```bash
    bash setupProject.sh
    ```

4. **Create a New Branch:** Create a new branch to work on your changes.

    ```bash
    git checkout -b <new-branch-name>
    ``

5. **Make Changes:** Work on what interests you - add new features, fix bugs, or improve documentation on a **_separate branch_**. It's your playground!

6. **Commit Changes:** Use clear and simple commit messages. For example:

    - "Added a weather command"
    - "Fixed voice recognition bug"

        ```bash
        git commit -m "<mandatory commit message here>" -m "<optional commit description here>"
        ```

7. **Push to Your Fork:** Send your changes back to your forked repository.

    ```bash
    git push origin <branch-name>
    ```

8. **Create a Pull Request (PR):** Open a PR to the `main` branch of `vihar-s1/Desktop-Assistant`. Describe your changes briefly and why they're awesome. MAKE SURE TO USE THE PREDEFINED PULL REQUEST TEMPLATE.

9. Note that the PR will have to successfully pass all the workflows setup via GitHub action. A successfully checked PR
   will be then reviewed and then merged. Any changes suggested must be met before PR can be merged.

## Guidelines

- Have fun! This is an open-source project, and we're all here to learn and enjoy coding together.
- Keep it simple. Make sure your code is easy for others (and your future self) to understand.
- Make sure to use comments wherever needed and update the `README.md` file if necessary.
- Test your changes. Ensure things work as expected.
- Share your thoughts. If you have ideas or questions, open an issue to discuss them.

That's it! Thanks for being part of this project. Every contribution, big or small, makes a difference.

---
