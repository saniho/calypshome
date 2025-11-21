# Calyps'HOME - Intégration Home Assistant

Intégration personnalisée pour contrôler vos volets roulants Calyps'HOME via Home Assistant.

## ⚠️ Avertissement / Disclaimer

**Ce composant personnalisé est indépendant et n'est en aucun cas affilié à la marque Calyps'HOME.**

- ✋ **Projet non officiel** : Ce composant a été développé de manière indépendante et n'est pas supporté par le fabricant Calyps'HOME
- 🚫 **Aucune garantie** : Ce logiciel est fourni "tel quel", sans aucune garantie de fonctionnement
- ⚠️ **Utilisation à vos risques** : L'auteur ne peut être tenu responsable de tout dysfonctionnement, dommage matériel ou perte de données résultant de l'utilisation de ce composant
- 🔧 **Support limité** : Le support technique est fourni sur la base du volontariat et sans engagement
- 📝 **Licence MIT** : Ce projet est fourni sous licence MIT - voir le fichier LICENSE pour plus de détails

**En utilisant ce composant, vous acceptez ces conditions.**

## Fonctionnalités

- ✅ Découverte automatique de tous les volets roulants
- ✅ Ouverture / Fermeture / Arrêt
- ✅ Positionnement précis (0-100%)
- ✅ Support de l'inclinaison (pour les BSO)
- ✅ Configuration via l'interface utilisateur
- ✅ Compatible avec toutes les automatisations Home Assistant

## Installation

### Méthode 1 : Installation manuelle

1. Copiez le dossier `custom_components/calypshome` dans votre dossier `config/custom_components/` de Home Assistant
2. Redémarrez Home Assistant
3. Allez dans **Configuration** → **Intégrations**
4. Cliquez sur **+ Ajouter une intégration**
5. Recherchez "Calyps'HOME"
6. Entrez les informations de connexion :
   - **Adresse IP** : L'adresse IP de votre box (ex: 192.168.1.69)
   - **Email** : Votre email de connexion
   - **Mot de passe** : Votre mot de passe

> **💡 Identifiants par défaut :**
> - Email : `aaa@aaa.aa`
> - Mot de passe : `aaaa`
> 
> ⚠️ **Important** : Il est fortement recommandé de modifier ces identifiants par défaut lors de la première connexion à votre box Calyps'HOME pour des raisons de sécurité.

### Méthode 2 : HACS (à venir)

Cette intégration pourra être installée via HACS une fois publiée.

## Configuration

Après l'installation, tous vos volets roulants seront automatiquement découverts et ajoutés comme entités `cover.*` dans Home Assistant.

## Utilisation

### Dans l'interface Lovelace

Les volets apparaîtront automatiquement dans votre interface avec les contrôles standard :
- Bouton Ouvrir
- Bouton Fermer
- Bouton Stop
- Curseur de position

### Dans les automatisations

```yaml
# Exemple : Fermer tous les volets au coucher du soleil
automation:
  - alias: "Fermer volets au coucher du soleil"
    trigger:
      platform: sun
      event: sunset
    action:
      - service: cover.close_cover
        target:
          entity_id: all
```

### Dans les scripts

```yaml
# Exemple : Ouvrir la cuisine à 50%
script:
  cuisine_mi_ouvert:
    sequence:
      - service: cover.set_cover_position
        target:
          entity_id: cover.cuisine
        data:
          position: 50
```

### Via les services

```yaml
# Ouvrir un volet (remplacez par le nom de votre volet)
service: cover.open_cover
target:
  entity_id: cover.votre_volet

# Fermer un volet
service: cover.close_cover
target:
  entity_id: cover.votre_volet

# Position spécifique (0 = fermé, 100 = ouvert)
service: cover.set_cover_position
target:
  entity_id: cover.votre_volet
data:
  position: 75

# Arrêter un volet en mouvement
service: cover.stop_cover
target:
  entity_id: cover.votre_volet

# Inclinaison (si BSO)
service: cover.set_cover_tilt_position
target:
  entity_id: cover.votre_volet
data:
  tilt_position: 45
```

## Entités créées

Pour chaque volet, une entité `cover.*` sera créée avec :
- **État** : open, closed, opening, closing
- **Position** : 0-100%
- **Inclinaison** : 0-100% (si supporté)

Exemple d'entités créées :
- `cover.ch_romane`
- `cover.ch_parental`
- `cover.fenetre_salon`
- `cover.cuisine`
- `cover.baie_vitree`
- `cover.ch_marine`

## Dépannage

### Les volets ne sont pas découverts

1. Vérifiez que vous pouvez accéder à la box via http://[IP]/m?a=getObjects
2. Vérifiez vos identifiants de connexion
3. Consultez les logs : **Configuration** → **Journaux** → Recherchez "calypshome"

### Les commandes ne fonctionnent pas

1. Vérifiez que les commandes fonctionnent avec le script testCalypso.py original
2. Vérifiez les logs Home Assistant
3. Assurez-vous que la box est bien sur le même réseau

### Logs

Pour activer les logs détaillés, ajoutez dans `configuration.yaml` :

```yaml
logger:
  default: info
  logs:
    custom_components.calypshome: debug
```

## Structure du projet

```
custom_components/calypshome/
├── __init__.py           # Initialisation du composant
├── manifest.json         # Métadonnées du composant
├── const.py             # Constantes
├── config_flow.py       # Configuration via UI
├── api.py               # Client API Calyps'HOME
├── cover.py             # Entités volets roulants
└── translations/        # Traductions
    ├── en.json
    └── fr.json
```

## Développement

Basé sur le script Python original qui communique avec l'API Calyps'HOME via HTTP avec authentification par cookies.

## À propos de ce projet

Ce composant est un projet **communautaire non officiel** créé pour permettre l'intégration des volets roulants Calyps'HOME dans Home Assistant. Il utilise l'API locale de la box Calyps'HOME pour envoyer des commandes via HTTP.

**Relation avec la marque** :
- ❌ Non développé par Calyps'HOME
- ❌ Non validé par Calyps'HOME
- ❌ Non supporté officiellement par Calyps'HOME
- ✅ Développé par la communauté pour la communauté

**Responsabilités** :
- L'auteur de ce composant n'est pas responsable des dysfonctionnements de votre installation
- Calyps'HOME n'est pas responsable des problèmes liés à l'utilisation de ce composant
- Toute modification de la configuration de votre box se fait sous votre responsabilité

## Licence

MIT License - Ce logiciel est fourni sans aucune garantie.

## Support

Pour toute question ou problème :
- 📖 Consultez d'abord la documentation
- 🔍 Vérifiez les issues existantes sur GitHub
- 💬 Ouvrez une nouvelle issue si nécessaire

**Note** : Pour les problèmes matériels ou liés à la box Calyps'HOME elle-même, contactez directement le support officiel de Calyps'HOME.

