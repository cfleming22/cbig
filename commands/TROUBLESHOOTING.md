# CBIG Troubleshooting Guide

## 🔴 Common Errors & Solutions

### "Command not found: cbig"
**Cause:** CBIG not installed globally
**Solution:**
```bash
cd /Users/cjmacbook/dv/tools/code-extractor/cbig
uv tool install --editable .
```

### "No files found to analyze"
**Cause:** Wrong path or no supported files
**Solution:**
```bash
# Check supported files exist
ls -la *.{py,js,java,rs,html}

# Use correct path
cbig main -p /correct/path/to/project
```

### "Permission denied"
**Cause:** No read access to files
**Solution:**
```bash
# Check permissions
ls -la /path/to/project

# Fix permissions
chmod -R +r /path/to/project
```

### "Out of memory"
**Cause:** Too many parallel workers
**Solution:**
```bash
# Reduce workers
cbig main -p . -j 2

# Or use sequential processing
cbig main -p . -j 1
```

### "VIRTUAL_ENV conflict"
**Cause:** Conflicting virtual environments
**Solution:**
```bash
deactivate
uv sync
uv run cbig main -p .
```

### "Cache corrupted"
**Cause:** Interrupted analysis or disk issues
**Solution:**
```bash
# Clear and rebuild cache
cbig main -p . --cache-dir .cbig_cache --clear-cache
```

### "Tree-sitter not available"
**Cause:** Parser not installed (warning only)
**Solution:**
```bash
# Reinstall with parsers
uv sync --upgrade
```

### "Unicode/Encoding errors"
**Cause:** Non-UTF8 files
**Solution:**
```bash
# Set environment
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8

# Exclude problematic files
cbig main -p . --exclude "*.bin" --exclude "*.dat"
```

## 🟡 Performance Issues

### Slow First Run
**Normal:** First run builds AST cache
**Solution:** Use --cache-dir for subsequent runs

### High Memory Usage
**Cause:** Large codebase + parallel processing
**Solutions:**
```bash
# Limit workers
cbig main -p . -j 4

# Process by directory
cbig main -p . --by-dir

# Filter languages
cbig main -p . -l python
```

### Disk Space Issues
**Cause:** Large cache or output files
**Solutions:**
```bash
# Check disk usage
du -sh .cbig_cache

# Clear old cache
rm -rf .cbig_cache

# Use minimal output
cbig main -p . --no-functions --no-classes
```

## 🟢 Best Practices

### For Large Projects
```bash
cbig main -p . \
  --cache-dir .cbig_cache \
  -j 4 \
  --exclude "node_modules/*" \
  --exclude "vendor/*" \
  --exclude "build/*" \
  --by-dir \
  --output-dir docs/
```

### For CI/CD
```bash
cbig main -p . \
  --format json \
  -o metrics.json \
  --no-md \
  --quiet \
  -j 2
```

### For Quick Analysis
```bash
# Use the aliases
cbig-fast
cbig-summary .
```

## 🔍 Debug Commands

### Check Installation
```bash
which cbig
cbig --version
uv tool list
```

### Check Environment
```bash
python --version
uv --version
echo $SHELL
echo $PATH
```

### Test Parsers
```bash
python -c "import tree_sitter_python; print('Python parser OK')"
python -c "import tree_sitter_javascript; print('JS parser OK')"
```

### Verbose Debugging
```bash
# Maximum verbosity
cbig main -p . -v

# With Python debugging
PYTHONVERBOSE=1 cbig main -p . -v
```

## 📞 Getting Help

1. Check error message carefully
2. Run with `-v` for more details
3. Check this troubleshooting guide
4. Verify environment with commands above
5. Try minimal test case:
   ```bash
   echo "print('test')" > test.py
   cbig main -p test.py --by-file
   ```

## 🔄 Complete Reset

If all else fails:
```bash
# Full cleanup and reinstall
cd /Users/cjmacbook/dv/tools/code-extractor/cbig
rm -rf .venv .cbig_cache python3.12
rm -rf ~/.local/share/uv/tools/cbig
uv tool uninstall cbig
uv sync
uv tool install --editable .
source ~/.zshrc
cbig --help
```