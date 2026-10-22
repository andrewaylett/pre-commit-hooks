FROM docker.io/rust:1.99.1-slim@sha256:d5928c68f8909c141df1bef47ac2c99c025fc9480d09870e08c3783b270eedec

RUN rustup component add clippy rustfmt

ENTRYPOINT ["/usr/local/cargo/bin/cargo"]
