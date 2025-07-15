import os
import re
# Plusieurs formules dax à venir
def add_dax_measure(tmdl_path, measure_name, dax_formula):
    if not os.path.exists(tmdl_path):
        return False
    with open(tmdl_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Vérifie si la mesure existe déjà
    if re.search(rf"measures\s*=\s*\{{[^}}]*'{measure_name}'", content, re.DOTALL):
        return False  # mesure déjà présente

    # Prépare le bloc de la mesure
    measure_block = f"  '{measure_name}' = {{\n    expression: {dax_formula}\n  }}\n"

    # Cherche le bloc measures
    match = re.search(r"(measures\s*=\s*\{)", content)
    if not match:
        # Si le bloc n'existe pas, on l'ajoute avant la dernière accolade
        content = re.sub(r"\}\s*$", f"  measures = {{\n{measure_block}  }}\n}}", content, flags=re.MULTILINE)
    else:
        # Ajoute la mesure dans le bloc existant
        insert_pos = match.end()
        content = content[:insert_pos] + "\n" + measure_block + content[insert_pos:]

    with open(tmdl_path, 'w', encoding='utf-8') as f:
        f.write(content)
    return True

add_dax_measure(
    tmdl_path=r"C:\Users\Jepssen\OneDrive - Triskill\Documents T\Agents IA\VentesPBI\ventes_projet\Model\tables\ventes.tmdl",
    measure_name="Total TVA",
    dax_formula="SUM(Ventes[ChiffreAffaires]) * 0.2"
)