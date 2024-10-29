from typing import Literal, Type, TypeVar, Union, Any, List

T = TypeVar('T', bound=Any)

def literal(
    values: List[T],
    tuple_index: int = None,
    attr_name: str = None
) -> Type[Literal]:
    """
    Crée un type Literal dynamique à partir d'une liste de valeurs,
    de tuples ou d'objets possédant des propriétés spécifiques.

    Args:
        values (list): Liste des valeurs pour créer le Literal.
        tuple_index (int, optional): Index des éléments à utiliser si les valeurs sont des tuples.
        attr_name (str, optional): Nom de la propriété à utiliser si les valeurs sont des objets.

    Returns:
        Type[Literal]: Un type Literal représentant les valeurs spécifiées.
    """
    # Récupération des valeurs à utiliser pour le Literal en fonction du type d'éléments dans `values`
    if tuple_index is not None:
        # Cas des tuples : sélectionne l'élément à l'index `tuple_index` pour chaque tuple
        extracted_values = [val[tuple_index] for val in values if isinstance(val, tuple)]
    elif attr_name is not None:
        # Cas des objets : sélectionne la propriété `attr_name` pour chaque objet
        extracted_values = [getattr(val, attr_name) for val in values if hasattr(val, attr_name)]
    else:
        # Cas des valeurs simples : utilise les valeurs directement
        extracted_values = values

    # Retourne un Literal dynamique basé sur les valeurs extraites
    return Union[tuple(extracted_values)]  # Renvoie Literal[<extracted_values>]
