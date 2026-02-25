FROM docker.io/rust:1.93.1-slim@sha256:903ffbe85258c893248ac5ee6fe0e89677ffe77fb0d47907162f52d11fe52dd3

RUN rustup component add clippy rustfmt

ENTRYPOINT ["/usr/local/cargo/bin/cargo"]
