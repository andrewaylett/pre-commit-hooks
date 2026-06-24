FROM docker.io/rust:1.96.0-slim@sha256:4ddd2ebb0043566905e1e5e82ba7c66c03444b32ef16caa6bf5a20155d6ffb15

RUN rustup component add clippy rustfmt

ENTRYPOINT ["/usr/local/cargo/bin/cargo"]
