FROM docker.io/rust:1.90.0-slim@sha256:40d4ee109c7e740b3a242f20cc3b5790af9c725828b86a458765f192391a6a4a

RUN rustup component add clippy rustfmt

ENTRYPOINT ["/usr/local/cargo/bin/cargo"]
