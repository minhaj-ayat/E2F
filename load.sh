while true;
do
	dd if=/dev/urandom bs=1000 count=1000 | pv -L 50M | nc 127.0.0.1 13000
	sleep 0.02;
done;
