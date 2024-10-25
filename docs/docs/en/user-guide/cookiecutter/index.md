# Project Setup Using Cookiecutter

Cookiecutter creates projects from cookiecutters (project templates), e.g. Python package projects from Python package templates. `FastAgency` provides a [cookiecutter template](https://github.com/airtai/cookiecutter-fastagency) to quickly setup environment and to quickly run the desired example.

### Using Cookiecutter Template

1. Open your terminal.

2. Install `cookiecutter` with the following command:
   ```bash
   pip install cookiecutter
   ```

3. Run the following command to generate a new `FastAgency` project:
   ```bash
   cookiecutter https://github.com/airtai/cookiecutter-fastagency.git
   ```
   This command will prompt you to provide some information about your project, such as the project name, project slug, and other configuration options.

4. After you've answered the prompts, Cookiecutter will create a new directory for your `FastAgency` project based on your responses.

5. Inside the newly generated directory, you will find a README file specific to your project. Follow the instructions in that README file to set up and run your `FastAgency` application.

6. That's it! You now have a new `FastAgency` project set up and ready to go. If you have any further questions or need additional assistance, please refer to the project-specific README file or reach out to the project maintainers.
