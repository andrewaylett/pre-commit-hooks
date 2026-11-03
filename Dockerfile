FROM docker.io/rust:1.99.1-slim@sha256:ea0999ff67355d958b8799b6751c879a6d770076d26047dca66f6e51e77930d3

RUN rustup component add clippy rustfmt

ENTRYPOINT ["/usr/local/cargo/bin/cargo"]
