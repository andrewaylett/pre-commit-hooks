FROM docker.io/rust:1.95.0-slim@sha256:985053ebf77f576c742435c12c1923ee04dbe511e17f087dd1a8f022307d3aeb

RUN rustup component add clippy rustfmt

ENTRYPOINT ["/usr/local/cargo/bin/cargo"]
