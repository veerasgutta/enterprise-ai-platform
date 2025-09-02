# Quick Demo Setup Script for Professional Showcase
# Perfect for LinkedIn portfolio demonstration

Write-Host "🚀 Enterprise AI Platform - Professional Demo Setup" -ForegroundColor Green
Write-Host "==================================================" -ForegroundColor Green
Write-Host ""

# Check prerequisites
Write-Host "📋 Checking prerequisites..." -ForegroundColor Yellow

# Check Python
try {
    $pythonVersion = python --version
    Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python not found. Please install Python 3.11+" -ForegroundColor Red
    exit 1
}

# Check .NET
try {
    $dotnetVersion = dotnet --version
    Write-Host "✅ .NET found: $dotnetVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ .NET not found. Please install .NET 8+" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "🎯 Starting Professional Demo..." -ForegroundColor Cyan
Write-Host ""

# Demo 1: AI Intelligence Platform
Write-Host "1️⃣ AI Intelligence Platform Demo" -ForegroundColor Yellow
Write-Host "   Generating autonomous business insights..." -ForegroundColor White

Start-Process powershell -ArgumentList "-Command", "cd ai-data-intelligence; python demo_enterprise_platform.py" -WindowStyle Minimized

# Wait for AI platform to generate some insights
Start-Sleep -Seconds 5

# Demo 2: Enterprise API
Write-Host ""
Write-Host "2️⃣ Enterprise API Demo" -ForegroundColor Yellow
Write-Host "   Starting .NET 8 backend services..." -ForegroundColor White

Start-Process powershell -ArgumentList "-Command", "cd backend; dotnet run" -WindowStyle Minimized

# Wait for API to start
Start-Sleep -Seconds 10

Write-Host ""
Write-Host "🎉 Professional Demo Ready!" -ForegroundColor Green
Write-Host "==========================" -ForegroundColor Green
Write-Host ""
Write-Host "📊 AI Intelligence:" -ForegroundColor Cyan
Write-Host "   • Check: ./ai-data-intelligence/generated_reports/" -ForegroundColor White
Write-Host "   • Live insights generation in progress..." -ForegroundColor White
Write-Host ""
Write-Host "🔧 Enterprise API:" -ForegroundColor Cyan
Write-Host "   • Health Check: http://localhost:5294/health" -ForegroundColor White
Write-Host "   • Swagger Docs: http://localhost:5294/swagger" -ForegroundColor White
Write-Host ""
Write-Host "📈 Executive Dashboard:" -ForegroundColor Cyan
Write-Host "   • Open: enterprise-dashboard.html in browser" -ForegroundColor White
Write-Host ""
Write-Host "⏱️  Perfect for 5-minute professional demonstrations!" -ForegroundColor Magenta
Write-Host ""
Write-Host "🌐 Quick Links for Professional Showcase:" -ForegroundColor Yellow
Write-Host "   • Portfolio: https://github.com/your-org/enterprise-ai-platform" -ForegroundColor White
Write-Host "   • LinkedIn: https://linkedin.com/in/your-org" -ForegroundColor White
Write-Host ""
Write-Host "Press any key to view live demo status..." -ForegroundColor Green
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

# Open demo endpoints
Start-Process "http://localhost:5294/health"
Start-Process "enterprise-dashboard.html"
