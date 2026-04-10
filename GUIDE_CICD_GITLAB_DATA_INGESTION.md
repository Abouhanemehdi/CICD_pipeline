# Guide pratique Git + CI/CD (GitLab)

Ce guide sert a faire monter l'equipe en competence sur Git et CI/CD, avec un cas d'usage concret de demo pour un projet de **Data Ingestion**.

---

## 1) Objectif equipe

Passer de "Git = sauvegarde" a "Git = collaboration + qualite + livraison fiable".

Resultats attendus:
- Historique propre et compréhensible
- Travail en parallele sans bloquer l'equipe
- Revues de code (Merge Requests) systematiques
- Detection rapide des erreurs via pipeline
- Mises en production plus predictibles

---

## 2) Workflow Git recommande (simple et robuste)

### Branches
- `main`: code stable, toujours deployable
- `develop` (optionnel): integration continue avant `main` (utile si l'equipe debute)
- `feature/<ticket>-<nom-court>`: nouvelles fonctionnalites
- `fix/<ticket>-<nom-court>`: corrections
- `hotfix/<ticket>-<nom-court>`: urgence production

> Pour une equipe debutante: soit **GitFlow simplifie** (`main` + `feature/*`), soit `main` + `develop` si vous avez plusieurs livraisons en parallele.

### Regles de base
- Jamais de commit direct sur `main`
- Une tache = une branche
- Une branche = une Merge Request (MR)
- MR validee par au moins 1 reviewer
- Pipeline verte obligatoire avant merge

### Convention de commits (Conventional Commits, version simple)
- `feat:` nouvelle fonctionnalite
- `fix:` correction bug
- `refactor:` changement interne sans effet fonctionnel
- `test:` ajout/modif tests
- `docs:` documentation
- `chore:` maintenance (deps, config, etc.)

Exemples:
- `feat: add ingestion job for customer events`
- `fix: handle null timestamp in parser`
- `test: add unit tests for csv validator`

---

## 3) Cycle de travail standard (developer)

1. Creer branche depuis `main`
2. Coder par petits commits
3. Mettre a jour sa branche regulierement (`git fetch` + `rebase` ou `merge`)
4. Pousser la branche
5. Ouvrir MR avec template
6. Corriger retours review + pipeline
7. Merge quand toutes les conditions sont OK

Commandes utiles:

```bash
git checkout main
git pull
git checkout -b feature/123-ingestion-csv-validation

# ... dev ...
git add .
git commit -m "feat: add csv schema validation step"
git push -u origin feature/123-ingestion-csv-validation
```

---

## 4) Gestion des conflits (process standard)

Quand conflit:
1. Recuperer les changements distants
2. Rejouer/merge sur votre branche
3. Resoudre fichier par fichier
4. Lancer tests localement
5. Commit de resolution
6. Push et relancer pipeline

Exemple:

```bash
git checkout feature/123-ingestion-csv-validation
git fetch origin
git rebase origin/main
# resoudre conflits
git add .
git rebase --continue
git push --force-with-lease
```

Bonnes pratiques:
- Conflits resolus en binome si besoin
- Toujours re-tester apres resolution
- Eviter les longues branches (> 3-5 jours)

---

## 5) Definition of Done (DoD) pour merger

Une MR est mergeable seulement si:
- [ ] Pipeline CI verte
- [ ] Revue approuvee (minimum 1 personne)
- [ ] Tests unitaires passes
- [ ] Changelog/description MR claire
- [ ] Pas de secrets dans le code
- [ ] Documentation mise a jour si impact

---

## 6) Pipeline CI/CD GitLab (base recommandee)

Etapes minimales:
1. **lint** (qualite code)
2. **test** (unit/integration)
3. **build** (package/image)
4. **deploy staging** (automatique)
5. **deploy production** (manuel avec approbation)

Principes:
- Pipeline lancee sur chaque push/MR
- Jobs rapides et paralleles
- Cache dependances
- Variables sensibles dans GitLab CI Variables
- Environnements `staging` et `production`

Exemple minimal `.gitlab-ci.yml` (Python data ingestion):

```yaml
stages:
  - lint
  - test
  - build
  - deploy

default:
  image: python:3.11
  cache:
    paths:
      - .venv/
      - .cache/pip

before_script:
  - python -m venv .venv
  - . .venv/bin/activate
  - pip install -U pip
  - pip install -r requirements.txt

lint:
  stage: lint
  script:
    - ruff check .

test:
  stage: test
  script:
    - pytest -q

build:
  stage: build
  script:
    - python -m build
  artifacts:
    paths:
      - dist/

deploy_staging:
  stage: deploy
  script:
    - echo "Deploy to staging"
  environment:
    name: staging
  only:
    - main

deploy_production:
  stage: deploy
  script:
    - echo "Deploy to production"
  environment:
    name: production
  when: manual
  only:
    - main
```

> Adapter les commandes selon votre stack (Spark, dbt, Airflow, Docker, etc.).

---

## 7) Cas d'usage concret de demo (UC)

### Contexte demo
Le pipeline de data ingestion lit un fichier CSV client et charge des donnees propres dans la base analytique.

### Scenario de demonstration (30-45 min)

#### Etape A - Preparation
- Branches protegees sur `main`
- Regles MR activees (approval + pipeline obligatoire)
- Template de MR configure
- CI active avec jobs lint/test/build

#### Etape B - Travail developpeur
1. Dev A cree `feature/201-add-csv-validator`
2. Ajoute validation schema CSV + tests
3. Push branche + ouvre MR

#### Etape C - Revue + CI
1. Pipeline detecte echec (ex: colonne manquante non geree)
2. Dev A corrige et push
3. Pipeline devient verte
4. Reviewer approuve MR

#### Etape D - Conflit volontaire (pedagogique)
1. Dev B modifie la meme fonction sur une autre branche
2. Merge de Dev B d'abord
3. MR Dev A a un conflit
4. Dev A resolve conflit en direct (demo)
5. Tests repasses + pipeline OK

#### Etape E - Merge et deployment
1. Merge vers `main`
2. Deploy staging automatique
3. Validation metier rapide
4. Deploy production manuel (approbation Lead)

### Message cle de la demo
"Le pipeline CI/CD n'est pas un controle de police; c'est un filet de securite qui protege l'equipe et la qualite."

---

## 8) RACI simple (qui fait quoi)

- **Developer**: code, tests, MR, correction pipeline
- **Reviewer**: feedback technique/fonctionnel, approbation
- **Tech Lead**: regles Git, qualite de review, arbitrage
- **DevOps/Platform**: maintien CI/CD, runners, secrets, environnements
- **PO/Metier**: validation fonctionnelle en staging

---

## 9) Plan de montee en competence (4 semaines)

### Semaine 1
- Formation express Git (branch, commit, rebase, conflit)
- Definition des conventions (naming, commit, MR)

### Semaine 2
- Mise en place regles GitLab (branch protections, approvals)
- Pipeline minimale lint + test

### Semaine 3
- Generalisation MR obligatoire
- Pair-review systematique
- Dashboard simple: taux pipeline verte

### Semaine 4
- Demo complete du cas d'usage
- Retrospective equipe
- Ajustement des regles (pas trop strictes au debut)

---

## 10) Anti-patterns a eviter

- Commit direct sur `main`
- Grosse MR (> 1000 lignes) difficile a reviewer
- Branches qui vivent des semaines
- "Pipeline rouge mais on merge quand meme"
- Secrets dans repo
- Pas de tests pour zones critiques

---

## 11) Checklist de lancement (copier-coller)

- [ ] Convention de branches validee
- [ ] Convention de commits validee
- [ ] Template MR cree
- [ ] Protection `main` activee
- [ ] Approval minimum 1 reviewer
- [ ] Pipeline CI (lint + test + build) operationnelle
- [ ] Staging configure
- [ ] Procedure conflit documentee
- [ ] Cas demo planifie et repete

---

## 12) Template MR (recommande)

```md
## Contexte
Pourquoi ce changement est necessaire ?

## Changement
- Point 1
- Point 2

## Tests
- [ ] Test unitaire
- [ ] Test integration
- [ ] Test manuel

## Risques
Quels impacts possibles ?

## Rollback
Comment revenir en arriere si probleme ?
```

---

## Conclusion

Votre enjeu n'est pas seulement technique: c'est un changement de pratique d'equipe.
Commencez simple, imposez peu de regles mais non negociables (MR + pipeline verte + review), puis augmentez le niveau de maturite chaque semaine.
