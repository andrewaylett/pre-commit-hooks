FROM docker.io/rust:1.94.0-slim@sha256:c31e3035d5c134821d8b861b3922402f3a009d33516a7f5261936cdb5739b6fc

RUN rustup component add clippy rustfmt

ENTRYPOINT ["/usr/local/cargo/bin/cargo"]
