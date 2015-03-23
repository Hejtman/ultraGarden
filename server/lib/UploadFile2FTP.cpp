#include <stdio.h>
#include <string.h>
#include <curl/curl.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <errno.h>
#include <unistd.h>
#include "../log.h"

 
void UploadFile2FTP(const char* filePath, const char* url)
{
	struct curl_slist *headerlist=NULL;

	struct stat file_info;
	if(stat(filePath, &file_info)) {
		LOG_ERRORF("Couldnt open '%s': %s\n", filePath, strerror(errno));
		return;
	}
	FILE *hd_src = fopen(filePath, "rb");

	curl_global_init(CURL_GLOBAL_ALL);

	CURL *curl = curl_easy_init();
	if(curl) {
		curl_easy_setopt(curl, CURLOPT_UPLOAD, 1L);
		curl_easy_setopt(curl, CURLOPT_URL, url);
		curl_easy_setopt(curl, CURLOPT_POSTQUOTE, headerlist);
		curl_easy_setopt(curl, CURLOPT_READDATA, hd_src);
		curl_easy_setopt(curl, CURLOPT_INFILESIZE_LARGE, (curl_off_t)file_info.st_size);

		CURLcode res = curl_easy_perform(curl);
		if(res != CURLE_OK)
			LOG_ERRORF("curl_easy_perform() failed: %s", curl_easy_strerror(res));

		curl_slist_free_all (headerlist);
		curl_easy_cleanup(curl);
	}
	fclose(hd_src);

	curl_global_cleanup();
}

