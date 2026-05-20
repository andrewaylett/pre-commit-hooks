FROM docker.io/rust:1.95.0-slim@sha256:a6bc7ce698c8c1025307bd85254b697c58c466f66e83012826a1a50937142cbe

RUN rustup component add clippy rustfmt

ENTRYPOINT ["/usr/local/cargo/bin/cargo"]
