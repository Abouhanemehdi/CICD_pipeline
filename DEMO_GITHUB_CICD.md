# Demo GitHub CI/CD - Data Ingestion

Ce document te donne un script de demo simple a executer avec ton equipe sur GitHub.

## 1) Ce qui est deja pret

- Pipeline GitHub Actions: `.github/workflows/ci-cd-demo.yml`
- Code de demo ingestion: `app/ingestion.py`
- Tests unitaires: `tests/test_ingestion.py`
- Dependances CI: `requirements-dev.txt`

## 2) Prerequis GitHub (5 min)

1. Creer un repo GitHub (ou utiliser un repo existant)
2. Pousser ce contenu sur la branche `main`
3. Dans GitHub:
   - Settings > Branches > Add rule sur `main`
   - Activer:
     - Require a pull request before merging
     - Require status checks to pass before merging
4. (Optionnel) Settings > Environments:
   - Creer `staging`
   - Creer `production` avec required reviewers (approbation manuelle)

## 3) Ce que fait le pipeline

### Sur Pull Request vers main
- Lint (verification syntaxe Python)
- Tests (`pytest`)
- Build artifact (`dist/` upload)

### Sur push vers main
- Rejoue CI
- Lance un deploy staging (simulation)

### Sur lancement manuel (workflow_dispatch)
- Lance deploy production (simulation) avec environnement `production`

## 4) Script de demo live (30 min)

### Etape A - Montre un passage vert (5 min)
1. Ouvre une PR avec un changement propre
2. Montre l'onglet Actions
3. Explique les jobs: CI -> staging

### Etape B - Introduis un echec volontaire (10 min)
1. Dans `app/ingestion.py`, casse une validation (ex: supprime controle `event_type`)
2. Push sur la PR
3. Montre test rouge dans Actions
4. Corrige le code
5. Push et montre pipeline redevenir verte

### Etape C - Merge policy (5 min)
1. Tente de merger quand pipeline rouge (bloque)
2. Montre qu'on ne peut merger que quand checks sont verts

### Etape D - Deploy demo (10 min)
1. Merge PR vers `main`
2. Montre job `Deploy to Staging (demo)`
3. Lance manuellement le workflow (Run workflow)
4. Montre job `Deploy to Production (manual approval)`

## 5) Message pedagogique a faire passer

- "La CI detecte vite les regressions"
- "La PR protege la qualite collective"
- "Le CD standardise la livraison"
- "Le process reduit le risque et les conflits tardifs"

## 6) Prochaine evolution (apres demo)

- Ajouter coverage (`pytest --cov`)
- Ajouter scans securite (CodeQL / dependency scan)
- Remplacer les steps `echo deploy` par vrai deploiement (Docker/K8s/Airflow)
- Ajouter notifications Teams/Slack

## Trigger note
- Test PR created to validate GitHub Actions checks before merge.

