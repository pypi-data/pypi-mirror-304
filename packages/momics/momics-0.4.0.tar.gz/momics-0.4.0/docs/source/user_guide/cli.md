# Introduction to `momics` CLI

The `momics` package includes command-line tools for creating, querying and manipulating `.momics` files.


## Basic CLI usage

```shell
momics -v

# Initiate a momics repository
momics create testCLI.momics

# Register chromosome lengths
momics ingest chroms -f /data/momics/S288c.chrom.sizes testCLI.momics

# Ingest genome reference sequence
momics ingest seq -f ~/genomes/S288c/S288c.fa testCLI.momics

# Ingest genomic coverage tracks
momics ingest tracks -f bw_a=track1.bw -f bw_b=track2.bw -f bw_c=track3.bw testCLI.momics

# Ingest genomic features
momics ingest features -f bed1=regions.bed testCLI.momics

# Print all created tables and arrays
momics tree testCLI.momics

# Generate a manifest of the repository configuration and timestamps
momics manifest -o manifest.json testCLI.momics

# Consolidate the repository to optimize storage and performance
momics consolidate --vacuum testCLI.momics

# Summary of each table
momics ls --table chroms testCLI.momics
momics ls --table tracks testCLI.momics
momics ls --table features testCLI.momics

# Perform queries
momics query seq --coordinates "I:10-1000" testCLI.momics
momics query seq --file regions.bed -o out.fa testCLI.momics
momics query tracks --coordinates "I:10-1000" testCLI.momics
momics query tracks --file regions.bed testCLI.momics
```

## Extra CLI utilities

```shell
# Remove a track
momics remove --track bw_b testCLI.momics
momics ls --table tracks testCLI.momics

# Bin the genome using a sliding window
momics binnify -w 1000 -s 1000 -o bins.bed testCLI.momics

# Copy tracks, features and sequence
momics cp --type track --label bw_b --output out.bw testCLI.momics
momics cp --type features --label bed1 --output out.bed testCLI.momics
momics cp --type sequence --output out.fa testCLI.momics

# Delete the repository
momics delete testCLI.momics
```

## Going further

- See the [full CLI reference](../cli/index) for more information.
