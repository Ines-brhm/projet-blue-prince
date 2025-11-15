
def payer_room_si_possible(room, inventaire,manoir):
    """
    Tente de payer le coût en gemmes de `room` avec `inventaire`.
    - Si la salle ne coûte rien (cout_gemmes <= 0) -> retourne `room`.
    - Si elle coûte > 0 :
        * essaie d'appeler une méthode de paiement si elle existe
          (payer_gemmes ou payer_gemme),
        * sinon, vérifie inventaire.gems et décrémente.
      Retourne `room` si le paiement est possible/effecuté, sinon `None`.
    """
    cout = getattr(room, "cout_gemmes", 0) or 0

    # Pas de coût -> OK
    if cout <= 0:
        return True

    # Essayer une méthode officielle si elle existe
    if hasattr(inventaire, "payer_gemmes"):
        ok = inventaire.payer_gemmes(cout)
        if ok:
            manoir.show_message( "vous avez payer des gemmes",1.0) 
            return True
        else:
            # Pas assez de gemmes
            manoir.show_message( "vous n'avez pas assez de gemmes",1.0) 
            return False
