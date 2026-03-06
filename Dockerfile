FROM docker.io/rust:1.94.0-slim@sha256:d6782f2b326a10eaf593eb90cafc34a03a287b4a25fe4d0c693c90304b06f6d7

RUN rustup component add clippy rustfmt

ENTRYPOINT ["/usr/local/cargo/bin/cargo"]
