FROM docker.io/rust:1.95.0-slim@sha256:275c320a57d0d8b6ab09454ab6d1660d70c745fb3cc85adbefad881b69a212cc

RUN rustup component add clippy rustfmt

ENTRYPOINT ["/usr/local/cargo/bin/cargo"]
