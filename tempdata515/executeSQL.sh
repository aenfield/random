#!/bin/bash
# Run the SQL specified on the command line
sqlite3 << EOF
.read $1
.exit
EOF