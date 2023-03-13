resource_metric = {
    "Microsoft.Sql/servers/databases": {
        "name": "cpu_percent",
        "aggregation": "Average",
    },
    "Microsoft.Web/serverFarms": {
        "name": "CpuPercentage",
        "aggregation": "Average",
    },
    "Microsoft.Maps/accounts": {
        "name": "Usage",
        "aggregation": "Count",
    },
    "Microsoft.Storage/storageAccounts": {
        "name":  "Transactions",
        "aggregation": "Total"
    },
    "Microsoft.Web/sites": {
        "name": "CpuTime",
        "aggregation": "Average",
    },
    "Microsoft.Web/staticSites": {
        "name": "SiteHits",
        "aggregation": "Total",
    }
}