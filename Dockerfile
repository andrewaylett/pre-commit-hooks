FROM docker.io/rust:1.99.1-slim@sha256:f938561c139ff3f8b4449fe5064ede0ea526229b0fc8ea58a5031c3bf40e72d3

RUN rustup component add clippy rustfmt

ENTRYPOINT ["/usr/local/cargo/bin/cargo"]
