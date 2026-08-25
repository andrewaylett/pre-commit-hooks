FROM docker.io/rust:1.98.0-slim@sha256:fb4b2f1dc68c06f46618948b09d0ade147e6d2b11a6581e599b0c808d5b8a167

RUN rustup component add clippy rustfmt

ENTRYPOINT ["/usr/local/cargo/bin/cargo"]
