[English](README.md) | [Italiano](README.it.md) | [Français](README.fr.md) | [Deutsch](README.de.md) | [Español](README.es.md)

# Lisa - Analyseur de Code pour LLM

Lisa (inspiré par Lisa Simpson) est un outil conçu pour simplifier l'analyse du code source à travers les Grands Modèles de Langage (LLM). Intelligente et analytique comme le personnage dont elle tire son nom, Lisa aide à étudier et interpréter le code avec logique et méthode.

## Description

Lisa est un outil essentiel pour ceux qui souhaitent analyser leur code ou étudier des projets open source à travers les Grands Modèles de Langage. Son objectif principal est de générer un fichier texte unique qui conserve toutes les références et la structure du code original, le rendant facilement interprétable par un LLM.

Cette approche résout l'un des problèmes les plus courants dans l'analyse de code avec les LLM : la fragmentation des fichiers et la perte des références entre les différents composants du projet.

## Configuration

Le projet utilise un fichier de configuration `combine_config.yaml` qui permet de personnaliser les fichiers à inclure ou exclure de l'analyse. La configuration par défaut est :

```yaml
# Motifs d'inclusion (extensions ou répertoires à inclure)
includes:
  - "*.py"  
  # Vous pouvez ajouter d'autres extensions ou répertoires

# Motifs d'exclusion (répertoires ou fichiers à exclure)
excludes:
  - ".git"
  - "__pycache__"
  - "*.egg-info"
  - "venv*"
  - ".vscode"
  - "agents*"
  - "log"
```

### Motifs d'Inclusion/Exclusion
- Les motifs dans `includes` déterminent quels fichiers seront traités (ex : "*.py" inclut tous les fichiers Python)
- Les motifs dans `excludes` spécifient quels fichiers ou répertoires ignorer
- Vous pouvez utiliser le caractère * comme joker
- Les motifs s'appliquent aux noms de fichiers et aux chemins des répertoires
- **Important** : Les règles d'exclusion ont toujours la priorité sur les règles d'inclusion

### Priorité des Règles
Lorsqu'il y a des "conflits" entre les règles d'inclusion et d'exclusion, celles d'exclusion ont toujours la priorité. Voici quelques exemples :

```
Exemple 1 :
/project_root
    /src_code
        /utils
            /logs
                file1.py
                file2.py
            helpers.py
```
Si nous avons ces règles :
- includes: ["*.py"]
- excludes: ["*logs"]

Dans ce cas, `file1.py` et `file2.py` NE seront PAS inclus malgré leur extension .py car ils se trouvent dans un répertoire qui correspond au motif d'exclusion "*logs". Le fichier `helpers.py` sera inclus.

```
Exemple 2 :
/project_root
    /includes_dir
        /excluded_subdir
            important.py
```
Si nous avons ces règles :
- includes: ["includes_dir"]
- excludes: ["*excluded*"]

Dans ce cas, `important.py` NE sera PAS inclus car il se trouve dans un répertoire qui correspond à un motif d'exclusion, même si son répertoire parent correspond à un motif d'inclusion.

## Utilisation

Le script s'exécute depuis la ligne de commande avec :

```bash
cmb [options]
```

> **Note** : Le underscore initial dans le nom du fichier est intentionnel et permet d'utiliser la complétion automatique (TAB) dans le shell.

### Structure et Nom par Défaut
Pour comprendre quel nom de fichier sera utilisé par défaut, considérons cette structure :

```
/home/user/projets
    /mon_projet_test     <- Ceci est le répertoire racine
        /scripts
            _combine_code.py
            combine_config.yaml
        /src
            main.py
        /tests
            test_main.py
```

Dans ce cas, le nom par défaut sera "MON_PROJET_TEST" (le nom du répertoire racine en majuscules).

### Paramètres disponibles :

- `--clean` : Supprime les fichiers texte précédemment générés
- `--output NOM` : Spécifie le préfixe du nom du fichier de sortie
  ```bash
  # Exemple avec le nom par défaut (de la structure ci-dessus)
  python \scripts\_combine_code.py
  # Sortie : MON_PROJET_TEST_20240327_1423.txt

  # Exemple avec un nom personnalisé
  python \scripts\_combine_code.py --output ANALYSE_PROJET
  # Sortie : ANALYSE_PROJET_20240327_1423.txt
  ```

### Sortie

Le script génère un fichier texte avec le format :
`NOM_AAAAMMJJ_HHMM.txt`

où :
- `NOM` est le préfixe spécifié avec --output ou celui par défaut
- `AAAAMMJJ_HHMM` est l'horodatage de génération

## Utilisation avec les Projets GitHub

Pour utiliser Lisa avec un projet GitHub, suivez ces étapes :

1. **Préparation de l'environnement** :
   ```bash
   # Créez et accédez à un répertoire pour vos projets
   mkdir ~/projets
   cd ~/projets
   ```

2. **Clonez le projet à analyser** :
   ```bash
   # Exemple avec un projet hypothétique "moon_project"
   git clone moon_project.git
   ```

3. **Intégrez Lisa dans le projet** :
   ```bash
   # Clonez le dépôt de Lisa
   git clone https://github.com/votrenom/lisa.git

   # Copiez le dossier scripts de Lisa dans moon_project
   cp -r lisa/scripts moon_project/
   cp lisa/scripts/combine_config.yaml moon_project/scripts/
   ```

4. **Exécutez l'analyse** :
   ```bash
   cd moon_project
   python scripts/_combine_code.py
   ```

### Meilleures Pratiques pour l'Analyse
- Avant d'exécuter Lisa, assurez-vous d'être dans le répertoire racine du projet à analyser
- Vérifiez et personnalisez le fichier `combine_config.yaml` selon les besoins spécifiques du projet
- Utilisez l'option `--clean` pour maintenir le répertoire ordonné lors de la génération de versions multiples

## Notes Supplémentaires

- Lisa maintient la structure hiérarchique des fichiers dans le document généré
- Chaque fichier est clairement délimité par des séparateurs indiquant son chemin relatif
- Le code est organisé en maintenant l'ordre de profondeur des répertoires
- Les fichiers générés peuvent être facilement partagés avec les LLM pour analyse

## Contribuer

Si vous souhaitez contribuer au projet, vous pouvez :
- Ouvrir des tickets pour signaler des bugs ou proposer des améliorations
- Soumettre des demandes d'intégration avec de nouvelles fonctionnalités
- Améliorer la documentation
- Partager vos cas d'utilisation et suggestions

## Licence

Licence MIT

Copyright (c) 2024

L'autorisation est accordée, gratuitement, à toute personne obtenant une copie
de ce logiciel et des fichiers de documentation associés (le "Logiciel"), de traiter
le Logiciel sans restriction, y compris, sans s'y limiter, les droits
d'utiliser, copier, modifier, fusionner, publier, distribuer, sous-licencier et/ou vendre
des copies du Logiciel, et de permettre aux personnes auxquelles le Logiciel est
fourni de le faire, sous réserve des conditions suivantes :

L'avis de droit d'auteur ci-dessus et cet avis d'autorisation doivent être inclus dans
toutes les copies ou parties substantielles du Logiciel.

LE LOGICIEL EST FOURNI "TEL QUEL", SANS GARANTIE D'AUCUNE SORTE, EXPRESSE OU
IMPLICITE, Y COMPRIS, MAIS SANS S'Y LIMITER, LES GARANTIES DE QUALITÉ MARCHANDE,
D'ADÉQUATION À UN USAGE PARTICULIER ET D'ABSENCE DE CONTREFAÇON. EN AUCUN CAS LES
AUTEURS OU LES DÉTENTEURS DU DROIT D'AUTEUR NE SERONT RESPONSABLES DE TOUTE RÉCLAMATION,
DOMMAGES OU AUTRE RESPONSABILITÉ, QUE CE SOIT DANS UNE ACTION DE CONTRAT, UN DÉLIT OU
AUTRE, DÉCOULANT DE, HORS DE OU EN RELATION AVEC LE LOGICIEL OU L'UTILISATION OU
D'AUTRES OPÉRATIONS DANS LE LOGICIEL.