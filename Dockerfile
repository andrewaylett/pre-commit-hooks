FROM docker.io/rust:1.90.0-slim@sha256:e4ae8ab67883487c5545884d5aa5ebbe86b5f13c6df4a8e3e2f34c89cedb9f54

RUN rustup component add clippy rustfmt

ENTRYPOINT ["/usr/local/cargo/bin/cargo"]
