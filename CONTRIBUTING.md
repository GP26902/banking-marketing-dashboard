# Contributing Guide

Thanks for contributing to the Banking Marketing Campaign Analytics Dashboard. Follow these steps for every task so the `main` branch always stays working.

## Workflow

1. **Never commit directly to `main`.** All work goes through a branch and a pull request.
2. **Start from an up-to-date `main`:**
   ```bash
   git checkout main
   git pull origin main
   ```
3. **Create a branch** named `yourname/task-name`, for example `gp/campaign-eda`:
   ```bash
   git checkout -b yourname/task-name
   ```
4. **Make your changes**, then test locally:
   ```bash
   pip install -r requirements.txt
   streamlit run app.py
   ```
   Open `http://localhost:8501` and confirm the page loads without errors and the numbers and charts look right.
5. **Commit and push:**
   ```bash
   git add .
   git commit -m "Short description of the change"
   git push -u origin yourname/task-name
   ```
6. **Open a pull request** into `main`, fill in the template, and **add the project manager as a reviewer**.

## What to include with every task

- The code changes.
- A small, targeted update to `README.md` if features, structure or findings changed.
- A task summary in `docs/task-summaries/` named `task-<short-name>.md` (see `task-campaign-eda.md` for the format).
- Screenshots, if the UI changed, in `docs/screenshots/`.

## Conventions

- Keep code commented and follow standard Python style (PEP 8).
- Read the dataset from `data/train.csv` (semicolon-separated).
- Do not commit secrets, virtual environments or large generated files.
- Keep each pull request focused on a single task.
