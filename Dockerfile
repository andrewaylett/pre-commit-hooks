FROM docker.io/rust:1.89.0-slim@sha256:6c828d9865870a3bc8c02919d73803df22cac59b583d8f2cb30a296abe64748f

RUN rustup component add clippy rustfmt

ENTRYPOINT ["/usr/local/cargo/bin/cargo"]
