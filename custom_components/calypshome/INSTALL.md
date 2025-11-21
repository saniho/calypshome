# Guide d'installation Calyps'HOME pour Home Assistant

## Prérequis

- Home Assistant installé et fonctionnel
- Accès au répertoire `config` de Home Assistant
- Box Calyps'HOME accessible sur le réseau local
- Identifiants de connexion à la box (email et mot de passe)

## Étape 1 : Installation du composant

### Option A : Installation manuelle (recommandée pour tester)

1. **Accédez au dossier de configuration de Home Assistant**
   ```
   cd /config
   ```

2. **Créez le dossier custom_components si nécessaire**
   ```bash
   mkdir -p custom_components
   ```

3. **Copiez le dossier calypshome**
   - Copiez tout le dossier `custom_components/calypshome` dans `/config/custom_components/`
   - Structure finale : `/config/custom_components/calypshome/`

4. **Vérifiez la structure**
   ```
   /config/custom_components/calypshome/
   ├── __init__.py
   ├── manifest.json
   ├── const.py
   ├── config_flow.py
   ├── api.py
   ├── cover.py
   ├── strings.json
   ├── README.md
   └── translations/
       ├── en.json
       └── fr.json
   ```

### Option B : Installation via SSH/Samba

1. Connectez-vous à votre Home Assistant via SSH ou Samba
2. Naviguez vers `/config/custom_components/`
3. Copiez le dossier `calypshome`

## Étape 2 : Redémarrage

1. Allez dans **Configuration** → **Contrôles du serveur**
2. Cliquez sur **Redémarrer**
3. Attendez que Home Assistant redémarre (1-2 minutes)

## Étape 3 : Configuration

1. **Allez dans Configuration → Intégrations**
   - URL directe : http://homeassistant.local:8123/config/integrations

2. **Cliquez sur "+ Ajouter une intégration"** (en bas à droite)

3. **Recherchez "Calyps'HOME"** dans la barre de recherche

4. **Entrez les informations de connexion :**
   - **Adresse IP ou nom d'hôte** : L'adresse IP de votre box (ex: `192.168.1.69`)
   - **Email** : Votre email de connexion (ex: `aaa@aaa.aa`)
   - **Mot de passe** : Votre mot de passe

5. **Cliquez sur Soumettre**

## Étape 4 : Vérification

1. **Vérifiez que l'intégration est active**
   - Elle doit apparaître dans la liste des intégrations
   - Un nombre d'entités doit être affiché (1 device, X entities)

2. **Allez dans Configuration → Entités**
   - Recherchez `cover.`
   - Vous devez voir tous vos volets : `cover.ch_romane`, `cover.cuisine`, etc.

3. **Testez un volet**
   - Cliquez sur une entité
   - Utilisez les boutons Ouvrir/Fermer/Stop
   - Essayez de régler la position avec le curseur

## Étape 5 : Ajout au Dashboard

1. **Allez dans votre dashboard principal**
2. **Cliquez sur "Modifier le tableau de bord"** (en haut à droite)
3. **Ajoutez une carte "Entités"**
4. **Sélectionnez vos volets**
   - Cochez tous les volets que vous voulez afficher
   - Les noms affichés correspondent à ceux de votre box Calyps'HOME
5. **Enregistrez**

💡 **Astuce** : Pour connaître les noms exacts de vos entités, allez dans Configuration → Entités et filtrez par "cover"

### Exemple de carte avancée (optionnel)

Éditez votre dashboard en mode YAML et ajoutez :

```yaml
type: entities
title: Volets Roulants
entities:
  - entity: cover.ch_romane
    name: Chambre Romane
  - entity: cover.ch_parental
    name: Chambre Parentale
  - entity: cover.fenetre_salon
    name: Fenêtre Salon
  - entity: cover.cuisine
    name: Cuisine
  - entity: cover.baie_vitree
    name: Baie Vitrée
  - entity: cover.ch_marine
    name: Chambre Marine
show_header_toggle: true
```

## Dépannage

### L'intégration n'apparaît pas dans la liste

1. **Vérifiez que le dossier est bien placé**
   ```
   /config/custom_components/calypshome/
   ```

2. **Vérifiez les logs**
   - Configuration → Journaux
   - Recherchez "calypshome"

3. **Redémarrez Home Assistant**
   - Configuration → Contrôles du serveur → Redémarrer

### Erreur "Cannot connect"

1. **Vérifiez l'adresse IP**
   - Ouvrez un navigateur : `http://[VOTRE_IP]/m?a=getObjects`
   - Vous devez voir un JSON avec vos volets

2. **Vérifiez les identifiants**
   - Testez avec le script Python original `testCalypso.py`

3. **Vérifiez le réseau**
   - La box et Home Assistant doivent être sur le même réseau

### Les volets ne répondent pas

1. **Vérifiez les logs**
   - Activez les logs détaillés (voir README.md)

2. **Testez avec le script original**
   - Si ça fonctionne avec testCalypso.py mais pas avec Home Assistant, ouvrez une issue

### Les volets ne se mettent pas à jour

1. L'intégration rafraîchit l'état toutes les 30 secondes par défaut
2. Vous pouvez forcer une mise à jour en cliquant sur "Actualiser" sur l'entité

## Logs détaillés

Pour activer les logs détaillés, ajoutez dans `configuration.yaml` :

```yaml
logger:
  default: info
  logs:
    custom_components.calypshome: debug
```

Puis redémarrez Home Assistant.

## Support

- GitHub Issues : [votre repo]
- Documentation complète : README.md
- Exemples d'automatisations : configuration.yaml.example

## Prochaines étapes

Une fois l'intégration installée et testée :

1. Créez des automatisations (voir configuration.yaml.example)
2. Intégrez avec Google Assistant / Alexa si configuré
3. Créez des scènes et scripts personnalisés
4. Ajoutez des conditions basées sur la météo, l'heure, etc.

Bon domotique ! 🏠🎉
# Guide d'installation Calyps'HOME pour Home Assistant

## Prérequis

- Home Assistant installé et fonctionnel
- Accès au répertoire `config` de Home Assistant
- Box Calyps'HOME accessible sur le réseau local
- Identifiants de connexion à la box (email et mot de passe)

## Étape 1 : Installation du composant

### Option A : Installation manuelle (recommandée pour tester)

1. **Accédez au dossier de configuration de Home Assistant**
   ```
   cd /config
   ```

2. **Créez le dossier custom_components si nécessaire**
   ```bash
   mkdir -p custom_components
   ```

3. **Copiez le dossier calypshome**
   - Copiez tout le dossier `custom_components/calypshome` dans `/config/custom_components/`
   - Structure finale : `/config/custom_components/calypshome/`

4. **Vérifiez la structure**
   ```
   /config/custom_components/calypshome/
   ├── __init__.py
   ├── manifest.json
   ├── const.py
   ├── config_flow.py
   ├── api.py
   ├── cover.py
   ├── strings.json
   ├── README.md
   └── translations/
       ├── en.json
       └── fr.json
   ```

### Option B : Installation via SSH/Samba

1. Connectez-vous à votre Home Assistant via SSH ou Samba
2. Naviguez vers `/config/custom_components/`
3. Copiez le dossier `calypshome`

## Étape 2 : Redémarrage

1. Allez dans **Configuration** → **Contrôles du serveur**
2. Cliquez sur **Redémarrer**
3. Attendez que Home Assistant redémarre (1-2 minutes)

## Étape 3 : Configuration

1. **Allez dans Configuration → Intégrations**
   - URL directe : http://homeassistant.local:8123/config/integrations

2. **Cliquez sur "+ Ajouter une intégration"** (en bas à droite)

3. **Recherchez "Calyps'HOME"** dans la barre de recherche

4. **Entrez les informations de connexion :**
   - **Adresse IP ou nom d'hôte** : L'adresse IP de votre box (ex: `192.168.1.69`)
   - **Email** : Votre email de connexion (ex: `aaa@aaa.aa`)
   - **Mot de passe** : Votre mot de passe

5. **Cliquez sur Soumettre**

## Étape 4 : Vérification

1. **Vérifiez que l'intégration est active**
   - Elle doit apparaître dans la liste des intégrations
   - Un nombre d'entités doit être affiché (1 device, X entities)

2. **Allez dans Configuration → Entités**
   - Recherchez `cover.`
   - Vous devez voir tous vos volets : `cover.ch_romane`, `cover.cuisine`, etc.

3. **Testez un volet**
   - Cliquez sur une entité
   - Utilisez les boutons Ouvrir/Fermer/Stop
   - Essayez de régler la position avec le curseur

## Étape 5 : Ajout au Dashboard

1. **Allez dans votre dashboard principal**
2. **Cliquez sur "Modifier le tableau de bord"** (en haut à droite)
3. **Ajoutez une carte "Entités"**
4. **Sélectionnez vos volets**
   - Cochez tous les volets que vous voulez afficher
5. **Enregistrez**

### Exemple de carte avancée (optionnel)

Éditez votre dashboard en mode YAML et ajoutez (remplacez par vos noms réels) :

```yaml
type: entities
title: Volets Roulants
entities:
  - entity: cover.votre_volet_1  # Remplacez par vos noms réels
    name: Volet 1
  - entity: cover.votre_volet_2
    name: Volet 2
  - entity: cover.votre_volet_3
    name: Volet 3
  # Ajoutez vos autres volets ici
show_header_toggle: true
```

## Dépannage

### L'intégration n'apparaît pas dans la liste

1. **Vérifiez que le dossier est bien placé**
   ```
   /config/custom_components/calypshome/
   ```

2. **Vérifiez les logs**
   - Configuration → Journaux
   - Recherchez "calypshome"

3. **Redémarrez Home Assistant**
   - Configuration → Contrôles du serveur → Redémarrer

### Erreur "Cannot connect"

1. **Vérifiez l'adresse IP**
   - Ouvrez un navigateur : `http://[VOTRE_IP]/m?a=getObjects`
   - Vous devez voir un JSON avec vos volets

2. **Vérifiez les identifiants**
   - Testez avec le script Python original `testCalypso.py`

3. **Vérifiez le réseau**
   - La box et Home Assistant doivent être sur le même réseau

### Les volets ne répondent pas

1. **Vérifiez les logs**
   - Activez les logs détaillés (voir README.md)

2. **Testez avec le script original**
   - Si ça fonctionne avec testCalypso.py mais pas avec Home Assistant, ouvrez une issue

### Les volets ne se mettent pas à jour

1. L'intégration rafraîchit l'état toutes les 30 secondes par défaut
2. Vous pouvez forcer une mise à jour en cliquant sur "Actualiser" sur l'entité

## Logs détaillés

Pour activer les logs détaillés, ajoutez dans `configuration.yaml` :

```yaml
logger:
  default: info
  logs:
    custom_components.calypshome: debug
```

Puis redémarrez Home Assistant.

## Support

- GitHub Issues : [votre repo]
- Documentation complète : README.md
- Exemples d'automatisations : configuration.yaml.example

## Prochaines étapes

Une fois l'intégration installée et testée :

1. Créez des automatisations (voir configuration.yaml.example)
2. Intégrez avec Google Assistant / Alexa si configuré
3. Créez des scènes et scripts personnalisés
4. Ajoutez des conditions basées sur la météo, l'heure, etc.

Bon domotique ! 🏠🎉

