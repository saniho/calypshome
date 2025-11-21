# 🎉 Composant Home Assistant Calyps'HOME créé avec succès !

## ✅ Structure créée

```
custom_components/calypshome/
├── __init__.py                    # Initialisation du composant
├── manifest.json                  # Métadonnées du composant
├── const.py                       # Constantes
├── config_flow.py                 # Configuration via interface UI
├── api.py                         # Client API Calyps'HOME
├── cover.py                       # Entités volets roulants
├── strings.json                   # Traductions par défaut
├── README.md                      # Documentation complète
├── INSTALL.md                     # Guide d'installation détaillé
├── configuration.yaml.example     # Exemples de configuration
└── translations/
    ├── en.json                    # Traduction anglaise
    └── fr.json                    # Traduction française
```

## 🚀 Fonctionnalités implémentées

### Contrôle des volets
- ✅ Ouverture
- ✅ Fermeture
- ✅ Arrêt
- ✅ Position précise (0-100%)
- ✅ Inclinaison/tilt (pour BSO)

### Intégration Home Assistant
- ✅ Découverte automatique des volets
- ✅ Configuration via interface UI (pas besoin de YAML)
- ✅ Entités type `cover` (standard Home Assistant)
- ✅ Compatible avec toutes les automatisations
- ✅ Support des groupes de volets
- ✅ Traductions FR/EN

### Fonctionnalités avancées
- ✅ Gestion asynchrone (non-bloquant)
- ✅ Informations sur les devices
- ✅ Logs détaillés pour dépannage
- ✅ Gestion d'erreurs robuste

## 📦 Installation

### Étape 1 : Copier le composant

Copiez le dossier `custom_components/calypshome` dans le dossier de configuration de Home Assistant :

```
/config/custom_components/calypshome/
```

### Étape 2 : Redémarrer Home Assistant

Configuration → Contrôles du serveur → Redémarrer

### Étape 3 : Ajouter l'intégration

1. Configuration → Intégrations
2. "+ Ajouter une intégration"
3. Rechercher "Calyps'HOME"
4. Entrer :
   - IP : `192.168.1.69`
   - Email : `aaa@aaa.aa`
   - Mot de passe : `aaaa`

### Étape 4 : Profiter !

Tous vos volets seront automatiquement découverts et disponibles comme entités `cover.*`

## 🎮 Utilisation

### Dans l'interface Lovelace

Les volets apparaissent avec :
- Bouton Ouvrir ⬆️
- Bouton Fermer ⬇️
- Bouton Stop ⏸️
- Curseur de position 🎚️

### Avec les services

```yaml
# Ouvrir
service: cover.open_cover
target:
  entity_id: cover.cuisine

# Fermer
service: cover.close_cover
target:
  entity_id: cover.baie_vitree

# Position (0-100)
service: cover.set_cover_position
target:
  entity_id: cover.ch_romane
data:
  position: 50

# Arrêter
service: cover.stop_cover
target:
  entity_id: cover.ch_parental
```

### Exemples d'automatisations

```yaml
# Fermer au coucher du soleil
automation:
  - alias: "Volets coucher soleil"
    trigger:
      platform: sun
      event: sunset
    action:
      service: cover.close_cover
      target:
        entity_id: all

# Ouvrir au lever
automation:
  - alias: "Volets lever soleil"
    trigger:
      platform: sun
      event: sunrise
    action:
      service: cover.open_cover
      target:
        entity_id:
          - cover.ch_romane
          - cover.ch_parental
          - cover.ch_marine
```

## 🔧 Entités créées

Les entités seront créées automatiquement avec les noms de vos volets configurés dans la box Calyps'HOME.

Exemples d'entités possibles :
- `cover.volet_salon` - Volet Salon
- `cover.volet_chambre` - Volet Chambre
- `cover.volet_cuisine` - Volet Cuisine

Note : Les noms exacts dépendent de votre configuration Calyps'HOME

## 🐛 Dépannage

### Activer les logs détaillés

Dans `configuration.yaml` :

```yaml
logger:
  default: info
  logs:
    custom_components.calypshome: debug
```

### Vérifier la connexion

Test dans un navigateur :
```
http://192.168.1.69/m?a=getObjects
```

Vous devez voir un JSON avec vos volets.

### Logs Home Assistant

Configuration → Journaux → Rechercher "calypshome"

## 📚 Documentation complète

- **README.md** : Documentation complète du composant
- **INSTALL.md** : Guide d'installation pas à pas
- **configuration.yaml.example** : Exemples d'automatisations et scripts

## 🎯 Intégrations possibles

Une fois installé, vous pouvez :

- ✅ Contrôler via Google Assistant
- ✅ Contrôler via Alexa
- ✅ Créer des automatisations complexes
- ✅ Utiliser dans des scènes
- ✅ Intégrer avec capteurs météo
- ✅ Programmer des horaires
- ✅ Contrôler depuis l'app mobile Home Assistant

## 🚀 Prochaines étapes

1. Copier le dossier dans Home Assistant
2. Redémarrer
3. Configurer l'intégration
4. Tester les volets
5. Créer vos automatisations préférées !

## 💡 Avantages vs script Python

| Script Python | Composant Home Assistant |
|--------------|--------------------------|
| ❌ Manuel | ✅ Automatique |
| ❌ CLI seulement | ✅ Interface graphique |
| ❌ Pas d'automatisation | ✅ Automatisations complètes |
| ❌ Pas d'historique | ✅ Historique complet |
| ❌ Pas de contrôle vocal | ✅ Google/Alexa |
| ❌ Pas d'app mobile | ✅ App mobile |

Bon domotique avec Calyps'HOME ! 🏠✨

