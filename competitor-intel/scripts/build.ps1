<#
.SYNOPSIS
  Renders a competitor-intel report: injects a JSON data file into the HTML template
  and (optionally) prints it to a single-page PDF with headless Chrome or Edge.

.EXAMPLE
  powershell -ExecutionPolicy Bypass -File build.ps1 -Data acme.json -Out acme_competitors-intel.html -Pdf
#>
param(
  [Parameter(Mandatory = $true)][string]$Data,
  [Parameter(Mandatory = $true)][string]$Out,
  [switch]$Pdf
)
$ErrorActionPreference = 'Stop'
$utf8 = New-Object System.Text.UTF8Encoding($false)

$template = [IO.File]::ReadAllText((Join-Path $PSScriptRoot '..\assets\template.html'), $utf8)
$json = [IO.File]::ReadAllText((Resolve-Path $Data), $utf8)
$null = $json | ConvertFrom-Json   # fail fast on invalid JSON
$json = $json -replace '</', '<\/'   # never let data close the <script> tag

$open = '<script type="application/json" id="report-data">'
$start = $template.IndexOf($open) + $open.Length
$end = $template.IndexOf('</script>', $start)
$html = $template.Substring(0, $start) + "`n" + $json + "`n" + $template.Substring($end)

$outPath = [IO.Path]::GetFullPath((Join-Path (Get-Location) $Out))
[IO.File]::WriteAllText($outPath, $html, $utf8)
Write-Output "HTML: $outPath"

if ($Pdf) {
  $browser = @(
    "$env:ProgramFiles\Google\Chrome\Application\chrome.exe",
    "${env:ProgramFiles(x86)}\Google\Chrome\Application\chrome.exe",
    "$env:LOCALAPPDATA\Google\Chrome\Application\chrome.exe",
    "${env:ProgramFiles(x86)}\Microsoft\Edge\Application\msedge.exe",
    "$env:ProgramFiles\Microsoft\Edge\Application\msedge.exe"
  ) | Where-Object { Test-Path $_ } | Select-Object -First 1
  if (-not $browser) { throw 'Chrome or Edge not found; open the HTML and print to PDF manually.' }

  $pdfPath = [IO.Path]::ChangeExtension($outPath, '.pdf')
  $uri = ([Uri]$outPath).AbsoluteUri
  $p = Start-Process -FilePath $browser -Wait -PassThru -WindowStyle Hidden -ArgumentList @(
    '--headless=new', '--disable-gpu', '--no-pdf-header-footer',
    '--virtual-time-budget=5000', "--print-to-pdf=`"$pdfPath`"", $uri
  )
  if (-not (Test-Path $pdfPath)) { throw "PDF export failed (exit $($p.ExitCode))." }
  Write-Output "PDF:  $pdfPath"
}
