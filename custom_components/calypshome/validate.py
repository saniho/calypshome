"""
Script de validation du composant Calyps'HOME
Vérifie que tous les fichiers nécessaires sont présents
"""
import os
import json

def check_file_exists(filepath, required=True):
    """Vérifie si un fichier existe"""
    exists = os.path.exists(filepath)
    status = "✅" if exists else ("❌" if required else "⚠️")
    filename = os.path.basename(filepath)
    print(f"{status} {filename:30} {'(requis)' if required else '(optionnel)'}")
    return exists

def validate_component():
    """Valide la structure du composant"""

    base_dir = os.path.dirname(__file__)

    print("\n" + "="*60)
    print("🔍 VALIDATION DU COMPOSANT CALYPS'HOME")
    print("="*60 + "\n")

    all_ok = True

    # Fichiers requis
    print("📋 FICHIERS REQUIS:")
    required_files = [
        "__init__.py",
        "manifest.json",
        "const.py",
        "api.py",
        "cover.py",
        "config_flow.py",
        "strings.json",
    ]

    for filename in required_files:
        filepath = os.path.join(base_dir, filename)
        if not check_file_exists(filepath, required=True):
            all_ok = False

    # Fichiers optionnels
    print("\n📄 DOCUMENTATION:")
    doc_files = [
        "README.md",
        "INSTALL.md",
        "TESTING.md",
        "SUMMARY.md",
        "CHANGELOG.md",
        "00_START_HERE.md",
    ]

    for filename in doc_files:
        filepath = os.path.join(base_dir, filename)
        check_file_exists(filepath, required=False)

    # Traductions
    print("\n🌍 TRADUCTIONS:")
    translation_dir = os.path.join(base_dir, "translations")
    if os.path.exists(translation_dir):
        print("✅ Dossier translations/")
        for lang in ["fr.json", "en.json"]:
            filepath = os.path.join(translation_dir, lang)
            check_file_exists(filepath, required=False)
    else:
        print("❌ Dossier translations/ manquant")
        all_ok = False

    # Validation du manifest.json
    print("\n🔍 VALIDATION DU MANIFEST:")
    manifest_path = os.path.join(base_dir, "manifest.json")
    if os.path.exists(manifest_path):
        try:
            with open(manifest_path, 'r', encoding='utf-8') as f:
                manifest = json.load(f)

            required_keys = ["domain", "name", "version", "documentation", "codeowners", "config_flow"]
            for key in required_keys:
                if key in manifest:
                    print(f"✅ {key:20} : {manifest[key]}")
                else:
                    print(f"❌ {key:20} : MANQUANT")
                    all_ok = False
        except Exception as e:
            print(f"❌ Erreur lors de la lecture du manifest: {e}")
            all_ok = False

    # Résultat final
    print("\n" + "="*60)
    if all_ok:
        print("✅ VALIDATION RÉUSSIE ! Le composant est prêt.")
        print("\n📦 Prochaines étapes:")
        print("   1. Copier ce dossier dans /config/custom_components/")
        print("   2. Redémarrer Home Assistant")
        print("   3. Ajouter l'intégration via Configuration → Intégrations")
        print("\n📖 Consultez 00_START_HERE.md pour les instructions complètes")
    else:
        print("❌ VALIDATION ÉCHOUÉE ! Fichiers manquants.")
        print("   Vérifiez que tous les fichiers requis sont présents.")
    print("="*60 + "\n")

    return all_ok

if __name__ == "__main__":
    validate_component()

