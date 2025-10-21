FROM docker.io/rust:1.90.0-slim@sha256:32853851eb770194cf08cfa90ae096f37928c393dfdb86d98f6f505abf3981c8

RUN rustup component add clippy rustfmt

ENTRYPOINT ["/usr/local/cargo/bin/cargo"]
