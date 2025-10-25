# Examples

This page provides practical examples of using qrkie.

## Basic Usage

### Getting Help

```bash
# Show main help
qrkie --help

# Show help for a specific command
qrkie [command] --help
```

### Check Version

```bash
qrkie --version
```

## Advanced Usage

### Using with Different Log Levels

```bash
# Run with debug logging
qrkie --log-level DEBUG [command]

# Run with minimal logging
qrkie --log-level ERROR [command]
```

### Using with Configuration

```bash
# Set configuration via environment variables
export QRKIE_SETTING_NAME=value
qrkie [command]

# Or create a .env file
echo "QRKIE_SETTING_NAME=value" > .env
qrkie [command]
```
## Common Workflows

### Example Workflow 1

```bash
# Step 1: Initialize
qrkie init

# Step 2: Process
qrkie process --input file.txt

# Step 3: Output
qrkie output --format json
```

### Example Workflow 2

```bash
# One-liner example
qrkie process --input file.txt --output result.txt --verbose
```

## Error Handling Examples

### Common Errors

```bash
# File not found
qrkie process --input nonexistent.txt
# Error: Input file 'nonexistent.txt' not found

# Invalid option
qrkie --invalid-option
# Error: No such option: --invalid-option
```

### Debugging

```bash
# Run with debug logging to troubleshoot
qrkie --log-level DEBUG process --input file.txt
```

## Integration Examples

### Use in Scripts

```bash
#!/bin/bash
set -e

# Check if qrkie is installed
if ! command -v qrkie &> /dev/null; then
    echo "qrkie is not installed"
    exit 1
fi

# Run the command
qrkie process --input "$1" --output "$2"
echo "Processing complete"
```

### Use with Make

```makefile
.PHONY: process
process:
	qrkie process --input input.txt --output output.txt

.PHONY: clean
clean:
	rm -f output.txt qrkie.log
```

## Performance Tips

- Use appropriate log levels in production
- Process files in batches when possible
- Use configuration files for repeated settings

## Next Steps

- Learn more about the [API Reference](../reference/)
- Check out the [Contributing Guide](../contributing.md)
- Visit the [GitHub repository](https://github.com/JnyJny/qrkie)