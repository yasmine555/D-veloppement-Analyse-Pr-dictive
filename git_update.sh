#!/bin/bash

# Exemple d’usage : ./git_update.sh "Ajout API Flask" v1.5

commit_message="$1"
tag_name="$2"

# Étape 1 : ajouter les fichiers
git add .

# Étape 2 : commit avec message
git commit -m "$commit_message"

# Étape 3 : push vers GitHub
git push origin main

# Étape 4 : création du tag si fourni
if [ ! -z "$tag_name" ]; then
    git tag "$tag_name"
    git push origin "$tag_name"
    echo "✅ Tag '$tag_name' ajouté et envoyé sur GitHub."
else
    echo "✅ Modifications poussées sans tag."
fi
