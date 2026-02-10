# Machine-traction

Repo du projet Explorascience Machine à traction hydraulique

[Requête à l'IA](https://chatgpt.com/share/69791d74-e6e4-8002-950b-1ab17f0a1ddd)

Guide d'utilisation de GitHub:

- Installer GitHub Desktop
- Ajouter la Repo dans GitHub Desktop
- Cliquer sur ouvrir dans VSCODE (Directement de GitHub, beaucoup plus complex à partir de vscode)
- Stage les changements
- Laisser la description du commit
- Commit
- Synchroniser la repo

## Comment utiliser un environnement virtuel (gestion des packages plus facile)

How to check if the virtual envireonnement is selected:
``Get-Command python``
``Get-Command pip``

Step 3 — VS Code must use the venv interpreter

This is separate from terminal activation.

In VS Code:

Press Ctrl + Shift + P

Select Python: Select Interpreter

Choose:

``.venv\Scripts\python.exe``

Once selected:

Look at bottom-right corner

You should see something like:

Python 3.x (.venv)

⚠️ If you skip this step, VS Code may:

Run code with global Python

Use venv in terminal only (or vice versa)
