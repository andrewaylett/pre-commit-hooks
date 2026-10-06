FROM docker.io/rust:1.99.0-slim@sha256:a32456165ecc2347c799bba7b54f5aabc158831934b2b98932b81080b312de62

RUN rustup component add clippy rustfmt

ENTRYPOINT ["/usr/local/cargo/bin/cargo"]
