# Function to crop the image into 16 pieces
function Split-Image {
    param (
        [string]$inputImage,
        [string]$outputDirectory,
        [int]$gridSize = 7
    )

    # Ensure output directory exists
    if (-Not (Test-Path $outputDirectory)) {
        New-Item -Path $outputDirectory -ItemType Directory
    }

    # Get dimensions of the input image
    $dimensions = (magick identify -format "%w %h" $inputImage).Split()
    $width = [int]$dimensions[0]
    $height = [int]$dimensions[1]

    # Ensure the image is quadratic
    if ($width -ne $height) {
        throw "The image must be quadratic (equal width and height)"
    }

    # Calculate the size of each subimage
    $subImageSize = $width / $gridSize

    # Crop the image into grid pieces and save them
    for ($y = 0; $y -lt $gridSize; $y++) {
        for ($x = 0; $x -lt $gridSize; $x++) {
            $cropX = $x * $subImageSize
            $cropY = $y * $subImageSize
            $outputFile = "$outputDirectory\subimage_$x$y.png"
            
            # Crop and save each subimage using the "magick" command in IMv7
            magick $inputImage -crop "${subImageSize}x${subImageSize}+${cropX}+${cropY}" $outputFile
        }
    }
}

# Function to store each cropped image as an alternate data stream in the cover image
function Store-Images-In-ADS {
    param (
        [string]$coverImage,
        [string]$inputDirectory,
        [int]$gridSize = 7
    )

    # Store each subimage in the cover image as an ADS with (x, y)-coordinates as the stream name
    for ($y = 0; $y -lt $gridSize; $y++) {
        for ($x = 0; $x -lt $gridSize; $x++) {
            $subImageFile = "$inputDirectory\subimage_$x$y.png"
            $streamName = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes("(${x}, ${y})"))
            
            # Store the subimage as an ADS
            Set-Content -Path $coverImage -Value $(Get-Content $subImageFile -ReadCount 0 -Encoding byte) -Encoding byte -Stream $streamName
        }
    }
}

# Paths
$inputImage = "flag.png"    # The quadratic image you want to split
$coverImage = "cover.jpg"    # The cover image
$streamImage = "dueodde_strand.jpg"  # Copy of cover image with the streams inserted
$outputDirectory = "tiles"   # Temporary directory for storing cropped images

Copy-Item -Path $coverImage -Destination $streamImage -Force

# Split the image into 16 subimages
Split-Image -inputImage $inputImage -outputDirectory $outputDirectory

# Store each subimage as an ADS in the cover image
Store-Images-In-ADS -coverImage $streamImage -inputDirectory $outputDirectory

# Clean up (optional): Remove the temporary directory with cropped images
Remove-Item -Path $outputDirectory -Recurse
