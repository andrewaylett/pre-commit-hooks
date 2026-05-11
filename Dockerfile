FROM docker.io/rust:1.95.0-slim@sha256:5021128d455987e7e7d6586bd7288fa876614821292614acbb761c21fc1ebb15

RUN rustup component add clippy rustfmt

ENTRYPOINT ["/usr/local/cargo/bin/cargo"]
