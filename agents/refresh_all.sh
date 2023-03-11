for d in ./* ; do (cd "$d" && echo "refreshing $d" && wget https://app.fixie.ai/api/refresh/fixie/${d:2} --post-data ""); done
