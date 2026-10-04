FROM docker.io/rust:1.99.0-slim@sha256:0952c7a429d2f53c7f1f5e0796190690e7d8db367ec4a66ce0419763b9e5e0d0

RUN rustup component add clippy rustfmt

ENTRYPOINT ["/usr/local/cargo/bin/cargo"]
