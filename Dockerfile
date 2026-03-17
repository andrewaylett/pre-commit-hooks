FROM docker.io/rust:1.94.0-slim@sha256:da9dab7a6b8dd428e71718402e97207bb3e54167d37b5708616050b1e8f60ed6

RUN rustup component add clippy rustfmt

ENTRYPOINT ["/usr/local/cargo/bin/cargo"]
