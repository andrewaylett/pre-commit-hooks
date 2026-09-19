FROM docker.io/rust:1.98.1-slim@sha256:ca5c572a3d4e8acfa44bc065aa6d9dafbee398bf14ec376d2bcf955820a4c9f3

RUN rustup component add clippy rustfmt

ENTRYPOINT ["/usr/local/cargo/bin/cargo"]
