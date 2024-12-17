# Function to extract subimages from ADS and rebuild the full image
function Rebuild-Image {
    param (
        [string]$coverImage,
        [string]$outputImage,
        [string]$outputDirectory,
        [int]$gridSize = 7
    )

    # Ensure output directory exists
    if (-Not (Test-Path $outputDirectory)) {
        New-Item -Path $outputDirectory -ItemType Directory
    }

    # Get dimensions of one subimage (assuming they are all the same)
	$streams = Get-Item -Path $coverImage -Stream * | Where-Object { $_.Stream -ne ':$DATA' }
    $firstStream = $streams | Select-Object -First 1
    $firstStreamName = $firstStream.Stream -replace ":", ""
    $tempFile = "$outputDirectory\temp.png"

    # Extract first stream to get dimensions
    Get-Content -Path $coverImage -Stream $firstStreamName -Encoding Byte | Set-Content -Path $tempFile -Encoding Byte
    $dimensions = (magick identify -format "%w %h" $tempFile).Split()
    $subImageWidth = [int]$dimensions[0]
    $subImageHeight = [int]$dimensions[1]

    # Calculate total dimensions of the reconstructed image
    $fullWidth = $subImageWidth * $gridSize
    $fullHeight = $subImageHeight * $gridSize

    # Create a blank canvas to assemble the full image
    magick -size "${fullWidth}x${fullHeight}" canvas:none $outputImage

    # Extract and place each subimage on the canvas
    foreach ($stream in $streams) {
        $encodedName = $stream.Stream -replace ":", ""
        if ($encodedName -ne "") {
            # Decode the stream name (base64 -> (x, y) coordinates)
            $decodedName = [Text.Encoding]::UTF8.GetString([Convert]::FromBase64String($encodedName))
            $coords = $decodedName -replace "[\(\)]", "" -split ",\s*"
            $x = [int]$coords[0]
            $y = [int]$coords[1]

            # Extract the subimage
            $subImageFile = "$outputDirectory\subimage_$x$y.png"
            Get-Content -Path $coverImage -Stream $encodedName -Encoding Byte | Set-Content -Path $subImageFile -Encoding Byte

            # Composite the subimage into the full image at the correct position
            $offsetX = $x * $subImageWidth
            $offsetY = $y * $subImageHeight
            magick composite -geometry +${offsetX}+${offsetY} $subImageFile $outputImage -colorspace sRGB $outputImage
        }
    }

    # Clean up temporary files
    Remove-Item $tempFile
}

# Paths
$coverImage = "dueodde_strand.jpg"        # The image with streams
$outputImage = "reconstructed.png"  # Path to save the reconstructed image
$outputDirectory = "extracted_tiles" # Temporary directory for storing extracted subimages

# Rebuild the original image from ADS
Rebuild-Image -coverImage $coverImage -outputImage $outputImage -outputDirectory $outputDirectory

# Clean up (optional): Remove the temporary directory with extracted subimages
# Remove-Item -Path $outputDirectory -Recurse
