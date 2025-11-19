FROM docker.io/rust:1.91.1-slim@sha256:f142b62571cf33a234dc90e83814909dfe61eeae11cea75febb27334da8cb4c8

RUN rustup component add clippy rustfmt

ENTRYPOINT ["/usr/local/cargo/bin/cargo"]
