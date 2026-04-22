# Coverage Model (v0.1 Static Slice)

This model states what bug classes are covered by current rules and what remains out of scope.

## Covered Bug Classes

- reset assumption mismatch
- assignment semantic mismatch (blocking/non-blocking misuse)
- handshake protocol/timing assumption mismatch
- premature completion claims under missing preconditions

## Estimated Coverage (Working Estimate)

- covered by current v0.1 rules: `high-frequency RTL assumption/semantic claim failures`
- estimated contribution to observed AI RTL failures: `working estimate only, not measured yet`

## Not Covered in v0.1

- full CDC methodology
- metastability mitigation design correctness
- synthesis/timing closure guarantees
- deep protocol-specific compliance packs
- formal proof completeness

## False-Negative Risk Notes

- a response may pass current contract but still fail physical timing or CDC safety
- simulation-only evidence can miss integration-level hazards

## Required Next Measurement

Coverage estimate must be replaced by measured replay data:

- rule hit rate per bug class
- missed-error rate (false negative)
- blocked-output rate (refusal or downgrade)
