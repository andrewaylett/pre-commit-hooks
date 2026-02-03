FROM docker.io/rust:1.93.0-slim@sha256:9e03c5f8a7562ab78f34ab8228dbaec6bbdd4e72c986bae659b4eb2d783de4f4

RUN rustup component add clippy rustfmt

ENTRYPOINT ["/usr/local/cargo/bin/cargo"]
