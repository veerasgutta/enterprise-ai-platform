#!/usr/bin/env powershell
# Script to add MCP configuration to VS Code settings

Write-Host "Configuring VS Code MCP Settings..." -ForegroundColor Green

$settingsPath = "$env:APPDATA\Code\User\settings.json"
$workspacePath = "C:\\Veera\\Enterprise-AI-Platform"

# Ensure directory exists
$settingsDir = Split-Path $settingsPath -Parent
if (-not (Test-Path $settingsDir)) {
    New-Item -ItemType Directory -Path $settingsDir -Force | Out-Null
}

# Read existing settings
if (Test-Path $settingsPath) {
    try {
        $content = Get-Content $settingsPath -Raw
        $existingSettings = $content | ConvertFrom-Json
        Write-Host "Found existing VS Code settings" -ForegroundColor Green
    } catch {
        Write-Host "Creating new settings (existing file had issues)" -ForegroundColor Yellow
        $existingSettings = New-Object PSObject
    }
} else {
    $existingSettings = New-Object PSObject
    Write-Host "Creating new VS Code settings file" -ForegroundColor Yellow
}

# Create MCP configuration
$existingSettings | Add-Member -NotePropertyName "github.copilot.chat.experimental.mcp.enabled" -NotePropertyValue $true -Force

$mcpServers = @{
    "filesystem" = @{
        "command" = "npx"
        "args" = @("@modelcontextprotocol/server-filesystem", $workspacePath)
        "description" = "Enterprise-Platform filesystem access"
    }
}

$existingSettings | Add-Member -NotePropertyName "github.copilot.chat.mcp.servers" -NotePropertyValue $mcpServers -Force

# Write back to settings file
$jsonOutput = $existingSettings | ConvertTo-Json -Depth 10
$jsonOutput | Out-File -FilePath $settingsPath -Encoding UTF8

Write-Host "VS Code MCP configuration updated!" -ForegroundColor Green
Write-Host "Settings file: $settingsPath" -ForegroundColor Cyan

# Verify the configuration
Write-Host "Verifying MCP configuration..." -ForegroundColor Yellow
if (Test-Path $settingsPath) {
    $content = Get-Content $settingsPath -Raw
    if ($content -match "mcp\.enabled.*true") {
        Write-Host "MCP is enabled" -ForegroundColor Green
    }
    if ($content -match "mcp\.servers") {
        Write-Host "MCP servers are configured" -ForegroundColor Green
    }
}

Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host "1. Restart VS Code completely" -ForegroundColor White
Write-Host "2. Open GitHub Copilot Chat" -ForegroundColor White
Write-Host "3. Test with: Can you access the filesystem?" -ForegroundColor White
Write-Host "4. Check for MCP server status in Copilot Chat" -ForegroundColor White
Write-Host ""
Write-Host "If you still get errors, check VS Code Developer Console" -ForegroundColor Yellow
