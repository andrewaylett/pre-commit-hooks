FROM docker.io/rust:1.92.0-slim@sha256:991b1768c575086cbf188eb03e78003ec4e31947029b1947e8034ae32aa6156b

RUN rustup component add clippy rustfmt

ENTRYPOINT ["/usr/local/cargo/bin/cargo"]
