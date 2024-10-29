from typing import Tuple,overload,Any,List
from memnoch_utils_texte import formate

# Defining a type alias for an exception template type
ExceptionTemplateType = Tuple[int, str]
"""
ExceptionTemplateType est un alias de type pour un tuple qui représente
un modèle d'exception. Ce modèle se compose d'un code d'erreur entier
et d'un message chaîne qui décrit l'erreur.

Arguments :
- Un entier (int) représentant le code d'erreur.
- Une chaîne (str) contenant le message d'erreur.

Type de retour :
- Tuple[int, str] : Un tuple contenant le code d'erreur et le message d'erreur.

Exemples :
1. Un exemple d'un modèle d'exception valide :
   exception = (404, "Non Trouvé")
   Cela représente une erreur avec le code 404 et le message "Non Trouvé".

2. Un autre exemple :
   exception = (500, "Erreur Interne du Serveur")
   Cela représente une erreur avec le code 500 et le message "Erreur Interne du Serveur".
"""



class CustomException(Exception):

    @overload
    def __init__(self, template: ExceptionTemplateType, *args) -> None: ...
    """
    Initialise une instance avec un template d'exception.

    Description :
    Cette surcharge permet d'initialiser l'exception avec un tuple
    contenant un code d'erreur et un message.

    Arguments :
    - template (ExceptionTemplateType) : Tuple contenant un code d'erreur (int)
      et un message d'erreur (str).
    - *args : Arguments supplémentaires optionnels.

    Type de retour :
    - None

    Exemple :
    ```
    exception = (404, "Non Trouvé")
    custom_exception = CustomException(exception)
    ```
    """

    @overload
    def __init__(self, err_num: int, *args) -> None: ...
    """
    Initialise une instance avec un code d'erreur.

    Description :
    Cette surcharge permet d'initialiser l'exception avec un code d'erreur
    entier.

    Arguments :
    - err_num (int) : Le code d'erreur à utiliser.
    - *args : Arguments supplémentaires optionnels.

    Type de retour :
    - None

    Exemple :
    ```
    custom_exception = CustomException(404)
    ```
    """

    @overload
    def __init__(self, description: str, *args) -> None: ...
    """
    Initialise une instance avec une description de l'erreur.

    Description :
    Cette surcharge permet d'initialiser l'exception avec un message décrivant
    l'erreur.

    Arguments :
    - description (str) : Le message d'erreur à utiliser.
    - *args : Arguments supplémentaires optionnels.

    Type de retour :
    - None

    Exemple :
    ```
    custom_exception = CustomException("Erreur de connexion")
    ```
    """

    @overload
    def __init__(self, err_num: int, description: str, *args) -> None: ...
    """
    Initialise une instance avec un code d'erreur et une description.

    Description :
    Cette surcharge permet d'initialiser l'exception avec à la fois un code
    d'erreur et un message décrivant l'erreur.

    Arguments :
    - err_num (int) : Le code d'erreur à utiliser.
    - description (str) : Le message d'erreur à utiliser.
    - *args : Arguments supplémentaires optionnels.

    Type de retour :
    - None

    Exemple :
    ```
    custom_exception = CustomException(500, "Erreur Interne du Serveur")
    ```
    """

    def __init__(self, *args):
        """
        Initialise l'instance de CustomException avec les arguments fournis.

        Description :
        Le constructeur traite différentes combinaisons d'arguments pour
        initialiser correctement les attributs _err_num, _description, et _p.

        Arguments :
        - *args : Arguments variés selon les surcharges définies.

        Type de retour :
        - None
        """
        self._err_num = 0
        self._description = "{0}"
        self._p: List[Any] = []
        # Traite les différentes combinaisons d'arguments selon les surcharges définies
        if len(args) == 1:
            if isinstance(args[0], tuple) :
                if len(args[0])==1 and isinstance(args[0][0],int):
                    self._err_num=args[0][0]
                elif len(args[0])==1 and isinstance(args[0][0],str):
                    self._description=args[0][0]
                elif len(args[0])==2:
                    if isinstance(args[0][0],int):
                        self._err_num=args[0][0]
                    elif isinstance(args[0][0],str):
                        self._description=args[0][0]
                    if isinstance(args[0][1],int):
                        self._err_num=args[0][1]
                    elif isinstance(args[0][1],str):
                        self._description=args[0][1]
            elif isinstance(args[0], int):
                # Cas où err_num est un int
                self.err_num = args[0]
            elif isinstance(args[0], str):
                # Cas où description est une str
                self.description = args[0]
        elif len(args) == 2:
            if isinstance(args[0], tuple) :
                if len(args[0])==1 and isinstance(args[0][0],int):
                    self._err_num=args[0][0]
                elif len(args[0])==1 and isinstance(args[0][0],str):
                    self._description=args[0][0]
                elif len(args[0])==2:
                    if isinstance(args[0][0],int):
                        self._err_num=args[0][0]
                    elif isinstance(args[0][0],str):
                        self._description=args[0][0]
                    if isinstance(args[0][1],int):
                        self._err_num=args[0][1]
                    elif isinstance(args[0][1],str):
                        self._description=args[0][1]
                self._p=list(args[1])
            elif isinstance(args[0], int):
                # Cas où err_num est un int
                self._err_num = args[0]
                self._description=args[1]
            elif isinstance(args[0], str):
                # Cas où description est une str
                self._description = args[0]
                self._p=list(args[1])
        elif len(args) >2:
            if isinstance(args[0], tuple) :
                if len(args[0])==1 and isinstance(args[0][0],int):
                    self._err_num=args[0][0]
                elif len(args[0])==1 and isinstance(args[0][0],str):
                    self._description=args[0][0]
                elif len(args[0])==2:
                    if isinstance(args[0][0],int):
                        self._err_num=args[0][0]
                    elif isinstance(args[0][0],str):
                        self._description=args[0][0]
                    if isinstance(args[0][1],int):
                        self._err_num=args[0][1]
                    elif isinstance(args[0][1],str):
                        self._description=args[0][1]
                self._p=list(args[1:])
            elif isinstance(args[0],int):
                self._err_num=args[0]
                if isinstance(args[1],str):
                    self._description=args[1]
                    self._p=list(args[2:])
                else:
                    self._p=list(args[1:])
            elif isinstance(args[0],str):
                self._description=args[0]
                self._p=list(args[1:])
        message=f"{formate(self._description,*self._p)}"
        super().__init__(message)

    @property
    def message(self) -> str:
        """
        Retourne le message de l'exception.

        Type de retour :
        - str : Le message de l'exception.

        Exemple :
        ```
        custom_exception = CustomException("Une erreur est survenue")
        print(custom_exception.message)  # Affiche le message de l'exception
        ```
        """
        return self
    
    @property
    def err_number(self) -> int:
        """
        Retourne le code d'erreur de l'exception.

        Type de retour :
        - int : Le code d'erreur de l'exception.

        Exemple :
        ```
        custom_exception = CustomException(404, "Non Trouvé")
        print(custom_exception.err_number)  # Affiche 404
        ```
        """
        return self._err_num

__all__=[
    'ExceptionTemplateType',
    'CustomException'
]