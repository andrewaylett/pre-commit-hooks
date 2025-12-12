FROM docker.io/rust:1.92.0-slim@sha256:973c5191dd2613f5caa07cdfd9f94b8b0b4bbfa10bc21f0073ffc115ff04c701

RUN rustup component add clippy rustfmt

ENTRYPOINT ["/usr/local/cargo/bin/cargo"]
