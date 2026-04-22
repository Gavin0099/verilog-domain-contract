# Clock/Reset Contract

## Must-Have Preconditions

- clock domain count and identifiers
- edge definition (`posedge`/`negedge`) per domain
- reset presence and polarity
- reset type (`sync`/`async`) and application scope

## Must Not Assume

- single clock domain by default
- reset polarity default
- async/sync default
- implicit reset for every register

## Downgrade Behavior

- missing clock definition -> restrict code generation and escalate
- missing reset definition -> restrict code generation and escalate
- implied multiple clock domains without CDC strategy -> stop
