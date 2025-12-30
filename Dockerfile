FROM docker.io/rust:1.92.0-slim@sha256:3a69c29ef5271461d42f9a550455f4172f8c288f7377056b8fbf1ca0e3a30b5e

RUN rustup component add clippy rustfmt

ENTRYPOINT ["/usr/local/cargo/bin/cargo"]
