def normalize_umlauts(name):
    return name.replace("\u00d6", "Oe").replace("\u00f6", "oe")\
        .replace("\u00dc", "Ue").replace("\u00fc", "ue")\
        .replace("\u00c4", "Ae").replace("\u00e4", "ae")
