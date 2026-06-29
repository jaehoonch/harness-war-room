# Four specialized agents driven by a deterministic supervisor

The War Room uses four MAF agents (Triage, Repro, Fix, Review) coordinated by a plain-code Supervisor rather than a self-routing autonomous group. The Supervisor runs tests between steps and re-loops Fix→Review until green, giving deterministic, test-gated handoffs that demo reliably and map directly to the harness Feedback/Review pillars.
