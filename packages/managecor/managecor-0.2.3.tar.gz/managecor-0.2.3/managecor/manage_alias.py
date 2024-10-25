import os
import sys
import winreg
from pathlib import Path


def create_batch_file(alias_name, command):
    """Crée un fichier batch pour l'alias"""
    scripts_dir = Path.home() / "Scripts"
    scripts_dir.mkdir(exist_ok=True)

    batch_path = scripts_dir / f"{alias_name}.bat"

    with open(batch_path, "w") as f:
        f.write("@echo off\n")
        # Remplace %* par les arguments passés à la commande
        f.write(f"{command} %*")

    return batch_path


def add_to_path(directory):
    """Ajoute un répertoire au PATH système"""
    try:
        # Ouvre la clé de registre PATH
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER, "Environment", 0, winreg.KEY_ALL_ACCESS
        )

        # Récupère la valeur actuelle du PATH
        try:
            path_value, _ = winreg.QueryValueEx(key, "PATH")
        except WindowsError:
            path_value = ""

        # Vérifie si le répertoire est déjà dans le PATH
        if str(directory) not in path_value:
            # Ajoute le nouveau répertoire au PATH
            new_path = f"{path_value};{directory}" if path_value else str(directory)
            winreg.SetValueEx(key, "PATH", 0, winreg.REG_EXPAND_SZ, new_path)

        winreg.CloseKey(key)
        return True
    except WindowsError as e:
        print(f"Erreur lors de la modification du PATH: {e}")
        return False


def create_alias(alias_name, command):
    """Crée un alias en créant un fichier batch et l'ajoute au PATH"""
    try:
        # Crée le fichier batch
        batch_path = create_batch_file(alias_name, command)

        # Ajoute le répertoire au PATH s'il n'y est pas déjà
        scripts_dir = str(Path.home() / "Scripts")
        if add_to_path(scripts_dir):
            print(f"Alias '{alias_name}' créé avec succès pour la commande: {command}")
            print(f"Fichier batch créé: {batch_path}")
            print(
                "Vous devrez peut-être redémarrer votre terminal pour utiliser le nouvel alias."
            )
            return True
        return False
    except Exception as e:
        print(f"Erreur lors de la création de l'alias: {e}")
        return False


def main():
    # Exemple d'utilisation
    aliases = {
        "latexcor": "docker run -it --rm -v %cd%:/data infocornouaille/tools:perso latexcor",
        # Ajoutez d'autres alias ici
    }

    for alias_name, command in aliases.items():
        create_alias(alias_name, command)


if __name__ == "__main__":
    main()
