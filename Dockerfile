FROM docker.io/rust:1.93.1-slim@sha256:9663b80a1621253d30b146454f903de48f0af925c967be48c84745537cd35d8b

RUN rustup component add clippy rustfmt

ENTRYPOINT ["/usr/local/cargo/bin/cargo"]
