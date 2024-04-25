#include <sys/socket.h>

int main(){
	sendmmsg(3, [{msg_hdr={msg_name=NULL, msg_namelen=0, msg_iov=[{iov_base="3\253\1\0\0\1\0\0\0\0\0\0\vhuggingface\2co\0\0\1\0\1", iov_len=32}], msg_iovlen=1, msg_controllen=0, msg_flags=0}, msg_len=32}, {msg_hdr={msg_name=NULL, msg_namelen=0, msg_iov=[{iov_base="\232\254\1\0\0\1\0\0\0\0\0\0\vhuggingface\2co\0\0\34\0\1", iov_len=32}], msg_iovlen=1, msg_controllen=0, msg_flags=0}, msg_len=32}], 2, MSG_NOSIGNAL);
	return 0;
}