FROM docker.io/rust:1.96.0-slim@sha256:26abcef3d79b8d890c4ceb17093154573e1f6479cf6dd7c1450043b8458350f6

RUN rustup component add clippy rustfmt

ENTRYPOINT ["/usr/local/cargo/bin/cargo"]
