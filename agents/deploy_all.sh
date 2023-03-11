for d in ./*/ ; do (cd "$d" && echo "deploying $d" && fixie agent deploy); done
