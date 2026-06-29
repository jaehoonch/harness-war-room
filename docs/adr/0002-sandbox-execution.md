# Generated code runs in a no-network copy-on-run subprocess sandbox

Agent-generated diffs are applied to a throwaway copy of the Demo Repo and tests run in an isolated subprocess with no network and timeouts, never in-process exec. This is the OWASP-correct stance for executing model-generated code; AKS can later tighten it to a pod-per-run.
