# Enterprise AI Platform Deployment Script (Windows)
# Run this script from the Enterprise-AI-Platform root directory

Write-Host "🚀 Starting Enterprise AI Platform Deployment" -ForegroundColor Green
Write-Host "=============================================" -ForegroundColor Green

# Check if we're in the right directory
if (-not (Test-Path "ai-data-intelligence") -or -not (Test-Path "backend")) {
    Write-Host "❌ Please run this script from the Enterprise-AI-Platform root directory" -ForegroundColor Red
    exit 1
}

Write-Host "🔍 Checking dependencies..." -ForegroundColor Blue

# Check Python
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python is not installed" -ForegroundColor Red
    exit 1
}

# Check .NET
try {
    $dotnetVersion = dotnet --version 2>&1
    Write-Host "✅ .NET found: $dotnetVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ .NET is not installed" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Dependencies verified" -ForegroundColor Green

# Start AI Data Intelligence Platform
Write-Host "🚀 Starting AI Data Intelligence Platform..." -ForegroundColor Blue
$aiJob = Start-Job -ScriptBlock {
    Set-Location $using:PWD\ai-data-intelligence
    python demo_enterprise_platform.py
}
Write-Host "✅ AI Data Intelligence Platform started (Job ID: $($aiJob.Id))" -ForegroundColor Green

# Start Backend API
Write-Host "🚀 Starting Backend API..." -ForegroundColor Blue
$apiJob = Start-Job -ScriptBlock {
    Set-Location $using:PWD\backend
    dotnet run
}
Write-Host "✅ Backend API starting (Job ID: $($apiJob.Id))" -ForegroundColor Green

# Wait a moment for services to start
Start-Sleep -Seconds 5

Write-Host ""
Write-Host "🎉 Enterprise AI Platform Deployment Complete!" -ForegroundColor Green
Write-Host ""
Write-Host "📊 PLATFORM STATUS:" -ForegroundColor Cyan
Write-Host "=================="
Write-Host "✅ AI Data Intelligence: Running (Job ID: $($aiJob.Id))" -ForegroundColor Green
Write-Host "✅ Backend API: Starting (Job ID: $($apiJob.Id))" -ForegroundColor Green
Write-Host "✅ Enterprise Dashboard: Available" -ForegroundColor Green
Write-Host ""
Write-Host "🔗 ACCESS POINTS:" -ForegroundColor Cyan
Write-Host "================"
Write-Host "📊 Executive Dashboard: file:///$($PWD -replace '\\','/')/ai-data-intelligence/generated_reports/dashboard_executive.html" -ForegroundColor Yellow
Write-Host "🌐 Enterprise Dashboard: file:///$($PWD -replace '\\','/')/enterprise-dashboard.html" -ForegroundColor Yellow
Write-Host "🛠️  API Documentation: http://localhost:5294/swagger" -ForegroundColor Yellow
Write-Host "⚡ API Health Check: http://localhost:5294/api/health" -ForegroundColor Yellow
Write-Host ""
Write-Host "📁 GENERATED REPORTS:" -ForegroundColor Cyan
Write-Host "===================="
Write-Host "📋 Reports Directory: ./ai-data-intelligence/generated_reports/" -ForegroundColor Yellow
Write-Host ""
Write-Host "🛑 TO STOP SERVICES:" -ForegroundColor Cyan
Write-Host "===================="
Write-Host "Stop-Job $($aiJob.Id), $($apiJob.Id); Remove-Job $($aiJob.Id), $($apiJob.Id)" -ForegroundColor Yellow
Write-Host ""
Write-Host "🚀 Platform ready for enterprise use!" -ForegroundColor Green

# Function to check service status
function Check-ServiceStatus {
    Write-Host ""
    Write-Host "🔍 Checking service status..." -ForegroundColor Blue
    
    # Check AI Platform job
    $aiStatus = Get-Job -Id $aiJob.Id
    Write-Host "AI Platform Status: $($aiStatus.State)" -ForegroundColor $(if ($aiStatus.State -eq 'Running') { 'Green' } else { 'Red' })
    
    # Check API job
    $apiStatus = Get-Job -Id $apiJob.Id
    Write-Host "Backend API Status: $($apiStatus.State)" -ForegroundColor $(if ($apiStatus.State -eq 'Running') { 'Green' } else { 'Red' })
    
    # Try to check API health
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:5294/api/health" -TimeoutSec 5 -ErrorAction Stop
        Write-Host "API Health Check: ✅ Healthy (Status: $($response.StatusCode))" -ForegroundColor Green
    } catch {
        Write-Host "API Health Check: ❌ Not responding" -ForegroundColor Red
    }
}

# Monitor services
Write-Host ""
Write-Host "Press Ctrl+C to stop monitoring and exit..."
try {
    while ($true) {
        Start-Sleep -Seconds 30
        Check-ServiceStatus
    }
} finally {
    Write-Host ""
    Write-Host "🛑 Stopping services..." -ForegroundColor Yellow
    Stop-Job $aiJob.Id, $apiJob.Id -ErrorAction SilentlyContinue
    Remove-Job $aiJob.Id, $apiJob.Id -ErrorAction SilentlyContinue
    Write-Host "✅ Services stopped" -ForegroundColor Green
}
