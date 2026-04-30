#!/bin/bash
cd ../src/adminServer/
echo building... $(pwd)
sh build.sh
cd ../auction/
echo building... $(pwd)
sh build.sh
cd ../centralLogin/
echo building... $(pwd)
sh build.sh
cd ../crossDataServer/
echo building... $(pwd)
sh build.sh
cd ../dropServer/
echo building... $(pwd)
sh build.sh
cd ../maple/
echo building... $(pwd)
sh build.sh
cd ../router/
echo building... $(pwd)
sh build.sh
cd ../orderService/
echo building... $(pwd)
sh build.sh
echo 'All build processes are successfully'