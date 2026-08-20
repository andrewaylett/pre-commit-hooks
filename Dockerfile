FROM docker.io/rust:1.98.0-slim@sha256:77abfb641e6ca03336ad986a7f875e4203f67441aa92337efe1f86c2891ca642

RUN rustup component add clippy rustfmt

ENTRYPOINT ["/usr/local/cargo/bin/cargo"]
