# Get directory where the script is located
$dirPath = Get-Location

# Change directory to dirPath - in PowerShell this isn't necessary as all paths are absolute.

# Get all items in the directory
$items = Get-ChildItem -Path $dirPath -File

# Loop through each item in the directory
foreach($item in $items) {
    # Skip "files_to_folder" file
    if ($item.Name -eq "files_to_folder") { continue }

    # Get file name without extension
    $filename = [IO.Path]::GetFileNameWithoutExtension($item.Name)

    # Create new directory with filename, -Force flag is used to avoid error if directory already exists
    New-Item -Path $dirPath -Name $filename -ItemType Directory -Force | Out-Null

    # Move file to the new directory
    Move-Item -Path $item.FullName -Destination (Join-Path $dirPath $filename)
}