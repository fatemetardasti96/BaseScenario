
echo "Run genesys2 script v2"
"#getting the scenario name from the current folder"
MY_DIR= ${PWD##*/}
echo Scenario: $MY_DIR
"DATE=""$(date +%Y-%m-%d_%H-%M)"""
"#current path"
"CPATH=""$(pwd | xargs basename)"""
"#generate filename from time and path"
"log_filename=$DATE""_genesys_log_""$CPATH"".txt"""
"echo ""Starting Genesys 2 with logging to ""$log_filename"
"#execute the optimisation as bg job"
"./genesys_2 --mode=analysis --scenario=""$MY_DIR"" -j=1>$log_filename&"
