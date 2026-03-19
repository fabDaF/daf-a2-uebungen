files_to_restore = [
    "DE_A2_1035V-mein-zuhause.html",
    "DE_A2_1036X-temporale-praepositionen.html",
    "DE_A2_1037G-superlativ.html",
    "DE_A2_1038S-ueber-die-wohnung-reden.html",
    "DE_A2_1041V-stadtleben.html",
    "DE_A2_1042X-die-meinung-sagen.html",
    "DE_A2_1043G-nebensaetze-dass-weil.html",
    "DE_A2_1046X-temporale-adverbien.html",
    "DE_A2_1047G-reflexive-verben.html",
    "DE_A2_1048S-kulturelle-interessen.html",
    "DE_A2_1052X-wortbildung-suffixe.html",
    "DE_A2_1053G-der-ein-woerter.html",
    "DE_A2_1056X-verb-lassen.html",
    "DE_A2_1062X-wenn-dann.html",
    "DE_A2_1063G-futur-I.html",
]

import os
for f in files_to_restore:
    base = f.replace('.html', '')
    backup = f.replace('.html', '.backup.html')
    html_exists = os.path.exists(f)
    backup_exists = os.path.exists(backup)
    print(f"{base}: HTML={html_exists}, BACKUP={backup_exists}")
