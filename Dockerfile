FROM docker.io/rust:1.91.1-slim@sha256:f379d71f15aa118a7b57caa5f305e58b8f50d317ea68336b05d797ad9360ea68

RUN rustup component add clippy rustfmt

ENTRYPOINT ["/usr/local/cargo/bin/cargo"]
