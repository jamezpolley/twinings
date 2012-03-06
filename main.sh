#!/bin/sh

trap 'kill $MID $TID $SID; echo; exit;' 1 2 3 6 9 14 15

. bin/activate

~/Developer/ooe/build/monitor -d html/image & MID=$!
./thumbnail.py & TID=$!
./server.py & SID=$!

echo PID $MID - monitor
echo PID $TID - thumbnail
echo PID $SID - server

wait $MID $TID $SID
