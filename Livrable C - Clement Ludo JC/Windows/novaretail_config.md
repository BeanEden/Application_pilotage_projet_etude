# NovaRetail — Configurations par notebook

> Extrait depuis les cellules des trois notebooks Bronze, Silver et Gold.  
> À compléter avec les paramètres du pool Spark et de l'environnement Fabric (non exportables automatiquement).

---

## Notebook_bronze_final (NB_01) — Ingestion Bronze

### Packages installés (`%pip install`)

```
docling>=2.0
py7zr>=0.20
```

> Docling tire `python-docx` en dépendance transitive (utilisé explicitement dans le parser).  
> À ajouter dans le pool Spark ou l'environnement Fabric pour éviter la réinstallation à chaque session (~2–4 min).

### Variables d'environnement (à positionner AVANT tout import Docling)

| Variable | Valeur | Rôle |
|----------|--------|------|
| `HF_HUB_OFFLINE` | `0` | Autorise le download HF au 1er run (passer à `1` une fois les modèles cachés) |
| `TRANSFORMERS_OFFLINE` | `0` | Idem pour Transformers |
| `HF_DATASETS_OFFLINE` | `0` | Idem pour Datasets |
| `HUGGINGFACE_HUB_VERBOSITY` | `error` | Réduit les logs HF |
| `HF_HUB_DISABLE_XET` | `0` | Désactive le thread réseau XET de HF Hub |
| `XET_DISABLE` | `0` | Idem côté XET |

> En production sur Fabric (pas d'accès internet) : passer `HF_HUB_OFFLINE`, `TRANSFORMERS_OFFLINE`, `HF_DATASETS_OFFLINE` à `1` et `HF_HUB_DISABLE_XET`, `XET_DISABLE` à `1`.

### Configuration Spark

| Clé | Valeur | Raison |
|-----|--------|--------|
| `spark.sql.parquet.datetimeRebaseModeInWrite` | `CORRECTED` | Évite les erreurs de sérialisation des dates Parquet entre calendriers julien/grégorien |

### Chemins OneLake (ABFSS)

| Variable | Chemin |
|----------|--------|
| `WORKSPACE_NAME` | `Projet_technique` |
| `LAKEHOUSE_NAME` | `Bons_de_commandes` |
| `LAKEHOUSE_ROOT` | `abfss://Projet_technique@onelake.dfs.fabric.microsoft.com/Bons_de_commandes.Lakehouse` |
| `SOURCE_ZIP_PATH` | `{LAKEHOUSE_ROOT}/Files/` |
| `SOURCE_SHAREPOINT_PATH` | `{LAKEHOUSE_ROOT}/Files/grp-Clement-JC-Ludovic/` |
| `SOURCE_AUTRES_PATH` | `{LAKEHOUSE_ROOT}/Files/raw_autres/` |
| `TEMP_EXTRACT_DIR` | `/tmp/novaretail_extract/` |

### Tables Delta produites

| Table | Chemin |
|-------|--------|
| `bronze_commandes_headers` | `{LAKEHOUSE_ROOT}/Tables/bronze_commandes_headers` |
| `bronze_commandes_lignes` | `{LAKEHOUSE_ROOT}/Tables/bronze_commandes_lignes` |
| `bronze_raw_json` | `{LAKEHOUSE_ROOT}/Tables/bronze_raw_json` |
| `bronze_audit_ingestion` | `{LAKEHOUSE_ROOT}/Tables/bronze_audit_ingestion` |
| `bronze_fichiers_corrompus` | `{LAKEHOUSE_ROOT}/Tables/bronze_fichiers_corrompus` |
| `bronze_inventaire_fichiers` | `{LAKEHOUSE_ROOT}/Tables/bronze_inventaire_fichiers` |

### Paramètres d'exécution (cellule 8)

| Paramètre | Valeur par défaut | Description |
|-----------|-------------------|-------------|
| `forcer_reingestion` | `True` | `False` = idempotence (skip documents déjà en Bronze) |
| `max_workers` | `8` | Parallélisme ThreadPoolExecutor Docling |
| `limite_fichiers` | `1000` | Nombre max de fichiers traités par run (None = illimité) |

---

## NB_SILVER_2 (NB_02) — Transformation Silver

### Packages installés

Aucun `%pip install` — uniquement des modules PySpark natifs et bibliothèque standard Python.

### Configuration Spark

| Clé | Valeur | Raison |
|-----|--------|--------|
| `spark.sql.parquet.datetimeRebaseModeInWrite` | `CORRECTED` | Cohérence avec la couche Bronze |
| `spark.sql.legacy.timeParserPolicy` | `LEGACY` | Compatibilité parsing dates multi-format via `to_date()` |

### Chemins OneLake

Mêmes `WORKSPACE_NAME` et `LAKEHOUSE_NAME` que Bronze.

| Variable | Chemin |
|----------|--------|
| `SILVER_CLIENTS` | `{LAKEHOUSE_ROOT}/Tables/silver_clients` |
| `SILVER_COMMERCIAUX` | `{LAKEHOUSE_ROOT}/Tables/silver_commerciaux` |
| `SILVER_ARTICLES` | `{LAKEHOUSE_ROOT}/Tables/silver_articles` |
| `SILVER_COMMANDES` | `{LAKEHOUSE_ROOT}/Tables/silver_commandes` |
| `SILVER_LIGNES_COMMANDE` | `{LAKEHOUSE_ROOT}/Tables/silver_lignes_commande` |
| `SILVER_AUDIT` | `{LAKEHOUSE_ROOT}/Tables/silver_audit` |

### Tables Delta produites

| Table | Mode écriture | Partition |
|-------|---------------|-----------|
| `silver_clients` | `overwrite` | — |
| `silver_commerciaux` | `overwrite` | — |
| `silver_articles` | `overwrite` | — |
| `silver_commandes` | `overwrite` | `periode_zip` |
| `silver_lignes_commande` | `overwrite` | — |
| `silver_audit` | `append` | — |

---

## NB_GOLD_2 (NB_03) — Modèle en étoile Gold

### Packages installés

Aucun `%pip install` — uniquement PySpark et bibliothèque standard Python.

### Configuration Spark

| Clé | Valeur | Raison |
|-----|--------|--------|
| `spark.sql.parquet.datetimeRebaseModeInWrite` | `CORRECTED` | Cohérence pipeline |
| `spark.sql.legacy.timeParserPolicy` | `LEGACY` | Cohérence avec Silver |

### Chemins OneLake

Mêmes `WORKSPACE_NAME` et `LAKEHOUSE_NAME`.

**Sources Silver (lecture)**

| Variable | Table source |
|----------|-------------|
| `SILVER_CLIENTS` | `silver_clients` |
| `SILVER_COMMERCIAUX` | `silver_commerciaux` |
| `SILVER_ARTICLES` | `silver_articles` |
| `SILVER_COMMANDES` | `silver_commandes` |
| `SILVER_LIGNES_COMMANDE` | `silver_lignes_commande` |

**Tables Gold produites**

| Table | Mode écriture | Partition |
|-------|---------------|-----------|
| `gold_fact_commande_ligne` | `append` | — |
| `gold_dim_commande` | `append` | `periode_zip` |
| `gold_dim_client` | `overwrite` | — |
| `gold_dim_produit` | `overwrite` | — |
| `gold_dim_temps` | `overwrite` | — |
| `gold_dim_fournisseur` | `overwrite` | — |
| `gold_dim_commerciaux` | `overwrite` | — |
| `gold_kpi_ca_mensuel` | `overwrite` | — |
| `gold_kpi_ca_client` | `overwrite` | — |
| `gold_kpi_ca_article` | `overwrite` | — |
| `gold_kpi_ca_commercial` | `overwrite` | — |
| `gold_kpi_delais_livraison` | `overwrite` | — |
| `gold_audit` | `append` | — |

### Constantes métier

| Constante | Valeur | Usage |
|-----------|--------|-------|
| `ID_FOURNISSEUR_NOVARETAIL` | `1` | FK `id_fournisseur` injectée en dur dans la fact |

---

## Configurations communes aux trois notebooks

| Paramètre | Valeur |
|-----------|--------|
| `WORKSPACE_NAME` | `Projet_technique` |
| `LAKEHOUSE_NAME` | `Bons_de_commandes` |
| Format tables | Delta Lake (`mergeSchema: true`) |
| `spark.sql.parquet.datetimeRebaseModeInWrite` | `CORRECTED` |
| `SparkSession` | `getOrCreate()` — session Fabric réutilisée, pas recréée |

---

## Notes Fabric

- **Environnement recommandé** : créer un *Fabric Environment* avec `docling` et `py7zr` pré-installés, attaché aux trois notebooks. Évite le `%pip install` à chaque session.
- **Cache HuggingFace** : Docling télécharge ses modèles au 1er run. Stocker le cache dans `{LAKEHOUSE_ROOT}/Files/hf_cache/` et pointer `HF_HOME` dessus pour le rendre persistant entre sessions.
- **Mssparkutils** : disponible nativement dans Fabric. Les fonctions `mssparkutils.fs.ls/cp/rm` n'ont pas de package à installer.
