FROM docker.io/rust:1.89.0-slim@sha256:5dd29ac327ebffd97df4cb9a6652d5567cdcba00697bb76cada8823561309224

RUN rustup component add clippy rustfmt

ENTRYPOINT ["/usr/local/cargo/bin/cargo"]
