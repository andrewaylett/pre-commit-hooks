FROM docker.io/rust:1.91.1-slim@sha256:1e6c58cc1d3e3a47021ba10009e02224eb9e0021823539a964ce206391eb30a3

RUN rustup component add clippy rustfmt

ENTRYPOINT ["/usr/local/cargo/bin/cargo"]
