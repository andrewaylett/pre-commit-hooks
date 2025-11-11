FROM docker.io/rust:1.91.1-slim@sha256:67a2c1b684498a4df3e016a871b5f4cc6dd515578eb885b95803def15fdddbbd

RUN rustup component add clippy rustfmt

ENTRYPOINT ["/usr/local/cargo/bin/cargo"]
