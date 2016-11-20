package kr.swmaestro.swmaestro.other;

import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Set;

import org.apache.http.HttpEntity;
import org.apache.http.HttpResponse;
import org.apache.http.NameValuePair;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.HttpClient;
import org.apache.http.client.entity.UrlEncodedFormEntity;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.entity.ContentType;
import org.apache.http.entity.mime.MultipartEntityBuilder;
import org.apache.http.entity.mime.content.FileBody;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.impl.client.HttpClientBuilder;
import org.apache.http.message.BasicNameValuePair;
import org.apache.http.params.HttpConnectionParams;
import org.apache.http.params.HttpParams;
import org.apache.http.util.EntityUtils;

import android.app.ProgressDialog;
import android.content.Context;
import android.os.AsyncTask;
import android.util.Log;

public class BaseAsyncTask extends AsyncTask<Void, String, Integer>{
	public static String TAG = "BaseAsyncTask";

	private static Boolean D = true;
	private ProgressDialog mProgressDialog;
	private Context mContext;
	private String title;

	public BaseAsyncTask(Context context, String title){
		mContext = context;
		this.title = title;
	}

	@Override
	protected void onPreExecute() {
		super.onPreExecute();
		mProgressDialog = new ProgressDialog(mContext);
		mProgressDialog.setTitle("잠시만 기다려주세요...");
		mProgressDialog.setMessage(title);
		mProgressDialog.show();
	}

	@Override
	protected Integer doInBackground(Void... params) {
		return null;
	}

	@Override
	protected void onProgressUpdate(String... values) {
		super.onProgressUpdate(values);
	}

	@Override
	protected void onPostExecute(Integer result) {
		super.onPostExecute(result);
		mProgressDialog.dismiss();
	}

	public static String postRequest(String url, HashMap<String, String> valuePair){
		InputStream is = null;
		String result = "";

		try{
			// HttpClient, HttpPost 생성
			HttpClient httpclient = new DefaultHttpClient();
			HttpPost httppost = new HttpPost(url);

			// HttpParam에 응답시간 5초 넘을 시 timeout
			HttpParams params = httpclient.getParams();
			HttpConnectionParams.setConnectionTimeout(params, 5000);
			HttpConnectionParams.setSoTimeout(params, 5000);

			// Parameter 세팅
			ArrayList<NameValuePair> nameValuePairs = new ArrayList<NameValuePair>();
			Set<String> keySet = valuePair.keySet();
			Iterator<String> iterator = keySet.iterator();
			while(iterator.hasNext()){
				String key = iterator.next();
				String value = valuePair.get(key);
				nameValuePairs.add(new BasicNameValuePair(key, value));
			}  

			// Parameter 인코딩, POST요청에 포함
			UrlEncodedFormEntity entityRequest = new UrlEncodedFormEntity(nameValuePairs, "UTF-8");
			httppost.setEntity(entityRequest);

			// 요청 및 결과값 리턴
			HttpResponse response = httpclient.execute(httppost);
			HttpEntity entity = response.getEntity();
			is = entity.getContent();

		}catch(Exception e){
			if(D) Log.e("log_tag", "Error in http connection "+e.toString());
		}

		// 결과값 String으로 변환
		try{
			BufferedReader reader = new BufferedReader(new InputStreamReader(is, "utf-8"));
			StringBuilder sb = new StringBuilder();
			String line = null;
			while ((line = reader.readLine()) != null) {
				sb.append(line + "\n");
			}
			is.close();
			result=sb.toString();
			//			if(D) Log.d("log_tag", result);
		}catch(Exception e){
			if(D) Log.e("log_tag", "Error converting result "+e.toString());
		}

		return result;
	}

	public static String postRequestFile(String url, HashMap<String, String> valuePair, HashMap<String, String> filePair){
		InputStream is = null;
		String result = "";

		try{
			// HttpClient, HttpPost 생성
			HttpClient httpclient = new DefaultHttpClient();
			HttpPost httpPost = new HttpPost(url);

			// HttpParam에 응답시간 5초 넘을 시 timeout
			HttpParams params = httpclient.getParams();
			HttpConnectionParams.setConnectionTimeout(params, 5000);
			HttpConnectionParams.setSoTimeout(params, 5000);

			// Builder
			MultipartEntityBuilder builder = MultipartEntityBuilder.create();
//			Charset chars = Charset.forName("UTF-8");
//			builder.setCharset(chars);
			
			// FilePair key,value String 세팅
			Set<String> fileKeySet = filePair.keySet();
			Iterator<String> fileIterator = fileKeySet.iterator();
			while(fileIterator.hasNext()){
				String key = fileIterator.next();
				String value = filePair.get(key);
				
				FileBody bin = new FileBody(new File(value));
				builder.addPart(key, bin);
			}

			// ValuePiar key,value String 세팅
			Set<String> keySet = valuePair.keySet();
			Iterator<String> iterator = keySet.iterator();
			while(iterator.hasNext()){
				String key = iterator.next();
				String value = valuePair.get(key);
//				value = URLEncoder.encode(value, "UTF-8");
				builder.addTextBody(key, value, ContentType.create("text/plain", "utf-8"));
//				builder.addTextBody(key, value);
			}

			// HttpEntity 생성, HttpPost setEntity
			HttpEntity reqEntity = builder.build();
			httpPost.setEntity(reqEntity);

			// 요청 및 결과값 리턴
			HttpResponse response = httpclient.execute(httpPost);
			HttpEntity entity = response.getEntity();
			is = entity.getContent();

		}catch(Exception e){
			if(D) Log.e("log_tag", "Error in http connection "+e.toString());
		}

		// 결과값 String으로 변환
		try{
			BufferedReader reader = new BufferedReader(new InputStreamReader(is, "utf-8"));
			StringBuilder sb = new StringBuilder();
			String line = null;
			while ((line = reader.readLine()) != null) {
				sb.append(line + "\n");
			}
			is.close();
			result=sb.toString();
			//			if(D) Log.d("log_tag", result);
		}catch(Exception e){
			if(D) Log.e("log_tag", "Error converting result "+e.toString());
		}

		return result;
	}

	public static String postRequestFile2(String url, HashMap<String, String> valuePair, String filePath){
		InputStream is = null;
		String result = "";

		// HttpClient, HttpPost 생성
		//		CloseableHttpClient httpClient = HttpClients.createDefault();
		//		CloseableHttpClient httpClient = HttpClientBuilder.create()
		//				  .setUserAgent("MyAgent")
		//				  .setMaxConnPerRoute(4)
		//				  .build();
		HttpClient httpClient = HttpClientBuilder.create().build();
		try{
			HttpPost httpPost = new HttpPost(url);

			// File 세팅
			FileBody bin = new FileBody(new File(filePath));
			MultipartEntityBuilder builder = MultipartEntityBuilder.create();
			builder.addPart("image", bin);

			// key,value String 세팅
			Set<String> keySet = valuePair.keySet();
			Iterator<String> iterator = keySet.iterator();
			while(iterator.hasNext()){
				String key = iterator.next();
				String value = valuePair.get(key);
				builder.addTextBody(key, value);
			}

			// HttpEntity 생성, HttpPost setEntity
			HttpEntity reqEntity = builder.build();
			httpPost.setEntity(reqEntity);

			HttpResponse response = httpClient.execute(httpPost);
			try {
				HttpEntity resEntity = response.getEntity();
				if (resEntity != null) {
					Log.d(TAG, "Response content length : " + resEntity.getContentLength());
				}
				is = resEntity.getContent();

				// 결과값 String으로 변환
				try{
					BufferedReader reader = new BufferedReader(new InputStreamReader(is, "utf-8"));
					StringBuilder sb = new StringBuilder();
					String line = null;
					while ((line = reader.readLine()) != null) {
						sb.append(line + "\n");
					}
					is.close();
					result=sb.toString();
					//					if(D) Log.d(TAG, result);
				}catch(Exception e){
					if(D) Log.e(TAG, "Error converting result "+e.toString());
				}

				EntityUtils.consume(resEntity);
			} finally {
				//				response.close();
			}
		} catch (ClientProtocolException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		} finally {
			//			try {
			////				httpClient.close();
			//			} catch (IOException e) {
			//				e.printStackTrace();
			//			}
		}
		return result;

	}
}
