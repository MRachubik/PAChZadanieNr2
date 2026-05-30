# Zadanie 2 (Sprawozdanie)

## TAGOWANIE I CACHE (Uzasadnienie)

Obrazy na ghcr.io są tagowane unikalnym skrótem z Githuba (`sha-<skrot>`). Dzięki tej informacji wiadomo dokładnie, z jakiej wersji kodu powstał dany kontener. Pomaga to uniknąć przypadkowym nadpisaniu obrazu np. podczas używania tagu latest.

Warstwy Cache na DockerHubie są zapisywane z parametrem `mode=max`. Tryb ten eksportuje wszystkie warstwy budowania w tym etapów pośrednich z pliku Dockerfile. Każde kolejne uruchomienie potoku dzięki temu trwa krócej.

# Wszystkie informacje: 
## Stworzenie lokalnego repozytorium

`git init -b main`

## Podpięcie loginu i tokenu z Docker Huba do Githuba (do zapisu cache)

`gh variable set DOCKERHUB_USERNAME --body "mrcellar"`
`gh secret set DOCKERHUB_TOKEN`

## Wyciszenie błędów w paczkach (CVE-2026-24049 oraz CVE-2026-23949) w pliku .trivyignore

## Wysyłanie plików, wystartowanie GitHub Actions:
```bash
git add .
git commit -m "Potok CI/CD"
git push -u origin main
```

## Podgąd działania potoku na żywo

Komenda: 

```
gh run watch
```

Wynik:

```bash
✓ main Zadanie 2 - Pipeline CI/CD · 26692642841
Triggered via push less than a minute ago

JOBS
✓ Build, tag and push Docker image in 49s (ID 78671693724)
  ✓ Set up job
  ✓ Check out the source_repo
  ✓ Log in to GitHub Container Registry
  ✓ Login to DockerHub
  ✓ Docker metadata definitions
  ✓ QEMU set-up
  ✓ Buildx set-up
  ✓ Build local image CVE test
  ✓ Run Trivy scanner
  ✓ Build and push Docker image
  ✓ Post Build and push Docker image
  ✓ Post Run Trivy scanner
  ✓ Post Build local image CVE test
  ✓ Post Buildx set-up
  ✓ Post QEMU set-up
  ✓ Post Login to DockerHub
  ✓ Post Log in to GitHub Container Registry
  ✓ Post Check out the source_repo
  ✓ Complete job

✓ Run Zadanie 2 - Pipeline CI/CD (26692642841) completed with 'success'
```

## Wymagania zadania

Dodany krok z emulatorem QEMU, budowanie obrazu jednocześnie na procesory `linux/amd64` oraz `linux/arm64`.

```bash
name: QEMU set-up
uses: docker/setup-qemu-action@v4
```

Brama Trivy, czyli skaner sprawdza obraz przed wysłaniem, przy wykryciu niezaakceptowanych błędów, wyrzuca błąd (exit-code).

Fragment:

```bash
name: Run Trivy scanner
uses: aquasecurity/trivy-action@master
with:
    image-ref: 'local_test_image:latest'
    format: 'table'
    exit-code: '1'
    ignore-unfixed: true
    vuln-type: 'os,library'
    severity: 'CRITICAL,HIGH'
```

Pamięć podręczna zapisywana i pobierana z Docker Huba. Włączony tryb mode=max, aby zapisać wszystkie warstwy budowania.

Fragment:

```bash
cache-from: type=registry,ref=${{ vars.DOCKERHUB_USERNAME }}/lab_pogoda:cache 
cache-to: type=registry,ref=${{ vars.DOCKERHUB_USERNAME }}/lab_pogoda:cache,mode=max  
```

