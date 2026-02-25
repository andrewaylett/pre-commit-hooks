FROM docker.io/rust:1.93.1-slim@sha256:7e6fa79cf81be23fd45d857f75f583d80cfdbb11c91fa06180fd747fda37a61d

RUN rustup component add clippy rustfmt

ENTRYPOINT ["/usr/local/cargo/bin/cargo"]
