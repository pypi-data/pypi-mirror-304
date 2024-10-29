import hashlib

REPLACEMENTS_CHARS = {
    'Ã‚Â°': '°',
    'Ã©': 'é',
    'Ãƒâ€°': 'É',
    'ÃƒÂ©': 'é',
    'ÃƒÂ¨': 'è',
    'ÃƒÂ ': 'à',
    'ÃƒÂ¢': 'â',
    'ÃƒÂ®': 'î',
    'ÃƒÂ´': 'ô',
    'ÃƒÂ»': 'û',
    'Ã¨': 'è',
    'Ã ': 'à',
    'Ã¢': 'â',
    'Ã®': 'î',
    'Ã´': 'ô',
    'Ã»': 'û'
}

def string2hash(input_string:str, algorithm:str='sha256') -> str:
    # Crée un nouvel objet de hash avec l'algorithme spécifié
    hash_function = hashlib.new(algorithm)
    # Met à jour l'objet de hash avec la chaîne de caractères (en encodage binaire)
    hash_function.update(input_string.encode('utf-8'))
    # Renvoie la chaîne de caractères hachée sous forme hexadécimale
    return hash_function.hexdigest()

def fix_encoding(text:str) -> str:
    """
    Corrige les problèmes d'encodage courants dans le texte.
    
    Args:
        text (str): Le texte mal encodé
        
    Returns:
        str: Le texte avec l'encodage corrigé
    """
    # Méthode 1: Utilisation de encode/decode
    try:
        # Essaie de décoder depuis latin1 puis encoder en utf-8
        return text.encode('latin1').decode('utf-8')
    except:
        pass
    
    # Méthode 2: Remplacement direct des séquences problématiques
    for bad, good in REPLACEMENTS_CHARS.items():
        text = text.replace(bad, good)
    
    return text
