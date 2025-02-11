import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ussd_simulator.settings')
django.setup()

from ussd.models import USSDMenu # type: ignore

def create_menus():
    # Menu Principal (#144)
    main_menu = USSDMenu.objects.create(title="Menu Principal", code="#144")

    # Sous-menus du Menu Principal
    solde_de_mes_comptes = USSDMenu.objects.create(title=" SOLDE DE MES COMPTE", parent=main_menu)
    transfert_argent = USSDMenu.objects.create(title="TRANSFERT D'ARGENT", parent=main_menu)
    paiement_facture = USSDMenu.objects.create(title="PAIEMENT DE FACTURE", parent=main_menu)
    achat_credit_pass = USSDMenu.objects.create(title="ACHAT CREDIT ET PASS", parent=main_menu)
    paiement_bien_services = USSDMenu.objects.create(title="PAIEMENT BIEN ET SERVICES", parent=main_menu)
    don_cotisation = USSDMenu.objects.create(title="DON ET COTISATION", parent=main_menu)
    option = USSDMenu.objects.create(title="OPTION", parent=main_menu)
    banque_assurance = USSDMenu.objects.create(title="Banque Assurance", parent=main_menu)
    jeux = USSDMenu.objects.create(title="JEUX", parent=main_menu)

    # Sous-sous-menus de CONSULTATION DE SOLDE
    Solde_Compte_OrangeMoney = USSDMenu.objects.create(title="Solde Compte OrangeMoney", parent=solde_de_mes_comptes)
    USSDMenu.objects.create(
    title="Solde Compte OrangeMoney",
    parent=solde_de_mes_comptes,
    requires_confirmation=True,  # Nécessite une confirmation
    confirmation_message="Entrez votre code secret de 4 chiffres pour confirmer ou 9 pour retourner."
    )

    mon_salaire= USSDMenu.objects.create(title="mon salaire", parent=solde_de_mes_comptes)
    USSDMenu.objects.create(
        title="mon salaire",
        parent=solde_de_mes_comptes
    )
    USSDMenu.objects.create(
        title="Avoir le solde de mon condamne",
        parent=mon_salaire,
        requires_confirmation=True,
        output="Je demande a recevoir le solde de mon condamne . Je confime en tapant mon code secret ou 2 pour annuler entrer 9 pour retourner a l'accueil et 0 pour le menu precedent"  
    )
 
    utiliser_mon_condamné= USSDMenu.objects.create(title="utiliser mon condamné", parent=mon_salaire)
    USSDMenu.objects.create(
        title="utiliser_mon_condamné=",
        parent=mon_salaire,
    )
    USSDMenu.objects.create(
        title="Transferer de mon condamne vers mon compte OrangeMoney",
        requires_confirmation=True,
        parent=mon_salaire,
        output="Transfert effectué avec succès."
    )
    USSDMenu.objects.create(
        title="Transferer de mon condamné vers mon compte principal Orange Money vers mon condamné",
        parent= utiliser_mon_condamné,
        requires_confirmation=True,
        output="Transfert effectué avec succès."
    )
    USSDMenu.objects.create(
        title="avoir mes 5 dernières opérations Mon condamné",
        parent=mon_salaire,
        requires_confirmation=True,
        output="Voici vos 5 dernières opérations : ..."
    )
    transfert_national= USSDMenu.objects.create(title="transfert national  ", parent=transfert_argent)
    USSDMenu.objects.create(
        title="transfert_national=",
        parent=transfert_argent,
    )
    # Sous-sous-menus de TRANSFERT D'ARGENT
    USSDMenu.objects.create(title="transfert national  ", parent=transfert_national)
    USSDMenu.objects.create(
        title="Transfert vers un numéro OM",
        parent=transfert_national,
        requires_confirmation=True,
        output="je saisis le numero de telephone du beneficiairebqui doit recevoir le transfert d'argent ou je tape 1 pour acceder a ma liste de numeros favoris."
    )
    USSDMenu.objects.create(
        title="transfert avec code",
        parent=transfert_national,
        requires_confirmation=True,
        output="je saisis le numero de telephone du beneficiairebqui doit recevoir le transfert d'argent ou je tape 1 pour acceder a ma liste de numeros favoris."
    )
    activer_un_forfait= USSDMenu.objects.create(title="transfert national  ", parent=transfert_national)
    USSDMenu.objects.create(
        title="activer un forfait",
        parent=transfert_national,
    )
    achat_pour_moi_meme=USSDMenu.objects.create(title="achat_pour_moi_meme  ", parent=activer_un_forfait)
    USSDMenu.objects.create(
        title="achat_pour_moi_meme",
        parent=activer_un_forfait,
    )
    USSDMenu.objects.create(title="forfait100000   ", parent=achat_pour_moi_meme)
    USSDMenu.objects.create(
        title="forfait100000",
        parent=achat_pour_moi_meme,
        requires_confirmation=True,
        output="je vais activer mon fofait de 100000 ......................."
    )
    USSDMenu.objects.create(title="forfait500000   ", parent=achat_pour_moi_meme)
    USSDMenu.objects.create(
        title="forfait500000",
        parent=achat_pour_moi_meme,
        requires_confirmation=True,
        output="je vais activer mon fofait de 100000 ......................."
    )
    USSDMenu.objects.create(title="forfait25000000   ", parent=achat_pour_moi_meme)
    USSDMenu.objects.create(
        title="forfait25000000",
        parent=achat_pour_moi_meme,
        requires_confirmation=True,
        output="je vais activer mon fofait de 25000000 ......................."
    )
    USSDMenu.objects.create(title="forfait50000000   ", parent=achat_pour_moi_meme)
    USSDMenu.objects.create(
        title="forfait50000000",
        parent=achat_pour_moi_meme,
        requires_confirmation=True,
        output="je vais activer mon fofait de 50000000 ......................."
    )
    achat_pour_un_autre=USSDMenu.objects.create(title="achat_pour_un_autre  ", parent=activer_un_forfait)
    USSDMenu.objects.create(
    title="achat_pour_un_autre",
    parent=activer_un_forfait,
    requires_confirmation=True,
    )
    USSDMenu.objects.create(title="forfait100000   ", parent=achat_pour_un_autre)
    USSDMenu.objects.create(
        title="forfait100000",
        parent=achat_pour_un_autre,
        requires_confirmation=True,
        output="je vais activer mon fofait de 100000 ......................."
    )
    USSDMenu.objects.create(title="forfait500000   ", parent=achat_pour_un_autre)
    USSDMenu.objects.create(
        title="forfait500000",
        parent=achat_pour_un_autre,
        requires_confirmation=True,
        output="je vais activer mon fofait de 500000 ......................."
    )
    USSDMenu.objects.create(title="forfait25000000   ", parent=achat_pour_un_autre)
    USSDMenu.objects.create(
        title="forfait25000000",
        parent=achat_pour_un_autre,
        requires_confirmation=True,
        output="je vais activer mon fofait de 25000000 ......................."
    )
    USSDMenu.objects.create(title="forfait50000000   ", parent=achat_pour_un_autre)
    USSDMenu.objects.create(
        title="forfait50000000",
        parent=achat_pour_un_autre,
        requires_confirmation=True,
        output="je vais activer mon fofait de 50000000 ......................."
    )
    transfert_international = USSDMenu.objects.create(title="Transfert International", parent=transfert_argent)
    USSDMenu.objects.create(
        title="Reception Internationale",
        parent=transfert_international,
        requires_confirmation=True,
        output="Votre solde de réception internationale est de 20000 FCFA."
    )
    international = USSDMenu.objects.create(title="International", parent=transfert_international)
    USSDMenu.objects.create(
        title="sous region",
        parent=international,
        requires_confirmation=True,
        output="Transfert sous-régional effectué avec succès."
    )
    USSDMenu.objects.create(
        title="Solde compte réception International",
        parent=international,
        output="Votre solde de réception internationale est de 20000 FCFA."
    )
    USSDMenu.objects.create(
        title="transfert vers un compte principale",
        parent=international,
        output="Transfert vers un compte principal effectué avec succès."
    )
    USSDMenu.objects.create(
        title="solde reception international",
        parent=international,
        output="Votre solde de réception internationale est de 20000 FCFA."
    )
    USSDMenu.objects.create(
        title="historique des opérations",
        parent=international,
        output="Voici votre historique des opérations : ..."
    )
    USSDMenu.objects.create(
        title="Utiliser mon code de transfert RIA",
        parent=transfert_argent,
        output="Transfert RIA effectué avec succès."
    )
    USSDMenu.objects.create(
        title="Annuler un transfert vers compte OM",
        parent=transfert_argent,
        output="Transfert annulé avec succès."
    )
    numero_favoris = USSDMenu.objects.create(title="Numero favoris de transfert", parent=transfert_argent)
    USSDMenu.objects.create(
        title="enregistrer un bénéficiaire",
        parent=numero_favoris,
        output="Bénéficiaire enregistré avec succès."
    )
    USSDMenu.objects.create(
        title="supprimer un bénéficiaire",
        parent=numero_favoris,
        output="Bénéficiaire supprimé avec succès."
    )
    USSDMenu.objects.create(
        title="enregistrer un nouveau numéro",
        parent=numero_favoris,
        output="Numéro enregistré avec succès."
    )
    USSDMenu.objects.create(
        title="annuler",
        parent=numero_favoris,
        output="Opération annulée."
    )
    USSDMenu.objects.create(
        title="voir la liste de mes numéros",
        parent=numero_favoris,
        output="Voici la liste de vos numéros favoris : ..."
    )
    # Ajoute les autres menus (#605, #111, etc.) de la même manière...

if __name__ == "__main__":
    create_menus()