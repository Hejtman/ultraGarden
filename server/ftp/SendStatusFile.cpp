#include "config.h" // FTP_USER, FTP_PASSWORD
#include <stdio.h>
#include <string.h>
 
#include <curl/curl.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <errno.h>
#include <unistd.h>
 
#define LOCAL_FILE      "/home/osmc/ultraGarden/server/status.php"
#define UPLOAD_FILE_AS  "status_tmp.php"
#define REMOTE_URL      "ftp://" FTP_USER ":" FTP_PASSWORD "@ftp.malina.moxo.cz/ultraGarden/balcony1/" UPLOAD_FILE_AS
#define RENAME_FILE_TO  "status.php"
 
void SendStatusFile()
{
	struct curl_slist *headerlist=NULL;
	static const char buf_1 [] = "RNFR " UPLOAD_FILE_AS;
	static const char buf_2 [] = "RNTO " RENAME_FILE_TO;

	struct stat file_info;
	if(stat(LOCAL_FILE, &file_info)) {
		printf("Couldnt open '%s': %s\n", LOCAL_FILE, strerror(errno));
		return;
	}
	curl_off_t fsize = (curl_off_t)file_info.st_size;

	printf("Local file size: %" CURL_FORMAT_CURL_OFF_T " bytes.\n", fsize);

	FILE *hd_src = fopen(LOCAL_FILE, "rb");

	curl_global_init(CURL_GLOBAL_ALL);

	CURL *curl = curl_easy_init();
	if(curl) {
		headerlist = curl_slist_append(headerlist, buf_1);
		headerlist = curl_slist_append(headerlist, buf_2);

		curl_easy_setopt(curl, CURLOPT_UPLOAD, 1L);
		curl_easy_setopt(curl,CURLOPT_URL, REMOTE_URL);
		curl_easy_setopt(curl, CURLOPT_POSTQUOTE, headerlist);
		curl_easy_setopt(curl, CURLOPT_READDATA, hd_src);
		curl_easy_setopt(curl, CURLOPT_INFILESIZE_LARGE, (curl_off_t)fsize);

		CURLcode res = curl_easy_perform(curl);
		if(res != CURLE_OK)
			fprintf(stderr, "curl_easy_perform() failed: %s\n", curl_easy_strerror(res));

		curl_slist_free_all (headerlist);
		curl_easy_cleanup(curl);
	}
	fclose(hd_src);

	curl_global_cleanup();
}

