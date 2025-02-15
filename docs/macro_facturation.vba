Sub GenererFacturesPDF()
    Dim wsFacture As Worksheet
    Dim wsListe As Worksheet
    Dim lastRow As Long
    Dim i As Long
    Dim numFacture As String
    Dim cheminDossier As String
    Dim cheminFichier As String
    
    ' Demander à l'utilisateur un numéro pour les factures
    numeroUtilisateur = InputBox("Veuillez entrer le numéro de la prochaine Facture:", "Numéro de Facture")
    
    ' Vérifier si l'utilisateur a annulé ou laissé vide
    If numeroUtilisateur = "" Then
        MsgBox "Aucun numéro de facture n'a été fourni. La macro va se terminer.", vbExclamation
        Exit Sub
    End If

    ' Définition des feuilles
    Set wsFacture = ThisWorkbook.Sheets("Facture Template")
    Set wsListe = ThisWorkbook.Sheets("Extract (Streamlit)")
    
    ' Déterminer la dernière ligne de données dans Liste_Factures
    lastRow = wsListe.Cells(wsListe.Rows.Count, 1).End(xlUp).Row
    
    ' Définir le dossier de sauvegarde des PDFs (vous pouvez le changer)
    cheminDossier = ThisWorkbook.Path & "\Factures_PDF\"
    
    ' Vérifier si le dossier existe, sinon le créer
    If Dir(cheminDossier, vbDirectory) = "" Then
        MkDir cheminDossier
    End If
    
    ' Boucle sur chaque ligne de Liste_Factures (en supposant que la première ligne est un en-tête)
    For i = 2 To lastRow
        numFacture = numeroUtilisateur + i - 2
        
        ' Remplir les variables de la feuille Facture avec les valeurs de Liste_Factures
        wsListe.Range("A" & i & ":AA" & i).Copy Destination:=wsFacture.Range("A1")
        wsFacture.Cells(1, "AK").Value = numFacture
        
        ' Définir le nom du fichier PDF (ex : basé sur un numéro de facture)
        cheminFichier = cheminDossier & "Facture_" & numFacture & ".pdf"
        
        ' Exporter la feuille Facture en PDF
        wsFacture.ExportAsFixedFormat Type:=xlTypePDF, _
            Filename:=cheminFichier, _
            Quality:=xlQualityStandard, _
            IncludeDocProperties:=True, _
            IgnorePrintAreas:=False, _
            OpenAfterPublish:=False, _
            From:=2, To:=2
    Next i
    
    ' Message de confirmation
    MsgBox "Factures générées avec succès dans : " & cheminDossier, vbInformation, "Terminé"
End Sub


