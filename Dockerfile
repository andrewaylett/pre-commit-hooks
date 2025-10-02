FROM docker.io/rust:1.90.0-slim@sha256:33b421a1c92686a6fa44ecaf34f1017e55267eaa184d7d6d4e5233689ab6bac3

RUN rustup component add clippy rustfmt

ENTRYPOINT ["/usr/local/cargo/bin/cargo"]
