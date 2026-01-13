FROM docker.io/rust:1.92.0-slim@sha256:6c5ca1b7563cb6ccd1cd0631aac30f07b2c1dd267463c9a3ccdcea432760ff2c

RUN rustup component add clippy rustfmt

ENTRYPOINT ["/usr/local/cargo/bin/cargo"]
