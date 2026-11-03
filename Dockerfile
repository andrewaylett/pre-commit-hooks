FROM docker.io/rust:1.99.1-slim@sha256:9daf2b244ccc30523e55cafe32edf8465671ba567d0101620e5612ccb76ea1a7

RUN rustup component add clippy rustfmt

ENTRYPOINT ["/usr/local/cargo/bin/cargo"]
