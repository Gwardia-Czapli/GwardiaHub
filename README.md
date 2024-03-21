# GwardiaHub Project 🌐

## 📄 About the project

We want to create website with Django, that will be useful to as many as three different user groups!

- Our classmates
- [Gwardia Czapli](https://github.com/Gwardia-Czapli/) members
- Genshin Impact players from both of above

### Modules

- For all our classmates:
  - information about lunch menu for given day,
  - calendar with events from Mobidziennik and other events, that our class want to include,
  - information about our homeworks with option to submit solution.
- For [Gwardia Czapli](https://github.com/Gwardia-Czapli/) members:
  - information about next meetings,
  - place to submit feedback about meetings,
  - assignments given on meetings.
- For Genshin Impact players:
  - TBD

## 🛠️ Installation guide for contributors

### Installation

1. Install [git](https://git-scm.com/downloads)
2. In terminal go to folder where you want to have this repository, fe. Documents and enter `git clone https://github.com/Gwardia-Czapli/GwardiaHub` command
3. Install [python-poetry](https://python-poetry.org/) and [pre-commit](https://pre-commit.com/)
4. In terminal go to repository folder (if we follow example from 2. it will be Documents/GwardiaHub) and enter `poetry install` and `pre-commit` commands
5. Open IDE (preferably PyCharm) and with `Open folder` option open repository folder as project in your IDE

### Server running

1. Open venv (if you use PyCharm just open terminal in GwardiaHub project)
2. Enter `python manage.py runserver`
