#!/bin/sh

cd `dirname $1`

data=`cat translations.json`
cat > translations.js << EOF
export default $data;
EOF