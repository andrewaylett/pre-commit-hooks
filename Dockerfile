FROM docker.io/rust:1.91.0-slim@sha256:d9ba8014603166915f7e0fcaa9af09df2a1fc30547e75a72c1d34165139f036a

RUN rustup component add clippy rustfmt

ENTRYPOINT ["/usr/local/cargo/bin/cargo"]
