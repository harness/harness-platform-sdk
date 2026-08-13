ARG REPOSITORY=
ARG IMAGE=python
ARG BASE_TAG=3.14.6-alpine
ARG MODULE=src

FROM ${REPOSITORY}${IMAGE}:${BASE_TAG} AS base
ARG MODULE
ENV PYTHONPATH=/app/${MODULE}/
ENV REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt
ENV SSL_VERIFY_X509_STRICT=true

USER root
WORKDIR /app_setup
COPY os_packages.txt /app_setup/os_packages.txt
# Date: 2026-04-13
# Issue 98: https://github.com/alpinelinux/docker-alpine/issues/98
#
# The repositories are incorrectly configured for HTTPS instead of HTTP
RUN sed -i 's/https/http/' /etc/apk/repositories;
RUN adduser --home /home/harness --shell /bin/sh --uid 1000 --disabled-password harness; \
    echo "Install Base Packages"; \
    PACKAGES=`awk '{printf("%s ",$0)} END { printf "\n" }' /app_setup/os_packages.txt`; \
    apk add --quiet --no-progress ${PACKAGES}; \
    # -----
    # Date: 2026-04-13
    # CVE-2026-3805: curl@8.19.0-r0 (os-pkgs, alpine)
    # Only available in the edge repository
    #
    # When doing a second SMB request to the same host again, curl would wrongly use a data pointer pointing into already freed memory.
    # -----
    apk add --quiet --no-progress "curl>=8.19.0-r0" --repository=http://dl-cdn.alpinelinux.org/alpine/edge/main/; \
    # -----
    # Date: 2026-07-01
    # CVE-2025-60876: busybox@1.37.0-r31 (os-pkgs, alpine)
    # Only available in the edge repository
    #
    # BusyBox wget thru 1.3.7 accepted raw CR (0x0D)/LF (0x0A) and other C0 control bytes in the HTTP
    # request-target (path/query), allowing the request line to be split and attacker-controlled headers
    # to be injected. To preserve the HTTP/1.1 request-line shape METHOD SP request-target SP HTTP/1.1,
    # a raw space (0x20) in the request-target must also be rejected (clients should use %20).
    # -----
    apk add --quiet --no-progress "busybox>=1.38.0-r4" --repository=http://dl-cdn.alpinelinux.org/alpine/edge/main/; \
    # -----
    # Date: 2026-08-13
    # CVE-2026-58055: nghttp2@1.70.0-r0 (os-pkgs, alpine)
    # Only available in the edge repository
    #
    # nghttp2's nghttpx proxy through 1.69.0 forwards an HTTP/1.1 Upgrade request that also carries a
    # Content-Length header and body onto reusable keep-alive backend connections, re-adding the Upgrade
    # and Connection headers while passing Content-Length verbatim. A backend that resolves the resulting
    # ambiguous message in the attacker's favor enables HTTP request/response smuggling and cross-client
    # response-queue poisoning.
    # -----
    apk add --quiet --no-progress "nghttp2>=1.70.0-r0" --repository=http://dl-cdn.alpinelinux.org/alpine/edge/main/; \
    apk add --quiet --no-progress "nghttp2-libs>=1.70.0-r0" --repository=http://dl-cdn.alpinelinux.org/alpine/edge/main/; \
    apk upgrade --quiet --no-progress --update-cache; \
    apk cache clean --purge;\
    rm -rf /app_setup
COPY scripts/python_ssl_verify_x509_strict_override.py sitecustomize.py
RUN python -c "import site; print(site.getsitepackages()[0])" | \
    xargs -I{} cp sitecustomize.py {}/sitecustomize.py

FROM base AS test
WORKDIR /app
COPY /pyproject.toml /app/pyproject.toml
RUN python -m pip install .
COPY ${MODULE}/ /app/${MODULE}/
COPY tests/unit_tests /app/tests/
RUN ln -s /app/${MODULE} /src

FROM base AS release
ARG MODULE
WORKDIR /app
COPY /pyproject.toml /app/pyproject.toml
COPY ${MODULE}/ /app/${MODULE}/
RUN python -m pip install .
ENTRYPOINT ["bash"]

USER 1000
