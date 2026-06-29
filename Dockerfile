FROM docker.io/rust:1.96.0-slim@sha256:c37af730be4fd8104cbf9aedbd6ab259e51ca2d5437817a0f8680edf66ac6c28

RUN rustup component add clippy rustfmt

ENTRYPOINT ["/usr/local/cargo/bin/cargo"]
