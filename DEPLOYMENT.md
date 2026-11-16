# Learning-environment deployment

Three services were deployed and checked on 2026-11-16:

- Pictures: IBM Code Engine, `/health` returns OK and `/count` returns 10.
- Songs: OpenShift with MongoDB; `/health` returns OK and the collection contains 20 seed songs. A disposable record was created (201), retrieved (200), updated (201), deleted (204), and verified absent (404); count returned to 20.
- Django: Kubernetes, `djangoserver` deployment, port 8000. Home, Songs and Photos render successfully using the two live APIs.

The ordinary OpenShift route timed out from this environment. The working Songs endpoint in deployment.yml is the lab's application proxy and requires the lab and `oc port-forward deployment/songs 8080:8080` to remain active. The Django browser proxy similarly requires `kubectl port-forward deployment/djangoserver 8000:8000`. These are temporary educational deployments, not permanent hosting.

Build: `docker build -t us.icr.io/$SN_ICR_NAMESPACE/djangoserver:1 .`
Push: `docker push us.icr.io/$SN_ICR_NAMESPACE/djangoserver:1`
Deploy: `kubectl apply -f deployment.yml`
Check: `kubectl get pods` and `kubectl logs deployment/djangoserver`

Set SONGS_API_URL and PICTURES_API_URL to the endpoints available in your own lab. Set DJANGO_ALLOWED_HOSTS as needed. Startup applies migrations. No default administrator credentials are created; use `python manage.py createsuperuser` interactively.

Run service-view tests: `python manage.py test concert.test_services`. Five tests passed, covering successful rendering, missing configuration, network errors and malformed service responses. Pictures' existing 11 pytest tests also passed. These checks are development evidence, not a Coursera grade. Administrator UI and final submission remain for review.
