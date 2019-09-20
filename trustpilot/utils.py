def get_cleaned_url(url, api_host, api_version):
    if any(prefix in url for prefix in ["http://", "https://"]):
        return url

    cleaned_url = api_host.rstrip("/")
    if url.startswith("/{}".format(api_version)):
        cleaned_url += url
    else:
        cleaned_url += "/{}{}".format(api_version, url)

    return cleaned_url
