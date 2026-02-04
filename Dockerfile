FROM docker.io/rust:1.93.0-slim@sha256:e2367a80bfc3cf85e5794dcfe0b9699f96b61f5aaf8c449b4d4e25d38976d987

RUN rustup component add clippy rustfmt

ENTRYPOINT ["/usr/local/cargo/bin/cargo"]
