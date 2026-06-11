FROM docker.io/rust:1.96.0-slim@sha256:082a5849a6870672b5f7a5bf4eddc71723fce38756fd834a0d734a5306a310ab

RUN rustup component add clippy rustfmt

ENTRYPOINT ["/usr/local/cargo/bin/cargo"]
