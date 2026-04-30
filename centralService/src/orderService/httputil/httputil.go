package httputil

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"strings"
)

var httpClient = &http.Client{}

func convertToQueryParams(params map[string]interface{}) string {
	if params == nil || len(params) == 0 {
		return ""
	}
	var buffer bytes.Buffer
	for k, v := range params {
		buffer.WriteString(fmt.Sprintf("%s=%v&", k, v))
	}
	buffer.Truncate(buffer.Len() - 1)
	return buffer.String()
}

func PostForm(url string, params map[string]interface{}) (string, error) {
	req, err := http.NewRequest("POST", url, strings.NewReader(convertToQueryParams(params)))
	if err != nil {
		return "", err
	}
	req.Header.Set("Content-Type", "application/x-www-form-urlencoded")
	resp, err := httpClient.Do(req)
	return responseHandle(resp, err)
}

func PostJson(url string, data map[string]interface{}) (string, error) {
	jsonData, err := json.Marshal(data)
	if err != nil {
		return "", err
	}
	request, err := http.NewRequest("POST", url, bytes.NewBuffer(jsonData))
	if err != nil {
		return "", err
	}
	request.Header.Set("Content-Type", "application/json; charset=UTF-8")
	resp, err := httpClient.Do(request)
	return responseHandle(resp, err)
}

func responseHandle(resp *http.Response, err error) (string, error) {
	defer func() {
		if resp != nil {
			if e := resp.Body.Close(); e != nil {
				fmt.Println(e.Error())
			}
		}
	}()
	if err != nil {
		return "", err
	}
	b, err := io.ReadAll(resp.Body)
	if err != nil {
		return "", err
	}
	respBody := string(b)
	return respBody, nil
}
