# Handshake / Interface Timing Contract

## Required Preconditions

- protocol semantics (for example `valid/ready` or `req/ack`)
- acceptance and backpressure behavior
- timing/latency expectation
- ordering/loss behavior expectation

## Must Not Assume

- always-ready sink
- one-cycle acceptance
- fixed latency
- lossless downstream behavior without declaration

## Downgrade Behavior

- missing interface spec -> analysis only
- missing timing expectation -> draft with explicit assumptions only
