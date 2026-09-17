ARG REPOSITORY=pkg.harness.io/nqeiomekrdybyovezvtcgg/scoe_images/
ARG IMAGE=hhi/python
ARG BASE_TAG=3.14.7
ARG MODULE=harness_platform_sdk

FROM ${REPOSITORY}${IMAGE}:${BASE_TAG}-dev AS builder
ARG MODULE

USER root
WORKDIR /app
RUN apk add --no-cache ca-certificates
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
COPY scripts/python_ssl_verify_x509_strict_override.py sitecustomize.py
RUN python -c "import site; print(site.getsitepackages()[0])" | \
    xargs -I{} cp sitecustomize.py {}/sitecustomize.py
COPY README.md /app/README.md
COPY pyproject.toml /app/pyproject.toml
COPY src/ /app/src
RUN python -m pip install --no-cache-dir .
RUN pip freeze


FROM ${REPOSITORY}${IMAGE}:${BASE_TAG} AS release
ARG MODULE
ARG RELEASE_VERSION
ARG RELEASE_SHA
ARG RELEASE_DATE
# ENV PYTHONPATH=/app/${MODULE}/
ENV SSL_VERIFY_X509_STRICT=true
ENV PATH="/app/${MODULE}/:/opt/venv/bin:$PATH"
COPY --from=builder /opt/venv /opt/venv
COPY --from=builder /app/src/${MODULE} /app/${MODULE}

LABEL org.opencontainers.image.authors="Harness <platform@harness.io>"
LABEL org.opencontainers.image.title="Harness Platform SDK"
LABEL org.opencontainers.image.description="Python SDK for the Harness Platform API"
LABEL org.opencontainers.image.url="https://hub.docker.com/r/harnesssolutionfactory/harness-platform-sdk"
LABEL org.opencontainers.image.documentation="https://developer.harness.io/harness-solutions-factory/use-hsf/plugins/harness-platform-sdk"
LABEL org.opencontainers.image.source="https://github.com/harness/harness-platform-sdk"
LABEL org.opencontainers.image.vendor="Harness"
LABEL org.opencontainers.image.licenses="BUSL-1.1"
LABEL org.opencontainers.image.version="${RELEASE_VERSION}"
LABEL org.opencontainers.image.revision="${RELEASE_SHA}"
LABEL org.opencontainers.image.created="${RELEASE_DATE}"
# PLACEHOLDER: Add any additional custom labels specific to your deployment infrastructure

ENTRYPOINT ["python"]

USER 1000
