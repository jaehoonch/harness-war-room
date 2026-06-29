// Harness War Room infrastructure: ACR + Container Apps env + Container App.
// Managed identity + AcrPull; no admin creds, no anonymous pull. Korea Central.
@description('Base name for resources')
param name string = 'warroom'
param location string = resourceGroup().location
@description('Container image; defaults to a placeholder until first build')
param image string = 'mcr.microsoft.com/k8se/quickstart:latest'

var acrName = toLower('${name}acr${uniqueString(resourceGroup().id)}')

resource acr 'Microsoft.ContainerRegistry/registries@2023-11-01-preview' = {
  name: acrName
  location: location
  sku: { name: 'Basic' }
  properties: { adminUserEnabled: false } // managed identity only
}

resource law 'Microsoft.OperationalInsights/workspaces@2023-09-01' = {
  name: '${name}-law'
  location: location
  properties: { sku: { name: 'PerGB2018' }, retentionInDays: 30 }
}

resource env 'Microsoft.App/managedEnvironments@2024-03-01' = {
  name: '${name}-env'
  location: location
  properties: {
    appLogsConfiguration: {
      destination: 'log-analytics'
      logAnalyticsConfiguration: {
        customerId: law.properties.customerId
        sharedKey: law.listKeys().primarySharedKey
      }
    }
  }
}

resource app 'Microsoft.App/containerApps@2024-03-01' = {
  name: name
  location: location
  identity: { type: 'SystemAssigned' }
  properties: {
    managedEnvironmentId: env.id
    configuration: {
      ingress: { external: true, targetPort: 8000 }
      registries: [ { server: acr.properties.loginServer, identity: 'system' } ]
    }
    template: {
      containers: [ {
        name: name
        image: image
        env: [ { name: 'DEMO_MODE', value: '1' } ]
        resources: { cpu: json('0.5'), memory: '1Gi' }
      } ]
      scale: { minReplicas: 0, maxReplicas: 2 }
    }
  }
}

resource acrPull 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(acr.id, app.id, 'acrpull')
  scope: acr
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', '7f951dda-4ed3-4680-a7ca-43fe172d538d')
    principalId: app.identity.principalId
    principalType: 'ServicePrincipal'
  }
}

output acrName string = acr.name
output appUrl string = 'https://${app.properties.configuration.ingress.fqdn}'
