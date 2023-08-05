def joker(gram,corpus="presse",debut=1789,fin=1950,after=True,n_joker=20):
    if not isinstance(recherche, str) and not isinstance(recherche, list):
            raise ValueError("La recherche doit être une chaîne de caractères ou une liste")
    assert corpus in ["lemonde","livres","presse"], 'Vous devez choisir le corpus parmi "lemonde","livres" et "presse"'
    gram = urllib.parse.quote_plus(gram.lower()).replace("-"," ").replace(" ","%20")
    df = pd.read_csv(f"https://shiny.ens-paris-saclay.fr/guni/joker?corpus={corpus}&mot={gram}&from={debut}&to={fin}&after={after}&n_joker={n_joker}")
        

