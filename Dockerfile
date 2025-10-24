FROM docker.io/rust:1.90.0-slim@sha256:7fa728f3678acf5980d5db70960cf8491aff9411976789086676bdf0c19db39e

RUN rustup component add clippy rustfmt

ENTRYPOINT ["/usr/local/cargo/bin/cargo"]
