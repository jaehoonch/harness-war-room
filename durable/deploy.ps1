# Package shared code with the Durable Functions app, then publish.
# Run from repo root. Requires: az, func core tools, an existing Function App.
param(
  [string]$ResourceGroup = "rg-harness-war-room",
  [string]$FunctionApp   = "warroom-fn"
)
$ErrorActionPreference = "Stop"
Copy-Item backend  durable/backend  -Recurse -Force
Copy-Item demo_repo durable/demo_repo -Recurse -Force
Push-Location durable
try { func azure functionapp publish $FunctionApp --python }
finally {
  Pop-Location
  Remove-Item durable/backend, durable/demo_repo -Recurse -Force
}
