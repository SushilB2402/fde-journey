# Log Search Exercise

Run these from `week3/shell/sandbox`, where `app.log` lives. It is a practice log of 5,023 lines (123 ERROR lines: 75 db timeout, 48 disk full), ignored by Git.

## Quick counts

```bash
grep -c ERROR app.log          # 123
grep -c "db timeout" app.log   # 75
grep -c "disk full" app.log    # 48
```

## First Attempt

```bash
grep ERROR app.log | sort | uniq -c | sort -rn | head
```

### Why it showed 1 for every line

The first pipeline showed 1 for every line because each ERROR message contained a different timestamp, service name, or number, so every line was unique and uniq -c could only count each one once.

## Final Command

```bash
grep ERROR app.log | cut -d' ' -f5- | sed -E 's/ [0-9]+$//' | sort | uniq -c | sort -rn
```

## Output

```text
75 db timeout after 30s on query
48 disk full on /var/data volume
```

## Explanation

The command removes the timestamp and service fields, strips the trailing variable numbers, groups identical error messages, counts them, and sorts the results by frequency.