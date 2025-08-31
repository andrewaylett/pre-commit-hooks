FROM docker.io/rust:1.89.0-slim@sha256:e556a015ecb064ca6b3b74bceb36a54deaf88afbe2956b8fe3e445da446d9cf8

RUN rustup component add clippy rustfmt

ENTRYPOINT ["/usr/local/cargo/bin/cargo"]
