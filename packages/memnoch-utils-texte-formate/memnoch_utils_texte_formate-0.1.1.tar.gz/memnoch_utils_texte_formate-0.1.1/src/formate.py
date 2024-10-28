def formate(chaine: str, *args) -> str:
    """
    Formate une chaîne en remplaçant les indices par les arguments fournis.

    Cette fonction crée un dictionnaire de remplacements où les indices 
    (sous forme de chaînes) sont les clés, et les valeurs correspondantes 
    sont les arguments fournis à la fonction. Elle utilise ensuite 
    `format_map` pour remplacer les indices dans la chaîne donnée.

    Args:
        chaine (str): La chaîne à formater, contenant des indices pour les 
                      remplacements (par exemple, '{0}', '{1}', etc.).
        *args: Une liste d'arguments à substituer dans la chaîne.

    Returns:
        str: La chaîne formatée avec les valeurs substituées.

    Exemple:
        >>> result = formate("Bonjour, {0}! Vous avez {1} nouveaux messages.", "Alice", 5)
        >>> print(result)
        "Bonjour, Alice! Vous avez 5 nouveaux messages."
    """
    replacements = {str(i): arg for i, arg in enumerate(args)}
    return chaine.format_map(replacements)
__all__=[
    'formate'
]