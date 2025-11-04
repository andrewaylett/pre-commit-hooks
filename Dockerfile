FROM docker.io/rust:1.91.0-slim@sha256:038689d4c9bf5a3fefd6139eea67bd8228a96b92eb8710836859ba42e6eeed7a

RUN rustup component add clippy rustfmt

ENTRYPOINT ["/usr/local/cargo/bin/cargo"]
